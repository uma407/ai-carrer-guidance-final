import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os

def init_db():
    """Initialize the SQLite database"""
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'career_guidance.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            is_admin BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create user_profiles table
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_profiles (
            user_id INTEGER PRIMARY KEY,
            full_name TEXT,
            education_level TEXT,
            skills TEXT,
            interests TEXT,
            career_goals TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create learning_resources table
    c.execute('''
        CREATE TABLE IF NOT EXISTS learning_resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            url TEXT,
            category TEXT,
            added_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (added_by) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def create_user(username, password, email, is_admin=False):
    """Create a new user"""
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'career_guidance.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    try:
        password_hash = generate_password_hash(password)
        c.execute('INSERT INTO users (username, password_hash, email, is_admin) VALUES (?, ?, ?, ?)',
                 (username, password_hash, email, is_admin))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(username, password):
    """Verify user credentials"""
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'career_guidance.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    c.execute('SELECT id, password_hash, is_admin FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    
    if user and check_password_hash(user[1], password):
        return {'id': user[0], 'is_admin': user[2]}
    return None

def update_user_profile(user_id, profile_data):
    """Update user profile"""
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'career_guidance.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    try:
        c.execute('''
            INSERT OR REPLACE INTO user_profiles 
            (user_id, full_name, education_level, skills, interests, career_goals)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, profile_data['full_name'], profile_data['education_level'],
              profile_data['skills'], profile_data['interests'], profile_data['career_goals']))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def get_user_profile(user_id):
    """Get user profile"""
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'career_guidance.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    c.execute('SELECT * FROM user_profiles WHERE user_id = ?', (user_id,))
    profile = c.fetchone()
    conn.close()
    
    if profile:
        return {
            'full_name': profile[1],
            'education_level': profile[2],
            'skills': profile[3],
            'interests': profile[4],
            'career_goals': profile[5]
        }
    return None

def add_learning_resource(title, description, url, category, added_by):
    """Add a new learning resource"""
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'career_guidance.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    try:
        c.execute('''
            INSERT INTO learning_resources (title, description, url, category, added_by)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, description, url, category, added_by))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def get_learning_resources(category=None):
    """Get learning resources"""
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'career_guidance.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    if category:
        c.execute('SELECT * FROM learning_resources WHERE category = ?', (category,))
    else:
        c.execute('SELECT * FROM learning_resources')
    
    resources = c.fetchall()
    conn.close()
    
    return [{
        'id': r[0],
        'title': r[1],
        'description': r[2],
        'url': r[3],
        'category': r[4],
        'added_by': r[5],
        'created_at': r[6]
    } for r in resources]