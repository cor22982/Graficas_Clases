import numpy as np
from Intercept import *
from math import atan2, acos, pi, isclose
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


class Plane(Shape):
    def __init__(self, position, material, normal):
        super().__init__(position, material)
        self.normal = normal
        self.type = "Plane"
    
    def ray_intersect(self, origin, dir):
        #distance = (plane Pos - rayOrigin o normal) / rayDir o nromal
        denom = np.dot(dir, self.normal)

        if isclose(0, denom):
            return None
        num = np.dot(np.subtract (self.position, origin), self.normal)

        t = num/denom

        if t < 0:
            return None

        # Puntodecontacto = origin  + dir * to
        P = np.add(origin, np.array(dir) * t)
        
        return Intercept(point=P, 
                         normal=self.normal,
                         distance=t,
                         texCords=None,
                         rayDirection=dir,
                         obj=self)
    

class Disk(Plane):
    def __init__(self, position, material, normal, radius):
        super().__init__(position, material, normal)
        self.radius  = radius
        self.type = "Disk"
    
    def ray_intersect(self, origin, dir):
        planeIntercept =  super().ray_intersect(origin, dir)
        if planeIntercept is None:
            return None
        contact = np.subtract(planeIntercept.point, self.position)
        contact = np.linalg.norm(contact) # vamos a sacar la magnitud de esto
        
        #para ignorar todo dentro del radio
        if contact > self.radius:
            return None

        return planeIntercept


#estas siglas significan que son access axis aligne bunding box
#es un cubo que no tiene rotacion, que esta alineado a x, y , z del mundo
""
class AABB(Shape):
    def __init__(self, position, material, sizes):
        super().__init__(position, material)
        self.sizes = sizes
        self.type = "AABB"
        #son planos con limites
        self.planes = []

        righPlane = Plane(
                    position=[position[0] + sizes[0]/2, position[1], position[2]], 
                    normal=[1,0,0], 
                    material=material)
        lefthPlane = Plane(
                    position=[position[0] - sizes[0]/2, position[1], position[2]], 
                    normal=[-1,0,0], 
                    material=material)
        
        UpPlane = Plane(
                    position=[position[0], position[1] + sizes[1]/2, position[2]], 
                    normal=[0,1,0], 
                    material=material)
        
        DownPlane = Plane(
                    position=[position[0], position[1] - sizes[1]/2, position[2]], 
                    normal=[0,-1,0], 
                    material=material)
        
        frontPlane = Plane(
                    position=[position[0], position[1] , position[2] + sizes[2]/2], 
                    normal=[0,0,1], 
                    material=material)
        
        backPlane = Plane(
                    position=[position[0], position[1] , position[2] + sizes[2]/2], 
                    normal=[0,0,-1], 
                    material=material)
        
        self.planes.append(righPlane)
        self.planes.append(lefthPlane)
        self.planes.append(UpPlane)
        self.planes.append(DownPlane)
        self.planes.append(frontPlane)
        self.planes.append(backPlane)

        #bounding box es una caja con limites

        #Bounds
        self.minBonds = [0,0,0]
        self.maxBounds = [0,0,0]

        #es un margen de error se podria decir
        epsilon = 0.001

        for i in range(3):
            self.minBonds[i] = position[i] - (epsilon+sizes[i]/2)
            self.maxBounds[i] = position[i] + (epsilon + sizes[i] / 2)


    def ray_intersect(self, origin, dir):
        intercept = None
        t = float("inf")
        for plane in self.planes:
            planeIntercept = plane.ray_intersect(origin, dir)

            if planeIntercept is not None:
                #revisar que esta dentro de los limites
                planePoint = planeIntercept.point
                #si cumplo con los limites en x
                if self.minBonds[0] <= planePoint[0] <= self.maxBounds[0]:
                    if self.minBonds[1] <= planePoint[1] <= self.maxBounds[1]:
                        if self.minBonds[2] <= planePoint[2] <= self.maxBounds[2]:
                            if planeIntercept.distance < t:
                                t = planeIntercept.distance
                                intercept = planeIntercept

        if intercept is None:
            return None
        
        u, v = 0,0

        if (abs(intercept.normal[0]> 0 )):
            #mapear las uvs para el eje x usando las coordenads de y y z
            u = (intercept.point[1]-self.minBonds[1])/self.sizes[1]
            v = (intercept.point[2]-self.minBonds[2])/self.sizes[2]

        elif (abs(intercept.normal[1]> 0 )):
            #mapear las uvs para el eje x usando las coordenads de y y z
            u = (intercept.point[0]-self.minBonds[0])/self.sizes[0]
            v = (intercept.point[2]-self.minBonds[2])/self.sizes[2]
        
        elif (abs(intercept.normal[2]> 0 )):
            #mapear las uvs para el eje x usando las coordenads de y y z
            u = (intercept.point[0]-self.minBonds[0])/self.sizes[0]
            v = (intercept.point[1]-self.minBonds[1])/self.sizes[1]
        u = min(0.999, max(0,u))
        v = min(0.999, max(0,v))
        return Intercept(point=intercept.point, 
                         normal=intercept.normal,
                         distance=t,
                         texCords=[u,v],
                         rayDirection=dir,
                         obj=self)




