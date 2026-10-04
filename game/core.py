import os
import math
import heapq
import random
import json
import pygame

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700
WORLD_WIDTH = 4000
WORLD_HEIGHT = 3000
PLAYER_SPEED = 4.0
COMPANION_SPEED = 3.5
NPC_MIN_SPEED = 1.0
NPC_MAX_SPEED = 1.7
NPC_INTERACTION_DISTANCE = 115
FPS = 60
# One full in-game day lasts 6 real minutes.
GAME_DAY_LENGTH_MS = 6 * 60 * 1000
NPC_HOME_HOUR = 20
NPC_WAKE_HOUR = 6

GAME_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(GAME_DIR)
ASSET_DIR = os.path.join(PROJECT_DIR, "assets", "fairies")

def asset_path(filename):
    return os.path.join(ASSET_DIR, filename)

def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))

def distance(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)

def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = word if not current else current + " " + word
        if font.size(test)[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines

def load_image(filename, size=None):
    path = asset_path(filename)
    if not os.path.exists(path):
        return None
    try:
        image = pygame.image.load(path).convert_alpha()
        if size:
            image = pygame.transform.smoothscale(image, size)
        return image
    except pygame.error:
        return None

