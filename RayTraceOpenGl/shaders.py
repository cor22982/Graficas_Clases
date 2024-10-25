
# voy a crear mis programas aqui pero voy a usar texto despues uso una funcion
# para compilarlos y usarlo
# en layout le digo que empiezo a leer el atributo en la posicion 0 y que es un vector llamado posicion
# vector numero el numero es la cantidad cuanto sale [0,0,0]
# los shaders son dificiles de debuggear porque es imposible poner un breackpoint
# glPosition es donde se guarda la posicion de los vertices
vertex_shader = """
#version 450 core
layout(location=0) in vec3 position;
layout(location=1) in vec2 textCoords;
layout(location=2) in vec3 normals;
out vec2 outTextCoords;
out vec3 outNormals;
uniform mat4 modelMatrix;
uniform float time;

void main()
{
  gl_Position = modelMatrix * vec4(position + normals * sin(time)/10, 1.0);
  outTextCoords =  textCoords;
  outNormals = normals;
}
"""
# uniform datos que son todos iguales 
# no hay que enviarle el atributo del vertice . En este caso tiene antes que pasar por el vertice
fragmet_shader = """
#version 450 core
in vec2 outTextCoords;
in vec3 outNormals;
out vec4 fragColor;
uniform sampler2D tex;
void main()
{
  fragColor = texture(tex, outTextCoords);
}
"""