import pygame
from pygame.locals import *
from gl import Renderer
from Buffer import Buffer
from shaders import *
from model import Model
#Vamos a hacer un poco de regresion porque lo que vamos a hacer es un rasterizador
#OPEN GL ya usa la tarjeta de video jajaj no tengo ni modo toco pedir una

width = 540
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
# triangle = [-0.5,-0.5,0,            1,0,0,
#             0   ,0.5,0,             0,1,0,
#             0.5,-0.5,0,             0,0,1]

# #guardaoms la informacion en el buffer
# #hecho a partir de la informacion del triangulo
# renderer.scene.append(Buffer(data=triangle))


faceModel = Model('RayTraceOpenGl\model (1).obj')
faceModel.AddTextures('RayTraceOpenGl\Textures\model.bmp')
renderer.scene.append(faceModel)
faceModel.rotation.y = 0
faceModel.translation.z = -3
isRunning = True


vShader = vertex_shader
fShader = fragmet_shader
renderer.SetShaders(vShader, fShader)
while isRunning:
  #esto va a tener mas uso en un frame rate mas aceptable
  deltaTime = clock.tick(60) / 1000
  keys = pygame.key.get_pressed()
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      isRunning = False
    elif event.type == pygame.KEYDOWN:
      if event.key  == pygame.K_ESCAPE:
        isRunning = False
      elif event.key == pygame.K_F1:
        renderer.FillMode()
      elif event.key == pygame.K_F2:
        renderer.WireFrameMode()
      elif event.key == pygame.K_3:
        vShader = vertex_shader
        renderer.SetShaders(vShader, fShader)
      elif event.key == pygame.K_4:
        vShader = distortion_shader
        renderer.SetShaders(vShader, fShader)
      elif event.key == pygame.K_5:
        vShader = water_shader
        renderer.SetShaders(vShader, fShader)
      elif event.key == pygame.K_6:
        fShader = fragmet_shader
        renderer.SetShaders(vShader, fShader)
      elif event.key == pygame.K_7:
        fShader = negative_shader
        renderer.SetShaders(vShader, fShader)
    
  if keys[K_LEFT]:
    faceModel.rotation.y -=10*deltaTime
  if keys[K_RIGHT]:
    faceModel.rotation.y +=10*deltaTime
  
  if keys[K_a]:
    renderer.camera.position.x -= 1 *deltaTime
  
  if keys[K_d]:
    renderer.camera.position.x += 1 *deltaTime
  
  if keys[K_w]:
    renderer.camera.position.y += 1 *deltaTime
  
  if keys[K_s]:
    renderer.camera.position.y -= 1 *deltaTime


  renderer.time += deltaTime
  renderer.Render()
  pygame.display.flip()

pygame.quit()