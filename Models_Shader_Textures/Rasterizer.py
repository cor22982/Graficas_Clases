
import pygame
from pygame.locals import *
from gl import *
from model import Model
from shaders import *

width = 960
height = 540

screen = pygame.display.set_mode((width, height), pygame.SCALED  )
clock = pygame.time.Clock()

rend = Renderer(screen)

modelo1 = Model("Models_Shader_Textures\models\model.obj")
modelo1.LoadTexture("Models_Shader_Textures\\textures\model.bmp")
modelo1.vertexShader = vertexShader
modelo1.fragmentShader = fragmentShader
modelo1.translate[2] = -5
modelo1.translate[0] = -2

modelo2 = Model("Models_Shader_Textures\models\model.obj")
modelo2.LoadTexture("Models_Shader_Textures\\textures\model.bmp")
modelo2.vertexShader = vertexShader
modelo2.fragmentShader = fragmentShader
modelo2.translate[2] = -5
modelo2.translate[0] = 0


modelo3 = Model("Models_Shader_Textures\models\model.obj")
modelo3.LoadTexture("Models_Shader_Textures\\textures\model.bmp")
modelo3.vertexShader = vertexShader
modelo3.fragmentShader = fragmentShader
modelo3.translate[2] = -5
modelo3.translate[0] = 2

# puntoA = [50, 50, 0]
# puntoB = [250, 500, 0]
# puntoC = [500, 50, 0]

rend.models.append(modelo1)
rend.models.append(modelo2)
rend.models.append(modelo3)
isRunning = True
while isRunning:
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			isRunning = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				isRunning = False
				
			elif event.key == pygame.K_1:
				rend.primitiveType = POINTS
				
			elif event.key == pygame.K_2:
				rend.primitiveType = LINES
				
			elif event.key == pygame.K_3:
				rend.primitiveType = TRIANGLES
				

			elif event.key == pygame.K_RIGHT:
				rend.camera.translate[0] += 1
			elif event.key == pygame.K_LEFT:
				rend.camera.translate[0] -= 1
			elif event.key == pygame.K_UP:
				rend.camera.translate[1] += 1
			elif event.key == pygame.K_DOWN:
				rend.camera.translate[1] -= 1
				
					
	rend.glClear()
	
	rend.glRender()
	# rend.glTriangle(puntoA, puntoB, puntoC)

	pygame.display.flip()
	clock.tick(60)
	
rend.glGenerateFrameBuffer("output.bmp")

pygame.quit()