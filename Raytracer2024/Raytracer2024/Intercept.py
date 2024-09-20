class Intercept (object):
  def __init__(self, point, normal, distance, obj, rayDirection):
    self.point = point
    self.normal = normal
    self.distance = distance
    #es el rayo entrante con el que se hizo contacto el intercepto
    self.rayDirection = rayDirection
    self.obj = obj
  


  
