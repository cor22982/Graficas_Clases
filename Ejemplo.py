# Pygame es utilizado para presentar la imagen de forma inmediata
import pygame
from pygame.locals import *

from GL import Renderer

# Estimar el tamaño de pantalla
width = 960
height = 540

# Generar la pantalla
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()  # Se utiliza para asegurarse de que el juego corra a una velocidad específica de cuadros por segundo

# Pasar la pantalla al Renderer de GL
rend = Renderer(screen)

rend.glColor(1, 0, 1)  # Establecer el color actual a magenta (RGB: 1, 0, 1)
rend.glClearColor(1, 1, 1)  # Establecer el color del fondo a rosa (RGB: 1, 0.5, 1)

# GameLoop
# Esto es para asegurarse de que el bucle principal siga corriendo, simulando el comportamiento en segundo plano
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

    rend.glClear()  # Limpiar la pantalla antes de dibujar nuevamente

    # Dibujar una línea en secuencia de puntos
    #for i in range(100):
    #    rend.glPoint(480 + i, 270 + i)

    #rend.glPoint(480, 270) # Dibujar un punto en el centro de la pantalla

    #rend.glLine((100,100),(500,450)) # Hacer la línea
    #rend.glLine((100,100),(200,250)) # Línea con pendiente cercana a 1
    #rend.glLine((100,100),(200,100)) # Línea con pendiente cercana a 1

    # Dibujar lineas usando Bresenham
    for x in range(0, width, 20):
        rend.glLineBresenham((0,0),(x, height))
        rend.glLineBresenham((0,height-1),(x, 0))
        rend.glLineBresenham((width-1,0),(x, height))
        rend.glLineBresenham((width-1,height-1),(x, 0))

    pygame.display.flip()  # Actualizar la pantalla con los cambios realizados
    clock.tick(60)  # Asegurar que el juego no exceda los 60 cuadros por segundo

rend.generateFrameBuffer("output.bmp")
pygame.quit()  # Salir del juego y cerrar la ventana de Pygame
