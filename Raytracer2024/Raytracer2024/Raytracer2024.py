
from gl import *
import pygame
from pygame.locals import *
from Figuras import *
from material import Material
from Lights import *
width = 128
height = 128

screen = pygame.display.set_mode((width, height), pygame.SCALED )
clock = pygame.time.Clock()

rt = RendererRT(screen)

#Materiales
brick = Material(difuse=[1,0.2,0.2], spec= 32, ks= 0.05)
grass = Material(difuse=[0.2,1,0.2], spec= 128, ks= 0.2)

#Lights 
rt.lights.append(DirectionalLight(direction=[-1,-1,-1] , color=[1,1,1]))
rt.lights.append(AmbientLight())

#objets
rt.scene.append(Sphere([0,0,-5], radius=1.5, material=brick)) #la creo en todo
rt.glRender()
isRunning = True
while isRunning:
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			isRunning = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				isRunning = False
				
				
	pygame.display.flip()
	clock.tick(60)
	
pygame.quit()