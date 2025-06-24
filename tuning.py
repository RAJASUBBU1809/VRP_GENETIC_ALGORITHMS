"""
tuning.py - Parameter tuning functionality for VRP GA
"""
import random
from vrp_solver import VRPSolver


class VRPTuner:
    """Parameter tuner for VRP genetic algorithm."""

    def __init__(self, locations, depot, num_vehicles):
        """
        Initialize the VRP tuner.

        Args:
            locations (list): List of (x, y) coordinate tuples for locations
            depot (tuple): Depot coordinates (x, y)
            num_vehicles (int): Number of vehicles
        """
        self.locations = locations
        self.depot = depot
        self.num_vehicles = num_vehicles
        self.solver = VRPSolver(locations, depot, num_vehicles)

    def random_search_tuning(self, n_trials=25, param_ranges=None, ngen=20, seed_base=0):
        """
        Perform random search parameter tuning.

        Args:
            n_trials (int): Number of parameter combinations to try
            param_ranges (dict): Parameter ranges to search
            ngen (int): Number of generations for each trial
            seed_base (int): Base seed for reproducibility

        Returns:
            tuple: (best_params, best_individual, best_distance, all_results)
        """
        if param_ranges is None:
            param_ranges = {
                "pop_size": (200, 800),
                "cxpb": (0.5, 0.9),
                "mutpb": (0.05, 0.25),
                "tournsize": (2, 4)
            }

        best_params = None
        best_individual = None
        best_distance = float("inf")
        all_results = []

        print(f"Starting parameter tuning with {n_trials} trials...")

        for trial in range(n_trials):
            # Sample parameters
            pop_size = random.randint(*param_ranges["pop_size"])
            cxpb = random.uniform(*param_ranges["cxpb"])
            mutpb = random.uniform(*param_ranges["mutpb"])
            tournsize = random.randint(*param_ranges["tournsize"])

            # Run GA with these parameters
            individual, _, _, _ = self.solver.solve(
                pop_size=pop_size,
                cxpb=cxpb,
                mutpb=mutpb,
                ngen=ngen,
                tournsize=tournsize,
                seed=seed_base + trial,
                verbose=False
            )

            distance = individual.fitness.values[0]

            # Record results
            result = {
                'trial': trial + 1,
                'pop_size': pop_size,
                'cxpb': cxpb,
                'mutpb': mutpb,
                'tournsize': tournsize,
                'distance': distance,
                'individual': individual
            }
            all_results.append(result)

            # Update best if this is better
            if distance < best_distance:
                best_distance = distance
                best_individual = individual
                best_params = {
                    'pop_size': pop_size,
                    'cxpb': cxpb,
                    'mutpb': mutpb,
                    'tournsize': tournsize
                }

            print(f"Trial {trial + 1}/{n_trials}: Distance = {distance:.1f}")

        print(f"\nBest distance: {best_distance:.1f}")
        print(f"Best parameters: {best_params}")

        return best_params, best_individual, best_distance, all_results

    def grid_search_tuning(self, param_grid, ngen=20, seed_base=0):
        """
        Perform grid search parameter tuning.

        Args:
            param_grid (dict): Dictionary with parameter lists to try
            ngen (int): Number of generations for each trial
            seed_base (int): Base seed for reproducibility

        Returns:
            tuple: (best_params, best_individual, best_distance, all_results)
        """
        import itertools

        # Generate all combinations
        param_names = list(param_grid.keys())
        param_values = list(param_grid.values())
        combinations = list(itertools.product(*param_values))

        best_params = None
        best_individual = None
        best_distance = float("inf")
        all_results = []

        print(f"Starting grid search with {len(combinations)} combinations...")

        for i, combo in enumerate(combinations):
            params = dict(zip(param_names, combo))

            # Run GA with these parameters
            individual, _, _, _ = self.solver.solve(
                pop_size=params['pop_size'],
                cxpb=params['cxpb'],
                mutpb=params['mutpb'],
                ngen=ngen,
                tournsize=params['tournsize'],
                seed=seed_base + i,
                verbose=False
            )

            distance = individual.fitness.values[0]

            # Record results
            result = {
                'trial': i + 1,
                **params,
                'distance': distance,
                'individual': individual
            }
            all_results.append(result)

            # Update best if this is better
            if distance < best_distance:
                best_distance = distance
                best_individual = individual
                best_params = params.copy()

            print(f"Trial {i + 1}/{len(combinations)}: Distance = {distance:.1f}")

        print(f"\nBest distance: {best_distance:.1f}")
        print(f"Best parameters: {best_params}")

        return best_params, best_individual, best_distance, all_results


def compare_tuning_methods(locations, depot, num_vehicles, n_trials=25):
    """
    Compare different tuning methods.

    Args:
        locations (list): List of locations
        depot (tuple): Depot coordinates
        num_vehicles (int): Number of vehicles
        n_trials (int): Number of trials for random search

    Returns:
        dict: Comparison results
    """
    tuner = VRPTuner(locations, depot, num_vehicles)

    # Random search
    print("=== Random Search Tuning ===")
    rs_params, rs_individual, rs_distance, rs_results = tuner.random_search_tuning(n_trials=n_trials)

    # Grid search (smaller grid for comparison)
    print("\n=== Grid Search Tuning ===")
    param_grid = {
        'pop_size': [200, 400, 600],
        'cxpb': [0.6, 0.8],
        'mutpb': [0.1, 0.2],
        'tournsize': [2, 3, 4]
    }
    gs_params, gs_individual, gs_distance, gs_results = tuner.grid_search_tuning(param_grid)

    return {
        'random_search': {
            'params': rs_params,
            'distance': rs_distance,
            'individual': rs_individual,
            'results': rs_results
        },
        'grid_search': {
            'params': gs_params,
            'distance': gs_distance,
            'individual': gs_individual,
            'results': gs_results
        }
    }
