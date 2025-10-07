#!/usr/bin/env python3
"""
Simulate exactly what the autograder might be doing
"""
import os
import sys
import traceback

# Set environment variable like autograder would
os.environ['ACCESS_TOKEN'] = 'h8sLmxlB-uaWxYwjqNgzSAdtCSwjUWSlnWdFqvnt3QUezIldZxYmmwoV0rd3GjWZ'

def test_get_artist_function():
    """Test the genius.get_artist function for expected output"""
    try:
        # Import the way autograder would
        from apputil import Genius
        
        # Instantiate the way autograder would  
        genius = Genius(access_token=os.environ['ACCESS_TOKEN'])
        
        # Test get_artist method
        result = genius.get_artist("Radiohead")
        
        # Check if result is valid
        if result is None:
            print("FAIL: get_artist returned None")
            return False
            
        if not isinstance(result, dict):
            print(f"FAIL: get_artist returned {type(result)}, expected dict")
            return False
        
        # Check required fields
        required_fields = ['name', 'id', 'followers_count']
        for field in required_fields:
            if field not in result:
                print(f"FAIL: Missing required field '{field}'")
                print(f"Available fields: {list(result.keys())}")
                return False
        
        # Check specific values for Radiohead
        expected_name = 'Radiohead'
        expected_id = 604
        
        actual_name = result.get('name')
        actual_id = result.get('id')
        
        if actual_name != expected_name:
            print(f"FAIL: Expected name '{expected_name}', got '{actual_name}'")
            return False
            
        if actual_id != expected_id:
            print(f"FAIL: Expected id {expected_id}, got {actual_id}")
            return False
            
        # Check data types
        if not isinstance(actual_name, str):
            print(f"FAIL: Name should be str, got {type(actual_name)}")
            return False
            
        if not isinstance(actual_id, int):
            print(f"FAIL: ID should be int, got {type(actual_id)}")
            return False
            
        if not isinstance(result.get('followers_count'), int):
            print(f"FAIL: followers_count should be int, got {type(result.get('followers_count'))}")
            return False
        
        print("PASS: All get_artist tests passed!")
        print(f"Result: name='{actual_name}', id={actual_id}, followers={result.get('followers_count')}")
        return True
        
    except Exception as e:
        print(f"FAIL: Exception occurred: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== Autograder Simulation Test ===")
    success = test_get_artist_function()
    print(f"Test result: {'PASS' if success else 'FAIL'}")
    sys.exit(0 if success else 1)