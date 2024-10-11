import glm
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

class Renderer(object):
  def __init__(self, screen):
    self.screen = screen
    _,_, self.width, self.height = screen.get_rect()

    #el color del fondo
    glClearColor(0.2,0.2,0.2,1.0)

    # lo que prendo aqui es el z buffer
    glEnable(GL_DEPTH_TEST)
    glViewport(0,0, self.width, self.height)

    #no es tan facil de venir y agregar el triangulo . Sino que voy a crear una nueva clase para guardarlo

    self.scene = []
  
  def Render(self):
    #cada vez que renderce
    #aqui la memoria es muy delicada
    #yo quiero que borre que haga clear toda la info del framebuffer de color
    #tambien borre la informacion de profundidad
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    #cuando yo llamo render lo que quiero es pasar por cada objeto 
    #y renderizar cada objeto
    for obj in self.scene:
      obj.Render()
    

    