
# voy a crear mis programas aqui pero voy a usar texto despues uso una funcion
# para compilarlos y usarlo
# en layout le digo que empiezo a leer el atributo en la posicion 0 y que es un vector llamado posicion
# vector numero el numero es la cantidad cuanto sale [0,0,0]
# los shaders son dificiles de debuggear porque es imposible poner un breackpoint
# glPosition es donde se guarda la posicion de los vertices
vertex_shader = """
#version 450 core
layout(location=0) in vec3 position;
layout(location=1) in vec3 vColor;
out vec3 outColor;
void main()
{
  gl_Position = vec4(position, 1.0);
  outColor = vColor;
}
"""


fragmet_shader = """
#version 450 core
in vec3 outColor;
out vec4 fragColor;

void main()
{
  fragColor = vec4(outColor, 1.0);
}
"""