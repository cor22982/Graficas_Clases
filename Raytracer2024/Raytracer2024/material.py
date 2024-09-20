#Determina cuales son las propiedades visuales de una superficie. 
#Como interactua la superficie con la luz
from MathLib import *

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2

class Material (object):
  #difuse se refiere al color de la superficie. Que cuando una superficie esta iluminaada de cierto luz que color refleja
  def __init__(self, difuse, spec = 1.0 , ks = 0.0, matType = OPAQUE):
    self.diffuse = difuse
    self.spec = spec
    self.ks = ks
    self.matType = matType

  def GetSurfaceColor(self, intercept, renderer):

    # el modelo fond de iluminacion phong
    #PHNG REFLETION MODEL
    # LightColors = lightCOlor + Specular
    # el color final es 
    # FinalCOlor = DiffuseColor * LightCOlor

    lightColor = [0,0,0]
    finalColor = self.diffuse
    reflectColor = [0,0,0]
    for light in renderer.lights:
      shadowIntercept = None
      if light.lightType == "Directional":
        lightDir = [-x for x in light.direction]
        shadowIntercept = renderer.glCastRay(intercept.point, lightDir, intercept.obj)
      
      if shadowIntercept == None:
        lightColor = [(lightColor[i] + light.GetSpecularColor(intercept, renderer.camera.translate)[i]) for i in range (3)]

        if self.matType == OPAQUE:
          lightColor = [(lightColor[i] + light.GetLightColor(intercept)[i]) for i in range (3)]
    if self.matType == REFLECTIVE:
      raydir = [-x for x in intercept.rayDirection]
      reflect = reflectVector(intercept.normal, raydir)
      ##generamos el rayo que va a venir del nuevo punto y con el vecto de reflecto
      reflectintercept = renderer.glCastRay(intercept.point, reflect, intercept.obj)
      #en base a este intercepto tengo que ahora obtener un nuevo color de la superficie
      #si hice contacto con algun objeto
      if reflectintercept != None:
        reflectColor = reflectintercept.obj.material.GetSurfaceColor(reflectintercept, renderer)
      else:
        reflectColor = renderer.clearColor
    
    finalColor = [(finalColor[i] * (lightColor[i] + reflectColor[i])) for i in range(3)]
    finalColor = [min(1, finalColor[i]) for i in range(3)]
    return finalColor

