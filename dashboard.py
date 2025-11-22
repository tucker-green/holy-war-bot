"""
Holy War Bot Dashboard
Real-time web interface showing bot stats and progress
"""

from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import json
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'holy-war-bot-secret'
socketio = SocketIO(app, cors_allowed_origins="*")

# Shared state file for bot stats
STATE_FILE = 'bot_state.json'

def get_bot_state():
    """Read current bot state from file"""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    
    return {
        'status': 'Offline',
        'gold': 0,
        'level': 1,
        'plunder_status': 'Idle',
        'plunder_progress': 0,
        'plunder_time_remaining': 0,
        'last_action': 'Starting...',
        'last_update': datetime.now().isoformat(),
        'stats': {
            'strength': 0,
            'attack': 0,
            'defence': 0,
            'agility': 0,
            'stamina': 0
        }
    }

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/state')
def get_state():
    """API endpoint to get current bot state"""
    return jsonify(get_bot_state())

@socketio.on('connect')
def handle_connect():
    """Client connected"""
    print('Client connected to dashboard')
    socketio.emit('state_update', get_bot_state())

if __name__ == '__main__':
    print("="*80)
    print("Holy War Bot Dashboard")
    print("="*80)
    print("\nDashboard URL: http://localhost:5000")
    print("Open this URL in your browser to view the dashboard\n")
    print("="*80)
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)

