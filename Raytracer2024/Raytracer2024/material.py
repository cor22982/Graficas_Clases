#Determina cuales son las propiedades visuales de una superficie. 
#Como interactua la superficie con la luz
class Material (object):
  #difuse se refiere al color de la superficie. Que cuando una superficie esta iluminaada de cierto luz que color refleja
  def __init__(self, difuse):
    self.diffuse = difuse
  def GetSurfaceColor(self, intercept, renderer):

    # el modelo fond de iluminacion phong
    #PHNG REFLETION MODEL
    # LightColors = lightCOlor + Specular
    # el color final es 
    # FinalCOlor = DiffuseColor * LightCOlor

    lightColor = [0,0,0]
    finalColor = self.diffuse
    for light in renderer.lights:
      currectLightCOlor = light.GetLightColor(intercept)
      lightColor = [(lightColor[i] + currectLightCOlor[i]) for i in range (3)]
    
    finalColor = [(finalColor[i] * lightColor[i]) for i in range(3)]
    finalColor = [min(1, finalColor[i]) for i in range(3)]

    return finalColor

