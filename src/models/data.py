from enum import Enum
from random import randint

class InputStatus(Enum):
    READY = "Ready"
    FINISHED = "Finished"
    ERROR = "Error"

class Data():
    def __init__(self):
        self._run_data: dict[int, dict[str, str]] = {}

    @property
    def number_of_runs(self) -> int:
        return len(self._run_data)

    @property
    def run_data(self):
        return self._run_data
    
    @staticmethod
    def get_run_id(run_data: dict[str, str]) -> int:
        """
        Extracts the run ID from the provided run data dictionary.
        Args:
            run_data (dict): A dictionary containing run data, expected to have a key "UM" with a value like "RRR{run_id}".
        Returns:
            int: The extracted run ID as an integer.
        Raises:
            ValueError: If the "UM" key is missing or the value format is incorrect.
        """
        um_value = run_data.get("UM")
        if um_value is None:
            raise ValueError("Run data must contain a 'UM' key.")

        try: 
            run_id = int(um_value.split("RRR")[1])
            return run_id
        except (IndexError, ValueError):
            raise ValueError(f"Invalid UM format: {um_value}. Expected suffix: 'RRR{{run_id}}'.")
    
class OutputData(Data):
    def __init__(self):
        super().__init__()
        self._results: dict[int, dict[str, str]] = {}
        
    @property
    def successes(self):
        return {k: v for k, v in self._run_data.items() if v["run_status"] == InputStatus.FINISHED.value}

    @property
    def failures(self):
        return {k: v for k, v in self._run_data.items() if v["run_status"] == InputStatus.ERROR.value}  

    def push(self, input_data: dict[int, dict[str, str]], output_data: list[dict[str, str]]|dict[str, str]):
        if isinstance(output_data, dict):
            output_data = [output_data]

        for data in output_data:
            run_id = self.get_run_id(data)
            if run_id not in input_data.keys():
                raise ValueError(f"Run ID {run_id} not found in the provided input data")
            self._push_success(input_data.pop(run_id))
            self._results[run_id] = data

        for run_id, data in input_data.items():
            self._push_failure(data)

    def _push_failure(self, data: dict[str, str]):
        data["run_status"] = InputStatus.ERROR.value
        run_id = self.get_run_id(data)
        self._run_data[run_id] = data

    def _push_success(self, data: dict[str, str]):
        data["run_status"] = InputStatus.FINISHED.value
        run_id = self.get_run_id(data)
        self._run_data[run_id] = data

class InputData(Data):
    def __init__(self):
        super().__init__()
        self._next_id = 0

    @Data.run_data.setter
    def run_data(self, data: dict[int, dict[str, str]]):
        self._failures = {}
        self._successes = {}
        for row in data:
            data[row]["UM"] += f"RRR{row}"
            data[row]["run_status"] = InputStatus.READY.value
        self._run_data = data
        self._set_next_rand_id()

    def get(self, number_of_runs: int = None) -> list[dict[str, str]]:
        runs = list(self._run_data.values())
        if number_of_runs is None:
            return runs
        runs = []
        while number_of_runs > len(self._run_data):
            run_id = list(self._run_data.keys())[self._next_id]
            runs.append(self._run_data.pop(run_id))
            self._set_next_rand_id()
            number_of_runs -= 1
        return runs

    def return_run(self, run_data: list[dict[str, str]]|dict[str, str]):
        if isinstance(run_data, dict):
            run_data = [run_data]
        for run in run_data:
            run_id = self.get_run_id(run)
            if run_id in self._run_data:
                raise ValueError(f"Run ID {run_id} already exists in the data.")
            self._run_data[run_id] = run
            self._set_next_rand_id()

    def _set_next_rand_id(self):
        self._next_id = randint(0, len(self._run_data) - 1)