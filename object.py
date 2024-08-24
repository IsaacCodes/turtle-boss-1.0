import pygame as pg

import settings

pg.init()

dir = settings.dir

def font(size):
  return settings.font(size)


#List of all game objects
objects = pg.sprite.Group()

#Object class
class Object(pg.sprite.Sprite):
  def __init__(self, type, location, size=False, color=pg.Color("black"), group=True, border_size=0, border_color=pg.Color("black"), text=False, font_size=36, text_color=pg.Color("black")):
    pg.sprite.Sprite.__init__(self)
    #Creates the surface
    #Rectangular surfaces
    self.type = type

    if type == "rectangle":
      if size == False:
        size = (20, 20)
      
        
      #If border
      if border_size != 0:
        #Makes the entire rect a border
        self.image = pg.Surface(size)
        self.image.fill(border_color)
        #Then adds the inside which is size-border
        inside = pg.Surface((size[0]-border_size*2, size[1]-border_size*2))
        inside.fill(color)
        self.image.blit(inside, (border_size, border_size))
      #Otherwise, just make a rect
      else:
        self.image = pg.Surface(size)
        self.image.fill(color)

      if text != False:
        #Text
        txt = font(font_size).render(str(text), True, text_color)
        #Text position
        center = txt.get_rect().center
        txt_location = (size[0]//2 - center[0], size[1]//2 - center[1])
        self.image.blit(txt, txt_location)

    elif type == "circle":
      self.image = pg.Surface(size, pg.SRCALPHA)
      pg.draw.circle(self.image, pg.Color(color), self.image.get_rect().center, size[0]/2)
      
    elif type == "text":
      self.image = font(font_size).render(str(text), True, text_color)
      self.rect = self.image.get_rect(center=location)
        
    #Image surfaces
    else:
      self.image = pg.image.load(f"{dir}//imgs//{type}")
      
    #Changes the size (if called for)
    if size != False:
      self.image = pg.transform.smoothscale(self.image, size)

    self.image = self.image.convert_alpha()
      
    #Creates a rect from the surface
    self.rect = self.image.get_rect(center=location)

    if group == True:
      #Adds player to all objects list
      objects.add(self)