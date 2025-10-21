"""
Session Manager - Maps Stripe session IDs to generated PDFs
"""
import json
import os
from datetime import datetime, timedelta

SESSION_FILE = 'session_pdf_mapping.json'

def load_sessions():
    """Load session mapping from file"""
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_sessions(sessions):
    """Save session mapping to file"""
    with open(SESSION_FILE, 'w') as f:
        json.dump(sessions, f, indent=2)

def register_session(session_id, pdf_filename, email):
    """Register a session with its generated PDF"""
    sessions = load_sessions()
    sessions[session_id] = {
        'pdf_filename': pdf_filename,
        'email': email,
        'created_at': datetime.now().isoformat(),
        'status': 'completed'
    }
    save_sessions(sessions)
    
def get_session_pdf(session_id):
    """Get PDF filename for a session"""
    sessions = load_sessions()
    return sessions.get(session_id)

def clean_old_sessions(days=7):
    """Remove sessions older than X days"""
    sessions = load_sessions()
    cutoff = datetime.now() - timedelta(days=days)
    
    cleaned = {
        sid: data for sid, data in sessions.items()
        if datetime.fromisoformat(data['created_at']) > cutoff
    }
    
    save_sessions(cleaned)
    return len(sessions) - len(cleaned)
