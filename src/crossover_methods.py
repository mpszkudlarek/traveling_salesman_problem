"""
crossover_methods.py

Contains implementations of crossover methods for genetic algorithms solving the
Traveling Salesman Problem (TSP). The methods include one-point crossover,
cycle crossover (CX), and partially mapped crossover (PMX).
Each of those crossover methods are based on:
https://en.wikipedia.org/wiki/Crossover_(genetic_algorithm)
"""

from typing import Tuple

import numpy as np


def single_point_crossover(
    parent1: Tuple[str, ...], parent2: Tuple[str, ...]
) -> Tuple[Tuple[str, ...], Tuple[str, ...]]:
    """
    Perform one-point crossover between two parent routes.

    Args:
        parent1 (Tuple[str, ...]): The first parent route.
        parent2 (Tuple[str, ...]): The second parent route.

    Returns:
        Tuple[Tuple[str, ...], Tuple[str, ...]]: Two child routes resulting from crossover.
    """
    size = len(parent1)
    if size < 2:
        return parent1, parent2
    point = np.random.randint(1, size)

    child1 = list(parent1[:point]) + [gene for gene in parent2 if gene not in parent1[:point]]
    child2 = list(parent2[:point]) + [gene for gene in parent1 if gene not in parent2[:point]]

    return tuple(child1), tuple(child2)


def cycle_crossover(
    parent1: Tuple[str, ...], parent2: Tuple[str, ...]
) -> Tuple[Tuple[str, ...], Tuple[str, ...]]:
    """
    Perform cycle crossover (CX) between two parent routes.

    Args:
        parent1 (Tuple[str, ...]): The first parent route.
        parent2 (Tuple[str, ...]): The second parent route.

    Returns:
        Tuple[Tuple[str, ...], Tuple[str, ...]]: Two child routes resulting from crossover.
    """

    size = len(parent1)

    child1 = [None] * size
    child2 = [None] * size

    parent2_indices = {value: idx for idx, value in enumerate(parent2)}

    visited = set()

    for start_idx in range(size):
        if start_idx in visited:
            continue

        cycle = []
        current_idx = start_idx

        while current_idx not in visited:
            visited.add(current_idx)
            cycle.append(current_idx)

            current_value = parent1[current_idx]
            current_idx = parent2_indices[current_value]

        for idx in cycle:
            if len(visited) % 2 == 1:

                child1[idx] = parent1[idx]
                child2[idx] = parent2[idx]
            else:

                child1[idx] = parent2[idx]
                child2[idx] = parent1[idx]

    for i in range(size):
        if child1[i] is None:
            child1[i] = parent2[i]
        if child2[i] is None:
            child2[i] = parent1[i]

    return (tuple(child1), tuple(child2))


def ox1_crossover(parent1: Tuple[str, ...], parent2: Tuple[str, ...]) -> Tuple[Tuple[str, ...], Tuple[str, ...]]:
    """
    Perform OX1 (Order Crossover) between two parent routes.

    Args:
        parent1 (Tuple[str, ...]): The first parent route.
        parent2 (Tuple[str, ...]): The second parent route.

    Returns:
        Tuple[Tuple[str, ...], Tuple[str, ...]]: Two child routes resulting from crossover.
    """
    size = len(parent1)
    if size < 2:
        return parent1, parent2

    point1, point2 = sorted(np.random.choice(range(size), size=2, replace=False))

    child1 = [""] * size
    child2 = [""] * size

    child1[point1:point2] = parent1[point1:point2]
    child2[point1:point2] = parent2[point1:point2]

    def fill_remaining_genes(child, parent):
        current_idx = point2 % size
        for gene in parent:
            if gene not in child:
                child[current_idx] = gene
                current_idx = (current_idx + 1) % size

    fill_remaining_genes(child1, parent2)
    fill_remaining_genes(child2, parent1)

    return tuple(child1), tuple(child2)
