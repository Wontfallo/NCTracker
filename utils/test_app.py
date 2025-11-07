"""
Simple test script to verify NCTracker application
"""

import sys
import traceback

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import streamlit as st
        print("✓ Streamlit imported successfully")
    except Exception as e:
        print(f"✗ Streamlit import failed: {e}")
        return False
    
    try:
        import pandas as pd
        print("✓ Pandas imported successfully")
    except Exception as e:
        print(f"✗ Pandas import failed: {e}")
        return False
    
    try:
        import plotly.express as px
        print("✓ Plotly imported successfully")
    except Exception as e:
        print(f"✗ Plotly import failed: {e}")
        return False
    
    try:
        from database import db
        print("✓ Database module imported successfully")
    except Exception as e:
        print(f"✗ Database import failed: {e}")
        traceback.print_exc()
        return False
    
    try:
        import utils
        print("✓ Utils module imported successfully")
    except Exception as e:
        print(f"✗ Utils import failed: {e}")
        traceback.print_exc()
        return False
    
    return True

def test_database():
    """Test database connection and basic operations"""
    print("\nTesting database...")
    
    try:
        from database import db
        
        # Test user authentication
        user = db.authenticate_user('admin', 'admin123')
        if user:
            print("✓ Default admin user authentication works")
        else:
            print("✗ Default admin user authentication failed")
            return False
        
        # Test dashboard stats
        stats = db.get_dashboard_stats()
        print(f"✓ Dashboard stats retrieved: {stats}")
        
        return True
    except Exception as e:
        print(f"✗ Database test failed: {e}")
        traceback.print_exc()
        return False

def test_app_structure():
    """Test if main app file structure is correct"""
    print("\nTesting app structure...")
    
    try:
        import app
        print("✓ App module imported successfully")
        return True
    except Exception as e:
        print(f"✗ App import failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("NCTracker Test Suite")
    print("===================")
    
    tests = [
        ("Import Test", test_imports),
        ("Database Test", test_database),
        ("App Structure Test", test_app_structure)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * len(test_name))
        
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
            traceback.print_exc()
    
    print(f"\nTest Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application should work correctly.")
        print("You can now run: streamlit run app.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    main()