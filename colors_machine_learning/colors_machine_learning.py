import csv
from random import random
import math
from collections import Counter


def load_colors(filename):
    with open(filename) as dataset_file:
        # cvs.reader is an object that iterates over the dataset and extracts
        # the comma separated values, in this case: 'r, g, b, color' as a list
        # of strings '[r, g, b, color]'.
        lines = csv.reader(dataset_file)
        for line in lines:
            # yield in the iterator in the format 'tuple(tuple(r, g, b), color)'
            yield tuple(float(y) for y in line[0:3]), line[3]


def generate_colors(num_of_colors=100):
    for i in range(num_of_colors):
        # random() generates a number in the range [0, 1]
        yield (random(), random(), random())


def colors_distance(color1, color2):
    squared_distance = sum((c1 - c2) ** 2 for c1, c2 in zip(color1, color2))
    return math.sqrt(squared_distance)


# Coroutine
def nearest_neighbors(model_colors, num_neighbors):
    # It converts the model to a list because it is going to be iterated a lot
    # of times.
    model = list(model_colors)
    
    # Wait for first 'send'. The first 'next' call executes the code til here.
    target = yield
    while True:
        # Calculates the distance between the sent color and all the colors
        # in the model in the format 'tuple(distance, color_data)'.
        # Finally it sorts this list based on the distance
        distances = sorted(((colors_distance(c[0], target), c) for c in model))
        
        # Wait for subsequent 'send's to yield the next color and return
        # the distances
        target = yield [d[1] for d in distances[0:num_neighbors]]
            

# Coroutine
# Recieves an existing coroutine (instance of 'nearest neighbors') to get
# the nearest neighbors
def name_colors(get_neighbors):
    # Wait for the first call to 'send' to recieve the color
    color = yield
    while True:
        near = get_neighbors.send(color)
        # Get the most common ocurrence of the nearest neighbors
        name_guess = Counter(n[1] for n in near).most_common(1)[0][0]
        # Wait for the subsequent calls to 'send' while return 'name_guess'
        color = yield name_guess


# Coroutine
# Writes the results to the output file in every 'send' yielded
def write_results(filename="output.csv"):
    with open(filename, "w") as file:
        writer = csv.writer(file)
        while True:
            # Wait to the call to 'send' to recieve the color and its name
            color, name = yield
            # Unlike 'csv.reader', 'csv.writer' gets a list and writes it
            # to the csv file in comma-separated format.
            writer.writerow(list(color) + [name])


# This is not a coroutine, but it creates three coroutines to work with
def process_colors(dataset_filename="colors.csv"):
    model_colors = load_colors(dataset_filename)
    
    # Uses the 10 nearest neighbors to verify the most common,
    get_neighbors = nearest_neighbors(model_colors, 10)
    get_color_name = name_colors(get_neighbors)
    output = write_results()
    
    # Initialize all the coroutines
    next(output)
    next(get_neighbors)
    next(get_color_name)
    
    # Default number of colors if no argument is passed is 100.
    for color in generate_colors():
        # 'get_color_name' uses internally another coroutine 'get_neighbors'
        name = get_color_name.send(color)
        # sends to 'output' coroutine the
        output.send((color, name))


process_colors()
