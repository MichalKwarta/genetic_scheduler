from loader import TaskDefinition, ProcessingTime, load_data_file
from scheduling import Scheduler


if __name__ == "__main__":
    file_choice = input("Choose file: ")
    data = load_data_file(f"{file_choice}.txt")
    iterations = 100
    population_size = 5000
    mutation_rate = 0.8
    best_candidate = Scheduler(data).genetic_algorithm(
        iterations, population_size, mutation_rate
    )
    print("Population size: ", population_size)
    print("Iterations: ", iterations)
    print("Best candidate:", best_candidate)
