import struct 

def char(c):
    #para generar y guardar en 1 byte
    return struct.pack("=c", c.encode("ascii"))
def word(w):
    return struct.pack("=h", w)

def dword(d):
    return struct.pack("=l", d)

class Renderer(object):
    # Constructor
    def __init__(self, screen):
        # Asigna la pantalla pasada como argumento al atributo de la clase
        self.screen = screen
        # Obtiene el rectángulo que describe la pantalla y extrae el ancho y el alto
        _, _, self.width, self.height = screen.get_rect()  # get_rect devuelve x, y, width, height, pero "_" es una convención para indicar que la variable no se usará

        self.glColor(1, 1, 1)  # Establecer el color inicial a blanco (RGB: 1, 1, 1)
        self.glClearColor(0, 0, 0)  # Establecer el color de fondo inicial a negro (RGB: 0, 0, 0)
        self.glClear()  # Limpiar la pantalla inicialmente

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
        # y = mx + b
        # asegurarse que los valores son enteros porque en un bitmap tira error
        x0 = int(v0[0])
        x1 = int(v1[0])
        y0 = int(v0[1])
        y1 = int(v1[1])
        m = (y1 - y0)/(x1-x0)
        b = y0 -m*x0
        color = [int(i * 255) for i in (color or self.currColor)]

        # dibujar la línea de forma inmediata posible
        for x in range(x0, x1 + 1):
            y = m*x + b
            self.glPoint(round(x),round(y))

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
            


            

