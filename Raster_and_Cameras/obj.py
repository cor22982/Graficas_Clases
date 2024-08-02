#Quiero crear una clase que me leea archivos obj. Tengo que parsear la informacion. 
#esta encargada para parsear la informacion del archivo en formato obj y guardar esa informaicon
class Obj(object):
    def __init__(self, filename):
        # Asumiendo que el archivo es un formato obj
        self.vertices = []
        self.texcoords = []
        self.normals = []
        self.faces = []

        try:
            with open(filename, "r") as file:
                lines = file.read().splitlines()  # Separar por saltos de línea

            for line in lines:
                # Si la línea no cuenta con un prefijo y un valor, seguimos a la siguiente línea.
                try:
                    prefix, value = line.split(" ", 1)
                except ValueError:
                    continue  # Si una línea vacía continúa a la siguiente

                # Dependiendo del prefijo, parseamos y guardamos la información en el contenedor correcto.
                if prefix == "v":  # Vértices
                    vertice = list(map(float, value.split(" ")))  # Convertir a float y luego a lista
                    self.vertices.append(vertice)
                elif prefix == "vt":  # Coordenadas de textura
                    cts = list(map(float, value.split(" ")))  # Convertir a float y luego a lista
                    self.texcoords.append(cts)
                elif prefix == "vn":  # Normales
                    vn = list(map(float, value.split(" ")))  # Convertir a float y luego a lista
                    self.normals.append(vn)
                elif prefix == "f":  # Caras
                    face = []
                    verts = value.split(" ")
                    for vertice in verts:
                        vert = list(map(int, vertice.split("/")))
                        face.append(vert)
                    self.faces.append(face)
        except FileNotFoundError:
            print(f"Error: El archivo {filename} no se encontró.")
        except Exception as e:
            print(f"Error inesperado: {e}")