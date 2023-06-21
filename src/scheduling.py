from dataclasses import dataclass
import itertools
from loader import TaskDefinition, ProcessingTime
import random

INF = float("inf")


@dataclass
class Candidate:
    order: list[int]
    total_processing_time: int


class Scheduler:
    machines_count: int
    jobs_count: int
    processing_times: tuple[ProcessingTime]

    def __init__(self, definition: TaskDefinition):
        self.machines_count = definition.machines_count
        self.jobs_count = definition.jobs_count
        self.processing_times = definition.processing_times

    def calculate_total_processing_time(self, order: list[int]):
        completion_times = [0] * self.machines_count
        for job_id in order:
            job_processing_times = self.processing_times[job_id - 1]
            for j in range(self.machines_count):
                if j:
                    completion_times[j] = (
                        max(completion_times[j], completion_times[j - 1])
                        + job_processing_times[j]
                    )
                else:
                    completion_times[j] += job_processing_times[j]

        return completion_times[self.machines_count - 1]

    def shuffle(self):
        return sorted(range(1, self.jobs_count + 1), key=lambda _: random.random())

    def crossover(self, parent1: Candidate, parent2: Candidate):
        crossover_point = random.randint(1, len(parent1.order) - 1)
        child1 = parent1.order[:crossover_point] + parent2.order[crossover_point:]
        child2 = parent2.order[:crossover_point] + parent1.order[crossover_point:]
        return child1, child2

    def mutate(self, individual: list[int]):
        index1, index2 = random.sample(range(len(individual)), 2)
        individual[index1], individual[index2] = individual[index2], individual[index1]
        return individual

    @staticmethod
    def mutation_decision(mutation_rate: float):
        return random.random() < mutation_rate

    def genetic_algorithm(
        self, population_size: int, num_iterations: int, mutation_rate: int
    ):
        initial_population = [
            Candidate(
                order := self.shuffle(), self.calculate_total_processing_time(order)
            )
            for _ in range(population_size)
        ]
        best_ever = Candidate([], INF)
        population = initial_population
        for _ in range(num_iterations):
            # scoring population

            new_population_candidates = itertools.chain(
                *[
                    self.crossover(*random.sample(population, 2))
                    for _ in range(population_size // 2)
                ]
            )

            # mutation
            new_population = sorted(
                [
                    Candidate(order, self.calculate_total_processing_time(order))
                    if self.mutation_decision(mutation_rate)
                    else population[idx]
                    for idx, order in enumerate(new_population_candidates)
                ],
                key=lambda x: x.total_processing_time,
            )

            population = new_population
            best_ever = min(
                best_ever, population[0], key=lambda x: x.total_processing_time
            )

        return best_ever
