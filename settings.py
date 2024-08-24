import pygame as pg
import os

pg.init()

#Set screen size
size = (640, 360)

#Game screen
screen = pg.display.set_mode(size)
pg.display.set_caption("Turtle Boss")

#Game font
def font(size):
  font = pg.font.Font('freesansbold.ttf', size)
  return font

#Finds current directory
dir = os.path.dirname(os.path.realpath(__file__))
