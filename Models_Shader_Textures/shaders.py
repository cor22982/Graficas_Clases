#si voy a usar numpy aqui
import numpy as np


def vertexShader(vertex, **kwargs):
    # Se lleva a cabo por cada vertice
    
    # Recibimos las matrices
    modelMatrix = kwargs["modelMatrix"]
    viewMatrix = kwargs["viewMatrix"]
    projectionMatrix = kwargs["projectionMatrix"]
    viewportMatrix = kwargs["viewportMatrix"]
    
    # Agregamos un componente W al vertice
    vt = [vertex[0],
          vertex[1],
          vertex[2],
          1]
    
    # Transformamos el vertices por todas las matrices en el orden correcto
    vt = viewportMatrix * projectionMatrix * viewMatrix * modelMatrix @ vt
    
    vt = vt.tolist()[0]
    
    # Dividimos x,y,z por w para regresar el vertices a un tama�o de 3
    vt = [vt[0] / vt[3],
          vt[1] / vt[3],
          vt[2] / vt[3]]
    
    return vt


def fragmentShader(**kwargs):
    # Se lleva a cabo por cada pixel individual
    
    # Obtenemos la informacion requerida
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    dirLight = kwargs["dirLight"]

    #sabiendo que las coordenadas de textura estan en 4ta 5ta posicion del indice
    #los obtenemos y guardamos
    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]


    # Empezamos siempre con color blanco
    r = 1
    g = 1
    b = 1
    
    vtP = [u*vtA[0] + v*vtB[0] + w*vtC[0],
           u*vtA[1] + v*vtB[1] + w*vtC[1]]
    
    
    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]
    # Se regresa el color
    return [r,g,b]


def flatShader(**kwargs):
    #ilumina de manera uniforme el triangulo
    # Se lleva a cabo por cada pixel individual
    
    # Obtenemos la informacion requerida
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    dirLight = kwargs["dirLight"]

    #sabiendo que las coordenadas de textura estan en 4ta 5ta posicion del indice
    #los obtenemos y guardamos
    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]

    #sabiendo que los valores de las normales 
    #estan en la 6ta 7ta 8va posicion hacemos lo mismo
    #asumismo que vienen normalizadas
    nA = [A[5], A[6], A[7]]
    nB = [B[5], B[6], B[7]]
    nC = [C[5], C[6], C[7]]


    # Empezamos siempre con color blanco
    r = 1
    g = 1
    b = 1
    
    vtP = [u*vtA[0] + v*vtB[0] + w*vtC[0],
           u*vtA[1] + v*vtB[1] + w*vtC[1]]
    
    
    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]
    # Se regresa el color
    return [r,g,b]

def gouradShader(**kwargs):
    # Se lleva a cabo por cada pixel individual
    
    # Obtenemos la informacion requerida
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    dirLight = kwargs["dirLight"]

    #sabiendo que las coordenadas de textura estan en 4ta 5ta posicion del indice
    #los obtenemos y guardamos
    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]

    #sabiendo que los valores de las normales 
    #estan en la 6ta 7ta 8va posicion hacemos lo mismo
    #asumismo que vienen normalizadas
    nA = [A[5], A[6], A[7]]
    nB = [B[5], B[6], B[7]]
    nC = [C[5], C[6], C[7]]

    #normal de este pixel
    normal = [u*nA[0] + v*nB[0] + w*nC[0],
              u*nA[1] + v*nB[1] + w*nC[1],
              u*nA[2] + v*nB[2] + w*nC[2]]
    
  
    # Empezamos siempre con color blanco
    r = 1
    g = 1
    b = 1
    
    vtP = [u*vtA[0] + v*vtB[0] + w*vtC[0],
           u*vtA[1] + v*vtB[1] + w*vtC[1]]
    
    
    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]
    # Se regresa el color

    #la formula de iluminacion que va a ser para calcular la intensidad
    #de que tan iluminada esta la superficie
    #intesity = normal DOT -dirlight

    #implementacion de producto punto de dos vectores

    intesity = np.dot(normal, -np.array(dirLight))
    intesity = max(0, intesity)
    r*= intesity
    g*= intesity
    b*= intesity
    return [r,g,b]
