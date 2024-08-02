
#yo tengo que darle a mi render una referencia a hacer referencia a este vertex. 

def VertexShader (vertex, **kwargs): #le puedo dar una cantidad ilimitada de argumentos.  esto es un diccionario lo puedo recibir varios
  modelMatrix = kwargs["modelMatrix"]
  #la camara estara aqui en vertexshader

  viewMatrix = kwargs["viewMatrix"]
  projectionMatrix = kwargs["projectionMatrix"]
  viewportMatrix = kwargs["viewportMatrix"]

  vt = [vertex[0],
        vertex[1],
        vertex[2],
        1]  #convertir el vertice en un tamaño de 4
  
  vt = viewportMatrix * projectionMatrix * viewMatrix * modelMatrix @ vt #en este caso como uso numpy usa el @ para representar la multiplicacion de matriz por vector

  vt = vt.tolist()[0] #que regrese el primer resultado. porque la multiplicacion regresa una lista

  vt = [vt[0]/vt[3],
        vt[1]/vt[3],
        vt[2]/vt[3],
        vt[3]/vt[3]]
  
  return vt