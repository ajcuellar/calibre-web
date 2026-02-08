#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Migration script for adding notification fields to Calibre-Web user database
This script adds the following fields to the User table:
- phone_number
- telegram_id
- notification_preferences

Usage:
    python migrate_notifications.py

Note: Backup your app.db before running this script!
"""

import sqlite3
import json
import os
import sys
from pathlib import Path

# Default notification preferences
DEFAULT_NOTIFICATION_PREFS = {
    "new_books": {
        "email": True,
        "whatsapp": False,
        "telegram": False,
        "push": False
    }
}


def find_database():
    """Find the Calibre-Web app.db database"""
    # Common locations
    possible_paths = [
        'app.db',
        './app.db',
        '../app.db',
        os.path.expanduser('~/.config/calibre-web/app.db'),
        '/var/lib/calibre-web/app.db',
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    # Ask user
    print("Could not find app.db automatically.")
    db_path = input("Please enter the path to your app.db file: ").strip()
    if os.path.exists(db_path):
        return db_path
    
    return None


def backup_database(db_path):
    """Create a backup of the database"""
    backup_path = f"{db_path}.backup"
    try:
        import shutil
        shutil.copy2(db_path, backup_path)
        print(f"✓ Database backed up to: {backup_path}")
        return True
    except Exception as e:
        print(f"✗ Failed to create backup: {e}")
        return False


def check_column_exists(cursor, table, column):
    """Check if a column exists in a table"""
    cursor.execute(f"PRAGMA table_info({table})")
    columns = [col[1] for col in cursor.fetchall()]
    return column in columns


def migrate_database(db_path):
    """Add notification fields to the user table"""
    print(f"\nMigrating database: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if columns already exist
        phone_exists = check_column_exists(cursor, 'user', 'phone_number')
        telegram_exists = check_column_exists(cursor, 'user', 'telegram_id')
        prefs_exists = check_column_exists(cursor, 'user', 'notification_preferences')
        
        if phone_exists and telegram_exists and prefs_exists:
            print("✓ All notification columns already exist. No migration needed.")
            conn.close()
            return True
        
        # Add phone_number column
        if not phone_exists:
            print("Adding phone_number column...")
            cursor.execute('ALTER TABLE user ADD COLUMN phone_number VARCHAR(20) DEFAULT ""')
            print("✓ phone_number column added")
        else:
            print("✓ phone_number column already exists")
        
        # Add telegram_id column
        if not telegram_exists:
            print("Adding telegram_id column...")
            cursor.execute('ALTER TABLE user ADD COLUMN telegram_id VARCHAR(120) DEFAULT ""')
            print("✓ telegram_id column added")
        else:
            print("✓ telegram_id column already exists")
        
        # Add notification_preferences column
        if not prefs_exists:
            print("Adding notification_preferences column...")
            cursor.execute('ALTER TABLE user ADD COLUMN notification_preferences JSON')
            
            # Set default notification preferences for all existing users
            default_prefs_json = json.dumps(DEFAULT_NOTIFICATION_PREFS)
            cursor.execute('UPDATE user SET notification_preferences = ?', (default_prefs_json,))
            print("✓ notification_preferences column added with default values")
        else:
            print("✓ notification_preferences column already exists")
        
        # Commit changes
        conn.commit()
        
        # Verify migration
        cursor.execute("SELECT COUNT(*) FROM user")
        user_count = cursor.fetchone()[0]
        print(f"\n✓ Migration completed successfully!")
        print(f"  {user_count} users in database ready for notifications")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"\n✗ Migration failed: {e}")
        return False


def main():
    print("=" * 60)
    print("Calibre-Web Notifications Migration Script")
    print("=" * 60)
    
    # Find database
    db_path = find_database()
    if not db_path:
        print("\n✗ Could not find app.db database")
        sys.exit(1)
    
    print(f"\nFound database: {db_path}")
    
    # Ask for confirmation
    response = input("\nDo you want to proceed with migration? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("Migration cancelled.")
        sys.exit(0)
    
    # Backup database
    if not backup_database(db_path):
        response = input("\nBackup failed. Continue anyway? (yes/no): ").strip().lower()
        if response not in ['yes', 'y']:
            print("Migration cancelled.")
            sys.exit(1)
    
    # Migrate
    success = migrate_database(db_path)
    
    if success:
        print("\n" + "=" * 60)
        print("Migration completed successfully!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Restart Calibre-Web")
        print("2. Configure notification services in Admin → Configuration")
        print("3. Users can set their notification preferences in their profile")
        print("\nSee NOTIFICATIONS.md for detailed configuration instructions.")
    else:
        print("\n" + "=" * 60)
        print("Migration failed!")
        print("=" * 60)
        print("\nYou can restore from backup:")
        print(f"  cp {db_path}.backup {db_path}")
        sys.exit(1)


if __name__ == "__main__":
    main()
