# test_db.py (create this in your project root)
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def test_imports():
    """Test if we can import our modules"""
    print("🔍 Testing imports...")
    try:
        from server.app.database import engine
        print("✅ Database module imported successfully!")
    except Exception as e:
        print(f"❌ Import failed: {e}")
        print("   Make sure you have:")
        print("   - app/__init__.py file")
        print("   - app/database.py file") 
        print("   - Virtual environment activated")
    
def test_database_connection():
    """Test if we can connect to the database"""
    print("🔍 Testing database connection...")
    try:
        from server.app.database import engine
        connection = engine.connect()
        print("✅ Database connection successful!")
        connection.close()
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("   Check your DATABASE_URL in config.py")

def main():
    """Run  tests step by step"""
    print("Starting database tests...\n")
    
    # Test 1: Can we import our modules?
    if not test_imports():
        print("\n❌ Fix import issues first!")
        return
    
    # Test 2: Can we connect to the database?
    if not test_database_connection():
        print("\n❌ Fix database connection issues first!")
        return
    
    

if __name__ == "__main__":
    main()