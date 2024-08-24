import pygame as pg

import object
import settings

pg.init()

size = (width, height) = settings.size

screen = settings.screen

def font(size):
  return settings.font(size)

#Menu screen
  
#Turtle boss text
title_text = object.Object("text", (width / 2, height / 2 - 100), text="Turtle Boss!", font_size=48, text_color=pg.Color("green"), group=False)

#Credits
credits = object.Object("text", (width / 2, height / 2 - 70), text="By: @BaconCodes", font_size=18, text_color=pg.Color("dimgray"), group=False)

#Play button
play_button = object.Object("rectangle", (width / 2, height / 2), (150, 75), pg.Color("white"), False, 5, pg.Color("dimgray"), "PLAY", 40, pg.Color("green"))

#Level button
level_button = object.Object("rectangle", (width / 2, height / 2 + 80), (150, 75), pg.Color("white"), False, 5, pg.Color("dimgray"), "LEVELS", 34, pg.Color("green"))


#Level screen
level_text = object.Object("text", (width / 2, height / 2 - 100), text="Levels", font_size=48, text_color=pg.Color("green"), group=False)

#Level buttons
level_buttons = pg.sprite.Group()
for i in range(-2, 3):
  btn = object.Object("rectangle", (width / 2 + i*85, height / 2), (75, 75), pg.Color("white"), False, 5, pg.Color("dimgray"), i+3, 48, pg.Color("green"))
  level_buttons.add(btn)

#Back button
back_button = object.Object("arrow.png", (20, 20), group=False)


#Whether on level menu
on_level = False

#What level to play
current_level = 1

#Main function
def menu():
  #Important vars
  running = True
  on_menu = True
  global on_level, current_level
  dead_time = (pg.time.get_ticks())/1000

  #Checks for events
  for event in pg.event.get():
    #Quit
    if event.type == pg.QUIT:
      running = False
    elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
      #Cursor position
      pos = pg.mouse.get_pos()
      #When on menu
      if on_level == False:
        #Play button clicked
        if play_button.rect.collidepoint(pos):
          on_menu = False
          current_level = 1

          print(f"level {current_level}")
          print("game started")
        elif level_button.rect.collidepoint(pos):
          on_level = True
          print("on level")
      #When on level menu
      else:
        if back_button.rect.collidepoint(pos):
          on_level = False
          print("on menu")
        else:
          for i in range(len(level_buttons)):
            if level_buttons.sprites()[i].rect.collidepoint(pos):
              on_menu = False
              current_level = i+1
              
              print(f"level {current_level}")
              print("game started")

  #Builds the screen based off of page
  if on_level == False:
    screen.fill(pg.Color("white"))
    screen.blit(title_text.image, title_text.rect)
    screen.blit(credits.image, credits.rect)
    screen.blit(play_button.image, play_button.rect)
    screen.blit(level_button.image, level_button.rect)
    
  else:
    screen.fill(pg.Color("white"))
    screen.blit(level_text.image, level_text.rect)
    screen.blit(back_button.image, back_button.rect)
    level_buttons.draw(screen)
    

  #Updates screen
  pg.display.update()

  
  #Returns relevant variables
  return (running, on_menu, current_level, dead_time)