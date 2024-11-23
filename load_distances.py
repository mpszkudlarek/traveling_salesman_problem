"""
This module contains a function to load a distance matrix from a file
and convert it into a dictionary format for use in problems like the
Traveling Salesman Problem.
"""
import os

class DistanceMatrixError(Exception):
    """
    Exception raised for errors related to the distance matrix,
    such as invalid data or matrix inconsistencies.
    """

def parse_matrix(lines, num_cities, city_names):
    """
    Parses the distance matrix from the lines of the file.

    Args:
        lines (list): The list of lines from the file.
        num_cities (int): The number of cities.
        city_names (list): The list of city names.

    Returns:
        dict: A dictionary of distances in the format {(city1, city2): distance, ...}.

    Raises:
        ValueError: If the matrix is malformed.
    """
    city_distances = {}

    for i, line in enumerate(lines[1: num_cities + 1]):
        values = list(map(int, line.split()))
        if len(values) != num_cities:
            raise ValueError(f"Row {i + 1} does not have {num_cities} columns.")
        for j, value in enumerate(values):
            if i != j:
                city_distances[(city_names[i], city_names[j])] = value

    return city_distances

def load_distances(file_name, folder="input") -> tuple:
    """
    Loads a distance matrix from a file in the `input` folder and converts it into a dictionary.

    Args:
        file_name (str): The name of the file containing the data.
        folder (str): The path to the folder containing the file.

    Returns:
        dict: A dictionary of distances in the format {(city1, city2): distance, ...}.
        list: A list of cities in the order they appear in the matrix.

    Raises:
        FileNotFoundError: If the distance matrix file is not found.
        ValueError: If there is an issue with parsing the file or
        if the matrix dimensions are incorrect.
        OSError: If there is a file access error.
        DistanceMatrixError: If the matrix has invalid data
        (e.g., non-symmetric, negative distances).
    """
    file_path = os.path.join(folder, file_name)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        num_cities = int(lines[0].strip())
        city_names = [f"city_{i+1}" for i in range(num_cities)]

        if len(lines) < num_cities + 1:
            raise ValueError(
                f"File contains fewer rows than expected for {num_cities} cities."
            )

        city_distances = parse_matrix(lines, num_cities, city_names)

        for (city1, city2), dist in city_distances.items():
            if dist < 0:
                raise ValueError(
                    f"Negative distance found between {city1} and {city2}: {dist}."
                )
            if city_distances.get((city2, city1), None) != dist:
                raise ValueError(
                    f"Distance matrix is not symmetric: ({city1}, {city2}) vs ({city2}, {city1})."
                )

    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"The file {file_name} was not found in the folder {folder}."
        ) from e
    except ValueError as e:
        raise ValueError(f"Error processing file {file_name}: {e}") from e
    except OSError as e:
        raise OSError(f"File access error: {e}") from e
    except Exception as e:
        raise DistanceMatrixError(f"An unexpected error occurred: {e}") from e

    return city_distances, city_names
