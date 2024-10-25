class Obj(object):
    """
    Clase para leer y parsear archivos en formato OBJ.

    Esta clase está diseñada para leer archivos OBJ y extraer información sobre vértices, coordenadas de textura, normales y caras.
    La información extraída se guarda en listas internas.

    Attributes:
        vertices (list of list of float): Lista de vértices del modelo. Cada vértice es una lista de coordenadas (x, y, z).
        texcoords (list of list of float): Lista de coordenadas de textura del modelo. Cada coordenada es una lista de valores (u, v).
        normals (list of list of float): Lista de normales del modelo. Cada normal es una lista de valores (x, y, z).
        faces (list of list of list of int): Lista de caras del modelo. Cada cara es una lista de índices de vértices, coordenadas de textura y normales.

    Args:
        filename (str): Nombre del archivo OBJ a leer. El archivo debe estar en formato OBJ válido.

    Raises:
        FileNotFoundError: Si el archivo especificado no se encuentra.
        Exception: Si ocurre un error inesperado durante la lectura o el procesamiento del archivo.
    """

    def __init__(self, filename):
        """
        Inicializa una instancia de la clase Obj y lee el archivo OBJ especificado.

        Este método abre el archivo, lee su contenido línea por línea y parsea la información basada en el prefijo de cada línea.
        La información se guarda en las listas correspondientes: vértices, coordenadas de textura, normales y caras.

        Args:
            filename (str): Nombre del archivo OBJ a leer.

        Raises:
            FileNotFoundError: Si el archivo especificado no se encuentra.
            Exception: Si ocurre un error inesperado durante la lectura o el procesamiento del archivo.
        """
        self.vertices = []
        self.texcoords = []
        self.normals = []
        self.faces = []

        try:
            with open(filename, "r") as file:
                lines = file.read().splitlines()

            for line in lines:
                # Elimina espacios al final de la línea
                line = line.rstrip()

                try:
                    prefix, value = line.split(" ", 1)
                except ValueError:
                    continue  # Ignora líneas que no tienen el formato esperado

                # Dependiendo del prefijo, parseamos y guardamos
                # la información en el contenedor correcto
                if prefix == "v":  # Vértices
                    try:
                        vert = list(map(float, value.split(" ")))
                        self.vertices.append(vert)
                    except ValueError:
                        print("Advertencia: Se encontró un vértice con valores no numéricos.")
                elif prefix == "vt":  # Coordenadas de textura
                    try:
                        vts = list(map(float, value.split(" ")))
                        self.texcoords.append([vts[0], vts[1]])
                    except ValueError:
                        print("Advertencia: Se encontró una coordenada de textura con valores no numéricos.")
                elif prefix == "vn":  # Normales
                    try:
                        norm = list(map(float, value.split(" ")))
                        self.normals.append(norm)
                    except ValueError:
                        print("Advertencia: Se encontró una normal con valores no numéricos.")
                elif prefix == "f":  # Caras
                    try:
                        face = []
                        verts = value.split(" ")
                        for vert in verts:
                            vert = list(map(int, vert.split("/")))
                            face.append(vert)
                        self.faces.append(face)
                    except ValueError:
                        print("Advertencia: Se encontró una cara con índices no numéricos.")
        except FileNotFoundError:
            print(f"Error: El archivo {filename} no se encontró.")
        except Exception as e:
            print(f"Error inesperado: {e}")
