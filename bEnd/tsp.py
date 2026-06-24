
# data ready for processing

import random
import numpy as np

best_route = list()
best_distance = None

POP_SIZE = 300
MUT_RATE = 0.025
CROSS_RATE = 0.9
GENS = 1000
ELITISM = 9

#Creating the initial population based on the population size and number of cities
def create_initial_pop(n_cities, POP_SIZE=300):
    population = list()
    init_route = list(range(n_cities))
    for _ in range(POP_SIZE):
        chromosome = init_route[:]
        random.shuffle(chromosome)
        population.append(chromosome)

    return population

#Computing the total distance of a route
def route_distance(route, dist_mtx):
    total = float()
    for i in range(len(route)):
        origin = route[i]
        destination = route[(i+1) % len(route)]
        total += dist_mtx[origin][destination]
    
    return total

# Order crossover
def order_crossover(parent1, parent2):
    size = len(parent1)
    
    # Pick two random cut points
    start, end = sorted(random.sample(range(size), 2))
    
    # Take the segment from parent1
    child = [None] * size
    child[start:end+1] = parent1[start:end+1]
    
    # Fill remaining positions with parent2's order, skipping duplicates
    p2_filtered = [city for city in parent2 if city not in child]
    
    pos = 0
    for i in range(size):
        if child[i] is None:
            child[i] = p2_filtered[pos]
            pos += 1
    
    return child

#Inversion mutation 
def inv_mutate(route):
    size = len(route)
    
    # Pick two random cut points
    start, end = sorted(random.sample(range(size), 2))
    
    # Reverse the segment between them
    route[start:end+1] = route[start:end+1][::-1]
    
    return route

#Applying 2-opt local search for improvement
#2-opt variables
NO_IMPROVE_LIMIT = 50   # generations without improvement before acting
MUTATION_BOOST   = 0.15  # boosted mutation rate when stagnant
RESTART_LIMIT    = 100  # generations without improvement before restart

no_improve_count = 0
best_ever_distance = float("inf")
best_ever_route = None

def two_opt(route, dist_matrix):
    global MUT_RATE, no_improve_count, best_ever_distance, best_ever_route, best_route, best_distance
    best = route
    best_distance = route_distance(route, dist_matrix)
    improved = True

    while improved:
        improved = False
        for i in range(1, len(route) - 1):
            for j in range(i + 1, len(route)):
                # Reverse the segment between i and j
                new_route = best[:i] + best[i:j+1][::-1] + best[j+1:]
                new_distance = route_distance(new_route, dist_matrix)

                if new_distance < best_distance:
                    best = new_route
                    best_distance = new_distance
                    improved = True  # Keep looping until no improvement

    return best

#Computing the fitness of each route
def fitness(solution, dist_mtx):
    return 1 / route_distance(solution, dist_mtx)

#Apply tournament selection to choose parents for crossover later on
def tournament_selection(population, fitnesses, k=5):
    samples = random.sample(range(len(population)), k)
    best = max(samples, key= lambda i:fitnesses[i])
    return population[best]

def tsp_for(cities, distance_matrix):
    num_cities = len(cities)
    population = create_initial_pop(num_cities, POP_SIZE)
    #MAIN
    for gen in range(1000):
        fitnesses = [fitness(chromosome, distance_matrix) for chromosome in population]
        new_population = []

        #Preserving the elites
        elites = sorted(population, key= lambda r:route_distance(r, distance_matrix))[:ELITISM]
        new_population.extend(elites)

        while len(new_population) < POP_SIZE:
            #Choosing random parents using tournament for crossover
            parent1 = tournament_selection(population, fitnesses)
            parent2 = tournament_selection(population, fitnesses)

            #Cross-over
            if random.random() < CROSS_RATE:
                child = order_crossover(parent1, parent2)
            else:
                child = parent1[:]

            #Mutation
            if random.random() < MUT_RATE:
                child = inv_mutate(child)

            new_population.append(child)
                
        #2-opt local search
        best_idx = min(range(len(population)), key=lambda i: route_distance(population[i], distance_matrix))
        population[best_idx] = two_opt(population[best_idx], distance_matrix)

        #Convergence check
        current_best_distance = min(route_distance(r, distance_matrix) for r in population)
        current_best_route    = min(population, key=lambda r: route_distance(r, distance_matrix))

        if current_best_distance < best_ever_distance:
            best_ever_distance = current_best_distance
            best_ever_route    = current_best_route
            no_improve_count   = 0  # Reset counter on improvement
        else:
            no_improve_count += 1

        # Adaptive mutation boost in case the child is stagnant
        if no_improve_count >= NO_IMPROVE_LIMIT:
            MUT_RATE = MUTATION_BOOST
        else:
            MUT_RATE = 0.025

        # Restart: reinject random individuals if deeply stagnant
        if no_improve_count >= RESTART_LIMIT:
            # Keep elites, replace the rest with fresh random routes
            elites = sorted(population, key=lambda r: route_distance(r, distance_matrix))[:ELITISM]
            population = elites + [random.sample(cities, len(cities)) for _ in range(POP_SIZE - ELITISM)]
            no_improve_count = 0
        
        population = new_population

    best_route = min(population, key= lambda r:route_distance(r, distance_matrix))
    best_distance = route_distance(best_route, distance_matrix)

    return {best_route, best_distance}





