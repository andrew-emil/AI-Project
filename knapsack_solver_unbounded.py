import random
from typing import Callable, List

Genome = List[float]
Population = List[Genome]
Fitness = Callable[[Genome], float]

class KnapsackUnbounded:
    def __init__(self, items, capacity):
        self.items = items  # List of tuples (weight, value)
        self.capacity = capacity
        self.genome_size = len(items)
        self.fitness_values = []

    def fitness(self, genome: list) -> float:
        total_weight = 0
        total_value = 0
        for i in range(self.genome_size):
            total_weight += genome[i] * self.items[i][0]
            total_value += genome[i] * self.items[i][1]
            
        if total_weight > self.capacity:
            return 0
        
        return total_value
    
    def generate_population(self, population_size: int) -> Population:
        population = []
        for _ in range(population_size):
            genome = [random.randint(0, self.capacity // self.items[i][0]) for i in range(self.genome_size)]
            population.append(genome)
        return population
    
    def crossover(self, parent1: Genome, parent2: Genome) -> list:
        crossover_point = random.randint(0, self.genome_size - 1)
        child = parent1[:crossover_point] + parent2[crossover_point:]
        return child
    
    def mutate(self, genome: Genome, mutation_rate: float) -> Genome:
        for i in range(self.genome_size):
            if random.random() < mutation_rate:
                # mutate the genes
                genome[i] = max(0, genome[i] + random.choice([-1, 1]))
        return genome
    
    def select_parent(self, population: Population, fitness_function: Fitness, tournament_size: int = 2) -> Genome:
        # Tournament selection: select the best genome from a random subset of the population
        tournament = random.sample(population, k=tournament_size)
        return max(tournament, key=fitness_function)

    def evolution(self, generations: int, population_size: int, mutation_rate: float) -> Genome:
        population = self.generate_population(population_size)
        
        for _ in range(generations):
            new_population = []
            elite = max(population, key=self.fitness)
            new_population.append(elite) 
            best_fitness = self.fitness(elite)
            self.fitness_values.append(best_fitness)
            for _ in range(population_size):
                parent1, parent2 = self.select_parent(population, self.fitness), self.select_parent(population, self.fitness)
                new_genome = self.crossover(parent1=parent1, parent2=parent2)
                new_genome = self.mutate(new_genome, mutation_rate)
                new_population.append(new_genome)
                
            population = new_population
            
        # Return the best solution from the final population
        best_genome = max(population, key=self.fitness)
        best_profit = self.fitness(best_genome)
        return [best_genome, best_profit, self.fitness_values]
