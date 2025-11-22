"""
Configuration file for Holy War Bot
Edit these values to customize bot behavior
"""

# Login credentials
USERNAME = "tvcker"
PASSWORD = "174210Tg"
WORLD = "17IN"  # e.g., "17IN" for International World 17

# Gold management
MIN_GOLD_RESERVE = 10  # Always keep this much gold
ELIXIR_THRESHOLD = 100  # Buy elixirs when gold exceeds this (and can't train anymore)

# Plunder settings
PLUNDER_DURATION_MINUTES = 10  # How long each plunder lasts (10, 20, 30, 40, 50, or 60)

# Attack settings
TARGET_PLAYER_LEVEL = 1  # What level of players to attack
ATTACK_COOLDOWN_MINUTES = 5  # Wait time between attacks

# Training priorities (order matters - trains in this order)
TRAINING_PRIORITY = [
    "Strength",
    "Attack",
    "Defence",
    "Agility",
    "Stamina"
]

# Browser settings
HEADLESS = False  # Set to True to run browser in background

