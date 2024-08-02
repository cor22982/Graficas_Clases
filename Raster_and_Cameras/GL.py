import struct 
import numpy as np
from camera import Camera
from math import tan, pi
def char(c):
    #para generar y guardar en 1 byte
    return struct.pack("=c", c.encode("ascii"))
def word(w):
    return struct.pack("=h", w)

def dword(d):
    return struct.pack("=l", d)

POINTS = 0
LINES  = 1
TRIANGLES = 2
QUADS = 3
class Renderer(object):
    # Constructor
    def __init__(self, screen):
        # Asigna la pantalla pasada como argumento al atributo de la clase
        self.screen = screen
        # Obtiene el rectángulo que describe la pantalla y extrae el ancho y el alto
        _, _, self.width, self.height = screen.get_rect()  # get_rect devuelve x, y, width, height, pero "_" es una convención para indicar que la variable no se usará

        self.camera = Camera()
        self.glViewport(0,0,self.width, self.height)
        self.glProyection()

        self.glColor(1, 1, 1)  # Establecer el color inicial a blanco (RGB: 1, 1, 1)
        self.glClearColor(0, 0, 0)  # Establecer el color de fondo inicial a negro (RGB: 0, 0, 0)
        self.glClear()  # Limpiar la pantalla inicialmente
        self.models = []
        self.vertexShader = None #ahorita no tengo asignado un vertex shader
        self.primitiveType = POINTS #por defecto es triangulo
    # Recomendable dejar RGB en valores entre 0 y 1 porque de 0 a 255 no es simple calcular colores
    def glColor(self, r, g, b):
        # Asegurarse de que los valores de RGB estén en el rango de 0 a 1
        r = min(1, max(0, r))  # Limitar el valor de r entre 0 y 1
        g = min(1, max(0, g))  # Limitar el valor de g entre 0 y 1
        b = min(1, max(0, b))  # Limitar el valor de b entre 0 y 1
        # Asignar el color actual a los valores RGB ajustados
        self.currColor = [r, g, b]

    # Color de fondo
    def glClearColor(self, r, g, b):
        r = min(1, max(0, r))  # Limitar el valor de r entre 0 y 1
        g = min(1, max(0, g))  # Limitar el valor de g entre 0 y 1
        b = min(1, max(0, b))  # Limitar el valor de b entre 0 y 1
        # Asignar el color de fondo actual a los valores RGB ajustados
        self.clearColor = [r, g, b]

    # Esto borra todo lo que está en la pantalla y lo coloca de un color
    def glClear(self):
        color = [int(i * 255) for i in self.clearColor]  # Convertir el color a un rango de 0 a 255
        self.screen.fill(color)  # Llenar la pantalla con el color de fondo

        # FrameBuffer -> comprensión de listas
        self.frameBuffer =  [[self.clearColor for y in range(self.height)]
                             for x in range(self.width)]
        
    # Si se dibuja algo, se manda el color; si no, no
    def glPoint(self, x, y, color=None):
        # Pygame empieza a renderizar desde la esquina superior izquierda y el bitmap desde la esquina inferior.
        # Por lo tanto, hay que voltear el valor y

        if (0 <= x < self.width) and (0 <= y < self.height):
            # Tener en cuenta que Pygame recibe los colores en un rango de 0 a 255, no de 0 a 1 como lo hicimos
            color = [int(i * 255) for i in (color or self.currColor)]
            # Establecer el color en la posición (x, y) en la pantalla, invirtiendo la coordenada y
            self.screen.set_at((x, self.height - 1 - y), color)
            self.frameBuffer[x][y] = color # guardar la información en algún lugar

            
    # Dibujar una línea donde v0 y v1 es un array porque es un punto x,y usando la fórmula de línea
    def glLine(self, v0, v1, color=None):
        x0, y0 = v0
        x1, y1 = v1

        x0 = int(x0)
        x1 = int(x1)
        y0 = int(y0)
        y1 = int(y1)

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        offset = 0
        threshold = dx
        y = y0
        y_step = 1 if y0 < y1 else -1

        for x in range(x0, x1 + 1):
            if steep:
                self.glPoint(y, x, color)
            else:
                self.glPoint(x, y, color)

            offset += dy * 2

            if offset >= threshold:
                y += y_step
                threshold += dx * 2

    # Dibujando una línea con algoritmo de Lineas de Bresenham
    # en y = mx + b hay errores de una línea:
    # 1. de un punto al mismo punto
    # 2. direccion de linea
    # 3. direccion de la pendiente
    def glLineBresenham(self, v0, v1, color = None):
        x0 = int(v0[0])
        x1 = int(v1[0])
        y0 = int(v0[1])
        y1 = int(v1[1])
        
        # en el primer caso se dibuja un punto
        if (x0 == x1) and (y0 == y1):
            self.glPoint(x0,y0)
            return

        # determinar si algo está muy inclinado con los deltas en que lado
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)
        steep = dy > dx
        
        # caso de inclinación para voltear los vértices
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        # caso para dibujar líneas en otras direcciones
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        
        # dado que se alteró la orientación se calcula nuevamente los deltas
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        offset = 0 # determinar si me pase a la siguiente fila para pintar pixeles
        limit = 0.75 # esto sirve para determinar cual de los dos pixeles pinto si esta cubriendo 2 y pintar el que tenga más proporcion de la línea
        
        # determinar el valor de y para el primer caso
        m = dy/dx
        y = y0

        # caso para el caso 3
        for x in range(x0, x1 + 1):
            if steep:
                self.glPoint(y,x, color or self.currColor)
            else:
                self.glPoint(x,y, color or self.currColor)
            
            offset += m # bandera para determinar cuanto me he movido
            
            if offset >= limit: # si sobrepasa el límite determino la nueva y
                if y0 < y1:
                    y += 1
                else:
                    y-= 1

                limit +=1 # para pasarme a la siguiente línea

    def generateFrameBuffer(self, filename):
        with open(filename, "wb") as file:
            #Header
            
            file.write(char("B"))
            file.write(char("M"))
            #el filezise tengo que ingresar el tamño del archivo completo en bytes
            # 14 bytes del header 40 del infoheader y el ancho por altura por 3 de los colores del canvas
            file.write(dword(14+ 40 + (self.width * self.height * 3)))
            file.write(dword(0))
            file.write(dword(14 + 40)) #el dataofset

            #InfoHeader
            file.write(dword(40))
            file.write(dword(self.width))#el ancho de los pixeles
            file.write(dword(self.height))#el alto de los pixeles
            file.write(word(1)) #numero de planos. 
            #si le digo 32 bits va a leer cada 4 bytes Y si le digo 24 va a leer de 3 bytes en 3 bytes
            #como interpreto un visualizador de imagenes y cuantos bits representan un pixel. 
            file.write(word(24))
            file.write(dword(0)) #tipo de compresion 4 bytes que no tiene xompresion
            file.write(dword(self.width * self.height * 3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            
            #TABLA DE COLORES
            #por cada color debo guardar un byte

            for y in range (self.height):
                for x in range (self.width):
                    color = self.frameBuffer[x][y]
                    color = bytes([color[2], color[1], color[0]])                    
                    file.write(color)
    
    def glRender (self):
        for model in self.models:
            #por cada modelo en la lista lo voy a dibujar
            #por cada modelo tengo que agarrar su matriz modelo

            mMat = model.GetModelMatrix()
            #
            vertexBuffer = []  #es un espacio reservado en memoria temporal el buffer, en cambio aqui guardare mis vertices
            

            for face in model.faces:
                #revisamos cuantos vertices tiene la cara si tiene
                #cuatro vertices , hay que crear un segundo traingulo
                vertCount = len(face)
                v0 = model.vertices[ face[0][0] - 1 ] 
                v1 = model.vertices[ face[1][0] - 1 ]
                v2 =  model.vertices[ face[2][0] - 1 ]
                if vertCount == 4 :
                    v3 = model.vertices[ face[3][0] - 1 ] #si hay un vertice demas crea otra.

                #si contamos con un vertex shader asignado se manda
                #cada vertice para transformarlos
                #pasar las matrices necesarias para este vertexshader
                if self.vertexShader:
                    v0 = self.vertexShader(v0, 
                                            modelMatrix = mMat, 
                                            viewMatrix = self.camera.GetViewMatrix(),
                                            projectionMatrix= self.projectionMatrix,
                                            viewportMatrix= self.viewPortMatrix)
                    v1 = self.vertexShader(v1, 
                                            modelMatrix = mMat, 
                                            viewMatrix = self.camera.GetViewMatrix(),
                                            projectionMatrix= self.projectionMatrix,
                                            viewportMatrix= self.viewPortMatrix)
                    v2 = self.vertexShader(v2, 
                                            modelMatrix = mMat, 
                                            viewMatrix = self.camera.GetViewMatrix(),
                                            projectionMatrix= self.projectionMatrix,
                                            viewportMatrix= self.viewPortMatrix)
                    if vertCount == 4 :
                        v3 = self.vertexShader(v3, 
                                            modelMatrix = mMat, 
                                            viewMatrix = self.camera.GetViewMatrix(),
                                            projectionMatrix= self.projectionMatrix,
                                            viewportMatrix= self.viewPortMatrix)
                
                vertexBuffer.append(v0)
                vertexBuffer.append(v1)
                vertexBuffer.append(v2)
                if vertCount == 4 :
                    vertexBuffer.append(v3) #lo agregmos a nuestro listado de vertices. Ahorita estmos guardando la posicion. 

            self.glDrawPrimitives(vertexBuffer)

                #self.glPoint(int(v0[0]), int(v0[1])) #obtengo la coordenada x del vertice
                #self.glPoint(int(v1[0]), int(v2[1]))
                #self.glPoint(int(v2[0]), int(v1[1]))
                #if vertCount == 4 :
                #    self.glPoint(int(v3[0]),int(v1[1]))

                # self.glLine((v0[0], v0[1]),(v1[0], v1[1]))
                # self.glLine((v1[0], v1[1]),(v2[0], v2[1]))
                # self.glLine((v2[0], v2[1]),(v0[0], v0[1])) #del 2 al 0 creamos un triangulo
                # if vertCount == 4 :
                #     self.glLine((v0[0], v0[1]),(v2[0], v2[1])) # si hay 4 vertices creamos el otro triangulo
                #     self.glLine((v2[0], v2[1]),(v3[0], v3[1]))
                #     self.glLine((v3[0], v3[1]),(v0[0], v0[1]))
    def glDrawPrimitives(self, buffer):
        if self.primitiveType == POINTS:
            for point in buffer:
                self.glPoint(int(point[0]), int(point[1]))
        elif self.primitiveType == LINES:
            if len(buffer) % 3 != 0:
                print("Warning: The buffer length for LINES is not a multiple of 3. Truncating the buffer.")
                buffer = buffer[:len(buffer) - (len(buffer) % 3)]
            for i in range(0, len(buffer), 3):
                p0 = buffer[i]
                p1 = buffer[i + 1]
                p2 = buffer[i + 2]
                self.glLine((p0[0], p0[1]), (p1[0], p1[1]))
                self.glLine((p1[0], p1[1]), (p2[0], p2[1]))
                self.glLine((p2[0], p2[1]), (p0[0], p0[1]))



    def glViewport (self, x, y, width, height):
        #el viewport puede ser mas pequeño que la pantalla. 
        self.vpx = int(x)
        self.vpy = int(y)
        self.vpWidht = width
        self.vpHeight = height
        self.viewPortMatrix = np.matrix([[width/2,0,0,x+ width/2],
                                         [0,height/2,0,y+height/2],
                                         [0,0,0.5,0.5],
                                         [0,0,0,1]])
        
    def glProyection (self, n = 0.1, f = 1000, fov = 60):
        aspectRatio = self.vpWidht/self.vpHeight
        fov *= pi / 180  #lo convierto a radianes y ahora calculo t
        t = tan(fov/2) * n
        r = t * aspectRatio
        self.projectionMatrix = np.matrix([[n/r,0,0,0],
                                           [0,n/t,0,0],
                                           [0,0,-(f+n)/(f-n),-(2*f*n)/(f-n)],
                                           [0,0,-1,0]])
        
    def glTriangle(self, A, B, C , color = None):

        if A[1] < B[1] :
            A, B = B, A
        elif A[1] < C[1] :
            A, C = C, A
        elif B[1] < C[1]:
            B, C = C, B
        
        self.glLine((A[0], A[1]),(B[0], B[1]))
        self.glLine((B[0], B[1]),(C[0], C[1]))
        self.glLine((C[0], C[1]),(A[0], A[1]))

        def flatBotton (vA, vB, vC):
            try:
                mBA =  (vB[0]-vA[0])/(vB[1]-vA[1]) #la pendiente en x.
                mCA = (vC[0]-vA[0])/(vC[1]-vA[1])
            except:
                pass
            else:
                x0 = vB[0]
                x1 = vC[0]
                for y in range (int(vB[1]), int(vA[1])):
                    #va pasando para todas las y de hasta abajo a arriba
                    self.glLine([x0, y], [x1, y], color) #aqui pintamos
                    x0 += mBA
                    x1 += mCA
                    
        def flatTop (vA, vB, vC):
            try:
                mCA =  (vC[0]-vA[0])/(vC[1]-vA[1]) #la pendiente en x.
                mCB = (vC[0]-vB[0])/(vC[1]-vB[1])
            except:
                pass
            else:
                x0 = vA[0]
                x1 = vB[0]
                for y in range (int(vC[1]), int(vA[1])):
                    #va pasando para todas las y de hasta abajo a arriba
                    self.glLine([x0, y], [x1, y], color) #aqui pintamos
                    x0 -= mCA
                    x1 -= mCB
            
        if B[1] == C[1]:
            flatBotton(A,B,C)
        elif A[1] == B[1]:
            flatTop(A,B,C)
        else:
            D =  [A[0] + ((B[1]- A[1])/(C[1]- A[1])) * (C[0]- A[0]), B[1]]
            flatBotton(A,B,D)
            flatTop(B,D,C) 
            #Tengo dividirlo en 2 triangulos
            # y dibujo ambos tipos de triangulos. 
            #Teorema del intercepto
            pass



        

                



            

