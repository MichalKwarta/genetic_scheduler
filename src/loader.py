from pathlib import Path
from dataclasses import dataclass

DATA_DIR = "data/"


ProcessingTime = tuple[int]


@dataclass
class TaskDefinition:
    machines_count: int
    jobs_count: int
    processing_times: tuple[ProcessingTime]


def load_data_file(name: str):
    with open(Path(DATA_DIR + name)) as f:
        contents = f.read()

    workers_definition, *processing_times = contents.split("\n")
    machines, jobs = workers_definition.split()
    return TaskDefinition(
        int(machines),
        int(jobs),
        tuple(tuple(map(int, pt.split())) for pt in processing_times),
    )
