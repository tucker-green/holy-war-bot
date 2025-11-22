"""
Bot Dashboard GUI - Kivy Implementation
Displays real-time stats and progress for the Holy War Bot
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.core.window import Window
from datetime import datetime
import threading


class BotDashboard(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        
        # Set dark background
        with self.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.12, 0.12, 0.12, 1)  # Dark gray
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)
        
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
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Title
        title = Label(
            text='[color=00ff00]⚔️ HOLY WAR BOT ⚔️[/color]',
            markup=True,
            font_size='24sp',
            size_hint=(1, None),
            height=50
        )
        self.add_widget(title)
        
        # Status
        self.status_label = Label(
            text='[color=00ff00]Status: Starting...[/color]',
            markup=True,
            font_size='14sp',
            size_hint=(1, None),
            height=30
        )
        self.add_widget(self.status_label)
        
        self.action_label = Label(
            text='[color=cccccc]Action: Initializing...[/color]',
            markup=True,
            font_size='12sp',
            size_hint=(1, None),
            height=25
        )
        self.add_widget(self.action_label)
        
        # Gold & Level
        self.gold_label = Label(
            text='[color=ffd700]💰 Gold: 0[/color]',
            markup=True,
            font_size='14sp',
            size_hint=(1, None),
            height=30
        )
        self.add_widget(self.gold_label)
        
        self.level_label = Label(
            text='[color=00d4ff]⭐ Level: 1[/color]',
            markup=True,
            font_size='14sp',
            size_hint=(1, None),
            height=30
        )
        self.add_widget(self.level_label)
        
        # Stats
        stats_label = Label(
            text='[color=ffffff][b]Stats[/b][/color]',
            markup=True,
            font_size='14sp',
            size_hint=(1, None),
            height=25
        )
        self.add_widget(stats_label)
        
        self.stat_labels = {}
        stats = ['strength', 'attack', 'defence', 'agility', 'stamina']
        for stat in stats:
            label = Label(
                text=f'[color=cccccc]{stat.capitalize()}: 0[/color]',
                markup=True,
                font_size='12sp',
                size_hint=(1, None),
                height=20
            )
            self.add_widget(label)
            self.stat_labels[stat] = label
        
        # Plunder
        plunder_label = Label(
            text='[color=ffffff][b]Plunder[/b][/color]',
            markup=True,
            font_size='14sp',
            size_hint=(1, None),
            height=25
        )
        self.add_widget(plunder_label)
        
        self.plunder_time_label = Label(
            text='[color=cccccc]Time Remaining: 0 min[/color]',
            markup=True,
            font_size='12sp',
            size_hint=(1, None),
            height=20
        )
        self.add_widget(self.plunder_time_label)
        
        # Progress Bar
        self.progress_bar = ProgressBar(
            max=100,
            size_hint=(1, None),
            height=20
        )
        self.add_widget(self.progress_bar)
        
        self.progress_label = Label(
            text='[color=cccccc]0%[/color]',
            markup=True,
            font_size='12sp',
            size_hint=(1, None),
            height=20
        )
        self.add_widget(self.progress_label)
        
        # Session Statistics (Scrollable)
        stats_title = Label(
            text='[color=ffffff][b]Session Statistics[/b][/color]',
            markup=True,
            font_size='14sp',
            size_hint=(1, None),
            height=30
        )
        self.add_widget(stats_title)
        
        # Scrollable stats content
        scroll_view = ScrollView(size_hint=(1, 1))
        self.stats_content = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        self.stats_content.bind(minimum_height=self.stats_content.setter('height'))
        scroll_view.add_widget(self.stats_content)
        self.add_widget(scroll_view)
        
        # Initialize stats display
        self._init_stats_display()
        
        # Last update
        self.update_time_label = Label(
            text='[color=888888]Last update: --:--:--[/color]',
            markup=True,
            font_size='10sp',
            size_hint=(1, None),
            height=20
        )
        self.add_widget(self.update_time_label)
    
    def _init_stats_display(self):
        """Initialize statistics with default values"""
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
    
    def _add_stats_section(self, title, items):
        """Add a section of stats"""
        # Section title
        title_label = Label(
            text=f'[color=00d4ff][b]{title}[/b][/color]',
            markup=True,
            font_size='12sp',
            size_hint_y=None,
            height=25
        )
        self.stats_content.add_widget(title_label)
        
        # Items
        for item in items:
            item_label = Label(
                text=f'[color=cccccc]  {item}[/color]',
                markup=True,
                font_size='11sp',
                size_hint_y=None,
                height=20
            )
            self.stats_content.add_widget(item_label)
    
    def update_status(self, status):
        """Update bot status"""
        self.data['status'] = status
        Clock.schedule_once(lambda dt: self._do_update_status(status), 0)
    
    def _do_update_status(self, status):
        self.status_label.text = f'[color=00ff00]Status: {status}[/color]'
        self._update_time()
    
    def update_action(self, action):
        """Update current action"""
        self.data['current_action'] = action
        Clock.schedule_once(lambda dt: self._do_update_action(action), 0)
    
    def _do_update_action(self, action):
        self.action_label.text = f'[color=cccccc]Action: {action}[/color]'
        self._update_time()
    
    def update_gold(self, gold):
        """Update gold amount"""
        self.data['gold'] = gold
        Clock.schedule_once(lambda dt: self._do_update_gold(gold), 0)
    
    def _do_update_gold(self, gold):
        self.gold_label.text = f'[color=ffd700]💰 Gold: {gold}[/color]'
        self._update_time()
    
    def update_level(self, level):
        """Update level"""
        self.data['level'] = level
        Clock.schedule_once(lambda dt: self._do_update_level(level), 0)
    
    def _do_update_level(self, level):
        self.level_label.text = f'[color=00d4ff]⭐ Level: {level}[/color]'
        self._update_time()
    
    def update_stats(self, **stats):
        """Update character stats"""
        Clock.schedule_once(lambda dt: self._do_update_stats(stats), 0)
    
    def _do_update_stats(self, stats):
        for stat, value in stats.items():
            if stat in self.stat_labels:
                self.data['stats'][stat] = value
                self.stat_labels[stat].text = f'[color=cccccc]{stat.capitalize()}: {value}[/color]'
        self._update_time()
    
    def update_plunder_time(self, minutes):
        """Update plunder time remaining"""
        self.data['plunder_time_remaining'] = minutes
        Clock.schedule_once(lambda dt: self._do_update_plunder_time(minutes), 0)
    
    def _do_update_plunder_time(self, minutes):
        self.plunder_time_label.text = f'[color=cccccc]Time Remaining: {minutes} min[/color]'
        self._update_time()
    
    def update_plunder_progress(self, current, total):
        """Update plunder progress bar"""
        Clock.schedule_once(lambda dt: self._do_update_plunder_progress(current, total), 0)
    
    def _do_update_plunder_progress(self, current, total):
        if total > 0:
            percentage = (current / total) * 100
            self.progress_bar.value = percentage
            self.progress_label.text = f'[color=cccccc]{percentage:.0f}%[/color]'
        else:
            self.progress_bar.value = 0
            self.progress_label.text = '[color=cccccc]0%[/color]'
        self._update_time()
    
    def update_statistics(self, stats_data):
        """Update the statistics display"""
        Clock.schedule_once(lambda dt: self._do_update_statistics(stats_data), 0)
    
    def _do_update_statistics(self, stats_data):
        # Clear existing stats
        self.stats_content.clear_widgets()
        
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
    
    def _update_time(self):
        """Update last update timestamp"""
        self.data['last_update'] = datetime.now().strftime('%H:%M:%S')
        self.update_time_label.text = f'[color=888888]Last update: {self.data["last_update"]}[/color]'
    
    def update_in_thread(self, func):
        """Schedule an update in the main thread"""
        Clock.schedule_once(lambda dt: func(), 0)


class DashboardApp(App):
    def build(self):
        Window.size = (450, 800)
        Window.clearcolor = (0.12, 0.12, 0.12, 1)
        self.dashboard = BotDashboard()
        return self.dashboard
    
    def get_dashboard(self):
        return self.dashboard


# Global app instance
_app_instance = None
_dashboard_instance = None


def get_dashboard():
    """Get or create the dashboard instance"""
    global _app_instance, _dashboard_instance
    if _app_instance is None:
        _app_instance = DashboardApp()
        # Build the app but don't run it yet
        _app_instance.build()
        _dashboard_instance = _app_instance.dashboard
    return _dashboard_instance


def run_dashboard():
    """Run the dashboard app (must be called from main thread)"""
    global _app_instance, _dashboard_instance
    if _app_instance is None:
        _app_instance = DashboardApp()
        _app_instance.build()
        _dashboard_instance = _app_instance.dashboard
    _app_instance.run()
