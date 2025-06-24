# Vehicle Routing Problem (VRP) Genetic Algorithm

A modular implementation of the Vehicle Routing Problem solver using Genetic Algorithms with the DEAP library. This project includes parameter tuning capabilities and comprehensive visualization tools.

## 🚀 Features

- **Modular Design**: Well-organized code structure with separate modules for different functionalities
- **Genetic Algorithm Implementation**: Uses DEAP library for efficient GA operations
- **Parameter Tuning**: Automated hyperparameter optimization with random search and grid search
- **Rich Visualizations**: Interactive plots using Plotly for route visualization and analysis
- **Comprehensive Dashboard**: All-in-one view of results and statistics
- **Jupyter Notebook Interface**: Easy-to-use notebook for running experiments

## 📁 Project Structure

```
vrp-genetic-algorithm/
├── main.ipynb              # Main Jupyter notebook to run experiments
├── locations.py           # Location generation and management
├── vrp_solver.py          # Core VRP genetic algorithm solver
├── tuning.py              # Parameter tuning functionality
├── plotting.py            # Visualization functions
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── README.md              # This file
└── .gitignore            # Git ignore rules
```

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/vrp-genetic-algorithm.git
cd vrp-genetic-algorithm
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Launch Jupyter notebook:
```bash
jupyter notebook main.ipynb
```

## 📋 Requirements

- Python 3.7+
- numpy >= 1.21.0
- deap >= 1.3.1
- plotly >= 5.0.0
- pandas >= 1.3.0
- jupyter >= 1.0.0
- matplotlib >= 3.5.0
- scipy >= 1.7.0

## 🚦 Quick Start

### Basic Usage

```python
from locations import generate_random_locations, create_depot
from vrp_solver import VRPSolver
from plotting import plot_vrp_routes

# Generate problem instance
locations = generate_random_locations(num_locations=20, seed=42)
depot = create_depot(550, 470)

# Solve VRP
solver = VRPSolver(locations, depot, num_vehicles=3)
best_individual, _, _, _ = solver.solve(pop_size=300, ngen=100)

# Visualize results
fig = plot_vrp_routes(locations, depot, best_individual, 3)
fig.show()
```

### Parameter Tuning

```python
from tuning import VRPTuner

# Initialize tuner
tuner = VRPTuner(locations, depot, num_vehicles=3)

# Perform random search
best_params, best_individual, best_distance, results = tuner.random_search_tuning(
    n_trials=25, ngen=20
)

print(f"Best distance: {best_distance:.1f}")
print(f"Best parameters: {best_params}")
```

## 📊 Features Overview

### VRP Solver (`vrp_solver.py`)
- Genetic algorithm implementation using DEAP
- Multi-objective optimization (distance + balance)
- Configurable GA parameters
- Route extraction and analysis

### Parameter Tuning (`tuning.py`)
- Random search optimization
- Grid search optimization
- Automated parameter space exploration
- Performance comparison tools

### Visualization (`plotting.py`)
- Interactive route visualization
- Parameter correlation analysis
- Convergence plotting
- Comprehensive dashboards

### Configuration (`config.py`)
- Centralized configuration management
- Default parameter settings
- Tuning ranges and grid definitions

## 🔧 Configuration

Modify `config.py` to customize:

- Problem parameters (locations, vehicles, depot)
- GA parameters (population size, crossover/mutation rates)
- Tuning ranges
- Visualization settings

## 📈 Example Results

The genetic algorithm typically finds solutions with:
- **Distance Optimization**: Minimizes total travel distance
- **Load Balancing**: Equalizes work among vehicles
- **Parameter Sensitivity**: Automatic identification of best GA settings

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [DEAP Library](https://deap.readthedocs.io/) for genetic algorithm framework
- [Plotly](https://plotly.com/) for interactive visualizations
- Vehicle Routing Problem research community

## 📚 References

- Genetic Algorithms for Vehicle Routing Problems
- DEAP Documentation and Examples
- Multi-objective Optimization in Transportation

---

**Note**: This implementation is designed for educational and research purposes. For production use, consider additional optimizations and constraints specific to your use case.
