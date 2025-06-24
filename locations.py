"""
locations.py - Module for generating and managing VRP locations
"""
import random


def generate_random_locations(num_locations, x_range=(0, 1000), y_range=(0, 1000), seed=None):
    """
    Generate random locations for the VRP problem.

    Args:
        num_locations (int): Number of locations to generate
        x_range (tuple): Range for x coordinates (min, max)
        y_range (tuple): Range for y coordinates (min, max)
        seed (int, optional): Random seed for reproducibility

    Returns:
        list: List of (x, y) coordinate tuples
    """
    if seed is not None:
        random.seed(seed)

    locations = [(random.randint(x_range[0], x_range[1]), 
                  random.randint(y_range[0], y_range[1])) 
                 for _ in range(num_locations)]
    return locations


def create_depot(x=550, y=470):
    """
    Create depot location.

    Args:
        x (int): X coordinate of depot
        y (int): Y coordinate of depot

    Returns:
        tuple: Depot coordinates (x, y)
    """
    return (x, y)
