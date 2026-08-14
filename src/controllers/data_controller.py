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

class InputData():
    def __init__(self):
        self._input_data = {
            "group": [],
            "code": [],
            "value": []
        }
        # A dictionary to store the group of each input code
        self._groups = dict()

        # A dictionary to store the values of each input code
        self._values = dict()

    def __str__ (self):
        """
        Returns a string representation of the input data in the format expected for the widget.
        Returns:
            str: A string representation of the input data.
        """
        try:
            input_string = ""
            for row in self.parent.input_sequence:
                for input in row:
                    input_string += f"{self.get_string(input.code)},"
                input_string += "\n"
            input_string = input_string[:-1] + "\n" + "0" # remove last comma and add newline
            return input_string
        except Exception as e:
            return f"Error generating input string: {e}"

    def __repr__ (self):
        """
        Returns:
            str: A string representation of the input data.
        """
        output = ""
        output += "Group".ljust(10) + "Code".ljust(10) + "Value".ljust(20) + "\n"
        for group, code, value in zip(self._data["group"], self._data["code"], self._data["value"]):
            output += group.ljust(10,".") + code.ljust(10,".") + value.ljust(20,".") + "\n"
        output += f"Total number of runs: {self.number_of_runs()}\n"

        for group in self.get_groups():
            output += f"Group {group} ({self.group_size(group)} tuples): "
            output += f"{self.get_input_codes(group)}\n"

        output += f"Total number of input codes: {len(self._groups)}\n"
        return output
    
    def _clear(self):
        """
        Clears the input data.
        """
        ## FIXME this will change the input file, so we need to write just a clear method
        self.__init__(self.parent)

    def get_groups(self, sort: bool = True) -> list[str]:
        """
        Returns a list of unique groups in the input data.
        
        Args:
            sort (bool): If True, the groups will be sorted in ascending order. Default is True.
        Returns:
            list[str]: A list of unique groups in the input data.
        """
        groups = set(self._data["group"])

        #sort the groups in ascending order if requested
        if sort:
            groups = sorted(groups, key=lambda x: int(x))
        return list(groups)


    




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


    def _split_data(self, data: str) -> dict:
        split_data = {}
        lines = data.strip().split("\n")
        for i, row in enumerate(self.parent.input_sequence):
            values = lines[i].strip().split(",")
            for j, input in enumerate(row):
                if values[j] == '' or values[j] == 'None':
                    values[j] = ""
                split_data[input.code] = values[j]
        return split_data

    def set_input_file_name(self, input_file: str):
        """
        Sets the target file for the input data.

        Args:
            input_file (str): The name of the input file.
        """
        # the input file name must be a valid name and not an empty string
        if not input_file:
            raise ValueError("Input file name cannot be empty.")

        # if it doesnt end with .dat then append it
        if not input_file.endswith(".dat"):
            input_file += ".dat"

        # check that the name is legal
        if any(c in input_file for c in r'<>:"/\|?*'):
            raise ValueError(f"Input file name '{input_file}' contains illegal characters.")

        self.input_file = self.parent.path / input_file

    def set_split(self, number_of_splits: int = 1, split_index: int = 0):
        """
        Sets the number of splits and the current split index for the input data.
        
        Args:
            number_of_splits (int): The total number of splits for the input data. Default is 1 (no splitting).
            split_index (int): The index of the current split (0-based). Default is 0 (first split).
        """
        if number_of_splits < 1:
            raise ValueError("number_of_splits must be greater than 0")
        if split_index < 0 or split_index >= number_of_splits:
            raise ValueError("split_index must be between 0 and number_of_splits - 1")

        number_of_runs = self.number_of_runs()
        self.start_index = int(split_index * number_of_runs / number_of_splits)
        self.end_index = int((split_index + 1) * number_of_runs / number_of_splits) if split_index < number_of_splits - 1 else number_of_runs

    def set_start_index(self, start_index: int):
        """
        Sets the start index for the input data.
        
        Args:
            start_index (int): The start index for the input data.
        """
        if start_index < 0 or start_index >= self.number_of_runs():
            raise ValueError("start_index must be between 0 and number_of_runs - 1")
        if start_index >= self.end_index:
            raise ValueError("start_index must be less than end_index")
        self.start_index = start_index

        self._expected_number_of_results = self.end_index - self.start_index

    def set_end_index(self, end_index: int):
        """
        Sets the end index for the input data.
        
        Args:
            end_index (int): The end index for the input data.
        """
        if end_index < 0 or end_index > self.number_of_runs():
            raise ValueError("end_index must be between 0 and number_of_runs")
        if end_index <= self.start_index:
            raise ValueError("end_index must be greater than start_index")
        self.end_index = end_index

        self._expected_number_of_results = self.end_index - self.start_index
    
    def write_input_file(self):
        """
        Writes the input data to the target file.
        """
        if not hasattr(self, 'input_file'):
            raise ValueError("Input file name has not been set. Use set_input_file_name() to set it.")
        
        input_string = self.get_input_string()
        self.expected_number_of_results = self.end_index - self.start_index
        try:
            with open(self.parent.path / self.input_file, "w") as f:
                f.write(input_string)
        except Exception as e:
            raise RuntimeError(f"Failed to write input data to {self.parent.path / self.input_file}: {e}")

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

    def change_group(self, code: str, new_group: str):
        """
        Changes the group of a given input code to a new group.

        Args:
            code (str): The input code for which to change the group.
            new_group (str): The new group to assign to the input code.
        """
        self.validate_group(new_group)
        for i, val in enumerate(self._data["code"]):
            if val == code:
                self._data["group"][i] = new_group
        self._groups[code] = new_group

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
            for i in range(len(self._data["code"])-1, -1, -1):
                if self._data["code"][i] == code:
                    del self._data["group"][i]
                    del self._data["code"][i]
                    del self._data["value"][i]

            # validate new values
            for value in values:
                if self.validate_value(code, value) is False:
                    raise ValueError(f"Invalid value '{value}' for input '{code}'")
                
        # add new values
        for value in values:
            self._data["group"].append(group)
            self._data["code"].append(code)
            self._data["value"].append(value)

        self._groups[code] = group
        self._values[code] = values

    def add_value(self, code: str, value: str, force: bool = False):
        """
        Adds a single value for a given input code. If the input code already exists, the new value will be added to the existing values.
        Args:
            code (str): The input code for which to add a value.
            value (str): The value to add for the input code.
            force (bool): If True, the value will be added even if it is invalid. Default is False.
        """
        if not force:
            # validate new value
            if self.validate_value(code, value) is False:
                raise ValueError(f"Invalid value '{value}' for input '{code}'")
        
        group = self.get_group(code)
        # group '0' should have a single value
        if group == '0':
            group = self.new_group()
            self.change_group(code, group)

        self._data["group"].append(group)
        self._data["code"].append(code)
        self._data["value"].append(value)
        if code not in self._values:
            self._values[code] = []
        self._values[code].append(value)

    def new_group(self) -> str:
        """
        Returns:
            str: A new, unused group identifier.
        """
        groups = self.get_groups(sort=True)
        return str(int(groups[-1]) + 1)

    def get_string(self, code: str) -> str:
        """
        Returns a string representation of the values for a given input code.
        Args:
            code (str): The input code for which to retrieve the string representation of values.
        Returns:
            str: A string representation of the values for the given input code.
        """
        group = self.get_group(code)
        values = self.get_values(code)
        if group == "0" and len(values) == 1:
            return values[0]

        else:
            return group + "{" + ",".join(values) + "}"

    def set_values_by_string(self, string: str, code: str, force: bool = False):
        """
        Sets the values for a given input code based on a string representation of the values.
        The string can be in the format "group{value1,value2,...}" or just "value" for group '0'.
        Args:
            string (str): The string representation of the values to set for the input code.
            code (str): The input code for which to set the values.
            force (bool): If True, the values will be set even if they are invalid. Default is False.
        """
        #parse the string and add the values to the input data
        if "{" in string:
            group, values = string.split("{")
            values = values[:-1].split(",")
            self.set_values(code, values, group, force=force)
        else:
            self.set_values(code, [string], '0', force=force)





    def get_code(self, row: int, column: int) -> str:
        """
        Returns the input code at the specified row and column in the input sequence.
        Args:
            row (int): The row index in the input sequence.
            column (int): The column index in the input sequence.
        Returns:
            str: The input code at the specified row and column.
        """
        rows_in_input_sequence = len(self.parent.input_sequence)
        if row < 0 or row >= rows_in_input_sequence:
            raise IndexError(f"Row index '{row}' out of range. Valid range is 0 to {rows_in_input_sequence - 1}.")
        if column < len(self.parent.input_sequence[row]):
            return self.parent.input_sequence[row][column].code
        raise IndexError(f"Column index '{column}' out of range for row '{row}'")

    def get_code_from_position(self, position: tuple[int, int]) -> str:
        """
        Returns the input code at the specified (row, column) position in the input string.
        Args:
            position (tuple[int, int]): A tuple containing the (row, column) position in the input string.
        Returns:
            str: The input code at the specified (row, column) position.
        """
        input_string = ""
        new_input_string = ""
        for idx, row in enumerate(self.parent.input_sequence):
            if idx == position[0]:
                for input in row:
                    new_input_string = input_string + f"{self.get_string(input.code)},"
                    if len(new_input_string) > position[1]:
                        return input.code
                    input_string = new_input_string
        raise ValueError(f"Position {position} is out of range in the input string.")

    def get_position(self, code: str) -> tuple[int, int, int]:
        """
        Returns the position of the specified input code in the input string.
        Args:
            code (str): The input code for which to find the position.
        Returns:
            (row, start, end): A tuple containing the row index and start and end column indices.
        """

        # find the start index by iterating through the rows of the input sequence
        # create the string along the way
        start_index = None
        for idx, row in enumerate(self.parent.input_sequence):
            input_string = ""
            for input in row:
                if input.code == code:
                    start_index = len(input_string)
                input_string += f"{self.get_string(input.code)},"
                if start_index is not None:
                    end_index = len(input_string) - 1 # subtract 1 to remove the comma
                    return (idx, start_index, end_index)

        raise ValueError(f"Code '{code}' not found in input sequence.")

    def get_row_and_column(self, code: str) -> tuple[int, int]:
        """
        Returns the row and column indices of the specified input code in the input sequence.
        Args:
            code (str): The input code for which to find the row and column indices.
        Returns:
            (row, column): A tuple containing the row and column indices of the input code.
        """
        for row_idx, row in enumerate(self.parent.input_sequence):
            for col_idx, input in enumerate(row):
                if input.code == code:
                    return (row_idx, col_idx)
        raise ValueError(f"Code '{code}' not found in input sequence.")
    
    def get_input_string(self):
        """
            Creates a string representation of the input data in the format expected by the executable.
            Every combination of values for each group will be created as a new block, with each block separated by a '0'.
            Groups with codes of varying size need to use modulo indexing so the values are repeated as needed to fill the block.
            Args:
                number_of_splits (int): The total number of splits for the input data. Default is 1 (no splitting).
                split_index (int): The index of the current split (0-based). Default is 0 (first split).
            Raises:
                ValueError: If the number_of_splits is less than 1 or if the split_index is out of range.
        """        
        groups = self.get_groups(sort=True)
        group_to_position = {group: idx for idx, group in enumerate(groups)}
        group_sizes = [self.group_size(group) for group in groups]
        
        output_lines = []
        for run_index in range(self.start_index, self.end_index):
            # Convert the linear run index to a per-group index tuple.
            per_group_indices = []
            remainder = run_index
            for size in reversed(group_sizes):
                per_group_indices.append(remainder % size)
                remainder //= size
            per_group_indices.reverse()

            block_lines = []
            for row in self.parent.input_sequence:
                row_values = []
                for input in row:
                    code = input.code
                    group = self.get_group(code)
                    values = self.get_values(code)
                    group_index = per_group_indices[group_to_position[group]]

                    if code == "UM":
                        row_values.append(values[group_index % len(values)] + "RRR" + str(run_index))
                    else:
                        row_values.append(values[group_index % len(values)])

                block_lines.append(",".join(row_values))

            output_lines.extend(block_lines)
            output_lines.append("0")

        return "\n".join(output_lines) + "\n"

    def get_input(self, index: int) -> dict:
        """
        Returns a dictionary of input codes and their corresponding values for
        the specified run index (0-based), matching the ordering used by
        get_input_string().
        """
        if index < 0:
            raise ValueError("index must be greater than or equal to 0")

        number_of_runs = self.number_of_runs()
        if index >= number_of_runs:
            raise IndexError(
                f"Run index '{index}' out of range. Valid range is 0 to {number_of_runs - 1}."
            )

        groups = self.get_groups(sort=True)
        if not groups:
            return {}

        group_to_position = {group: idx for idx, group in enumerate(groups)}
        group_sizes = [self.group_size(group) for group in groups]

        per_group_indices = []
        remainder = index
        for size in reversed(group_sizes):
            per_group_indices.append(remainder % size)
            remainder //= size
        per_group_indices.reverse()

        input_values = {}
        for row in self.parent.input_sequence:
            for input in row:
                group = self.get_group(input.code)
                values = self.get_values(input.code)
                if not values:
                    raise ValueError(f"No values found for input '{input.code}'")

                group_index = per_group_indices[group_to_position[group]]
                input_values[input.code] = values[group_index % len(values)]

        return input_values

    def get_input_values(self) -> dict[str, list[str]]:
        """
        Returns a dictionary mapping each input code to the full cartesian-product
        of values across all runs, in the same order used by get_input_string().

        Returns:
            dict[str, list[str]]: A dictionary where each key is an input code and
            each value is the list of values that code takes across all runs.
        """
        groups = self.get_groups(sort=True)
        if not groups:
            return {}

        group_to_position = {group: idx for idx, group in enumerate(groups)}
        group_sizes = [self.group_size(group) for group in groups]
        number_of_runs = self.number_of_runs()

        values_by_code: dict[str, list[str]] = {}
        for row in self.parent.input_sequence:
            for input in row:
                values_by_code[input.code] = []

        for run_index in range(number_of_runs):
            per_group_indices = []
            remainder = run_index
            for size in reversed(group_sizes):
                per_group_indices.append(remainder % size)
                remainder //= size
            per_group_indices.reverse()

            for row in self.parent.input_sequence:
                for input in row:
                    code = input.code
                    if code == "UM":
                        values_by_code[code].append(str(run_index))
                        continue

                    group = self.get_group(code)
                    values = self.get_values(code)

                    group_index = per_group_indices[group_to_position[group]]
                    values_by_code[code].append(values[group_index % len(values)])

        return values_by_code

    def get_widget(self, *args, **kwargs):
        """
        Returns a Tkinter widget for displaying and editing the input data.
        """
        from src.controllers.string_inputs_controller import Widget
        return Widget(self, *args, **kwargs)

    def set_data(self, data: str|Path, force: bool = False):
        """
        Sets the input data from an InputData object, a string, or a file path. 
        The data can be in the form of an InputData object, a .dat or .csv file, or a string representation.

        Args:
            data (InputData|str|Path): The input data, which can be an InputData object, a .dat or .csv file path, or a string representation.
            force (bool): If True, the input data will be set even if it is invalid. Default is False.
        """
        self._clear()
        if isinstance(data, str):
            # There is a method that can be moved over from the RRXData class to handle this
            raise Exception("Not implemented yet")
        if isinstance(data, InputData):
            self._set_data_from_inputdata(data, force=force)
        if isinstance(data, Path):
            if data.suffix.lower() == ".csv":
                self._set_data_from_csv(data, force=force)
            if data.suffix.lower() == ".dat":
                self.import_data_from_dat(data)

    def _set_data_from_inputdata(self, data, force: bool = False):
        """
        Sets the input data from a dictionary.
        """
        if force:
            self._data = data._data
            self._groups = data._groups
            self._values = data._values
        else:
            for code, group, value in zip(data._data["code"], data._data["group"], data._data["value"]):
                self.set_values(code, value, group, force=force)

    def _set_data_from_csv(self, csv_file: Path, force: bool = False):
        """
        Sets the input data from a CSV file.
        """
        self.import_data(csv_file)
        if not force:
            for code, group, value in zip(self._data["code"], self._data["group"], self._data["value"]):
                if self.validate_value(code, value) is False:
                    raise ValueError(f"Invalid value '{value}' for input '{code}'")
        


