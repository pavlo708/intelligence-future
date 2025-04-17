import pygame as pg  

SCREEN_WIDTH = 822
SCREEN_HEIGHT = 562
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Soul Knight")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Цвета кнопок
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 200)
RED = (255, 0, 0)
DARK_RED = (200, 0, 0)
GRAY = (150, 150, 150)
DARK_GRAY = (100, 100, 100)
GOLD = (255, 215, 0)  # Используется для текста денег в магазине

# Частота кадров
clock = pg.time.Clock()
FPS = 60