import random
import tkinter as tk
from tkinter import scrolledtext

# Definimos los objetos (unidades, valor)
items = [(2, 3), (3, 4), (4, 8), (5, 8), (9, 10)]

# Capacidad máxima de la mochila
max_weight = 15

def generate_population(size, num_items):
    return [[random.randint(0, 1) for _ in range(num_items)] for _ in range(size)]

def fitness_function(individual):
    total_weight = total_value = 0
    for i, item in enumerate(individual):
        if item == 1:
            total_weight += items[i][0]
            total_value += items[i][1]
    if total_weight > max_weight:
        return 0
    return total_value

def total_weight(individual):
    return sum(items[i][0] for i in range(len(individual)) if individual[i] == 1)

def tournament_selection(population, fitnesses, tournament_size):
    selected_parents = []
    for _ in range(len(population)):
        tournament = random.sample(list(zip(population, fitnesses)), tournament_size)
        winner = max(tournament, key=lambda x: x[1])
        selected_parents.append(winner[0])
    return selected_parents

def uniform_crossover(parents, num_offspring):
    offspring = []
    for _ in range(num_offspring):
        parent1 = random.choice(parents)
        parent2 = random.choice(parents)
        child = [parent1[i] if random.random() > 0.5 else parent2[i] for i in range(len(parent1))]
        offspring.append(child)
    return offspring

def mutate(offspring, mutation_rate):
    for i in range(len(offspring)):
        for j in range(len(offspring[i])):
            if random.random() < mutation_rate:
                offspring[i][j] = 1 if offspring[i][j] == 0 else 0
    return offspring

def genetic_algorithm(population_size, generations, mutation_rate, tournament_size, output_widget):
    population = generate_population(population_size, len(items))
    output_widget.insert(tk.END, "Resultados del Algoritmo Genético:\n")

    for generation in range(generations):
        fitnesses = [fitness_function(individual) for individual in population]
        parents = tournament_selection(population, fitnesses, tournament_size)
        best_individual = max(population, key=fitness_function)

        # Elitismo: guarda el mejor individuo
        new_population = [best_individual]
        
        offspring = uniform_crossover(parents, population_size - 1)  # -1 porque ya añadimos el mejor
        offspring = mutate(offspring, mutation_rate)
        
        new_population.extend(offspring)
        population = new_population

        output_widget.insert(tk.END, f"Generacion {generation}: Mejor solucion = {best_individual}, Valor = {fitness_function(best_individual)}\n")

    best_solution = max(population, key=fitness_function)
    best_value = fitness_function(best_solution)
    best_weight = total_weight(best_solution)

    # Mostrar el resultado final con explicación
    output_widget.insert(tk.END, f"\nMejor combinacion encontrada: {best_solution}, con valor total: {best_value}\n")
    output_widget.insert(tk.END, f"Peso total de la combinacion: {best_weight} unidades.\n\n")
    output_widget.insert(tk.END, "Explicación del cálculo del valor:\n")
    output_widget.insert(tk.END, "Cada elemento de la solución representa si se incluye (1) o no (0) en la mochila.\n")
    output_widget.insert(tk.END, "El valor se calcula como la suma de los valores de los artículos seleccionados:\n")

    # Detalle del cálculo
    for i in range(len(best_solution)):
        if best_solution[i] == 1:
            output_widget.insert(tk.END, f" - Artículo {i + 1}: Unidades = {items[i][0]}, Peso = {items[i][1]}\n")

    output_widget.insert(tk.END, f"Valor total: {best_value} (que es la suma de los pesos de los artículos seleccionados).\n")
    output_widget.insert(tk.END, f"Importante: Las unidades totales ({best_weight}) no excede la capacidad máxima de la mochila ({max_weight}).\n")

def main():
    # Parámetros del algoritmo genético
    population_size = 20
    generations = 5
    mutation_rate = 0.1
    tournament_size = 3

    root = tk.Tk()
    root.title("Resultados del Algoritmo Genético")

    output_widget = scrolledtext.ScrolledText(root, width=80, height=20)
    output_widget.pack()

    run_button = tk.Button(root, text="Ejecutar Algoritmo Genético", command=lambda: genetic_algorithm(population_size, generations, mutation_rate, tournament_size, output_widget))
    run_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
