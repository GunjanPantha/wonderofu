#!/usr/bin/env python
"""
Simple test script to verify Django setup
"""
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

try:
    import django
    print(f"✅ Django {django.get_version()} is installed")
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    django.setup()
    print("✅ Django setup completed")
    
    # Test imports
    from django.http import HttpResponse
    print("✅ Django imports working")
    
    # Test our modules
    import views
    print("✅ Views module imported successfully")
    
    import ai_service
    print("✅ AI service module imported successfully")
    
    print("\n🎮 Game setup appears to be working!")
    print("You can now run: python manage.py runserver")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
