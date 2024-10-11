import glm
from numpy import array, float32
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
# usamos esta clase de buffer para guardar la informacion de lo que se va a dibujar
class Buffer(object):
  def __init__(self, data):
    # python no le importa el tamaño de los datos
    # que en el buffer de vertices cada float ocupa 4 bytes
    self.vertBuffer = array(data, float32)

    # Vertex Buffer Object
    #aqui es donde mando la informacion a la tarjeta de video
    self.VBO = glGenBuffers(1)

    #el otro objeto que necesito crear es 
    # Vertex Array Object
    #tenemos que mandarle la informacion de atributos como color normales, texcords
    self.VAO = glGenVertexArrays(1)
  
  def Render(self):
    # cada vez que llame render
    # voy a atar un bufffer a la tarjeta de video
    glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
    glBindVertexArray(self.VAO)

    # Mandar la informacion de vertices
    # buffer id
    # tamaño del buffer en bytes
    #datos
    # uso static draw es para dibujar de manera estatica
    glBufferData(GL_ARRAY_BUFFER,
                 self.vertBuffer.nbytes,
                 self.vertBuffer,
                 GL_STATIC_DRAW)
    # atributos especificar que representa y como usarla

    #atributo de posiciones
    # numero de atributo como es 1 al principio dejemolo en 0
    # tamaño de datos por cada posicion son 3
    # tipo
    # si esta normalizado
    # stride o el tamaño del paso de cada cuanto informacion hay un nuevo atributo
    #offset este ser refiere a en donde en que posicion empieza la informacion de posicion
    glVertexAttribPointer(0,
                          3,
                          GL_FLOAT,
                          GL_FALSE,
                          4 * 3,
                          ctypes.c_void_p(0))

    #este paso es que atributo quiero activar
    glEnableVertexAttribArray(0)

    #dibujar buffer
    #modo en que modo
    # desde donde empezamos a dibujar
    # cuantos vertices vamos a dibujar por vertices hay 3 por eso se coloca
    glDrawArrays(GL_TRIANGLES, 0,int(len(self.vertBuffer)/3))