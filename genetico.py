
import random
import numpy as np
import tkinter as tk
from tkinter import messagebox

# Definir una matriz de distancias fijas entre las ciudades
def generar_matriz_distancias():
    return np.array([
        [0, 19, 27, 26, 25],
        [10, 0, 35, 28, 30],
        [18, 89, 0, 34, 20],
        [20, 25, 60, 0, 45],
        [29, 8, 20, 11, 0]
    ])

def calcular_distancia_total(recorrido, distancias):
    total = sum(distancias[recorrido[i], recorrido[i + 1]] for i in range(len(recorrido) - 1))
    total += distancias[recorrido[-1], recorrido[0]]  # Regreso a la ciudad inicial
    return total


# total = sum(...): Usa una comprensión de lista para sumar las distancias entre las ciudades en el recorrido. Itera sobre los índices de las ciudades, sumando la distancia entre la ciudad i y la ciudad i + 1.

# total += ...: Agrega la distancia de regreso a la ciudad inicial para cerrar el recorrido.


def crear_poblacion(num_ciudades, tamano_poblacion):
    return [random.sample(range(num_ciudades), num_ciudades) for _ in range(tamano_poblacion)]

def seleccionar_mejores(poblacion, distancias, num_seleccionados):
    aptitudes = [(individuo, calcular_distancia_total(individuo, distancias)) for individuo in poblacion]
    aptitudes.sort(key=lambda x: x[1])  # Ordenar por distancia
    return [ind[0] for ind in aptitudes[:num_seleccionados]]  # Seleccionar los mejores

def crossover(padre1, padre2):
    punto = random.randint(1, len(padre1) - 2)  # Un punto de cruce aleatorio
    hijo1 = padre1[:punto] + [ciudad for ciudad in padre2 if ciudad not in padre1[:punto]]
    hijo2 = padre2[:punto] + [ciudad for ciudad in padre1 if ciudad not in padre2[:punto]]
    return hijo1, hijo2

def mutar(individuo):
    if random.random() < 0.2:  # 10% de probabilidad de mutación
        i, j = random.sample(range(len(individuo)), 2)
        individuo[i], individuo[j] = individuo[j], individuo[i]
    return individuo

def algoritmo_genetico_tsp(num_ciudades, tamano_poblacion, generaciones):
    distancias = generar_matriz_distancias()
    poblacion = crear_poblacion(num_ciudades, tamano_poblacion)

    for _ in range(generaciones):
        mejores = seleccionar_mejores(poblacion, distancias, tamano_poblacion // 2)
        nueva_poblacion = mejores.copy()
        
        while len(nueva_poblacion) < tamano_poblacion:
            padre1, padre2 = random.sample(mejores, 2)  # Seleccionar dos padres
            hijo1, hijo2 = crossover(padre1, padre2)  # Cruce
            nueva_poblacion.append(mutar(hijo1))  # Mutación
            nueva_poblacion.append(mutar(hijo2))  # Mutación
        
        poblacion = nueva_poblacion

    mejor_solucion = seleccionar_mejores(poblacion, distancias, 1)[0]
    mejor_distancia = calcular_distancia_total(mejor_solucion, distancias)

    return mejor_solucion, mejor_distancia

def mostrar_resultados():
    # Parámetros del problema 
    num_ciudades = 5
    tamano_poblacion = 5
    generaciones = 5

    mejor_solucion, mejor_distancia = algoritmo_genetico_tsp(num_ciudades, tamano_poblacion, generaciones)

    mejor_recorrido = mejor_solucion + [mejor_solucion[0]]  # Añadimos la ciudad inicial al final
    
    # Crear un mensaje que muestre las distancias entre las ciudades en el recorrido
    recorrido_detallado = []
    distancias = generar_matriz_distancias()  # Reobtenemos la matriz de distancias
    for i in range(len(mejor_recorrido) - 1):
        ciudad_origen = mejor_recorrido[i]
        ciudad_destino = mejor_recorrido[i + 1]
        distancia = distancias[ciudad_origen, ciudad_destino]
        recorrido_detallado.append(f"{ciudad_origen} -> {ciudad_destino}: {distancia} km")
    
    # Unir todos los detalles del recorrido en un solo mensaje
    mensaje_detallado = "\n".join(recorrido_detallado)
    mensaje = f"Mejor recorrido: {mejor_recorrido}\nDistancia total: {mejor_distancia} km\n\nDetalles del recorrido:\n{mensaje_detallado}"

    messagebox.showinfo("Resultado del Problema del Viajante", mensaje)


# Interfaz gráfica con Tkinter
def interfaz_grafica():
    ventana = tk.Tk()
    ventana.title("Algoritmo Genético - Problema del Viajante")
    ventana.geometry("400x200")

    etiqueta = tk.Label(ventana, text="Encontrar el camino más corto para\n recorrer un conjunto de ciudades.", font=("Helvetica", 12))
    etiqueta.pack(pady=20)

    boton = tk.Button(ventana, text="Buscar", command=mostrar_resultados)
    boton.pack(pady=20)

    ventana.mainloop()

# Ejecutar la interfaz gráfica
if __name__ == "__main__":
    interfaz_grafica()
