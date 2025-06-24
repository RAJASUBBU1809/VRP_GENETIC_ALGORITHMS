"""
config.py - Configuration settings for VRP project
"""

# Default VRP problem settings
DEFAULT_VRP_CONFIG = {
    "num_locations": 20,
    "num_vehicles": 3,
    "depot": (550, 470),
    "location_range_x": (0, 1000),
    "location_range_y": (0, 1000),
    "seed": 42
}

# Default GA parameters
DEFAULT_GA_CONFIG = {
    "pop_size": 300,
    "cxpb": 0.7,
    "mutpb": 0.2,
    "ngen": 300,
    "tournsize": 3,
    "seed": 42
}

# Parameter tuning ranges
TUNING_RANGES = {
    "pop_size": (200, 800),
    "cxpb": (0.5, 0.9),
    "mutpb": (0.05, 0.25),
    "tournsize": (2, 4)
}

# Grid search parameters (smaller for faster execution)
GRID_SEARCH_PARAMS = {
    'pop_size': [200, 400, 600],
    'cxpb': [0.6, 0.8],
    'mutpb': [0.1, 0.2],
    'tournsize': [2, 3, 4]
}

# Plotting configuration
PLOT_CONFIG = {
    "colors": ['red', 'green', 'blue', 'orange', 'purple', 'brown', 'pink', 'gray', 'cyan', 'magenta'],
    "depot_color": 'black',
    "depot_size": 15,
    "location_color": 'lightblue',
    "location_size": 8,
    "line_width": 3,
    "figure_width": 800,
    "figure_height": 600
}

# File paths
RESULTS_DIR = "results"
PLOTS_DIR = "plots"
DATA_DIR = "data"
