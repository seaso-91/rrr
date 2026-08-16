from src.controllers.controller import BaseController

from src.models.executable import Executable
from pathlib import Path

class DataController(BaseController):
    def __init__(self, parent: Executable):
        super().__init__()
        self.parent = parent
        self._input_data = {
            "group": [],
            "code": [],
            "value": []
        }
        # A dictionary to store the group of each input code
        self._groups = dict()

        # A dictionary to store the values of each input code
        self._values = dict()

    def set_values(self, code: str, values: list[str]|str, group: str, force: bool = False):
        """
        Sets one or more values for a given input code and group.
        If the input code already exists, its values will be replaced with the new values.
        
        Args:
            code (str): The input code for which to set values.
            values (list[str]|str): The values to set for the input code.
            group (str): The group to which the input code belongs.
            force (bool): If True, the values will be set even if they are invalid. Default is False.
        """
        if isinstance(values, str):
            values = [values]

        if not force:
            self.validate_group(group)

            # remove old values
            for i in range(len(self._input_data["code"])-1, -1, -1):
                if self._input_data["code"][i] == code:
                    del self._input_data["group"][i]
                    del self._input_data["code"][i]
                    del self._input_data["value"][i]

            # validate new values
            for value in values:
                if self.validate_value(code, value) is False:
                    raise ValueError(f"Invalid value '{value}' for input '{code}'")
                
        # add new values
        for value in values:
            self._input_data["group"].append(group)
            self._input_data["code"].append(code)
            self._input_data["value"].append(value)

        self._groups[code] = group
        self._values[code] = values

    def get_values(self, code: str) -> list[str]:
        """
        Returns the list of values for a given input code.
        
        Args:
            code (str): The input code for which to retrieve values.
        Returns:
            list[str]: A list of values for the given input code.
        """
        if code not in self._values.keys():
            raise KeyError(f"Input code '{code}' not found in input data. a")
        return self._values[code]

    def validate_value(self, code: str, value: str) -> bool:
        """
        Validates a value for a given input code using the input's validate method.
        Args:
            code (str): The input code for which to validate the value.
            value (str): The value to validate for the input code.
        Returns:
            bool: True if the value is valid for the given input code, False otherwise.
        """
        
        # validate the input exists
        try:
            input = self.parent.inputs[code]
        except KeyError:
            raise KeyError(f"Input code '{code}' not found in executable.")
        # validate the value using the input's validate method
        return input.validate(value)

    def export_data(self, csv_file: Path):
        """
        Exports input data to a CSV file.

        Args:
            csv_file (Path): The path to the CSV file to export the input data to.
        """
        with open(csv_file, "w") as f:
            f.write("group,input,value\n")
            for i in range(len(self._data["group"])):
                f.write(f"{self._data['group'][i]},{self._data['code'][i]},{self._data['value'][i]}\n")

    def import_csv(self, csv_file: Path):
        """
        Imports input data from a CSV file.

        Args:
            csv_file (Path): The path to the CSV file containing the input data.
        """
        self._clear()
        with open(csv_file, "r") as f:
            lines = f.readlines()
        for line in lines[1:]:
            group, code, value = line.strip().split(",")
            self._input_data["group"].append(group)
            self._input_data["code"].append(code)
            self._input_data["value"].append(value)
            self._groups[code] = group
            if code not in self._values:
                self._values[code] = []
            self._values[code].append(value)

    def import_dat(self, dat_file: Path):
        """
        Imports input data from a .dat file.

        Args:
            dat_file (Path): The path to the .dat file containing the input data.
        """
        #open the dat file and read the lines
        with open(dat_file, "r") as f:
            string = f.read()

        from src.models.string_input import StringInput
        string_input = StringInput(self)
        string_input.text = string
        try:
            string_input.validate()
        except Exception as e:
            raise ValueError(f"Invalid input data in {dat_file}: {e}")
        string_input.set_values()
        
    def validate_group(self, group: str) -> bool:
        """
        Validates a group identifier. Only non-negative integers are allowed as group names.
        Args:
            group (str): The group identifier to validate.
        Returns:
            bool: True if the group identifier is valid, False otherwise.
        """
        # only allow non negative integers as group names
        result = False
        if group.isdigit():
            result = int(group) >= 0
        if result is False:
            raise ValueError(f"Invalid group '{group}'")
        return result

    def get_group(self, code: str) -> str:
        """
        Returns the group for a given input code.
        
        Args:
            code (str): The input code for which to retrieve the group.
        Returns:
            str: The group for the given input code.
        """

        if code not in self._groups.keys():
            raise KeyError(f"Input code '{code}' not found in input data. b")
        return self._groups[code]

    def get_groups(self, sort: bool = True) -> list[str]:
        """
        Returns a list of unique groups in the input data.
        
        Args:
            sort (bool): If True, the groups will be sorted in ascending order. Default is True.
        Returns:
            list[str]: A list of unique groups in the input data.
        """
        groups = set(self._input_data["group"])

        #sort the groups in ascending order if requested
        if sort:
            groups = sorted(groups, key=lambda x: int(x))
        return list(groups)

    def get_input_codes(self, group: str) -> list[str]:
        """
        Returns the list of input codes for a given group.
        
        Args:
            group (str): The group for which to retrieve inputs.
        Returns:
            list[str]: A list of unique inputs in the input data for the given group.
        """
        input_codes = []
        for key in self._groups.keys():
            if self._groups[key] == group:
                input_codes.append(key)
        return input_codes

    def group_size(self, group: str) -> int:
        """
        Returns the number of values for a given group.
        
        Args:
            group (str): The group for which to retrieve the number of values.
        Returns:
            int: The number of values for the given group.
        """
        size = 0
        input_codes = self.get_input_codes(group)
        for code in input_codes:
            size = max(size, len(self.get_values(code)))
        return size

    def number_of_runs(self) -> int:
        """
        Returns the total number of runs based on the number of values for each group.
        The total number of runs is the cartesian product of each group.

        Returns:
            int: The total number of runs.
        """
        runs = 1
        for group in self.get_groups():
            runs *= self.group_size(group)
        return runs
    
    def get_runs_as_dicts(self) -> dict[int, dict[str, str]]:
            """
            Generates row 
            """
            groups = self.get_groups(sort=True)
            if not groups:
                return {}

            group_to_position = {group: idx for idx, group in enumerate(groups)}
            group_sizes = [self.group_size(group) for group in groups]
            number_of_runs = self.number_of_runs()

            transposed_runs: dict[int, dict[str, str]] = {}

            for run_index in range(number_of_runs):
                per_group_indices = []
                remainder = run_index
                for size in reversed(group_sizes):
                    per_group_indices.append(remainder % size)
                    remainder //= size
                per_group_indices.reverse()

                run_dict = {}
                for row in self.parent.input_sequence:
                    for input in row:
                        code = input.code
                        if code == "UM":
                            run_dict[code] = str(run_index)
                            continue

                        group = self.get_group(code)
                        values = self.get_values(code)

                        group_index = per_group_indices[group_to_position[group]]
                        run_dict[code] = values[group_index % len(values)]

                transposed_runs[run_index] = run_dict

            return transposed_runs

    def _clear(self):
        """
        Clears the input data.
        """
        self._input_data = {
            "group": [],
            "code": [],
            "value": []
        }
        self._groups = dict()
        self._values = dict()

    def flush(self):
        self.parent.input_data.run_data = self.get_runs_as_dicts()

    def print_to_csv(self, filename: str = "output.csv", show_failures: bool = False, show_successes: bool = True):
        """
        Prints the input data to a CSV file named 'input_data.csv' in the current working directory.
        """        
        #check if filename ends with .csv, if not add it
        if not filename.endswith(".csv"):
            filename += ".csv"

        if self.parent.input_data.number_of_runs != 0 or self.parent.output_data.number_of_runs == 0:
            raise ValueError("The results are not finished, or there are no results to show.")

        results = self.parent.output_data.results
        if len(results) > 0:
            result_headers = list(results[next(iter(results))].keys())

        run_data = self.parent.output_data.run_data
        if len(run_data) > 0:
            run_headers = list(run_data[next(iter(run_data))].keys())

        headers = ["run_id"]

        if show_failures and show_successes:
            headers = list(headers + run_headers + result_headers)
            run_data = self.parent.output_data.run_data
            # add to dictionary the results for each run_id
            for run_id, data in run_data.items():
                if run_id in results:
                    data.update(results[run_id])
            
        elif show_failures and not show_successes:
            headers = list(headers + run_headers)
            run_data = self.parent.output_data.failures

        elif not show_failures and show_successes:
            headers = list(headers + run_headers + result_headers)
            run_data = self.parent.output_data.successes
            # add to dictionary the results for each run_id
            for run_id, data in run_data.items():
                if run_id in results:
                    data.update(results[run_id])

        elif not show_failures and not show_successes:
            raise ValueError("Both show_failures and show_successes cannot be False. Please set at least one to True.")

        with open(filename, "w") as f:
            # Write the header
            f.write(",".join(headers) + "\n")
            for run_id, data in run_data.items():
                row = [str(run_id)] + [data.get(code, "") for code in headers[1:]]
                f.write(",".join(row) + "\n")


if __name__ == "__main__":
    from src.models.aevap import AEVAP
    aevap = AEVAP()
    data_controller = DataController(aevap)
    data_controller.import_dat("C:\\Users\\jajones\\Desktop\\rrr\\D1.DAT")
