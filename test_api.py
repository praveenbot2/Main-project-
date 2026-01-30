"""
Test Web Server API
Tests all API endpoints of the Flask web server
"""

import requests
import json
import time


BASE_URL = "http://localhost:5000"


def test_health_check():
    """Test health check endpoint"""
    print("\n1. Testing Health Check Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"   Error: {e}")
        return False


def test_prediction():
    """Test prediction endpoint"""
    print("\n2. Testing Prediction Endpoint...")
    try:
        data = {
            'heart_rate': 75.0,
            'blood_pressure_systolic': 120.0,
            'blood_pressure_diastolic': 80.0,
            'temperature': 36.8,
            'oxygen_saturation': 98.0,
            'respiratory_rate': 16.0
        }
        response = requests.post(f"{BASE_URL}/predict", json=data, timeout=5)
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Risk Level: {result['prediction']['risk_level']}")
        print(f"   Confidence: {result['prediction']['probability']}")
        return response.status_code == 200
    except Exception as e:
        print(f"   Error: {e}")
        return False


def test_chat():
    """Test chat endpoint"""
    print("\n3. Testing Chat Endpoint...")
    try:
        data = {'message': 'What is a normal heart rate?'}
        response = requests.post(f"{BASE_URL}/chat", json=data, timeout=5)
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Bot Response: {result['bot_response'][:100]}...")
        return response.status_code == 200
    except Exception as e:
        print(f"   Error: {e}")
        return False


def test_monitor():
    """Test monitor endpoint"""
    print("\n4. Testing Monitor Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/monitor?condition=healthy", timeout=5)
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Vitals: HR={result['vitals']['heart_rate']}, "
              f"Temp={result['vitals']['temperature']}")
        return response.status_code == 200
    except Exception as e:
        print(f"   Error: {e}")
        return False


def test_alerts():
    """Test alerts endpoint"""
    print("\n5. Testing Alerts Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/alerts", timeout=5)
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Alerts Summary: {result['alerts']}")
        return response.status_code == 200
    except Exception as e:
        print(f"   Error: {e}")
        return False


def test_simulate():
    """Test simulate endpoint"""
    print("\n6. Testing Simulate Endpoint...")
    try:
        data = {'condition': 'healthy'}
        response = requests.post(f"{BASE_URL}/simulate", json=data, timeout=5)
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Monitoring Result: Risk Level = "
              f"{result['monitoring_result']['prediction']['risk_level']}")
        return response.status_code == 200
    except Exception as e:
        print(f"   Error: {e}")
        return False


def main():
    """Run all tests"""
    print("="*70)
    print("  WEB SERVER API TESTS")
    print("="*70)
    print("\nNOTE: Make sure the web server is running with: python web_server.py")
    print("Waiting 3 seconds before starting tests...")
    time.sleep(3)
    
    tests = [
        ("Health Check", test_health_check),
        ("Prediction", test_prediction),
        ("Chat", test_chat),
        ("Monitor", test_monitor),
        ("Alerts", test_alerts),
        ("Simulate", test_simulate)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n   Test failed with error: {e}")
            results.append((name, False))
        time.sleep(0.5)
    
    # Summary
    print("\n" + "="*70)
    print("  TEST SUMMARY")
    print("="*70)
    for name, success in results:
        status = "✓ PASSED" if success else "✗ FAILED"
        print(f"  {status}: {name}")
    
    passed = sum(1 for _, s in results if s)
    total = len(results)
    print(f"\n  Total: {passed}/{total} tests passed")
    print("="*70)


if __name__ == "__main__":
    main()
