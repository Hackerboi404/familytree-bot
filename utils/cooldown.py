import time

# Simple dictionary to store last command time
user_cooldowns = {}

def check_cooldown(user_id, cooldown_time=2):
    """Returns True if allowed, False if cooldown active."""
    current_time = time.time()
    last_time = user_cooldowns.get(user_id, 0)
    
    if current_time - last_time < cooldown_time:
        return False
    
    user_cooldowns[user_id] = current_time
    return True