class OutputData():
    def __init__(self, parent: Executable):
        self.parent = parent
        self.ready = False
        self._data = {
            
        }

    def _clear(self):
        """
        Clears the output data.
        """
        self.__init__(self.parent)

    def _get_path(self):
        return self.parent.path / f"{self.parent.program.name}.csv"

    def load(self) -> tuple[list[int], list[list[str]]]:
        """
        Loads the output data from the CSV file.
        Raises:
            RuntimeError: If the output data cannot be loaded from the CSV file.
        
        """
        try:
            with open(self._get_path(), "r") as f:
                lines = f.readlines()
        except Exception as e:
            raise RuntimeError(f"Failed to load output data from {self._get_path()}: {e}")
        id_index = self.parent.result_mapping["UM"] - 1
        assert id_index is not None, "UM index is None"
        split_um_values = []
        for line in lines[1:]:
            split_um_values.append(line.strip().split(",")[id_index].split("RRR"))
        assert len(split_um_values[1]) == 2, "UM index is not correct"
        result_indices = [int(split_um[1]) for split_um in split_um_values]
        result_values = []
        for row, line in enumerate(lines[1:]):
            vals = line.strip().split(",")
            for col, val in enumerate(vals):
                result_values[row].append("".join(val.split()) if col != id_index else "".join(split_um_values[row][0].split()))
            # Ensure each row has been initialized
            if len(result_values) <= row:
                result_values.append([])

        return result_indices, result_values
            

    def number_of_results(self) -> int:
        """
        Returns the number of results in the output data.
        """
        return len(self._data)

    def get_value(self, run_id: str, code: str) -> str:
        """
        Returns the value for a given run ID and output code.
        Args:
            run_id (str): The run ID for which to retrieve the value.
            code (str): The output code for which to retrieve the value.
        Returns:
            str: The value for the given run ID and output code.
        """
        if run_id not in self._data:
            raise KeyError(f"Run ID '{run_id}' not found in output data.")
        index = self.parent.result_mapping.get(code)
        if index is None:
            raise KeyError(f"Output code '{code}' not found in result mapping.")
        return self._data[run_id][index - 1]  # Adjust for 0-based indexing

    def get_values(self, code: str) -> list[str]:
        """
        Returns a list of values for a given output code across all runs.
        Args:
            code (str): The output code for which to retrieve the values.
        Returns:
            list[str]: A list of values for the given output code across all runs.
        """
        index = self.parent.result_mapping.get(code)
        if index is None:
            raise KeyError(f"Output code '{code}' not found in result mapping.")
        return [vals[index - 1] for vals in self._data.values()]  # Adjust for 0-based indexing


if __name__ == "__main__":
    from src.models.aevap import AEVAP
    aevap = AEVAP()
    data_controller = DataController(aevap)
    data_controller.import_dat("C:\\Users\\jajones\\Desktop\\rrr\\D1.DAT")
