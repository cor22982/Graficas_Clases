#para agilizar las cosas mucho mas va a usar numpy, pero cada uno
#debe de construir su libreria de matematicas que es numpy. 

import numpy as np #esto no
from math import pi, sin, cos #esto si lo podemos usar


def ScaleMatrix(x,y,z):
  sMat = np.matrix([[x,0,0,0],
                    [0,y,0,0],
                    [0,0,z,0],
                    [0,0,0,1]
                    ])
  return sMat


def TranslationMatrix (x, y, z):
  tMat = np.matrix([[1,0,0,x],
                    [0,1,0,y],
                    [0,0,1,z],
                    [0,0,0,1]
                    ])
  return tMat


def RotationMatrix (pitch, yaw, roll):
  pitch *=  pi/180
  yaw *= pi/180
  roll *= pi/180

  pitchMat = np.matrix([[1,0,0,0],
                      [0,cos(pitch),-sin(pitch),0],
                      [0,sin(pitch),cos(pitch),0],
                      [0,0,0,1]])

  yawMat = np.matrix([[cos(yaw),0,sin(yaw),0],
                    [0,1,0,0],
                    [-sin(yaw),0,cos(yaw),0],
                    [0,0,0,1]])

  rollMat = np.matrix([[cos(roll),-sin(roll),0,0],
                     [sin(roll),cos(roll),0,0],
                     [0,0,1,0],
                     [0,0,0,1]])
  
  return pitchMat*yawMat*rollMat