
from gl import *
import pygame
from pygame.locals import *
from Figuras import *
from material import *
from Lights import *
from texture import Texture
width = 188
height = 188

screen = pygame.display.set_mode((width, height), pygame.SCALED )
clock = pygame.time.Clock()

rt = RendererRT(screen)
rt.enveriomentMap = Texture("Raytracer2024\Raytracer2024\parkingLot.bmp")
rt.glClearColor(0.5,0.0,0.0)
rt.glClear()
#Materiales
brick = Material(difuse=[1,0.2,0.2], spec= 32, ks= 0.1)
grass = Material(difuse=[0.2,1,0.2], spec= 64, ks= 0.2)
mirror = Material(difuse=[0.9,0.9,0.9], spec= 128, ks= 0.2, matType=REFLECTIVE)

#Lights 
rt.lights.append(DirectionalLight(direction=[-1,-1,-1], intensity=0.8 ))
rt.lights.append(DirectionalLight(direction=[0.5,-0.5,-1], intensity=0.8, color=[1,1,1] ))
rt.lights.append(AmbientLight(intensity=0.1))

#objets
rt.scene.append(Sphere([0,0,-5], radius=1.5, material=mirror)) #la creo en todo
rt.scene.append(Sphere([1,0.8,-3], radius=0.35, material=grass)) #la creo en todo
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