"""
Credential Index Manager - maintains a discoverable index of ArchivesSpace credentials
"""

import json
import logging
import keyring
from typing import List, Dict, Optional
from dataclasses import dataclass
from controller.connection import Connection

logger = logging.getLogger(__name__)

@dataclass
class CredentialInfo:
    """Information about a stored credential"""
    username: str
    server: str
    display_name: str
    storage_key: str  # The actual key used in keyring

    def to_dict(self) -> dict:
        return {
            'username': self.username,
            'server': self.server,
            'display_name': self.display_name,
            'storage_key': self.storage_key
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'CredentialInfo':
        return cls(
            username=data['username'],
            server=data['server'],
            display_name=data['display_name'],
            storage_key=data['storage_key']
        )

class CredentialIndexManager:
    """
    Manages an index of ArchivesSpace credentials stored in the keyring.

    Since keyring discovery doesn't work reliably, we maintain our own index
    that maps user-friendly names to the actual keyring storage keys.
    """

    INDEX_SERVICE = "ArchivesSpace Collections Manager"
    INDEX_KEY = "_credential_index_"
    CREDENTIAL_SERVICE = "ArchivesSpace Collections Manager"

    def __init__(self):
        self._index_cache = None

    def _get_index(self) -> List[CredentialInfo]:
        """Get the credential index from keyring"""
        if self._index_cache is not None:
            return self._index_cache

        try:
            index_json = keyring.get_password(self.INDEX_SERVICE, self.INDEX_KEY)
            if index_json:
                index_data = json.loads(index_json)
                self._index_cache = [CredentialInfo.from_dict(item) for item in index_data]
                logger.debug(f"Loaded credential index with {len(self._index_cache)} entries")
            else:
                self._index_cache = []
                logger.debug("No credential index found, starting with empty index")
        except Exception as e:
            logger.error(f"Error loading credential index: {e}")
            self._index_cache = []

        return self._index_cache

    def _save_index(self, index: List[CredentialInfo]) -> None:
        """Save the credential index to keyring"""
        try:
            index_data = [item.to_dict() for item in index]
            index_json = json.dumps(index_data, indent=2)
            keyring.set_password(self.INDEX_SERVICE, self.INDEX_KEY, index_json)
            self._index_cache = index
            logger.debug(f"Saved credential index with {len(index)} entries")
        except Exception as e:
            logger.error(f"Error saving credential index: {e}")
            raise

    def store_credential(self, server: str, username: str, password: str) -> bool:
        """
        Store a credential and update the index

        Args:
            server: ArchivesSpace server URL
            username: Username
            password: Password

        Returns:
            True if successful, False otherwise
        """
        try:
            # Create storage key (same format as before for compatibility)
            storage_key = username + server
            display_name = f"{username} @ {server}"

            # Store the actual credential
            keyring.set_password(self.CREDENTIAL_SERVICE, storage_key, password)
            logger.debug(f"Stored credential with key: {storage_key}")

            # Update the index
            index = self._get_index()

            # Remove any existing entry for this server/username combination
            index = [item for item in index if not (item.username == username and item.server == server)]

            # Add the new entry
            cred_info = CredentialInfo(
                username=username,
                server=server,
                display_name=display_name,
                storage_key=storage_key
            )
            index.append(cred_info)

            # Save updated index
            self._save_index(index)
            logger.info(f"Successfully stored and indexed credential: {display_name}")
            return True

        except Exception as e:
            logger.error(f"Error storing credential: {e}")
            return False

    def get_all_credentials(self) -> List[CredentialInfo]:
        """Get information about all stored credentials"""
        return self._get_index()

    def get_credential_password(self, cred_info: CredentialInfo) -> Optional[str]:
        """Get the password for a specific credential"""
        try:
            password = keyring.get_password(self.CREDENTIAL_SERVICE, cred_info.storage_key)
            return password
        except Exception as e:
            logger.error(f"Error retrieving password for {cred_info.display_name}: {e}")
            return None

    def load_credential(self, cred_info: CredentialInfo) -> Optional[Connection]:
        """Load a credential as a Connection object"""
        password = self.get_credential_password(cred_info)
        if password:
            return Connection(cred_info.server, cred_info.username, password)
        return None

    def delete_credential(self, cred_info: CredentialInfo) -> bool:
        """Delete a credential and remove from index"""
        try:
            # Delete from keyring
            keyring.delete_password(self.CREDENTIAL_SERVICE, cred_info.storage_key)
            logger.debug(f"Deleted credential from keyring: {cred_info.storage_key}")

            # Remove from index
            index = self._get_index()
            index = [item for item in index if item.storage_key != cred_info.storage_key]
            self._save_index(index)

            logger.info(f"Successfully deleted credential: {cred_info.display_name}")
            return True

        except Exception as e:
            logger.error(f"Error deleting credential {cred_info.display_name}: {e}")
            return False

    def cleanup_invalid_credentials(self) -> int:
        """
        Clean up the index by removing entries for credentials that no longer exist in keyring

        Returns:
            Number of invalid entries removed
        """
        index = self._get_index()
        valid_entries = []
        removed_count = 0

        for cred_info in index:
            password = keyring.get_password(self.CREDENTIAL_SERVICE, cred_info.storage_key)
            if password is not None:
                valid_entries.append(cred_info)
            else:
                logger.debug(f"Removing invalid index entry: {cred_info.display_name}")
                removed_count += 1

        if removed_count > 0:
            self._save_index(valid_entries)
            logger.info(f"Cleaned up {removed_count} invalid credential index entries")

        return removed_count

    def migrate_existing_credentials(self) -> int:
        """
        Attempt to find and index existing credentials that were stored without the index.
        This is a one-time migration helper.

        Returns:
            Number of credentials found and indexed
        """
        logger.info("Attempting to migrate existing credentials...")

        # This is tricky since discovery doesn't work, but we can try some common patterns
        common_patterns = self._generate_migration_patterns()
        found_count = 0
        index = self._get_index()

        for pattern in common_patterns:
            try:
                password = keyring.get_password(self.CREDENTIAL_SERVICE, pattern['storage_key'])
                if password:
                    # Check if already in index
                    if not any(item.storage_key == pattern['storage_key'] for item in index):
                        cred_info = CredentialInfo(
                            username=pattern['username'],
                            server=pattern['server'],
                            display_name=f"{pattern['username']} @ {pattern['server']}",
                            storage_key=pattern['storage_key']
                        )
                        index.append(cred_info)
                        found_count += 1
                        logger.info(f"Found existing credential: {cred_info.display_name}")

            except Exception as e:
                logger.debug(f"Migration pattern check failed for {pattern['storage_key']}: {e}")

        if found_count > 0:
            self._save_index(index)
            logger.info(f"Successfully migrated {found_count} existing credentials")
        else:
            logger.info("No existing credentials found to migrate")

        return found_count

    def _generate_migration_patterns(self) -> List[Dict[str, str]]:
        """Generate common credential storage patterns for migration"""
        patterns = []

        # Common ArchivesSpace configurations
        common_usernames = ["admin", "admin_api", "archivesspace", "user"]
        common_servers = [
            "https://localhost:8089",
            "https://localhost:443",
            "http://localhost:8089",
            # Add your known server here
            "https://devstaffarchivesspace.lib.rochester.edu:443"
        ]

        for username in common_usernames:
            for server in common_servers:
                patterns.append({
                    'username': username,
                    'server': server,
                    'storage_key': username + server
                })

        return patterns

# Global instance
credential_manager = CredentialIndexManager()