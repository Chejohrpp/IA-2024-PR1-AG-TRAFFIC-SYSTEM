from enum import Enum
import random
import queue
import threading

import time


from genetic_algorithm.entities.model_constructor import ModelConstructor

class typesCriteriaFinalization(Enum):
    NUMBER_GENERATION = 1
    PERCENT_EFFECTIVE = 2

class GeneticAlgorithm:
    def __init__(self, size_population: int, 
                 mutation_rate_x, mutation_rate_y, 
                 type_criteria_finalization, traffic_model: ModelConstructor):
        self._start_number_population = size_population
        self._mutation_x = mutation_rate_x
        self._mutation_y = mutation_rate_y
        self._type_finalization = type_criteria_finalization
        self._traffic_model: ModelConstructor = traffic_model
        self._number_generation = 10
        self._percent_Efficient = 0

    def set_number_generation(self, number_generation):
        self._number_generation = number_generation
    
    def set_percent_efficient(self, percent_efficient):
        self._percent_efficient = percent_efficient

    def training(self):
        print('training')
        self._traffic_model.define_node() #requires
        populations = self.create_population()
        #While or threads for the cants of generations
        # while True:
        #     fitnesses = self.evaluate_aptitude(populations)
            # break
        current_Y_gen = 0
        if self._type_finalization is typesCriteriaFinalization.NUMBER_GENERATION:
            for generation in range(self._number_generation):
                current_Y_gen += 1
                fitness_values = [self.fitness(bloke) for bloke in populations]
                new_population = []
                for _ in range(self._start_number_population // 2):
                    parent1 = self.pick_parent(populations, fitness_values)
                    parent2 = self.pick_parent(populations, fitness_values)
                    # print("Parent", parent1, parent2)
                    child_1, child_2 = self.crossover(parent1, parent2)
                    # print("Child", child_1, child_2)
                    if current_Y_gen == self._mutation_y:
                        new_population.extend([self.mutate(child_1), self.mutate(child_2)])
                    else:
                        new_population.extend([child_1, child_2])

                if current_Y_gen == self._mutation_y:
                    current_Y_gen = 0
                # print("Newpopulation", new_population)
                populations = new_population
                fitness_values = [self.fitness(bloke) for bloke in populations]
                best_fitness_val = max(fitness_values)
                print(f"generation {generation} best fitness is {best_fitness_val}")

            best_index =  fitness_values.index(max(fitness_values))
            best_solution = populations[best_index]

            print(f"the best solution is  {best_solution}")
            print(f"the best fitness is {self.fitness(best_solution)}")
            self._traffic_model.update_paths(best_solution)

        # self._traffic_model.repaint_items() #repinta el escenario

    def evaluate_aptitude(self, population):
        fitnesses = []
        for bloke in population:
            fitnesses.append(self.fitness(bloke))
        return fitnesses

    def fitness(self, bloke):
        cant_cars_out = self._traffic_model.cant_cars_out(bloke)
        # print(f"cant cars for {bloke} is --> {cant_cars_out}")
        return cant_cars_out
    
    def pick_parent(self, populaton, fitness_values):
        total_fitnes = sum(fitness_values)
        pick = random.uniform(0, total_fitnes)
        current = 0
        for bloke, fitness_val in zip(populaton, fitness_values):
            current += fitness_val
            if current >= pick:
                return bloke
            
    def crossover(self,parent1,parent2):
        # print(parent1)
        crossover_point =  random.randint(0, len(parent1) -1 )
        # print('crossover point', crossover_point)
        cros_parent1 = parent1[:crossover_point] + parent2[crossover_point:]
        cros_parent2 = parent2[:crossover_point] + parent1[crossover_point:]

        # print('cros_parent1', cros_parent1 )

        normalize_cros_pa1 =  self._traffic_model.validate_percentages(cros_parent1)
        normalize_cros_pa2 =  self._traffic_model.validate_percentages(cros_parent2)

        # print('normalize_cros_pa1', normalize_cros_pa1 )

        return normalize_cros_pa1, normalize_cros_pa2

    def mutate(self,bloke):
        mutation_frequency = self._mutation_x / self._start_number_population
        mutation_probability = random.random()

        if mutation_probability <= mutation_frequency:
            random_index = random.randint(0, len(bloke) - 1)
            item, random_value = bloke[random_index]
            new_random_value = random.randint(item.min_percent, item.max_percent)
            bloke[random_index] = (item, new_random_value)

        return self._traffic_model.validate_percentages(bloke)



    def _repaint_thread(self):
        while True:
            repaint_request = self._repaint_queue.get()
            if repaint_request == 'repaint':
                self._traffic_model.repaint_items()
                self._repaint_event.set()  # Signal repaint completion
        

    def create_population(self):
        #cant of new population
        paths = self._traffic_model.get_number_paths() # array of dictionaries
        population =  self.generate_random_population(paths)
        normalized_population = []
        for bloke in population:
            normalized_population.append(self._traffic_model.validate_percentages(bloke)) #remove the maximum percentage, could be worked
        return normalized_population

    
    def generate_random_population(self,paths):
        return [self.generate_random_single_population(paths) for _ in range(self._start_number_population)]
    
    def generate_random_single_population(self, paths):
        bloke = []
        for path in paths:
            random_value = self.generate_random_path(path['percent_min'], path['percent_max']) 
            bloke.append((path['key'], random_value))
        return bloke

    def generate_random_path(self,minimun_percent,maximun_percent):
        return random.randint(minimun_percent, maximun_percent)
    
    def generate_static_path(self,minimun_percent,maximun_percent):
        return 50
        
        


