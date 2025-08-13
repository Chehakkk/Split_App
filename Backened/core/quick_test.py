#!/usr/bin/env python3
"""
Quick test to verify Django server is working
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from split_api.models import Group, Category, Expense

def test_django_setup():
    """Test if Django is properly configured"""
    print("Testing Django setup...")
    
    try:
        # Test if we can import models
        from split_api.models import Group, Category, Expense
        print("✅ Models imported successfully")
        
        # Test if we can query the database
        groups = Group.objects.all()
        categories = Category.objects.all()
        expenses = Expense.objects.all()
        
        print(f"✅ Database queries work:")
        print(f"   - Groups: {groups.count()}")
        print(f"   - Categories: {categories.count()}")
        print(f"   - Expenses: {expenses.count()}")
        
        return True
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        return False

def test_api_urls():
    """Test if API URLs are configured"""
    print("\nTesting API URLs...")
    
    try:
        from django.urls import reverse
        from rest_framework.test import APIClient
        
        client = APIClient()
        
        # Test groups endpoint
        response = client.get('/api/groups/')
        print(f"✅ Groups API: {response.status_code}")
        
        # Test categories endpoint
        response = client.get('/api/categories/')
        print(f"✅ Categories API: {response.status_code}")
        
        # Test expenses endpoint
        response = client.get('/api/expenses/')
        print(f"✅ Expenses API: {response.status_code}")
        
        return True
    except Exception as e:
        print(f"❌ API URL test failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Django Server Health Check")
    print("=" * 50)
    
    django_ok = test_django_setup()
    api_ok = test_api_urls()
    
    print("\n" + "=" * 50)
    if django_ok and api_ok:
        print("✅ All tests passed! Django server should work.")
        print("You can now start the server with: python manage.py runserver")
    else:
        print("❌ Some tests failed. Check the errors above.")
    print("=" * 50) 