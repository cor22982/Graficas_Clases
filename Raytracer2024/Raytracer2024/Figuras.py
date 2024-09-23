import numpy as np
from Intercept import *
from math import atan2, acos, pi
class Shape(object):
    def __init__(self, position, material):
        self.position = position
        self.type = "None"
        self.material = material
    
    def ray_intersect(self, origin, dir):
        return None

class Sphere(Shape):
    def __init__(self, position, radius, material):
        super().__init__(position , material)  # Corrige la llamada a super()
        self.radius = radius
        self.type = "Sphere"
    
    def ray_intersect(self, origin, dir):
        L = np.subtract(self.position, origin)
        tca = np.dot(L, dir)
        a = np.linalg.norm(L)
        f = a **2
        d = f - tca**2
        if d > self.radius:
            return None
        thc = (self.radius ** 2 - d ** 2) ** 0.5 
        t0 = tca - thc
        t1 = tca + thc
        #esto quiere decir que esta atras
        if t0 < 0:
            t0 = t1
        if t0< 0:
            return None
        P = np.add(origin, np.multiply(dir, t0))
        normal = np.subtract(P, self.position) 
        normal /= np.linalg.norm(normal)
        
        #normal como la direccion del rayo para calcular la direccion de la esfera texturizada
        u = (atan2(normal[2], normal[0])) / (2*pi) +0.5
        v = acos(-normal[1]) /pi

        return Intercept(point=P, normal=normal, distance=t0, obj=self, rayDirection=dir, texCords=[u,v])
