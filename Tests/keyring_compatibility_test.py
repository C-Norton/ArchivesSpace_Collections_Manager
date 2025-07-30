#!/usr/bin/env python3
"""
Debug tool to investigate keyring storage issues with KDE Wallet
"""

import keyring
import keyring.backends
import logging

logger = logging.getLogger(__name__)

def debug_keyring_setup():
    """Debug the keyring configuration"""
    logger.info("=== Keyring Debug Information ===")

    # Get current keyring backend
    current_keyring = keyring.get_keyring()
    logger.info(f"Current keyring backend: {type(current_keyring).__name__}")
    logger.info(f"Current keyring: {current_keyring}")

    # List available backends
    logger.info("Available keyring backends:")
    for backend in keyring.backend.get_all_keyring():
        logger.info(f"  - {type(backend).__name__}: {backend}")

    # Check priority
    logger.info(f"Keyring priority: {current_keyring.priority}")

    return current_keyring

def test_keyring_operations():
    """Test basic keyring operations"""
    logger.info("=== Testing Keyring Operations ===")

    service_name = "ArchivesSpace Collections Manager"
    test_username = "test_user_debug"
    test_password = "test_password_123"

    current_keyring = keyring.get_keyring()

    try:
        # Test storing a credential
        logger.debug(f"Storing test credential...")
        logger.debug(f"  Service: {service_name}")
        logger.debug(f"  Username: {test_username}")
        logger.debug(f"  Password: {test_password}")

        current_keyring.set_password(service_name, test_username, test_password)
        logger.info("✓ Store operation completed")

        # Test retrieving the credential
        logger.debug(f"Retrieving test credential...")
        retrieved_password = current_keyring.get_password(service_name, test_username)

        if retrieved_password:
            logger.info(f"✓ Retrieved password: {retrieved_password}")
            if retrieved_password == test_password:
                logger.info("✓ Password matches!")
            else:
                logger.error(f"✗ Password mismatch! Expected: {test_password}, Got: {retrieved_password}")
        else:
            logger.error("✗ No password retrieved")

        # Test get_credential
        logger.debug(f"Testing get_credential...")
        cred = current_keyring.get_credential(service_name, test_username)
        if cred:
            logger.info(f"✓ get_credential returned: username={cred.username}, password={cred.password}")
        else:
            logger.warning("✗ get_credential returned None")

        # Test with empty username
        logger.debug(f"Testing get_credential with empty username...")
        cred_empty = current_keyring.get_credential(service_name, "")
        if cred_empty:
            logger.info(f"✓ get_credential('', '') returned: username={cred_empty.username}, password={cred_empty.password}")
        else:
            logger.warning("✗ get_credential('', '') returned None")

    except Exception as e:
        logger.error(f"✗ Error during keyring operations: {e}")
        logger.exception("Full traceback:")

    try:
        # Clean up test credential
        logger.debug(f"Cleaning up test credential...")
        current_keyring.delete_password(service_name, test_username)
        logger.info("✓ Test credential deleted")
    except Exception as e:
        logger.warning(f"Could not delete test credential: {e}")

def test_kde_wallet_specific():
    """Test KDE Wallet specific functionality"""
    logger.info("=== KDE Wallet Specific Tests ===")

    current_keyring = keyring.get_keyring()
    backend_name = type(current_keyring).__name__

    if "KDE" in backend_name or "kwallet" in backend_name.lower():
        logger.info(f"✓ Using KDE Wallet backend: {backend_name}")

        # KDE Wallet specific tests
        try:
            # Check if we can access wallet info
            if hasattr(current_keyring, 'wallet'):
                logger.debug(f"Wallet object: {current_keyring.wallet}")
            if hasattr(current_keyring, '_wallet_name'):
                logger.debug(f"Wallet name: {current_keyring._wallet_name}")
        except Exception as e:
            logger.warning(f"Could not access wallet details: {e}")

    else:
        logger.warning(f"⚠ Not using KDE Wallet backend. Using: {backend_name}")
        logger.warning("This might explain why credentials don't appear in KDE Wallet!")

def check_existing_credentials():
    """Check for existing ArchivesSpace credentials"""
    logger.info("=== Checking Existing Credentials ===")

    service_name = "ArchivesSpace Collections Manager"
    current_keyring = keyring.get_keyring()

    # Try various methods to find credentials
    test_usernames = [
        "",
        "admin",
        "admin_api",
        "user",
        "test",
    ]

    logger.info(f"Searching for credentials under service: '{service_name}'")

    found_any = False
    for username in test_usernames:
        try:
            # Method 1: get_password
            password = current_keyring.get_password(service_name, username)
            if password:
                logger.info(f"✓ Found password for username '{username}': {password[:10]}...")
                found_any = True

            # Method 2: get_credential
            cred = current_keyring.get_credential(service_name, username)
            if cred and cred.username and cred.password:
                logger.info(f"✓ Found credential for search '{username}': actual_username='{cred.username}', password={cred.password[:10]}...")
                found_any = True

        except Exception as e:
            logger.debug(f"Error checking username '{username}': {e}")

    if not found_any:
        logger.warning("No existing ArchivesSpace credentials found")

def main():
    """Main debug function"""
    # Configure logging with detailed format
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('keyring_debug.log')
        ]
    )

    logger.info("KDE Wallet / Keyring Debug Tool")
    logger.info("=" * 50)

    try:
        debug_keyring_setup()
        test_keyring_operations()
        test_kde_wallet_specific()
        check_existing_credentials()

        logger.info("=" * 50)
        logger.info("Debug complete!")
        logger.info("If credentials show as stored but don't appear in KDE Wallet:")
        logger.info("1. Check if you're using the KDE Wallet backend")
        logger.info("2. Verify KDE Wallet is running and unlocked")
        logger.info("3. Check if there are permission issues")
        logger.info("4. Try using a different keyring backend")
        logger.info("Debug log written to: keyring_debug.log")

    except Exception as e:
        logger.error(f"Debug failed: {e}")
        logger.exception("Full debug failure traceback:")

if __name__ == "__main__":
    main()
