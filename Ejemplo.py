# Pygame es utilizado para presentar la imagen de forma inmediata
import pygame
from pygame.locals import *
from GL import Renderer
from model import Model
from shaders import VertexShader
# Estimar el tamaño de pantalla
width = 960
height = 540

# Generar la pantalla
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()  # Se utiliza para asegurarse de que el juego corra a una velocidad específica de cuadros por segundo

#Cargar modelo
modelo1 = Model("model.obj")
modelo1.translate[0] = width/2  #que su poiscion en x sea
modelo1.translate[1] = height/3

modelo1.scale[0] = 10
modelo1.scale[1] = 10
modelo1.scale[2] = 10

# Pasar la pantalla al Renderer de GL
rend = Renderer(screen)
rend.vertexShader = VertexShader #asgino el vertex

rend.glColor(0, 0, 1)  # Establecer el color actual a magenta (RGB: 1, 0, 1)
rend.glClearColor(0, 0, 0)  # Establecer el color del fondo a rosa (RGB: 1, 0.5, 1)

# GameLoop
# Esto es para asegurarse de que el bucle principal siga corriendo, simulando el comportamiento en segundo plano
rend.models.append(modelo1)
isRunning = True
while isRunning:
    # Procesar eventos en la cola de eventos
    for event in pygame.event.get():
        # Si se detecta el evento de salir (cerrar la ventana), se detiene el bucle
        if event.type == pygame.QUIT:
            isRunning = False
        # Si se detecta que una tecla ha sido presionada
        elif event.type == pygame.KEYDOWN:
            # Si la tecla presionada es ESCAPE, se detiene el bucle
            if event.key == pygame.K_ESCAPE:
                isRunning = False

            elif event.key == pygame.K_RIGHT:
                modelo1.rotate[1] += 10
            elif event.key == pygame.K_LEFT:
                modelo1.rotate[1] -= 10
            elif event.key == pygame.K_UP:
                modelo1.rotate[0] += 10
            elif event.key == pygame.K_DOWN:
                modelo1.rotate[0] -= 10
            elif event.key  == pygame.K_k:                
                modelo1.scale[0] += 2
                modelo1.scale[1] += 2
                modelo1.scale[2] += 2
            elif event.key == pygame.K_l:
                modelo1.scale[0] -= 2
                modelo1.scale[1] -= 2
                modelo1.scale[2] -= 2
            elif event.key == pygame.K_w:
                modelo1.translate[1] += 5
            elif event.key == pygame.K_a:
                modelo1.translate[0] -= 5
            elif event.key == pygame.K_s:
                modelo1.translate[1] -= 5
            elif event.key == pygame.K_d:
                modelo1.translate[0] += 5


    rend.glClear()  # Limpiar la pantalla antes de dibujar nuevamente

    # Dibujar una línea en secuencia de puntos
    #for i in range(100):
    #    rend.glPoint(480 + i, 270 + i)

    #rend.glPoint(480, 270) # Dibujar un punto en el centro de la pantalla

    #rend.glLine((100,100),(500,450)) # Hacer la línea
    #rend.glLine((100,100),(200,250)) # Línea con pendiente cercana a 1
    #rend.glLine((100,100),(200,100)) # Línea con pendiente cercana a 1

    # Dibujar lineas usando Bresenham
    
    rend.glRender()

    pygame.display.flip()  # Actualizar la pantalla con los cambios realizados
    clock.tick(60)  # Asegurar que el juego no exceda los 60 cuadros por segundo

rend.generateFrameBuffer("./output.bmp")
pygame.quit()  # Salir del juego y cerrar la ventana de Pygame
