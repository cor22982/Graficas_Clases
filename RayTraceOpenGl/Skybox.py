import glm
from numpy import array, float32
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pygame as pg
class Skybox(object):
  def __init__(self, texturesList, vertexShader, fragmentShader):
    SkyboxVertices = [
        # Cara trasera
        -1.0,  1.0, -1.0,
        -1.0, -1.0, -1.0,
        1.0, -1.0, -1.0,
        1.0, -1.0, -1.0,
        1.0,  1.0, -1.0,
        -1.0,  1.0, -1.0,

        # Cara izquierda
        -1.0, -1.0,  1.0,
        -1.0, -1.0, -1.0,
        -1.0,  1.0, -1.0,
        -1.0,  1.0, -1.0,
        -1.0,  1.0,  1.0,
        -1.0, -1.0,  1.0,

        # Cara derecha
        1.0, -1.0, -1.0,
        1.0, -1.0,  1.0,
        1.0,  1.0,  1.0,
        1.0,  1.0,  1.0,
        1.0,  1.0, -1.0,
        1.0, -1.0, -1.0,

        # Cara frontal
        -1.0, -1.0,  1.0,
        -1.0,  1.0,  1.0,
        1.0,  1.0,  1.0,
        1.0,  1.0,  1.0,
        1.0, -1.0,  1.0,
        -1.0, -1.0,  1.0,

        # Cara superior
        -1.0,  1.0, -1.0,
        1.0,  1.0, -1.0,
        1.0,  1.0,  1.0,
        1.0,  1.0,  1.0,
        -1.0,  1.0,  1.0,
        -1.0,  1.0, -1.0,

        # Cara inferior
        -1.0, -1.0, -1.0,
        -1.0, -1.0,  1.0,
        1.0, -1.0, -1.0,
        1.0, -1.0, -1.0,
        -1.0, -1.0,  1.0,
        1.0, -1.0,  1.0
    ]
    self.vertexBuffer = array(SkyboxVertices, dtype=float32)
    self.VBO = glGenBuffers(1)
    self.VAO = glGenVertexArrays(1)

    self.shaders = compileProgram(compileShader(vertexShader, GL_VERTEX_SHADER),
                                  compileShader(fragmentShader, GL_FRAGMENT_SHADER))

    self.texture = glGenTextures(1)
    for i in range(len(texturesList)):
      texture = pg.image.load(texturesList[i])
      textureData = pg.image.tostring(texture, "RGB", False)
      glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X + i, 
                   0,
                   GL_RGB,
                   texture.get_width(),
                   texture.get_height(),
                   0,
                   GL_RGB,
                   GL_UNSIGNED_BYTE,
                   textureData)

      glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
      glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
      glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
      glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
      glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)
  
  def Render(self, viewMatrix, projectionMatrix):
    if self.shaders == None:
      return
    else:
      viewMatrix = glm.mat4(glm.mat3(viewMatrix))
      glUseProgram(self.shaders)
      # es una propiedad que por ahora ignore la profundidad
      glUniformMatrix4fv( glGetUniformLocation(self.active_shaders, 
                                                  "viewMatrix"), 
                                                  1, 
                                                  GL_FALSE, 
                                                  glm.value_ptr(viewMatrix))
      glUniformMatrix4fv( glGetUniformLocation(self.active_shaders, 
                                                  "proyectionMatrix"), 
                                                  1, 
                                                  GL_FALSE, 
                                                  glm.value_ptr(projectionMatrix))
      glDepthMask(GL_FALSE)
      

      glBindTexture(GL_TEXTURE_CUBE_MAP)
      glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
      glBindVertexBuffer(self.VAO)

      glBufferData(GL_ARRAY_BUFFER,
                   self.vertexBuffer.nbytes,
                   self.vertexBuffer,
                   GL_STATIC_DRAW)
      
      glVertexAttribPointer(0,
                            3,
                            GL_FLOAT,
                            GL_FALSE,
                            4*3,
                            ctypes.c_void_p(0))
      
      glEnableVertexAttribArray(0)

      glDrawArrays(GL_TRIANGLES, 0,36)

      #pero tengo que volver a prenderlo
      glDepthMask(GL_TRUE)

