
from gl import *
import pygame
from pygame.locals import *
from Figuras import *
from material import *
from Lights import *
from texture import Texture
width = 255
height = 255

screen = pygame.display.set_mode((width, height), pygame.SCALED )
clock = pygame.time.Clock()

rt = RendererRT(screen)
#rt.enveriomentMap = Texture("Raytracer2024\Raytracer2024\parkingLot.bmp")
#rt.glClearColor(0.5,0.0,0.0)
rt.glClearColor(0.0,0.0,0.0)
rt.glClear()
#Materiales
brick = Material(difuse=[1,0.2,0.2], spec= 32, ks= 0.1)
grass = Material(difuse=[0.2,1,0.2], spec= 64, ks= 0.2)
mirror = Material(difuse=[0.9,0.9,0.9], spec= 128, ks= 0.2, matType=REFLECTIVE)
# bluemirror = Material(difuse=[0.5,0.5,1], spec= 128, ks= 0.2, matType=REFLECTIVE)
# wood = Material(texture=Texture("Raytracer2024\Raytracer2024\lava.bmp"), spec=128, ks=0.2, matType=REFLECTIVE)
glass = Material(ior=1.5, spec=128, ks=0.2, matType=TRANSPARENT)
woodtexture = Material(texture=Texture('Raytracer2024\Raytracer2024\woodenBox.bmp'))

#Lights 
#rt.lights.append(DirectionalLight(direction=[-1,-1,-1], intensity=0.8 ))
rt.lights.append(AmbientLight(intensity=0.1))
#rt.lights.append(PointLight(position=[-2,0,-5]))
rt.lights.append(SpotLight(position=[2,0,-5], direction=[-1,0,0]))


#objets
#rt.scene.append(Sphere([0,0,-5], radius=1.5, material=glass)) #la creo en todo
#rt.scene.append(Plane(position=[0,-5,-5], normal=[0,1,0], material=brick))
#rt.scene.append(Sphere([0,0,-5], radius=1, material=brick)) #la creo en todo
#rt.scene.append(Disk(position=[0,-1,-5], normal=[0,1,0], radius=1.5, material=mirror))
#rt.scene.append(AABB(position=[1.5,-1.5,-5], sizes=[1,1,1], material=woodtexture))
# rt.scene.append(Sphere(position=[-1.5,0,-5], radius=1, material=brick))
# rt.scene.append(Sphere(position=[3,0,-5], radius=1, material=brick))
# rt.scene.append(Sphere(position=[1,0,-4.7], radius=0.1, material=grass))
rt.scene.append(Plane(position=[0,-1,0], normal=[0,1,0], material=brick))


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