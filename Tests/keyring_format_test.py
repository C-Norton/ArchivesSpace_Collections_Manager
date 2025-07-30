#!/usr/bin/env python3
"""
Debug tool to test different keyring storage formats
"""

import keyring
import logging

logger = logging.getLogger(__name__)

def test_storage_formats():
    """Test different ways of storing credentials"""

    # Test data
    server = "https://devstaffarchivesspace.lib.rochester.edu:443"
    username = "admin_api"
    password = "test_password_123"

    logger.info("=== Testing Different Storage Formats ===")

    test_cases = [
        {
            "name": "Current format (combined key)",
            "service": "ArchivesSpace Collections Manager",
            "key": username + server,
            "password": password
        },
        {
            "name": "Simple service name",
            "service": "ArchivesSpace",
            "key": username + server,
            "password": password
        },
        {
            "name": "Separate username",
            "service": "ArchivesSpace Collections Manager",
            "key": username,
            "password": password
        },
        {
            "name": "Server as service",
            "service": server,
            "key": username,
            "password": password
        },
        {
            "name": "JSON-like key",
            "service": "ArchivesSpace Collections Manager",
            "key": f"{username}@{server}",
            "password": password
        },
        {
            "name": "Short service name",
            "service": "ACM",
            "key": username + server,
            "password": password
        }
    ]

    results = []

    for i, test_case in enumerate(test_cases):
        logger.info(f"\n--- Test {i+1}: {test_case['name']} ---")

        try:
            # Store the credential
            logger.debug(f"Storing: service='{test_case['service'][:50]}...', key='{test_case['key'][:50]}...'")
            keyring.set_password(test_case['service'], test_case['key'], test_case['password'])
            logger.info("✓ Store successful")

            # Immediately try to retrieve it
            retrieved = keyring.get_password(test_case['service'], test_case['key'])
            if retrieved == test_case['password']:
                logger.info("✓ Retrieve successful")
                store_retrieve_success = True
            else:
                logger.error(f"✗ Retrieve failed: got '{retrieved}' expected '{test_case['password']}'")
                store_retrieve_success = False

            # Try get_credential method
            cred = keyring.get_credential(test_case['service'], test_case['key'])
            if cred and cred.username == test_case['key'] and cred.password == test_case['password']:
                logger.info("✓ get_credential successful")
                credential_success = True
            else:
                logger.warning("✗ get_credential failed or returned different data")
                credential_success = False

            # Try discovery with empty username
            discover_cred = keyring.get_credential(test_case['service'], "")
            if discover_cred and discover_cred.username == test_case['key']:
                logger.info("✓ Discovery with empty username works")
                discovery_success = True
            else:
                logger.warning("✗ Discovery with empty username failed")
                discovery_success = False

            results.append({
                'test': test_case['name'],
                'service_len': len(test_case['service']),
                'key_len': len(test_case['key']),
                'store_retrieve': store_retrieve_success,
                'credential_method': credential_success,
                'discovery': discovery_success
            })

        except Exception as e:
            logger.error(f"✗ Test failed with exception: {e}")
            results.append({
                'test': test_case['name'],
                'service_len': len(test_case['service']),
                'key_len': len(test_case['key']),
                'store_retrieve': False,
                'credential_method': False,
                'discovery': False,
                'error': str(e)
            })

    # Clean up test credentials
    logger.info("\n=== Cleaning up test credentials ===")
    for test_case in test_cases:
        try:
            keyring.delete_password(test_case['service'], test_case['key'])
            logger.debug(f"Deleted: {test_case['name']}")
        except Exception as e:
            logger.debug(f"Could not delete {test_case['name']}: {e}")

    return results

def analyze_results(results):
    """Analyze the test results"""
    logger.info("\n=== Test Results Analysis ===")

    logger.info("Format: Test Name | Service Len | Key Len | Store/Retrieve | get_credential | Discovery")
    logger.info("-" * 90)

    for result in results:
        store_status = "✓" if result['store_retrieve'] else "✗"
        cred_status = "✓" if result['credential_method'] else "✗"
        disc_status = "✓" if result['discovery'] else "✗"

        logger.info(f"{result['test'][:25]:25} | {result['service_len']:11} | {result['key_len']:7} | {store_status:13} | {cred_status:14} | {disc_status}")

        if 'error' in result:
            logger.error(f"  Error: {result['error']}")

    # Find best format
    best_formats = [r for r in results if r['store_retrieve'] and r['discovery']]

    if best_formats:
        logger.info(f"\n✓ Working formats found: {len(best_formats)}")
        for fmt in best_formats:
            logger.info(f"  - {fmt['test']}")
    else:
        logger.warning("\n✗ No fully working formats found!")

        # Find partially working ones
        partial = [r for r in results if r['store_retrieve']]
        if partial:
            logger.info("Partially working formats (store/retrieve only):")
            for fmt in partial:
                logger.info(f"  - {fmt['test']}")

def test_current_app_format():
    """Test the exact format your app is using"""
    logger.info("\n=== Testing Current App Format ===")

    # Simulate your exact storage format
    server = "https://devstaffarchivesspace.lib.rochester.edu:443"
    username = "admin_api"
    password = "your_actual_password"

    service_name = "ArchivesSpace Collections Manager"
    storage_key = username + server

    logger.info(f"Service: '{service_name}'")
    logger.info(f"Storage key: '{storage_key}'")
    logger.info(f"Key length: {len(storage_key)} characters")

    try:
        # Store
        keyring.set_password(service_name, storage_key, password)
        logger.info("✓ Storage completed")

        # Retrieve by exact key
        retrieved = keyring.get_password(service_name, storage_key)
        if retrieved == password:
            logger.info("✓ Direct retrieval works")
        else:
            logger.error(f"✗ Direct retrieval failed: {retrieved}")

        # Try discovery methods
        cred1 = keyring.get_credential(service_name, "")
        cred2 = keyring.get_credential(service_name, username)
        cred3 = keyring.get_credential(service_name, server)

        logger.info(f"Discovery with '': {cred1 is not None}")
        logger.info(f"Discovery with username: {cred2 is not None}")
        logger.info(f"Discovery with server: {cred3 is not None}")

        # Clean up
        keyring.delete_password(service_name, storage_key)
        logger.info("✓ Cleanup completed")

    except Exception as e:
        logger.error(f"Current format test failed: {e}")

def main():
    """Main function"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s - %(message)s'
    )

    logger.info("Keyring Storage Format Debug Tool")
    logger.info("=" * 50)

    # Show current keyring info
    current = keyring.get_keyring()
    logger.info(f"Using keyring: {type(current).__name__}")

    # Run tests
    results = test_storage_formats()
    analyze_results(results)
    test_current_app_format()

    logger.info("\n" + "=" * 50)
    logger.info("Debug complete!")

if __name__ == "__main__":
    main()