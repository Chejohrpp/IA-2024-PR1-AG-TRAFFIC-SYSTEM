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

    def training(self):
        print('training')
        self._traffic_model.define_node() #requires
        populations = self.create_population()
        #While or threads for the cants of generations
        while True:
            self.evaluate_aptitude(populations)
            break      
        # self._traffic_model.repaint_items() #repinta el escenario
        # self.selection()
        # self.crossover()
        # self.mutation()
        # self.sustitution()

    def evaluate_aptitude(self, population):
        blokes = []
        for bloke in population:
            self.fitness(bloke)

    def fitness(self, bloke):
        cant_cars_out = self._traffic_model.cant_cars_out(bloke)
        print(f"cant cars for {bloke} is --> {cant_cars_out}")
        

    def _repaint_thread(self):
        while True:
            repaint_request = self._repaint_queue.get()
            if repaint_request == 'repaint':
                self._traffic_model.repaint_items()
                self._repaint_event.set()  # Signal repaint completion
        

    def create_population(self):
        #cant of new population
        # new_population = []
        paths = self._traffic_model.get_number_paths() # array of dictionaries
        return self.generate_random_population(paths)
    
    def generate_random_population(self,paths):
        return [self.generate_random_single_population(paths) for _ in range(self._start_number_population)]
    
    def generate_random_single_population(self, paths):
        bloke = []
        for path in paths:
            random_value = self.generate_static_path(path['percent_min'], path['percent_max']) 
            bloke.append((path['key'], random_value))
        return bloke

    def generate_random_path(self,minimun_percent,maximun_percent):
        return random.randint(minimun_percent, maximun_percent)
    
    def generate_static_path(self,minimun_percent,maximun_percent):
        return 50
        
        


