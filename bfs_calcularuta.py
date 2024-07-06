import matplotlib.pyplot as plt #se utiliza para crear gráficos y visualizaciones.
import numpy as np # se utiliza para operaciones numéricas, especialmente con matrices.
from collections import deque #es una cola de doble extremo que permite añadir y 
#eliminar elementos desde ambos extremos, útil para el algoritmo de búsqueda en amplitud (BFS).

# Definir tamaño de la cuadrícula
tamano_cuadricula = 6 #tamaño de la cuadrícula como 6x6.

#Inicializar la cuadrícula
cuadricula = np.zeros((tamano_cuadricula, tamano_cuadricula)) #crea una matriz de 6x6 llena de ceros. Cada cero representa una celda vacía en la cuadrícula.
# print(cuadricula)
def crear_cuadricula(cuadricula): 
    # Crear una visualización de la cuadrícula
    _, ax = plt.subplots() # crea una figura y un conjunto de ejes.
    ax.matshow(cuadricula, cmap='Greys') # muestra la matriz en una escala de grises.

    for i in range(tamano_cuadricula):
        for j in range(tamano_cuadricula): #Se recorre cada celda de la matriz.
            if cuadricula[i, j] == 2: #Dependiendo del valor de la celda (2, 3, 1 o 4), se dibuja un texto 'I' para inicio
                ax.text(j, i, 'I', va='center', ha='center', color='green')
            elif cuadricula[i, j] == 3:
                ax.text(j, i, 'F', va='center', ha='center', color='red')
            elif cuadricula[i, j] == 1:
                ax.text(j, i, 'O', va='center', ha='center', color='black')
            elif cuadricula[i, j] == 4:
                ax.text(j, i, 'R', va='center', ha='center', color='purple')
    
    plt.show() #Muestra la figura con la cuadrícula y los textos dibujados.

# Función para solicitar una coordenada del usuario
def solicitar_coordenada(mensaje):  
    while True: #Inicia un bucle while que se repetirá indefinidamente hasta que se rompa explícitamente con return
        try:#Inicia un bloque try por si ocurra alguna excepcion y en este caso para manejar entradas invalidas
            coord_input = input(mensaje)#muestra mensaje(pasado como argumento) y espera que el usuario ingrese un valor y se almacena coord
            x, y = map(int, coord_input.split(',')) #da como resultado una lista de dos cadenas (supuestamente) convierte esa cadena en enteros asignando a xy.
            if 0 <= x < tamano_cuadricula and 0 <= y < tamano_cuadricula: #Valida la entrada para asegurarse de que está dentro del rango permitido.
                return (x, y) #si ambas son validas rompe el bucle while y termina la funcion.
            else:
                print(f"Por favor, ingrese coordenadas válidas en el rango 0-{tamano_cuadricula - 1}.") #tiene que estar dentro del rango para ser valido
        except ValueError:
            print("Entrada inválida. Por favor, ingrese coordenadas en el formato x,y.") # debe ingresar con un formato valido

# Solicitar coordenadas de inicio y fin

inicio = solicitar_coordenada("Ingrese la posición de inicio (formato: x,y): ")
cuadricula[inicio] = 2  # Inicio marcado con 2

fin = solicitar_coordenada("Ingrese la posición de fin (formato: x,y): ")
cuadricula[fin] = 3    # Fin marcado con 3
crear_cuadricula(cuadricula)
# print(cuadricula)
# Solicitar coordenadas de obstáculos
obstaculos = [] #inilista vacia
while True: #inicia bucle while hasta que se rompa con el break
    obs_input = input("Ingrese la posición del obstáculo (formato: x,y) o 'fin' para terminar: ")#pos de obs en el formato o fin para terminar se almacena 
    if obs_input.lower() == 'fin':#comprueba si es fin ignorando la mayuscula y minuscula
        break#rompe y termina entrada de obs
    try: #inicia un bloque try para ver si hay excepciones que podrian ver. para manejar entradas invalidas
        obs_x, obs_y = map(int, obs_input.split(','))#divide por coma, resu:lista de 2 caden.mapint convierte en enteros asignado a obs xy
        if 0 <= obs_x < tamano_cuadricula and 0 <= obs_y < tamano_cuadricula: #verifica si esta dentro del rango valido
            obstaculos.append((obs_x, obs_y)) #si son validas añadetup a la listaobs
        else:
            print(f"Por favor, ingrese coordenadas válidas en el rango 0-{tamano_cuadricula - 1}.")
    except ValueError:
        print("Entrada inválida. Por favor, ingrese coordenadas en el formato x,y.")

