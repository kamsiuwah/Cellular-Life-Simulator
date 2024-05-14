"""
=============================================================================
Title : Kamsiyochukwu_Uwah_R11723940_final_project.py
Author : Kauwah (R11723940)
Date : 04/26/2024
Notes : Final Project
=============================================================================
"""

import argparse  #module to handle command line arguments
import os  
import multiprocessing  # module to allow parallel processing
from copy import deepcopy  # deepcopy function for creating deep copies of objects

# Define a class to handle operations on a matrix of cells
class CellMatrix:
    def __init__(self, matrix):
        self.matrix = matrix  
        self.n_rows = len(matrix)  
        self.n_cols = len(matrix[0]) if self.matrix else 0  

    # Method to get all neighboring cells of a specified cell
    def get_neighbors(self, x, y):
        neighbors = []  
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if i != x or j != y: 
                    neighbors.append(self.matrix[i % self.n_rows][j % self.n_cols])
        return neighbors

    # Method to update the value of a cell
    def update_cell(self, x, y, value):
        self.matrix[x][y] = value  

    # Method to get the value of a specific cell
    def get_cell(self, x, y):
        return self.matrix[x][y]

# Function to count 'O' neighbors around a cell at (x, y)
def count_alive_neighbors(matrix_obj, x, y):
    neighbors = matrix_obj.get_neighbors(x, y)
    return sum(1 for cell in neighbors if cell == 'O')

# Function to check if a number is prime
def is_prime(n):
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# Function to process a single cell in the matrix
def process_cell(matrix_obj, x, y):
    alive_neighbors = count_alive_neighbors(matrix_obj, x, y)
    current_cell = matrix_obj.get_cell(x, y)
    if current_cell == 'O' and not is_prime(alive_neighbors):
        return (x, y, '.')
    elif current_cell != 'O' and alive_neighbors % 2 == 0 and alive_neighbors != 0:
        return (x, y, 'O')
    return (x, y, current_cell)

# Function to update the entire matrix in parallel
def update_matrix_parallel(matrix_obj, num_processes, steps):
    with multiprocessing.Pool(processes=num_processes) as pool:
        for _ in range(steps):
            tasks = [(matrix_obj, i, j) for i in range(matrix_obj.n_rows) for j in range(matrix_obj.n_cols)]
            results = pool.starmap(process_cell, tasks)
            for (i, j, value) in results:
                matrix_obj.update_cell(i, j, value)

# Function to read a matrix from a file
def read_matrix(filename):
    with open(filename, 'r') as file:
        matrix = [list(line.strip()) for line in file]
    return CellMatrix(matrix)

# Function to write a matrix to a file
def write_matrix(filename, matrix_obj):
    with open(filename, 'w') as file:
        for row in matrix_obj.matrix:
            file.write(''.join(row) + '\n')

# Main function that sets up the command line interface
def main():
    print("Project :: R11723940")
    parser = argparse.ArgumentParser(description='Matrix Simulation Program')
    parser.add_argument('-i', '--input', type=str, required=True, help='Input file path')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output file path')
    parser.add_argument('-p', '--processes', type=int, default=1, help='Number of processes')
    args = parser.parse_args()

    if not os.path.exists(args.input):
        raise FileNotFoundError(f"Input file not found: {args.input}")

    matrix = read_matrix(args.input)
    update_matrix_parallel(matrix, args.processes, 100)
    write_matrix(args.output, matrix)

if __name__ == "__main__":
    main()
