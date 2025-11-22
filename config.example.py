# config.py
# Configuration file for Holy War Bot

# Login credentials
USERNAME = "your_username"  # Your game username
PASSWORD = "your_password"  # Your game password
WORLD = "17IN"              # Your world (e.g., "17IN" for International World 17)

# Gold management
MIN_GOLD_RESERVE = 10       # Minimum gold to keep at all times
ELIXIR_THRESHOLD = 65       # Buy elixirs when gold exceeds this (and can't train)

# Plunder settings
PLUNDER_DURATION_MINUTES = 10  # Duration of each plunder (10, 20, 30, 40, 50, or 60)

# Attack settings
TARGET_PLAYER_LEVEL = 1     # Level of players to attack when no plunder time
ATTACK_COOLDOWN_MINUTES = 5 # Wait time between attacks

# Browser settings
HEADLESS = False            # Set to True to run browser in background

