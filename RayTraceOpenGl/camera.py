import glm
import numpy as np
from numpy import sin, radians, cos
class Camera(object):
  def __init__(self, width, height):
    self.position = glm.vec3(0,0,0)

    #angulos de euler
    self.rotation = glm.vec3(0,0,0)
    self.screenWidth = width
    self.screenHeight = height
    self.viewMatrix = None
    self.usingLookAt = False
    self.CreateProjectionMatrix(60, 0.1, 1000)
  
  def GetViewMaTrix(self):
    if not self.usingLookAt:
      identity = glm.mat4(1)
      translateMat = glm.translate(identity, self.position)
      
      pitchMat = glm.rotate(identity, glm.radians(self.rotation.x), glm.vec3(1,0,0))
      yawMat   = glm.rotate(identity, glm.radians(self.rotation.y), glm.vec3(0,1,0))
      rollMat  = glm.rotate(identity, glm.radians(self.rotation.z), glm.vec3(0,0,1))
      
      rotationMat = pitchMat * yawMat * rollMat
      
      
      camMat = translateMat * rotationMat
      
      self.viewMatrix =  glm.inverse(camMat)
    return self.viewMatrix
  
  def GetProjectionMatrix(self):
    return self.proyectionMatrix
  
  def CreateProjectionMatrix(self, fov, nearPlane, farPlane):
    self.proyectionMatrix = glm.perspective(glm.radians(fov), self.screenWidth/self.screenHeight, nearPlane, farPlane)


  def LookAt(self, center):
    self.usingLookAt = True
    self.viewMatrix = glm.lookAt(self.position,center, glm.vec3(0,1,0))
    

    #Los quaterniones es un sistema de numeros complejos para representar rotaciones
    #Los quaterniones representan una matriz de 4x4 en un vector4 . De esta manera eliminar espacio de sobra

    #esta funcion me lo regresa en radianes y lo necesito en grados
    

  def Orbit(self, center, distance, angle):
    self.position.x = center.x + sin(radians(angle)) * distance
    self.position.z = center.z + cos(radians(angle)) * distance


