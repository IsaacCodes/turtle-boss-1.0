import pygame as pg

import object
import settings

pg.init()

#Screen size
size = (width, height) = settings.size
#Game screen
screen = settings.screen

#Game font
def font(size):
  return settings.font(size)


#Pause function (Already wrapped in game event loop + if pause clicked statement)
def pause():
  #Pauses game
  paused = True
  #Resets dead_time
  dead_time = 0
  print("paused")
      
  #Creates a mostly clear grey background
  bg = pg.Surface(screen.get_size(), pg.SRCALPHA)
  bg.fill((0, 0, 0, 15))
        
  #Creates pause text, blits, and updates display
  pause_text = object.Object("text", (width / 2, height / 2), text="Paused", font_size=24, text_color=pg.Color("black"), group=False)

  #Updates screen
  screen.blit(bg, (0, 0))
  screen.blit(pause_text.image, pause_text.rect)
  pg.display.update()

  #Returns appropriate variables
  return [paused, dead_time]



#Unpause function
def unpause(pause_button, time):
  #Resets variables
  running = True
  paused = True
  dead_time = 0

  #Looks for events
  for event in pg.event.get():
    #Quit
    if event.type == pg.QUIT:
      running = False
        
    #On left click
    elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
      #Cursor position
      pos = pg.mouse.get_pos()
      #Pause clicked
      if pause_button.rect.collidepoint(pos):
        #Unpauses
        paused = False
        #Finds dead_time
        dead_time += pg.time.get_ticks()/1000 - time
        print("unpaused")
        
  #Returns relevant variables
  return [running, paused, dead_time]