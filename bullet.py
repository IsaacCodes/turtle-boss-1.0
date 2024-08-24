import pygame as pg
import random as r

import object

import settings

pg.init()


size = width, height = settings.size

#Bullet groups
bullet_group = pg.sprite.Group()
waiting_bullet_group = pg.sprite.Group()
active_bullet_group = pg.sprite.Group()

def reset_groups():
  global bullet_group, waiting_bullet_group, active_bullet_group
  #Bullet groups
  bullet_group.empty()
  waiting_bullet_group.empty()
  active_bullet_group.empty()

#Bullet class
class Bullet(object.Object):
  def __init__(self, type, location, sizes, size=False, color=pg.Color("black"), active=False, bullet_type="normal"):
    object.Object.__init__(self, type, location, size, color)

    #Bullet id number 
    #Mainly used for distinguishing bullets during testing
    self.id = ""
    for i in range(6):
      self.id += str(r.randint(0, 9))
    
    #Bullet type (normal or mortar)
    self.bullet_type = bullet_type
    
    #Original location (used for mortar bullet calcs)
    self.original_pos = location

    #Varying a value for mortar equation 
    self.quad_a = r.randint(1, 75)/10000 #Between .0001 and .0075
    
    #Mask used for hit detection
    self.mask = pg.mask.from_surface(self.image)

    #Bullet (circle) diameter
    diameter = self.image.get_size()[0]
    #Possible sizes for each category
    large = [False, sizes[0][0]+1,sizes[0][0],sizes[0][0]-1]
    medium = [sizes[1][0]+1,sizes[1][0],sizes[1][0]-1]
    small = [sizes[2][0]+1,sizes[2][0],sizes[2][0]-1]

    #Sets bullet speed based off of size (radius)
    if diameter in large:
      self.speed = 1
    elif diameter in medium:
      self.speed = 2
    elif diameter in small:
      self.speed = 3
    else:
      self.speed = 1

      
    #Adds sprite to the bullet group
    bullet_group.add(self)
      
    #Adds sprite to the active bullet group
    if active == True:
      active_bullet_group.add(self)
    else:
      waiting_bullet_group.add(self)

  #Moves the bullets
  def move(self):
    #For mortar type bullets
    if self.bullet_type == "mortar":
      #print(f"{self.id}: ({self.rect.x}, {self.rect.y})\r")
      
      #Opens downwards due to left left being (0, 0)
      #y = a(x - h)^2 + k
      self.rect.x -= self.speed
      
      #Vars for y calc
      x = self.rect.x
      og_x, og_y = self.original_pos
      
      #Offset on the quadrtic equation
      offset = 150, self.quad_a*(150)**2
      
      #Calcultes y
      self.rect.y = self.quad_a*(x + offset[0] - og_x)**2 + og_y - offset[1]
      
      #print(f" to ({self.rect.x}, {self.rect.y})")
    #For normal (horizontal) bullets
    else:
      self.rect.x -= self.speed
    