import pygame
import sys,time
pygame.init()

size = width, height = (1600, 900)
screen = pygame.display.set_mode(size)
screenposition = (300, height)

def world2screen(x, y):
  newx = x - screenposition[0]
  newy = (height - y) + (screenposition[1] - height)
  return (newx, newy)

def screen2world(x, y):
  newx = x + screenposition[0]
  newy = (y - (screenposition[1] - height) - height) * -1
  return (newx, newy)

class GameObject():
  def __init__(self, worldposition, width, height):
    self.x = worldposition[0]
    self.y = worldposition[1]
    self.width = width
    self.height = height

  def get_rect(self): #lol
    screenx, screeny = world2screen(self.x, self.y)
    return pygame.Rect(screenx, screeny, self.width, self.height)

  def colliderect(self, object):
    return self.get_rect().colliderect(object.get_rect()) #lol


gameclock = pygame.time.Clock()
starttime = time.time()

speed = 4
gravity = -1
yvelocity = 0
grounded = False

skyimage = pygame.image.load("images/sky.png")
sky = GameObject((0, 1600), 3200, 1600)

playerimage = pygame.image.load("images/cube1.png")
playerimageoriginal = playerimage
playerrect = playerimage.get_rect() #lol
player = GameObject((0, height), playerrect.width, playerrect.height)

worldcolliders = []
ground = GameObject((0, 100), 3200, 100)
worldcolliders.append(ground)
platform1 = GameObject((1200, 125), 400, 25)
worldcolliders.append(platform1)

collisionarea = (ground.width, 1200)
playergroundcollider = GameObject((player.x, player.y + player.height), player.width, collisionarea[1] - (player.y + player.height))
playerleftcollider = GameObject((0, player.y), player.x, player.height)
playerrightcollider = GameObject((player.x + player.width, player.y), collisionarea[0] - (player.x + player.width), player.height)

screenboundlower = (0, height)
screenboundupper = (collisionarea[0] - width, collisionarea[1])

def clamp(x, a, b):
  return min(max(x, a), b)

def clamptuple(x, a, b):
  aout = clamp(x[0], a[0], b[0])
  bout = clamp(x[1], a[1], b[1])
  return (aout, bout)

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()

  gametick = gameclock.tick(60)
  gametime = time.time() - starttime
  #screen.fill((0, 170, 255))
  screen.blit(skyimage, sky.get_rect()) #lol

  keys = pygame.key.get_pressed()

  playergroundcollider.x, playergroundcollider.y = player.x, player.y + player.height
  playergroundcollider.height = collisionarea[1] - (player.y + player.height)

  playerleftcollider.y = player.y
  playerleftcollider.width = player.x

  playerrightcollider.width = collisionarea[0] - (player.x + player.width)
  playerrightcollider.x, playerrightcollider.y = player.x + player.width, player.y
  ################################################################################ 
  leftbound = 0
  rightbound = collisionarea[0] - player.width
  groundheight = 0
  for object in worldcolliders:
    if playergroundcollider.colliderect(object):
      if object.y > groundheight: groundheight = object.y
    if playerleftcollider.colliderect(object):
      rightedge = object.x + object.width
      if rightedge > leftbound: leftbound = rightedge
    if playerrightcollider.colliderect(object):
      leftedge = object.x
      if leftedge < rightbound: rightbound = leftedge - player.width

  player.x += (keys[pygame.K_d] - keys[pygame.K_a]) * speed
  player.x = clamp(player.x, leftbound, rightbound)

  if grounded:
    yvelocity = 15 * keys[pygame.K_SPACE]
  else:
    yvelocity += gravity

  player.y += yvelocity
  playergroundy = groundheight + player.height
  if player.y <= playergroundy:
    player.y = playergroundy
    grounded = True
  else:
    grounded = False

  screenposition = (player.x - width / 2 + player.width / 2, player.y + height / 2 - player.height / 2)
  screenposition = clamptuple(screenposition, screenboundlower, screenboundupper)

  currentplayerrect = player.get_rect() #lol 
  screen.blit(playerimage,(currentplayerrect.x, currentplayerrect.y))
  pygame.draw.rect(screen, (45, 180, 75), ground.get_rect()) #lol
  pygame.draw.rect(screen, (150, 150, 150), platform1.get_rect()) #lol
  #pygame.draw.rect(screen, (255, 255, 255), playergroundcollider)
  #pygame.draw.rect(screen, (255, 255, 255), playerleftcollider)
  #pygame.draw.rect(screen, (255, 255, 255), playerrightcollider)

  #playerimage = pygame.transform.rotate(playerimageoriginal, gametime)


  pygame.display.update()