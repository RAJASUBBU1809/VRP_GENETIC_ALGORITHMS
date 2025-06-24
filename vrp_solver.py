"""
vrp_solver.py - Main VRP Genetic Algorithm solver components
"""
import random
import numpy as np
from deap import base, creator, tools, algorithms


class VRPSolver:
    """Vehicle Routing Problem solver using Genetic Algorithm with DEAP library."""

    def __init__(self, locations, depot, num_vehicles):
        """
        Initialize the VRP solver.

        Args:
            locations (list): List of (x, y) coordinate tuples for locations
            depot (tuple): Depot coordinates (x, y)
            num_vehicles (int): Number of vehicles
        """
        self.locations = locations
        self.depot = depot
        self.num_vehicles = num_vehicles
        self.num_locations = len(locations)
        self.toolbox = None
        self._setup_ga()

    def _setup_ga(self):
        """Setup the genetic algorithm components."""
        # Create fitness and individual classes
        if not hasattr(creator, "FitnessMin"):
            creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0))
        if not hasattr(creator, "Individual"):
            creator.create("Individual", list, fitness=creator.FitnessMin)

        # Setup toolbox
        self.toolbox = base.Toolbox()
        self.toolbox.register("indices", random.sample, range(self.num_locations), self.num_locations)
        self.toolbox.register("individual", tools.initIterate, creator.Individual, self.toolbox.indices)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        self.toolbox.register("evaluate", self._evaluate_vrp)
        self.toolbox.register("mate", tools.cxPartialyMatched)
        self.toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
        self.toolbox.register("select", tools.selTournament, tournsize=3)

    def _evaluate_vrp(self, individual):
        """
        Evaluate VRP solution fitness.

        Args:
            individual (list): Individual representing route order

        Returns:
            tuple: (total_distance, balance_penalty)
        """
        total_distance = 0
        distances = []

        for i in range(self.num_vehicles):
            vehicle_route = [self.depot] + [self.locations[individual[j]] 
                           for j in range(i, len(individual), self.num_vehicles)] + [self.depot]
            vehicle_distance = sum(np.linalg.norm(np.array(vehicle_route[k+1]) - np.array(vehicle_route[k]))
                                 for k in range(len(vehicle_route)-1))
            total_distance += vehicle_distance
            distances.append(vehicle_distance)

        balance_penalty = np.std(distances)
        return total_distance, balance_penalty

    def solve(self, pop_size=300, cxpb=0.7, mutpb=0.2, ngen=300, tournsize=3, seed=42, verbose=True):
        """
        Solve the VRP using genetic algorithm.

        Args:
            pop_size (int): Population size
            cxpb (float): Crossover probability
            mutpb (float): Mutation probability
            ngen (int): Number of generations
            tournsize (int): Tournament size for selection
            seed (int): Random seed
            verbose (bool): Whether to print statistics

        Returns:
            tuple: (best_individual, population, stats, hall_of_fame)
        """
        random.seed(seed)

        # Update tournament size
        self.toolbox.unregister("select")
        self.toolbox.register("select", tools.selTournament, tournsize=tournsize)

        # Create population and hall of fame
        pop = self.toolbox.population(n=pop_size)
        hof = tools.HallOfFame(1)

        # Statistics
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("min", np.min)
        stats.register("max", np.max)

        # Run the algorithm
        algorithms.eaSimple(pop, self.toolbox, cxpb, mutpb, ngen, 
                          stats=stats, halloffame=hof, verbose=verbose)

        return hof[0], pop, stats, hof

    def get_vehicle_routes(self, individual):
        """
        Get vehicle routes from individual representation.

        Args:
            individual (list): Individual representing route order

        Returns:
            list: List of routes for each vehicle
        """
        routes = []
        for i in range(self.num_vehicles):
            vehicle_route = [self.depot] + [self.locations[individual[j]] 
                           for j in range(i, len(individual), self.num_vehicles)] + [self.depot]
            routes.append(vehicle_route)
        return routes
