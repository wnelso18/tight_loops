"""Main module."""

import random

def generate_random_string(length=15):
    """Generates a random string."""
    return ''.join([random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(length)])
