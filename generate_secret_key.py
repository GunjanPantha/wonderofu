#!/usr/bin/env python3
"""
Generate a secure Django SECRET_KEY for production
"""
import secrets
import string

def generate_secret_key(length=50):
    """Generate a secure random secret key"""
    characters = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    return ''.join(secrets.choice(characters) for _ in range(length))

if __name__ == "__main__":
    secret_key = generate_secret_key()
    print("=" * 60)
    print("🔐 Generated Django SECRET_KEY for production:")
    print("=" * 60)
    print(secret_key)
    print("=" * 60)
    print("Copy this key and set it as the SECRET_KEY environment variable")
    print("in your hosting platform (Railway, Render, Heroku, etc.)")
    print("=" * 60)
