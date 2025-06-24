#!/usr/bin/env python3
"""Test script to repopulate NPB database with updated historical data including Tuffy Rhodes."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.npb.data.database import NPBDatabase
from src.npb.data.historical_data import populate_test_data

def main():
    """Repopulate the NPB database with updated historical data."""
    print("Repopulating NPB database with historical data...")
    
    # Initialize database (this will create tables if needed)
    db = NPBDatabase()
    
    # Clear existing data
    with db.get_connection() as conn:
        cursor = conn.cursor()
        # Clear in correct order due to foreign keys
        cursor.execute("DELETE FROM batting_stats")
        cursor.execute("DELETE FROM pitching_stats")
        cursor.execute("DELETE FROM players")
        cursor.execute("DELETE FROM teams")
        conn.commit()
    
    print("Cleared existing data.")
    
    # Populate with test data (now includes Tuffy Rhodes)
    populate_test_data(db)
    
    print("Database repopulated successfully!")
    
    # Verify Tuffy Rhodes was added
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.name_english, COUNT(bs.season) as seasons, 
                   SUM(bs.home_runs) as total_hrs
            FROM players p
            JOIN batting_stats bs ON p.player_id = bs.player_id
            WHERE p.player_id = 'rhodes-tuffy'
            GROUP BY p.player_id
        """)
        result = cursor.fetchone()
        
        if result:
            print(f"\nVerified: {result[0]} - {result[1]} seasons, {result[2]} home runs")
        else:
            print("\nERROR: Tuffy Rhodes not found in database!")

if __name__ == "__main__":
    main()