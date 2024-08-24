import pygame as pg

import object
import settings

pg.init()

size = (width, height) = settings.size


#Player class
class Player(object.Object):
  def __init__(self, type, location, size=False):
    #Inherits Object class
    object.Object.__init__(self, type, location, size)
    #A static (not rotated) surface image
    self.static_image = self.image
    #Sets player speed
    self.speed = 3

    #Mask used for hit detection
    self.mask = pg.mask.from_surface(self.image)
    
  #Updates the mask (required when turtle turns)
  def update_mask(self):
    self.mask = pg.mask.from_surface(self.image)
      
  def move(self, keys, boss):
    #Keys[pg.K_key] detects true or false (1 or 0) for movement
    right = keys[pg.K_d] or keys[pg.K_RIGHT]
    left = keys[pg.K_a] or keys[pg.K_LEFT]
    up = keys[pg.K_w] or keys[pg.K_UP]
    down = keys[pg.K_s] or keys[pg.K_DOWN]

    #Then subtracts directions from eachother and * by speed
    horz_change = (right - left) * self.speed
    vert_change = (down - up) * self.speed
    
    #Prevents player from going out of bounds
    #Horizontal bounds
    if self.rect.left + horz_change < 0:
      #Sets player location + removes change
      self.rect.left = 0
      horz_change = 0
    #Uses boss.rect.left instead of width so player cannot run through/past boss
    elif self.rect.right + horz_change > boss.rect.left:
      #Sets player location + removes change
      self.rect.right = boss.rect.left
      horz_change = 0
      
    #Vertical Bounds
    if self.rect.top + vert_change < 0:
      #Sets player location + removes change
      self.rect.top = 0
      vert_change = 0
    elif self.rect.bottom + vert_change > height:
      #Sets player location + removes change
      self.rect.bottom = height
      vert_change = 0

    
    #Diagonal movement
    if horz_change != 0 and vert_change != 0:
      #So you only go {speed} forward, not {speed} up and {speed} down
      #a^2 + b^2 = speed^2 where a == b
      #2a^2 = speed^2
      #a^2 = speed^2 / 2
      #a = sqrt(speed^2 / 2)
      #Negative when going left/up
      if horz_change < 0:
        horz_change = -((self.speed**2 / 2)**0.5)
      else:
        horz_change = (self.speed**2 / 2)**0.5
        
      if vert_change < 0:
        vert_change = -((self.speed**2 / 2)**0.5)
      else:
        vert_change = (self.speed**2 / 2)**0.5

    #Moves player
    self.rect = self.rect.move(round(horz_change), round(vert_change))
    #Rotates according to movement
    self.rotate(horz_change, vert_change)
      
      
    
  #Rotates the player to face movement direction
  def rotate(self, horz_change, vert_change):
    #All rotations are counterclockwise
    #Turtle faces right by defualt
    
    turn = 0 #Right = 0
    #1st Up
    if vert_change < 0:
      turn += 90
      if horz_change < 0: #if 2nd Left
        turn += 45
      #2nd Right
      elif horz_change > 0: #elif 2nd Right
        turn -= 45
    #1st Down
    elif vert_change > 0:
      turn -= 90
      if horz_change < 0: #2nd Left
        turn -= 45
      elif horz_change > 0: #2nd Right
        turn += 45
    #1st Left
    elif horz_change < 0:
      turn += 180
    #1st Right 
      #turn = 0 (already 0 by defualt)

    #If turtle has moved,
    if horz_change != 0 or vert_change != 0:
      #Turn defualt model by {turn} degrees
      self.image = pg.transform.rotate(self.static_image, turn).convert_alpha()
      self.update_mask()