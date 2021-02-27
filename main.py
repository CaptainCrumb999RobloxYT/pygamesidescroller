import pygame
import sys,time
pygame.init()

size = width, height = (1600, 900)
screen = pygame.display.set_mode(size)
screenposition = (0, height)

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

gameclock = pygame.time.Clock()
starttime = time.time()

speed = 4
gravity = 1
yvelocity = 0
grounded = False

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
playergroundcollider = pygame.Rect(player.x, player.y + player.height, player.width, collisionarea[1] - (player.y + player.height))
playerleftcollider = pygame.Rect(0, player.y, player.x, player.height)
playerrightcollider = pygame.Rect(player.x + player.width, player.y, collisionarea[0] - (player.x + player.width), player.height)



def clamp(x, a, b):
  return min(max(x, a), b)

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()

  gametick = gameclock.tick(60)
  gametime = time.time() - starttime
  screen.fill((0, 170, 255))
  
  keys = pygame.key.get_pressed()

  playergroundcollider.x, playergroundcollider.y = player.x, player.y + player.height
  playergroundcollider.height = collisionarea[1] - (player.y + player.height)

  playerleftcollider.y = player.y
  playerleftcollider.width = player.x

  playerrightcollider.width = collisionarea[0] - (player.x + player.width)
  playerrightcollider.x, playerrightcollider.y = player.x + player.width, player.y
  ################################################################################
  leftbound = 0
  rightbound = width - player.width
  groundheight = height
  for collider in worldcolliders:
    if playergroundcollider.colliderect(collider):
      if collider.y < groundheight: groundheight = collider.y
    if playerleftcollider.colliderect(collider):
      rightedge = collider.x + collider.width
      if rightedge > leftbound: leftbound = rightedge
    if playerrightcollider.colliderect(collider):
      leftedge = collider.x
      if leftedge < rightbound: rightbound = leftedge - player.width

  player.x += (keys[pygame.K_d] - keys[pygame.K_a]) * speed
  player.x = clamp(player.x, leftbound, rightbound)

  if grounded:
    yvelocity = -15 * keys[pygame.K_SPACE]
  else:
    yvelocity += gravity

  player.y += yvelocity
  playergroundy = groundheight - player.height
  if player.y >= playergroundy:
    player.y = playergroundy
    grounded = True
  else:
    grounded = False

  screen.blit(playerimage,(player.x, player.y))
  pygame.draw.rect(screen, (45, 180, 75), groundrect)
  pygame.draw.rect(screen, (150, 150, 150), platform1)
  #pygame.draw.rect(screen, (255, 255, 255), playergroundcollider)
  #pygame.draw.rect(screen, (255, 255, 255), playerleftcollider)
  #pygame.draw.rect(screen, (255, 255, 255), playerrightcollider)

  #playerimage = pygame.transform.rotate(playerimageoriginal, gametime)


  pygame.display.update()