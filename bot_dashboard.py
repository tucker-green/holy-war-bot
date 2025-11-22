"""
Bot Dashboard GUI
Displays real-time stats and progress for the Holy War Bot
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime
import threading


class BotDashboard:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Holy War Bot Dashboard")
        self.root.geometry("450x800+0+0")  # Increased size for stats
        self.root.configure(bg='#1e1e1e')
        
        # Keep window on top
        self.root.attributes('-topmost', True)
        
        # Data storage
        self.data = {
            'status': 'Starting...',
            'gold': 0,
            'level': 1,
            'plunder_time_remaining': 0,
            'current_action': 'Initializing...',
            'last_update': datetime.now().strftime('%H:%M:%S'),
            'stats': {
                'strength': 0,
                'attack': 0,
                'defence': 0,
                'agility': 0,
                'stamina': 0
            }
        }
        
        self.create_widgets()
        
        # Force initial render
        self.root.update_idletasks()
        
    def create_widgets(self):
        """Create all GUI widgets"""
        # Title
        title = tk.Label(
            self.root,
            text="⚔️ HOLY WAR BOT ⚔️",
            font=('Arial', 18, 'bold'),
            bg='#1e1e1e',
            fg='#00ff00'
        )
        title.pack(pady=10)
        
        # Status Frame
        status_frame = tk.LabelFrame(
            self.root,
            text="Status",
            font=('Arial', 12, 'bold'),
            bg='#2d2d2d',
            fg='#ffffff',
            padx=10,
            pady=10
        )
        status_frame.pack(fill='x', padx=10, pady=5)
        
        self.status_label = tk.Label(
            status_frame,
            text="Status: Starting...",
            font=('Arial', 11),
            bg='#2d2d2d',
            fg='#00ff00',
            anchor='w'
        )
        self.status_label.pack(fill='x')
        
        self.action_label = tk.Label(
            status_frame,
            text="Action: Initializing...",
            font=('Arial', 10),
            bg='#2d2d2d',
            fg='#cccccc',
            anchor='w'
        )
        self.action_label.pack(fill='x', pady=(5, 0))
        
        # Gold & Level Frame
        info_frame = tk.LabelFrame(
            self.root,
            text="Character Info",
            font=('Arial', 12, 'bold'),
            bg='#2d2d2d',
            fg='#ffffff',
            padx=10,
            pady=10
        )
        info_frame.pack(fill='x', padx=10, pady=5)
        
        gold_frame = tk.Frame(info_frame, bg='#2d2d2d')
        gold_frame.pack(fill='x')
        
        tk.Label(
            gold_frame,
            text="💰 Gold:",
            font=('Arial', 11, 'bold'),
            bg='#2d2d2d',
            fg='#ffd700'
        ).pack(side='left')
        
        self.gold_label = tk.Label(
            gold_frame,
            text="0",
            font=('Arial', 11),
            bg='#2d2d2d',
            fg='#ffd700'
        )
        self.gold_label.pack(side='left', padx=5)
        
        level_frame = tk.Frame(info_frame, bg='#2d2d2d')
        level_frame.pack(fill='x', pady=(5, 0))
        
        tk.Label(
            level_frame,
            text="⭐ Level:",
            font=('Arial', 11, 'bold'),
            bg='#2d2d2d',
            fg='#00d4ff'
        ).pack(side='left')
        
        self.level_label = tk.Label(
            level_frame,
            text="1",
            font=('Arial', 11),
            bg='#2d2d2d',
            fg='#00d4ff'
        )
        self.level_label.pack(side='left', padx=5)
        
        # Stats Frame
        stats_frame = tk.LabelFrame(
            self.root,
            text="Stats",
            font=('Arial', 12, 'bold'),
            bg='#2d2d2d',
            fg='#ffffff',
            padx=10,
            pady=10
        )
        stats_frame.pack(fill='x', padx=10, pady=5)
        
        self.stat_labels = {}
        stats = ['Strength', 'Attack', 'Defence', 'Agility', 'Stamina']
        
        for stat in stats:
            frame = tk.Frame(stats_frame, bg='#2d2d2d')
            frame.pack(fill='x', pady=2)
            
            tk.Label(
                frame,
                text=f"{stat}:",
                font=('Arial', 10),
                bg='#2d2d2d',
                fg='#cccccc',
                width=10,
                anchor='w'
            ).pack(side='left')
            
            value_label = tk.Label(
                frame,
                text="0",
                font=('Arial', 10, 'bold'),
                bg='#2d2d2d',
                fg='#ffffff'
            )
            value_label.pack(side='left')
            
            self.stat_labels[stat.lower()] = value_label
        
        # Plunder Frame
        plunder_frame = tk.LabelFrame(
            self.root,
            text="Plunder",
            font=('Arial', 12, 'bold'),
            bg='#2d2d2d',
            fg='#ffffff',
            padx=10,
            pady=10
        )
        plunder_frame.pack(fill='x', padx=10, pady=5)
        
        self.plunder_time_label = tk.Label(
            plunder_frame,
            text="Time Remaining: 0 min",
            font=('Arial', 10),
            bg='#2d2d2d',
            fg='#cccccc'
        )
        self.plunder_time_label.pack()
        
        # Progress Bar
        self.progress = ttk.Progressbar(
            plunder_frame,
            mode='determinate',
            length=300
        )
        self.progress.pack(pady=5)
        
        self.progress_label = tk.Label(
            plunder_frame,
            text="0%",
            font=('Arial', 10),
            bg='#2d2d2d',
            fg='#cccccc'
        )
        self.progress_label.pack()
        
        # Statistics Frame (Scrollable)
        stats_frame = tk.LabelFrame(
            self.root,
            text="Session Statistics",
            font=('Arial', 12, 'bold'),
            bg='#2d2d2d',
            fg='#ffffff',
            padx=10,
            pady=10
        )
        stats_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create scrollable canvas for stats
        canvas = tk.Canvas(stats_frame, bg='#2d2d2d', highlightthickness=0)
        scrollbar = tk.Scrollbar(stats_frame, orient='vertical', command=canvas.yview)
        self.stats_content = tk.Frame(canvas, bg='#2d2d2d')
        
        self.stats_content.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )
        
        canvas.create_window((0, 0), window=self.stats_content, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Stats labels (will be populated)
        self.stats_labels = {}
        
        # Initialize with empty stats
        self._add_stats_section("💰 Gold", [
            "Earned: 0g",
            "Spent: 0g",
            "Net: 0g",
            "On Stats: 0g",
            "On Elixirs: 0g"
        ])
        self._add_stats_section("⬆️ Stat Upgrades", [
            "Strength: 0x",
            "Attack: 0x",
            "Defence: 0x",
            "Agility: 0x",
            "Stamina: 0x",
            "Total: 0 trainings"
        ])
        self._add_stats_section("🧪 Elixirs", [
            "Consecrated (50g): 0x = 0g",
            "Baptised (90g): 0x = 0g",
            "Blessed (450g): 0x = 0g"
        ])
        self._add_stats_section("⚔️ Combat", [
            "Victories: 0",
            "Defeats: 0",
            "Win Rate: 0.0%"
        ])
        self._add_stats_section("📊 Activity", [
            "Plunders: 0",
            "Plunder Time: 0.0h",
            "Attacks: 0",
            "Training Sessions: 0"
        ])
        
        # Last Update
        self.update_time_label = tk.Label(
            self.root,
            text="Last update: --:--:--",
            font=('Arial', 9),
            bg='#1e1e1e',
            fg='#888888'
        )
        self.update_time_label.pack(side='bottom', pady=5)
        
    def update_status(self, status):
        """Update bot status"""
        self.data['status'] = status
        self.status_label.config(text=f"Status: {status}")
        self._update_time()
        
    def update_action(self, action):
        """Update current action"""
        self.data['current_action'] = action
        self.action_label.config(text=f"Action: {action}")
        self._update_time()
        
    def update_gold(self, gold):
        """Update gold amount"""
        self.data['gold'] = gold
        self.gold_label.config(text=str(gold))
        self._update_time()
        
    def update_level(self, level):
        """Update level"""
        self.data['level'] = level
        self.level_label.config(text=str(level))
        self._update_time()
        
    def update_stats(self, **stats):
        """Update character stats"""
        for stat, value in stats.items():
            if stat in self.stat_labels:
                self.data['stats'][stat] = value
                self.stat_labels[stat].config(text=str(value))
        self._update_time()
        
    def update_plunder_time(self, minutes):
        """Update plunder time remaining"""
        self.data['plunder_time_remaining'] = minutes
        self.plunder_time_label.config(text=f"Time Remaining: {minutes} min")
        self._update_time()
        
    def update_plunder_progress(self, current, total):
        """Update plunder progress bar"""
        if total > 0:
            percentage = (current / total) * 100
            self.progress['value'] = percentage
            self.progress_label.config(text=f"{percentage:.0f}%")
        else:
            self.progress['value'] = 0
            self.progress_label.config(text="0%")
        self._update_time()
        
    def _update_time(self):
        """Update last update timestamp"""
        self.data['last_update'] = datetime.now().strftime('%H:%M:%S')
        self.update_time_label.config(text=f"Last update: {self.data['last_update']}")
    
    def update_statistics(self, stats_data):
        """Update the statistics display"""
        # Clear existing stats
        for widget in self.stats_content.winfo_children():
            widget.destroy()
        
        # Gold Summary
        self._add_stats_section("💰 Gold", [
            f"Earned: {stats_data.get('gold_earned', 0):,}g",
            f"Spent: {stats_data.get('gold_spent', 0):,}g",
            f"Net: {stats_data.get('gold_net', 0):,}g",
            f"On Stats: {stats_data.get('gold_on_stats', 0):,}g",
            f"On Elixirs: {stats_data.get('gold_on_elixirs', 0):,}g"
        ])
        
        # Stat Upgrades
        upgrades = stats_data.get('stat_upgrades', {})
        self._add_stats_section("⬆️ Stat Upgrades", [
            f"Strength: {upgrades.get('strength', 0)}x",
            f"Attack: {upgrades.get('attack', 0)}x",
            f"Defence: {upgrades.get('defence', 0)}x",
            f"Agility: {upgrades.get('agility', 0)}x",
            f"Stamina: {upgrades.get('stamina', 0)}x",
            f"Total: {stats_data.get('total_trainings', 0)} trainings"
        ])
        
        # Elixirs
        elixirs = stats_data.get('elixirs', {})
        self._add_stats_section("🧪 Elixirs", [
            f"Consecrated (50g): {elixirs.get('consecrated_count', 0)}x = {elixirs.get('consecrated_cost', 0)}g",
            f"Baptised (90g): {elixirs.get('baptised_count', 0)}x = {elixirs.get('baptised_cost', 0)}g",
            f"Blessed (450g): {elixirs.get('blessed_count', 0)}x = {elixirs.get('blessed_cost', 0)}g"
        ])
        
        # Combat
        self._add_stats_section("⚔️ Combat", [
            f"Victories: {stats_data.get('victories', 0)}",
            f"Defeats: {stats_data.get('defeats', 0)}",
            f"Win Rate: {stats_data.get('win_rate', 0):.1f}%"
        ])
        
        # Activity
        self._add_stats_section("📊 Activity", [
            f"Plunders: {stats_data.get('plunders', 0)}",
            f"Plunder Time: {stats_data.get('plunder_hours', 0):.1f}h",
            f"Attacks: {stats_data.get('attacks', 0)}",
            f"Training Sessions: {stats_data.get('training_sessions', 0)}"
        ])
        
        self._update_time()
    
    def _add_stats_section(self, title, items):
        """Add a section of stats"""
        # Section title
        title_label = tk.Label(
            self.stats_content,
            text=title,
            font=('Arial', 10, 'bold'),
            bg='#2d2d2d',
            fg='#00d4ff',
            anchor='w'
        )
        title_label.pack(fill='x', pady=(5, 2))
        
        # Items
        for item in items:
            item_label = tk.Label(
                self.stats_content,
                text=f"  {item}",
                font=('Arial', 9),
                bg='#2d2d2d',
                fg='#cccccc',
                anchor='w'
            )
            item_label.pack(fill='x', pady=1)
        
        # Separator
        separator = tk.Frame(self.stats_content, height=1, bg='#444444')
        separator.pack(fill='x', pady=5)
        
    def start(self):
        """Start the dashboard in the main thread"""
        # This should be called from the main thread
        pass
    
    def run(self):
        """Run the dashboard mainloop (must be called from main thread)"""
        self.root.mainloop()
        
    def update_in_thread(self, func):
        """Schedule an update in the main thread"""
        self.root.after(0, func)
        
    def stop(self):
        """Stop the dashboard"""
        try:
            self.root.quit()
            self.root.destroy()
        except:
            pass


# Singleton instance
_dashboard_instance = None


def get_dashboard():
    """Get or create the dashboard instance"""
    global _dashboard_instance
    if _dashboard_instance is None:
        _dashboard_instance = BotDashboard()
    return _dashboard_instance

