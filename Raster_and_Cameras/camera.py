from Mathlib import *
import numpy as np
class Camera (object):
  def __init__(self) -> None:
    self.translate = [0,0,0,0]
    self.rotate = [0,0,0,0]

  def GetViewMatrix (self) :
    translateMat = TranslationMatrix(self.translate[0],
                                         self.translate[1],
                                         self.translate[2]) 
    rotateMat = RotationMatrix(self.rotate[0],
                                    self.rotate[1],
                                    self.rotate[2])
    cam = translateMat * rotateMat
    return np.linalg.inv(cam) #la inversa de la matriz de la camara con numpy
