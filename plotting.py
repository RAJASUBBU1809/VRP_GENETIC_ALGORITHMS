"""
plotting.py - Visualization functions for VRP solutions
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np


def plot_vrp_routes(locations, depot, individual, num_vehicles, title="VRP Routes"):
    """
    Plot VRP routes using Plotly.

    Args:
        locations (list): List of location coordinates
        depot (tuple): Depot coordinates
        individual (list): Individual representing route order
        num_vehicles (int): Number of vehicles
        title (str): Plot title

    Returns:
        plotly.graph_objects.Figure: Plotly figure
    """
    colors = ['red', 'green', 'blue', 'orange', 'purple', 'brown', 'pink', 'gray', 'cyan', 'magenta']
    fig = go.Figure()

    # Add depot marker
    fig.add_trace(go.Scatter(
        x=[depot[0]], y=[depot[1]],
        mode='markers',
        marker=dict(color='black', size=15, symbol='square'),
        name='Depot'
    ))

    # Add location markers
    x_locs, y_locs = zip(*locations)
    fig.add_trace(go.Scatter(
        x=x_locs, y=y_locs,
        mode='markers',
        marker=dict(color='lightblue', size=8),
        name='Customers'
    ))

    # Add vehicle routes
    for i in range(num_vehicles):
        vehicle_route = [depot] + [locations[individual[j]] 
                        for j in range(i, len(individual), num_vehicles)] + [depot]
        x_route, y_route = zip(*vehicle_route)

        fig.add_trace(go.Scatter(
            x=x_route, y=y_route,
            mode='lines+markers',
            line=dict(color=colors[i % len(colors)], width=3),
            marker=dict(size=10),
            name=f'Vehicle {i+1}'
        ))

    fig.update_layout(
        title=title,
        xaxis_title='X Coordinate',
        yaxis_title='Y Coordinate',
        legend_title_text='Routes',
        width=800, 
        height=600,
        showlegend=True
    )

    return fig


def plot_tuning_results(results, metric='distance'):
    """
    Plot parameter tuning results.

    Args:
        results (list): List of tuning results
        metric (str): Metric to plot ('distance' or other fitness component)

    Returns:
        plotly.graph_objects.Figure: Plotly figure
    """
    df = pd.DataFrame(results)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['trial'],
        y=df[metric],
        mode='lines+markers',
        name=f'{metric.capitalize()}',
        line=dict(width=2),
        marker=dict(size=6)
    ))

    # Add best result line
    best_value = df[metric].min()
    fig.add_hline(
        y=best_value, 
        line_dash="dash", 
        line_color="red",
        annotation_text=f"Best: {best_value:.1f}"
    )

    fig.update_layout(
        title=f'Parameter Tuning Results - {metric.capitalize()}',
        xaxis_title='Trial',
        yaxis_title=metric.capitalize(),
        width=900,
        height=500
    )

    return fig


def plot_parameter_correlation(results):
    """
    Plot correlation between parameters and performance.

    Args:
        results (list): List of tuning results

    Returns:
        plotly.graph_objects.Figure: Plotly figure with subplots
    """
    from plotly.subplots import make_subplots

    df = pd.DataFrame(results)
    params = ['pop_size', 'cxpb', 'mutpb', 'tournsize']

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=[f'{param} vs Distance' for param in params]
    )

    colors = ['blue', 'red', 'green', 'orange']

    for i, param in enumerate(params):
        row = (i // 2) + 1
        col = (i % 2) + 1

        fig.add_trace(
            go.Scatter(
                x=df[param],
                y=df['distance'],
                mode='markers',
                marker=dict(color=colors[i], size=8),
                name=param
            ),
            row=row, col=col
        )

    fig.update_layout(
        title='Parameter vs Performance Correlation',
        height=600,
        width=900,
        showlegend=False
    )

    return fig


def plot_convergence_comparison(stats_list, labels):
    """
    Compare convergence of different GA runs.

    Args:
        stats_list (list): List of statistics objects from different runs
        labels (list): Labels for each run

    Returns:
        plotly.graph_objects.Figure: Plotly figure
    """
    fig = go.Figure()
    colors = ['blue', 'red', 'green', 'orange', 'purple']

    for i, (stats, label) in enumerate(zip(stats_list, labels)):
        generations = list(range(len(stats.select("min"))))
        min_fitness = stats.select("min")

        fig.add_trace(go.Scatter(
            x=generations,
            y=min_fitness,
            mode='lines',
            name=label,
            line=dict(color=colors[i % len(colors)], width=2)
        ))

    fig.update_layout(
        title='Convergence Comparison',
        xaxis_title='Generation',
        yaxis_title='Best Fitness',
        width=900,
        height=500,
        showlegend=True
    )

    return fig


def create_vrp_summary_dashboard(locations, depot, individual, num_vehicles, results=None):
    """
    Create a comprehensive dashboard for VRP results.

    Args:
        locations (list): List of location coordinates
        depot (tuple): Depot coordinates
        individual (list): Best individual
        num_vehicles (int): Number of vehicles
        results (list, optional): Tuning results

    Returns:
        plotly.graph_objects.Figure: Dashboard figure
    """
    from plotly.subplots import make_subplots

    # Calculate route statistics
    total_distance = 0
    vehicle_distances = []

    for i in range(num_vehicles):
        vehicle_route = [depot] + [locations[individual[j]] 
                        for j in range(i, len(individual), num_vehicles)] + [depot]
        distance = sum(np.linalg.norm(np.array(vehicle_route[k+1]) - np.array(vehicle_route[k]))
                      for k in range(len(vehicle_route)-1))
        total_distance += distance
        vehicle_distances.append(distance)

    # Create subplots
    if results:
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('VRP Routes', 'Vehicle Load Distribution', 
                          'Tuning Progress', 'Route Statistics'),
            specs=[[{"colspan": 2}, None],
                   [{"type": "bar"}, {"type": "table"}]]
        )
    else:
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('VRP Routes', 'Vehicle Load Distribution'),
            specs=[[{"colspan": 1}, {"type": "bar"}]]
        )

    # Add route plot data (simplified for subplot)
    colors = ['red', 'green', 'blue', 'orange', 'purple']

    # Add depot
    fig.add_trace(go.Scatter(
        x=[depot[0]], y=[depot[1]],
        mode='markers',
        marker=dict(color='black', size=10, symbol='square'),
        name='Depot',
        showlegend=True
    ), row=1, col=1)

    # Add locations
    x_locs, y_locs = zip(*locations)
    fig.add_trace(go.Scatter(
        x=x_locs, y=y_locs,
        mode='markers',
        marker=dict(color='lightblue', size=6),
        name='Customers',
        showlegend=True
    ), row=1, col=1)

    # Add routes
    for i in range(num_vehicles):
        vehicle_route = [depot] + [locations[individual[j]] 
                        for j in range(i, len(individual), num_vehicles)] + [depot]
        x_route, y_route = zip(*vehicle_route)

        fig.add_trace(go.Scatter(
            x=x_route, y=y_route,
            mode='lines',
            line=dict(color=colors[i % len(colors)], width=2),
            name=f'Vehicle {i+1}',
            showlegend=True
        ), row=1, col=1)

    # Add vehicle distances bar chart
    if results is None:
        fig.add_trace(go.Bar(
            x=[f'Vehicle {i+1}' for i in range(num_vehicles)],
            y=vehicle_distances,
            name='Distance',
            marker_color=colors[:num_vehicles]
        ), row=1, col=2)
    else:
        fig.add_trace(go.Bar(
            x=[f'Vehicle {i+1}' for i in range(num_vehicles)],
            y=vehicle_distances,
            name='Distance',
            marker_color=colors[:num_vehicles]
        ), row=2, col=1)

        # Add tuning progress
        df = pd.DataFrame(results)
        fig.add_trace(go.Scatter(
            x=df['trial'],
            y=df['distance'],
            mode='lines+markers',
            name='Tuning Progress'
        ), row=2, col=2)

    fig.update_layout(
        title=f'VRP Solution Dashboard - Total Distance: {total_distance:.1f}',
        height=800 if results else 400,
        width=1000,
        showlegend=True
    )

    return fig
