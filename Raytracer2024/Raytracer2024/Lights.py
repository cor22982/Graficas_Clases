# la luz ambiental el nivel minimo para que no se miren las cosas oscuras
# la luz direccional aplica en todas partes en la misma direccion en todas las superficies
# Luz de punto. Un point light es una luz que tiene un origen y apartir de ese origen genera rayos de luz en todas las direcciones
# Spot light es como una linterna. De este punto tiene un angulo minimo y solo tira luz en un cono

import numpy as np
from MathLib import *
class Light(object):
  def __init__(self, color = [0,0,0], intensity = 1, lightType = "None"):
    self.color = color
    self.intensity = intensity
    self.lightType = lightType

  def GetLightColor(self, intercept = None):
    return [(i* self.intensity) for i in self.color]

  def GetSpecularColor(self, intercept, viewPos):
    return [0,0,0]




class AmbientLight(Light):
  def __init__(self, color=[0, 0, 0], intensity=1):
    super().__init__(color, intensity, "Ambient")
  

class DirectionalLight(Light):
  def __init__(self, color=[0, 0, 0], intensity=1, direction = {0,-1,0}):
    super().__init__(color, intensity,"Directional")
    self.direction = direction / np.linalg.norm(direction)
  
  def GetLightColor(self, intercept = None):
    lightColor = super().GetLightColor(intercept)
    if intercept:
      dir = [(i*-1) for i in self.direction]
      intensity = np.dot(intercept.normal, dir)
      intensity = max(0, min(1, intensity))
      lightColor = [(i * intensity ) for i in lightColor]
    return lightColor
  
  def GetSpecularColor(self, intercept, viewPos):
    specColor = super().GetSpecularColor(intercept, viewPos)
    if intercept:
      dir = [(i*-1) for i in self.direction]
      reflect  = reflectVector(intercept.normal, dir)
      viewDIr = np.subtract(viewPos, intercept.point)
      viewPos /= np.linalg.norm(viewDIr)
      specularity = max (0,(np.dot(viewDIr, reflect) ** intercept.obj.material.spec))
      specularity *= intercept.obj.material.ks
      specularity *= self.intensity
      specColor = [(i*specularity) for i in specColor]
    return specColor
