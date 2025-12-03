#!/usr/bin/env python3
"""
Test script for Zabbix MCP Server

This script validates the server configuration and tests basic functionality
to ensure everything is working correctly.

Author: Zabbix MCP Server Contributors
License: MIT
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def setup_logging() -> None:
    """Setup logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


def test_import() -> bool:
    """Test if the server module can be imported.
    
    Returns:
        bool: True if import successful
    """
    try:
        print("🔍 Testing module import...")
        from zabbix_mcp_server import get_zabbix_client
        print("✅ Module import successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        print("Please install dependencies: uv sync")
        return False
    except Exception as e:
        print(f"❌ Unexpected import error: {e}")
        return False


def test_environment() -> bool:
    """Test environment configuration.
    
    Returns:
        bool: True if environment is properly configured
    """
    print("\n🔍 Testing environment configuration...")
    
    # Check required variables
    zabbix_url = os.getenv("ZABBIX_URL")
    if not zabbix_url:
        print("❌ ZABBIX_URL not configured")
        return False
    
    print(f"✅ ZABBIX_URL: {zabbix_url}")
    
    # Check authentication
    token = os.getenv("ZABBIX_TOKEN")
    user = os.getenv("ZABBIX_USER")
    password = os.getenv("ZABBIX_PASSWORD")
    
    if token:
        print("✅ Authentication: API Token configured")
    elif user and password:
        print(f"✅ Authentication: Username/Password configured ({user})")
    else:
        print("❌ Authentication not configured")
        print("Please set either ZABBIX_TOKEN or both ZABBIX_USER and ZABBIX_PASSWORD")
        return False
    
    # Check read-only mode
    read_only = os.getenv("READ_ONLY", "true").lower() in ("true", "1", "yes")
    print(f"ℹ️  Read-only mode: {'Enabled' if read_only else 'Disabled'}")
    
    # Check SSL verification
    verify_ssl = os.getenv("VERIFY_SSL", "true").lower() in ("true", "1", "yes")
    print(f"ℹ️  SSL verification: {'Enabled' if verify_ssl else 'Disabled'}")
    
    return True


def test_connection() -> bool:
    """Test basic connection to Zabbix.
    
    Returns:
        bool: True if connection successful
    """
    print("\n🔍 Testing Zabbix connection...")
    
    try:
        from zabbix_mcp_server import get_zabbix_client
        
        # Test getting client and API version
        client = get_zabbix_client()
        version_info = client.apiinfo.version()
        
        print(f"✅ Connected to Zabbix API version: {version_info}")
        return True
        
    except ValueError as e:
        if "environment variable" in str(e).lower():
            print(f"❌ Configuration error: {e}")
        else:
            print(f"❌ Connection failed: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False


def test_basic_operations() -> bool:
    """Test basic read operations.
    
    Returns:
        bool: True if operations successful
    """
    print("\n🔍 Testing basic operations...")
    
    try:
        from zabbix_mcp_server import get_zabbix_client
        client = get_zabbix_client()
        
        # Test host groups (usually always present)
        print("  - Testing host group retrieval...")
        groups = client.hostgroup.get(limit=1)
        if groups:
            print(f"    ✅ Retrieved {len(groups)} host group(s)")
        else:
            print("    ⚠️  No host groups found (this might be normal)")
        
        # Test hosts
        print("  - Testing host retrieval...")
        hosts = client.host.get(limit=1)
        if hosts:
            print(f"    ✅ Retrieved {len(hosts)} host(s)")
        else:
            print("    ⚠️  No hosts found (this might be normal)")
        
        # Test items
        print("  - Testing item retrieval...")
        items = client.item.get(limit=1)
        if items:
            print(f"    ✅ Retrieved {len(items)} item(s)")
        else:
            print("    ⚠️  No items found (this might be normal)")

        # Test auditlogs
        print("  - Testing item retrieval...")
        auditlogs = client.auditlog.get(limit=1)
        if auditlogs:
            print(f"    ✅ Retrieved {len(items)} auditlog(s)")
        else:
            print("    ⚠️  No items found (this might be normal)")
        
        print("✅ Basic operations successful")
        return True
        
    except Exception as e:
        print(f"❌ Basic operations failed: {e}")
        return False


def test_transport_config() -> bool:
    """Test transport configuration.
    
    Returns:
        bool: True if transport configuration is valid
    """
    print("\n🔍 Testing transport configuration...")
    
    try:
        from zabbix_mcp_server import get_transport_config
        
        config = get_transport_config()
        transport = config["transport"]
        
        print(f"✅ Transport type: {transport}")
        
        if transport == "streamable-http":
            print(f"  - Host: {config['host']}")
            print(f"  - Port: {config['port']}")
            print(f"  - Stateless: {config['stateless_http']}")
            
            # Check AUTH_TYPE requirement
            auth_type = os.getenv("AUTH_TYPE", "").lower()
            if auth_type == "no-auth":
                print("  ✅ AUTH_TYPE correctly set to 'no-auth'")
            else:
                print("  ❌ AUTH_TYPE must be set to 'no-auth' for HTTP transport")
                return False
        else:
            print("  ✅ STDIO transport configured correctly")
        
        return True
        
    except ValueError as e:
        print(f"❌ Transport configuration error: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error testing transport: {e}")
        return False


def test_read_only_mode() -> bool:
    """Test read-only mode functionality.
    
    Returns:
        bool: True if read-only mode works correctly
    """
    read_only = os.getenv("READ_ONLY", "true").lower() in ("true", "1", "yes")
    
    if not read_only:
        print("\n⏭️  Skipping read-only mode test (not enabled)")
        return True
    
    print("\n🔍 Testing read-only mode...")
    
    try:
        from zabbix_mcp_server import validate_read_only
        
        # This should raise an exception in read-only mode
        validate_read_only()
        print("❌ Read-only mode not working correctly")
        return False
        
    except ValueError as e:
        if "read-only mode" in str(e).lower():
            print("✅ Read-only mode working correctly")
            return True
        else:
            print(f"❌ Unexpected error: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Unexpected error testing read-only mode: {e}")
        return False


def show_summary(tests_passed: int, total_tests: int) -> None:
    """Show test summary.
    
    Args:
        tests_passed: Number of tests that passed
        total_tests: Total number of tests
    """
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    if tests_passed == total_tests:
        print(f"🎉 All {total_tests} tests passed!")
        print("✅ The Zabbix MCP Server is ready to use")
        
        print("\nNext steps:")
        print("1. Configure your MCP client (see MCP_SETUP.md)")
        print("2. Start the server: uv run python src/zabbix_mcp_server.py")
        print("3. Test with your MCP client")
        
    else:
        print(f"❌ {tests_passed}/{total_tests} tests passed")
        print("Please fix the issues above before using the server")
    
    print("=" * 50)


def main() -> None:
    """Main test function."""
    setup_logging()
    
    print("🧪 Zabbix MCP Server Test Suite")
    print("=" * 50)
    
    tests = [
        ("Module Import", test_import),
        ("Environment Configuration", test_environment),
        ("Transport Configuration", test_transport_config),
        ("Zabbix Connection", test_connection),
        ("Basic Operations", test_basic_operations),
        ("Read-Only Mode", test_read_only_mode),
    ]
    
    tests_passed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                tests_passed += 1
        except KeyboardInterrupt:
            print("\n\n⏹️  Tests interrupted by user")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Unexpected error in {test_name}: {e}")
    
    show_summary(tests_passed, len(tests))
    
    # Exit with appropriate code
    if tests_passed == len(tests):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
