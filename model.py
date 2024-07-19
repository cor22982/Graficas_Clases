from obj import Obj
from Mathlib import *
class Model(object):
    def __init__(self, filename):
        objFile = Obj(filename)  # Extraer la lectura del modelo
        self.vertices = objFile.vertices  # Extraer los vértices
        self.faces = objFile.faces  # Extraer las caras

        self.translate = [0,0,0]
        self.rotate = [0,0,0]
        self.scale = [1,1,1] # la escala minima siempre debe ser 1. 
        
    def GetModelMatrix (self):
        translateMat = TranslationMatrix(self.translate[0],
                                         self.translate[1],
                                         self.translate[2]) 
        rotateMat = RotationMatrix(self.rotate[0],
                                         self.rotate[1],
                                         self.rotate[2])
        scaleMat = ScaleMatrix(self.scale[0],
                               self.scale[1],
                               self.scale[2])
        return translateMat * rotateMat * scaleMat #esto ya esta hecho por numpy debemos de crearla nosotros. 
    