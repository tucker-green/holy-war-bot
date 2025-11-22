"""
Bot Statistics Tracking
Tracks all bot activities, gold earned/spent, stat upgrades, elixir purchases, and combat results
"""

import json
from datetime import datetime
from pathlib import Path


class BotStats:
    def __init__(self, stats_file='bot_stats.json'):
        self.stats_file = stats_file
        self.stats = {
            'session_start': datetime.now().isoformat(),
            'total_gold_earned': 0,
            'total_gold_spent': 0,
            'gold_spent_on_stats': 0,
            'gold_spent_on_elixirs': 0,
            'stat_upgrades': {
                'strength': 0,
                'attack': 0,
                'defence': 0,
                'agility': 0,
                'stamina': 0
            },
            'elixirs_purchased': {
                'consecrated': {'count': 0, 'total_cost': 0},  # 50g
                'baptised': {'count': 0, 'total_cost': 0},      # 90g
                'blessed': {'count': 0, 'total_cost': 0}        # 450g
            },
            'plunder_count': 0,
            'plunder_total_minutes': 0,
            'attack_count': 0,
            'victories': 0,
            'defeats': 0,
            'training_sessions': 0,
            'total_trainings': 0
        }
        self.load()
    
    def load(self):
        """Load stats from file"""
        try:
            if Path(self.stats_file).exists():
                with open(self.stats_file, 'r') as f:
                    loaded = json.load(f)
                    # Merge loaded stats with defaults
                    self._merge_stats(loaded)
        except Exception as e:
            print(f"Warning: Could not load stats: {e}")
    
    def _merge_stats(self, loaded):
        """Merge loaded stats with current structure"""
        for key, value in loaded.items():
            if key in self.stats:
                if isinstance(value, dict) and isinstance(self.stats[key], dict):
                    self.stats[key].update(value)
                else:
                    self.stats[key] = value
    
    def save(self):
        """Save stats to file"""
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save stats: {e}")
    
    # Gold tracking
    def add_gold_earned(self, amount):
        """Track gold earned from plundering"""
        self.stats['total_gold_earned'] += amount
        self.save()
    
    def add_gold_spent_on_stat(self, stat_name, cost):
        """Track gold spent on stat training"""
        self.stats['total_gold_spent'] += cost
        self.stats['gold_spent_on_stats'] += cost
        if stat_name in self.stats['stat_upgrades']:
            self.stats['stat_upgrades'][stat_name] += 1
        self.stats['total_trainings'] += 1
        self.save()
    
    def add_gold_spent_on_elixir(self, elixir_name, cost):
        """Track gold spent on elixirs"""
        self.stats['total_gold_spent'] += cost
        self.stats['gold_spent_on_elixirs'] += cost
        
        # Map elixir name to key
        elixir_key = None
        if 'consecrated' in elixir_name.lower():
            elixir_key = 'consecrated'
        elif 'baptised' in elixir_name.lower():
            elixir_key = 'baptised'
        elif 'blessed' in elixir_name.lower():
            elixir_key = 'blessed'
        
        if elixir_key:
            self.stats['elixirs_purchased'][elixir_key]['count'] += 1
            self.stats['elixirs_purchased'][elixir_key]['total_cost'] += cost
        
        self.save()
    
    # Activity tracking
    def add_plunder(self, duration_minutes):
        """Track plunder activity"""
        self.stats['plunder_count'] += 1
        self.stats['plunder_total_minutes'] += duration_minutes
        self.save()
    
    def add_attack(self):
        """Track attack"""
        self.stats['attack_count'] += 1
        self.save()
    
    def add_victory(self):
        """Track victory"""
        self.stats['victories'] += 1
        self.save()
    
    def add_defeat(self):
        """Track defeat"""
        self.stats['defeats'] += 1
        self.save()
    
    def add_training_session(self):
        """Track training session"""
        self.stats['training_sessions'] += 1
        self.save()
    
    # Getters for dashboard
    def get_stat_upgrades(self):
        """Get stat upgrade counts"""
        return self.stats['stat_upgrades']
    
    def get_gold_summary(self):
        """Get gold earned/spent summary"""
        return {
            'earned': self.stats['total_gold_earned'],
            'spent': self.stats['total_gold_spent'],
            'net': self.stats['total_gold_earned'] - self.stats['total_gold_spent'],
            'on_stats': self.stats['gold_spent_on_stats'],
            'on_elixirs': self.stats['gold_spent_on_elixirs']
        }
    
    def get_elixir_summary(self):
        """Get elixir purchase summary"""
        return self.stats['elixirs_purchased']
    
    def get_combat_summary(self):
        """Get combat summary"""
        total = self.stats['victories'] + self.stats['defeats']
        win_rate = (self.stats['victories'] / total * 100) if total > 0 else 0
        return {
            'victories': self.stats['victories'],
            'defeats': self.stats['defeats'],
            'total': total,
            'win_rate': win_rate
        }
    
    def get_activity_summary(self):
        """Get activity summary"""
        return {
            'plunders': self.stats['plunder_count'],
            'plunder_hours': self.stats['plunder_total_minutes'] / 60,
            'attacks': self.stats['attack_count'],
            'training_sessions': self.stats['training_sessions'],
            'total_trainings': self.stats['total_trainings']
        }


# Singleton instance
_stats_instance = None


def get_stats():
    """Get or create the stats instance"""
    global _stats_instance
    if _stats_instance is None:
        _stats_instance = BotStats()
    return _stats_instance

