#Quiero crear una clase que me leea archivos obj. Tengo que parsear la informacion. 

class Obj(object):
  def init(self, filename):
    #asumiendo que el archivo es un formato obj
    with open (filename , "r") as file:
      lines = file.read().splitlines() #me lo va a separar por todos los saltos de lineas.
      #tengo que pasar linea por linea y guardar la informacion de la manera correcta. 
    self.vertices = []
    self.texcoords = []
    self.normals = []
    self.faces = [] 

    for line in lines:
      #si  la linea no cuenta con un prefijo y un valor 
      #seguimos a la siguiente linea. esto se hace si hay un linea vacia. 
      try:
        prefix , value = line.split(" ", 1) # que separe por espacios 1 vez.

      except:
        continue # si una linea vacia continua a la siguiente
      #dependiendo del prefijo parseamos y guardamos la informacion en el contenedor correcto. 

      if prefix == "v": #vertices
        vertice = list(map(float, value.split(" "))) #convierte todos los elemtnos de la lista a float. y luego lo convierte a una lista
        self.vertices.append(vertice)
      elif prefix == "vt": # texturas
        cts = list(map(float, value.split(" "))) #convierte todos los elemtnos de la lista a float. y luego lo convierte a una lista
        self.texcoords.append(cts)
      elif prefix == "vn": #normales
        vn = list(map(float, value.split(" "))) #convierte todos los elemtnos de la lista a float. y luego lo convierte a una lista
        self.vertices.append(vn)
      elif prefix == "f":
        face = []
        verts = value.split(" ")
        for vertice in verts:
          vert = list(map(int, vertice.split("/")))
          face.append(vert)
        self.faces.append(face)