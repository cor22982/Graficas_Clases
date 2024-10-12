import pygame
from pygame.locals import *
from gl import Renderer
from Buffer import Buffer
from shaders import *
#Vamos a hacer un poco de regresion porque lo que vamos a hacer es un rasterizador
#OPEN GL ya usa la tarjeta de video jajaj no tengo ni modo toco pedir una

width = 960
height = 540

pygame.init()

# el segundo argumento en vez de dibujar directamente los puntos
# de la pantalla vamos a dibujar con OPENGL

# Double buffering 
screen = pygame.display.set_mode((width,height), pygame.OPENGL | pygame.DOUBLEBUF)

clock = pygame.time.Clock()

renderer = Renderer(screen=screen)

renderer.SetShaders(vShader=vertex_shader, fShader=fragmet_shader)

#y si hacemos un triangulo xyz
# todo paso de corrido punto 1 x,y,z punto 2 x,y,z

# le vamos a agregar nuevas propiedad que va a ser el color

#             posision               color
triangle = [-0.5,-0.5,0,            1,0,0,
            0   ,0.5,0,             0,1,0,
            0.5,-0.5,0,             0,0,1]

#guardaoms la informacion en el buffer
#hecho a partir de la informacion del triangulo
renderer.scene.append(Buffer(data=triangle))

isRunning = True

while isRunning:
  #esto va a tener mas uso en un frame rate mas aceptable
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      isRunning = False
    elif event.type == pygame.KEYDOWN:
      if event.key  == pygame.K_ESCAPE:
        isRunning = False

  deltaTime = clock.tick(60) / 1000
  renderer.Render()
  pygame.display.flip()

pygame.quit()