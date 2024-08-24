import pygame as pg
import random as r

import object
import bullet
import settings

size = width, height = settings.size
dir = settings.dir

objects = object.objects

#First game level
def level(level, bullet_group=None, boss=None):
  #Removes objects that are being recreated (if already created)
  if bullet_group != None and boss != None:
    objects.remove(bullet_group)
    objects.remove(boss)


  #Builds the boss with multiple layers

  #Creates the boss from the ships body
  boss = object.Object("ship_body.png", (width / 2 + 250, height / 2))

  #Creates cannons
  cannon = pg.image.load(f"{dir}//imgs//cannon.png")
  #List of cannon locations on ship
  cannons = [[35, 15], [25, 35], [10, 70], [5, 105], [0, 140], [0, 175], [0, 210], [5, 245], [5, 280], [5, 315], [5, 330]]
  #Blits cannons to ship
  for i in range(len(cannons)):
    boss.image.blit(cannon, cannons[i])

  #Adds masts and sils to ship
  masts_and_sails = pg.image.load(f"{dir}//imgs//masts_and_sails.png")
  boss.image.blit(masts_and_sails, (0, 0))
  #Converts to alpha
  boss.image = boss.image.convert_alpha()

  #Resets the bullet groups
  bullet.reset_groups()
  #Bullet size by defualt = (25, 25)
  sizes = [[25, 25], [20, 20], [10, 10]]

  #Makes normal bullets
  def create_normal(normal_bullet_count):
    #Creates all normal cannonball bullets
    for i in range(normal_bullet_count):
      #Cannon cords for the current bullet being created
      cannon_pos = cannons[i%len(cannons)]
  
      #Bullet size creator
      bullet_size = r.choice(sizes).copy() 
      #.copy() is needed to prevent list jankiness
      
      #Prevents large bullets from firing from top + bottom cannons (to prevent overlapping)
      first_or_last = i%len(cannons) == 0 or  i%len(cannons) == len(cannons) - 1
      while bullet_size == sizes[0] and first_or_last == True:
        bullet_size = r.choice(sizes).copy()
      
      #Offsets size by a random amount
      diff = r.randint(-1 , 1)
      bullet_size[0] += diff
      bullet_size[1] += diff
      #Location creator
      location = (boss.rect.left + cannon_pos[0], cannon_pos[1] + cannon.get_rect().height // 2)
      #Acutally makes the bullet
      bullet.Bullet("circle", location, sizes, bullet_size, pg.Color("black"))

  #Makes mortar type bullets
  def create_mortar(mortar_bullet_count):
    #Mortar type bullets
    for i in range(mortar_bullet_count):
      #Cannon cords for the current bullet being created
      cannon_pos = cannons[i%len(cannons)]
  
      #Bullet size creator
      bullet_size = r.choice(sizes).copy() 
      #.copy() is needed to prevent list jankiness
      
      
      #Offsets size by a random amount
      diff = r.randint(-1 , 1)
      bullet_size[0] += diff
      bullet_size[1] += diff
      #Location creator
      location = (boss.rect.left + cannon_pos[0], cannon_pos[1] + cannon.get_rect().height // 2)
      #Acutally makes the bullet
      bullet.Bullet("circle", location, sizes, bullet_size, pg.Color("black"), bullet_type="mortar")

  #For all normal levels
  if level != 5:
    #Bullet counts depending on level
    normal_bullet_count = 90
    mortar_bullet_count = 0
    if level >= 2:
      normal_bullet_count += 30
    if level >= 3:
      mortar_bullet_count += 30
    if level >= 4:
      mortar_bullet_count += 30
  
    create_normal(normal_bullet_count)
    create_mortar(mortar_bullet_count)

  #For the final level
  else:
    for i in range(3):
      create_normal(35)
      create_mortar(35)
    
  #Bullet groups
  bullet_group = bullet.bullet_group
  waiting_bullet_group = bullet.waiting_bullet_group
  active_bullet_group = bullet.active_bullet_group
  
  return (boss, bullet_group, waiting_bullet_group, active_bullet_group)