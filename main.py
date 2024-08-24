#Imports/Initilizes stuff
import pygame as pg

import plyr
import object
import menu
import pause
import levels

import settings

pg.init()

#Screen size
size = (width, height) = settings.size
#Sets up screen
screen = settings.screen

#Game background
bg = pg.Color("cadetblue2")

#Game font
def font(size):
  return settings.font(size)


#Objects group
objects = object.objects

#Order of construction = z level hierarchy
player = plyr.Player("turtle.png", (width / 2, height / 2))

#Pause button
pause_button = object.Object("pause.png", (width-10, 10), (15, 20))

#FPS counter
def update_fps(fps):
  #Uses gobal counter
  global fps_counter
  #If in group, remove from group (to prevent overlap/ group bugs)
  try: objects.remove(fps_counter)
  except: pass
  #Recreate counter
  fps_counter = object.Object("text", (20, 8), text=f"{fps} fps", font_size=12, text_color=pg.Color("black"))

#Counter
fps = 30
update_fps(fps)


#Clock used to time ticks
clock = pg.time.Clock()
#Keeps program running
running = True
#Whether viewing the menu
on_menu = True
#Game pause state
paused = False
#How long the game was last paused for
dead_time = 0
#Adds the game load time to dead time
dead_time += pg.time.get_ticks()/1000
#Game time variable
time = 0
#Last time that time was printed
last_time = 0
#Bullet wave number
wave = 0
#Whether player is dead or not
dead = False
#Whether player has won or not
won = False
#Whether the player is on a new level
new_level = False
#Whether this is the first time creating a level
first_creation = True
while running == True:
  #Sets to 30 fps
  clock.tick(30)

  #While on menu
  if on_menu == True:
    #Runs menu code + gets statuses
    statuses = menu.menu()
    #Checks whether player has exited or clicked start (meaning the player is no longer on_menu)
    running = statuses[0]
    on_menu = statuses[1]
    current_level = statuses[2]
    #If not on menu, wait 100 ms and add that wait time + time spent on menu to dead_time
    if on_menu == False:
      dead_time += statuses[3] + 0.1
      pg.time.wait(100)

    new_level = True

    #Restarts loop to prevent other game functions
    continue

  
  if new_level == True:
    if first_creation == True:
      #Return vars from level creation 
      #(boss, bullet_group, waiting_bullet_group, active_bullet_group)
      statuses = levels.level(current_level)
      boss = statuses[0]
      bullet_group, waiting_bullet_group, active_bullet_group = statuses[1], statuses[2], statuses[3]
      
      first_creation = False
    else:
      #Removes objects tht are being recreated
      objects.remove(bullet_group)
      objects.remove(boss)
      
      #Bullet wave number
      wave = 0
      #Whether player is dead or not
      dead = False
      #Whether player has won or not
      won = False
      
      #Recreates level specific variables
      statuses = levels.level(current_level, bullet_group, boss)
      boss = statuses[0]
      bullet_group, waiting_bullet_group, active_bullet_group = statuses[1], statuses[2], statuses[3]
  
      #Resets player pos
      player.rect.center = (width / 2, height / 2)
      player.image = player.static_image
  
      #Resets time related + new_level variables
      last_time = 0
      dead_time = pg.time.get_ticks()/1000
      new_level = False


    

  #While the game is paused
  if paused == True:
    #Pauses game + takes statuses
    statuses = pause.unpause(pause_button, time)

    #Sets statuses to corresponding variables
    running = statuses[0]
    paused = statuses[1]
    dead_time = statuses[2]

    #Restarts loop to prevent other game functions
    continue


  #While dead
  if dead == True:
    #Death text
    death_text = object.Object("text", (width / 2, height / 2 - 50), text="You Died!", font_size=48, text_color=pg.Color("red"), group=False)

    #Replay button
    replay_button = object.Object("rectangle", (width / 2, height / 2 + 50), (150, 75), pg.Color("white"), False, 5, pg.Color("dimgray"), "REPLAY", 32, pg.Color("green"))
    
    #Looks for events
    for event in pg.event.get():
      #Quit
      if event.type == pg.QUIT:
        running = False

      elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
      #Cursor position
        pos = pg.mouse.get_pos()
        #If replay is clicked
        if replay_button.rect.collidepoint(pos):
          #Resets/goes to new level
          new_level = True
          dead = False
          print("replay")

    #Updates display
    screen.blit(death_text.image, death_text.rect)
    screen.blit(replay_button.image, replay_button.rect)
    pg.display.update()
    
    continue

  #While you won
  if won == True:
    #Win text
    win_text = object.Object("text", (width / 2, height / 2 - 50), text="You Won!", font_size=48, text_color=pg.Color("green"), group=False)

    #5 is max level
    if current_level != 5:
      #Next level button
      next_level_button = object.Object("rectangle", (width / 2, height / 2 + 50), (150, 75), pg.Color("white"), False, 5, pg.Color("dimgray"), f"LEVEL {current_level+1}", 32, pg.Color("green"))
    else:
      #No more levels
      next_level_button = object.Object("rectangle", (width / 2, height / 2 + 50), (150, 75), pg.Color("white"), False, 5, pg.Color("dimgray"), f"MENU", 36, pg.Color("green"))
    
    #Looks for events
    for event in pg.event.get():
      #Quit
      if event.type == pg.QUIT:
        running = False

      elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
      #Cursor position
        pos = pg.mouse.get_pos()
        #If next level is clicked
        if next_level_button.rect.collidepoint(pos):
          #If there is another level
          if current_level != 5:
            #Resets/goes to new level
            new_level = True
            current_level += 1
            dead = False
            print(f"level {current_level}")
          #Otherwise go to menu
          else:
            #Resets if played again
            new_level = True
            current_level = 1
            #Brings player to menu
            on_menu = True

    #Updates display
    screen.blit(win_text.image, win_text.rect)
    screen.blit(next_level_button.image, next_level_button.rect)
    pg.display.update()
    
    continue

    #Updates screen
    screen.blit(win_text.image, win_text.rect)
    pg.display.update()

    continue

    
    
  #Time updater + printer
  #Time since start in seconds excluding dead time (ex: menu, pause, previous rounds, etc.)
  time = pg.time.get_ticks()/1000 - dead_time
  if time >= last_time + 0.5:
    print(round(time, 3))
    last_time = time

    

  #Main event loop
  #Looks for events
  for event in pg.event.get():
    #On quit event
    if event.type == pg.QUIT:
      running = False

    #If the mouse is clicked,
    elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
      #Cursor position
      pos = pg.mouse.get_pos()
      
      #If pause is clicked
      if pause_button.rect.collidepoint(pos):
        #Pauses game and takes variables
        statuses = pause.pause()
        #Sets variables (technically always True and 0)
        paused = statuses[0]
        dead_time = statuses[1]
        
      #Other button's functions would go here
      else:
        pass

  #Restarts game loop to pause the game (if necessary)
  if paused == True:
    continue
    

        
  #Gets current keypresses
  keys = pg.key.get_pressed()
  #Moves player accordingly (using custom player move function)
  player.move(keys, boss) #Boss is used as right limit
  
  #Moves the active bullets forward
  for proj in active_bullet_group:
    proj.move()
    if proj.rect.x < 0 or proj.rect.y > height:
      active_bullet_group.remove(proj)

  #Count of bullets per volley (firing)
  vly_count = 5
  if current_level >= 2:
    vly_count = 6
  if current_level == 5:
    vly_count = 7
      
  #5 sec delay at start + starts a new wave every 5 sec
  if time > wave*3+3:
    wave += 1
    if waiting_bullet_group.sprites() != []:
      print("new wave")
    #Shoots 6 bullets
    new_bullets = waiting_bullet_group.sprites()[0:vly_count]
    active_bullet_group.add(new_bullets)
    waiting_bullet_group.remove(new_bullets)

  #If no more bullets in active or waiting groups
  if active_bullet_group.sprites() == [] and waiting_bullet_group.sprites() == []:
    print("You won!")
    #Sticks game in win loop
    won = True
  #If all bullets have passed the player, you win
  elif waiting_bullet_group.sprites() == []:
    #You win
    won = True
    #Unless there is still a bullet to your right
    for blt in active_bullet_group:
      if blt.rect.right > player.rect.left:
        won = False
        break
    
  #Hit detection
  collision = pg.sprite.spritecollide(player, active_bullet_group, False, pg.sprite.collide_mask)
  
  #If there is a sprite in collsions
  if collision != []:
    print("You died!")
    #Sticks game in dead loop
    dead = True


  #Updates fps counter to current
  fps = round(clock.get_fps())
  update_fps(fps)
    
    
  #Clears the screen then re-adds the everything (to animate movement)
  screen.fill(bg)
  
  #Displays the player + other objects
  #Makes a active only group 
  active = objects.copy()
  #This group doesn't include inactive bullets
  active.remove(bullet_group)
  active.add(active_bullet_group)
  #Only draw on all active objects
  active.draw(screen)
  
  #Updates display
  pg.display.update()