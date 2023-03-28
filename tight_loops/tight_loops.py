"""Main module."""

import random

def generate_random_string(length):
    """Generates a random string."""
    return ''.join([random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(length)])