# Marcar el inicio, fin y obstáculos
for x, y in obstaculos:# toma todas las coordenadas de obstáculos ingresado ymarca la cuadricula, asigna el valor 1 a las celdas que corresponde
    cuadricula[x, y] = 1  # Obstáculos marcados con 1

def es_movimiento_valido(x, y, cuadricula):
    # Verificar si un movimiento es válido (dentro de los límites y no es un obstáculo)
    return 0 <= x < tamano_cuadricula and 0 <= y < tamano_cuadricula and cuadricula[x, y] != 1

def encontrar_camino(cuadricula, inicio, fin):#tres parámetros:
    # Implementación de BFS para encontrar el camino más corto
    direcciones = [(0, 1), (1, 0), (0, -1), (-1, 0)]#representan los posibles movimientos en la cuadrícula: derecha, abajo, izquierda y arriba.
    cola = deque([[inicio]])#cola es una cola de doble extremo (deque) que se inicializa con una lista que contiene la coordenada de inicio.
    #Esta cola se usará para almacenar los caminos parciales que se están explorando.
    visitados = set()#es un conjunto q se utiliza para llevar un registro de las coordenadas que ya han sido visitadas.
    visitados.add(inicio)#La coordenada de inicio se agrega al conjunto visitados para indicar que ya ha sido visitos

    while cola:#Inicia un bucle while que continuará ejecutándose mientras cola no esté vacía.
        camino = cola.popleft()#toma el primer camino parcial de la cola y lo elimina de la misma. Este camino parcial es una lista de coordenadas.
        x, y = camino[-1]#x y y toman las coordenadas de la última celda en el camino parcial.

        if (x, y) == fin: #si las coordenas actuales son iguales
            return camino  # Si se llega al destino, retornar el camino

        for dx, dy in direcciones: #itera sobre todas las direcciones posibles de movimiento.
            nx, ny = x + dx, y + dy #son las nuevas coordenadas después de moverse en una dirección específica.
            if es_movimiento_valido(nx, ny, cuadricula) and (nx, ny) not in visitados:#Verifica si el movimiento a las nuevas coordenadas (nx, ny) es válido
#(dentro de los límites de la cuadrícula y no es un obstáculo) y si (nx, ny) no ha sido visitado aún.
                cola.append(camino + [(nx, ny)])
#Si el movimiento es válido y la celda no ha sido visitada, se añade una nueva lista a cola, que es el camino parcial actual más la nueva coordenada (nx, ny).
                visitados.add((nx, ny))#La nueva coordenada (nx, ny) se agrega al conjunto visitados.

    return []  # Si no hay camino, retornar una lista vacía
#Si se sale del bucle while sin haber encontrado el destino, la función retorna una lista vacía, indicando que no hay camino disponible.
def trazar_camino(cuadricula, camino):
    # Marcar el camino encontrado en la cuadrícula
    for x, y in camino:
        if cuadricula[x, y] == 0:
            cuadricula[x, y] = 4  # Camino marcado con 4

    crear_cuadricula(cuadricula)

# Crear la cuadrícula inicial
crear_cuadricula(cuadricula)

# Encontrar el camino y trazarlo
camino = encontrar_camino(cuadricula, inicio, fin)
if camino:
    trazar_camino(cuadricula, camino)
    print('Camino encontrado:', camino)
else:
    print('No se encontró un camino')
