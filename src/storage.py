import sqlite3
import os
from datetime import datetime

class JobDataBase:
    def __init__(self, db_path="data/job_history.db"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row 
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        """Initialization of the file if it doesn't exist"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                company TEXT,
                location TEXT,
                url TEXT UNIQUE,
                date_found DATETIME,
                source TEXT,
                description TEXT,
                is_new BOOLEAN DEFAULT 1
            )
        ''')
        self.conn.commit()
    
    def save_jobs(self, jobs_list, source="LinkedIn"):
        """
        Save jobs list 
        Return number of new added offers
        """
        new_count = 0
        today = datetime.now().strftime("%Y-%m-%d %H:%H:%S")

        for job in jobs_list :
            try:
                self.cursor.execute('''
                    INSERT INTO jobs (title, company, location, url, date_found, source, description, is_new)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 1)
                ''', (
                    job.get('title'),
                    job.get('company'),
                    job.get('location'),
                    job.get('url'),
                    today,
                    source,
                    job.get('description', ''),
                ))
                new_count +=1
                print(f"[NEW] {job.get('title')} at {job.get('company')}")
            except sqlite3.IntegrityError : 
                pass
        self.conn.commit()
        return new_count
    
    def get_recent_jobs(self, limit=50):
        """Get new jobs for the report"""
        self.cursor.execute('''
            SELECT title, company, location, url, source, description, date_found, is_new
            FROM jobs
            ORDER BY date_found DESC
            LIMIT ?
        ''', (limit,))
        return [dict(row) for row in self.cursor.fetchall()]
    
    def mark_as_seen(self):
        """
        Called after the generation of the report
        Set 'is_new' to 0 to avoid seeing it in the next report
        """
        self.cursor.execute('UPDATE jobs SET is_new = 0 WHERE is_new = 1')
        self.conn.commit()
    
    def close(self):
        self.conn.close()

                