from enum import Enum

class InputType(Enum):
    LIST = 1
    SET = 2
    RANGE = 3

class Input():
    def __init__(self, 
                 code: str,
                 data_type: type,
                 description:str,
                 value = None,
                 is_required: bool = False):
        
        self._code = code
        self._data_type = data_type
        self._description = description
        self._is_required = is_required
        self._value = []
        self.value = value

    @property
    def description(self):
        return self._description

    @property
    def required(self):
        return self._is_required

    @property
    def data_type(self):
        return self._data_type

    @property
    def code(self):
        return self._code

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_values):
        if new_values is None:
            new_values = []
        elif not isinstance(new_values, (list, tuple)):
            new_values = [new_values]

        values = []
        valid = True
        try:
            for value in new_values:
                new_value = self._coerce(value)
                values.append(new_value)
                if not self.validate(new_value):
                    valid = False
        except Exception as e:
            raise ValueError(f"Error coercing value for {self.code}: {e}") from e
        if valid:
            self._value = values

    def _coerce(self, value):
        if value is None:
            return None
        if isinstance(value, str):
            if value == "None" or value == "":
                return None
        try:
            return self.data_type(value)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Error coercing value for {self.code}: {e}") from e
    
    def __eq__(self, other):
        if isinstance(other, Input):
            try:
                return self.value == other.value
            except Exception as e:
                print(f"Error comparing Input objects: {e}")
                return False
        return False
    
    def __str__(self):
        if self.value is None:
            return ""
        return str(self.value)
    
    def __repr__(self):
        return f"code: {self.code}, value: {self.value}, description: {self.description}"

    def validate(self, value):
        value = self._coerce(value)

        if value is None:
            return not self._is_required

        return self._validate(value)

    def _validate(self, value):
        return True
    
class InputClass(Input):
    def __init__(self, 
                 options: list,
                 *args,
                 **kwargs):
        self.options = options
        super().__init__(*args, **kwargs)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_values):
        if new_values is None:
            new_values = []
        elif not isinstance(new_values, (list, tuple)):
            new_values = [new_values]
        values = []
        set_values = set()
        valid = True
        try:
            for value in new_values:
                new_value = self._coerce(value)
                values.append(new_value)
                set_values.add(new_value)
            for value in set_values:
                valid = self.validate(value)
                if not valid:
                    break
        except Exception as e:
            raise ValueError(f"Error coercing value for {self.code}: {e}") from e
        if valid:
            self._value = values

    def __repr__(self):
        return f"code: {self.code}, value: {self.value}, description: {self.description}, options: {self.options}"

    def _validate(self, value):
        if not super()._validate(value):
            return False
        if self.options is not None and value not in self.options:
            return False
        return True

    
class InputRange(Input):
    def __init__(self,
                 min_value = None,
                 max_value = None,
                 *args,
                 **kwargs):
        self._min_value = min_value
        self._max_value = max_value

        self._range_data = {
            "min": None,
            "max": None,
            "num_values": None
        }
        super().__init__(*args, **kwargs)
            
    @property
    def min_value(self):
        return self._min_value

    @property
    def max_value(self):
        return self._max_value

    @property
    def min(self):
        return min(self._values) if self._values else None

    @property
    def max(self):
        return max(self._values) if self._values else None
    
    @property
    def input_type(self):
        return self._input_type

    @input_type.setter
    def input_type(self, value: InputType):
        if not isinstance(value, InputType):
            raise ValueError(f"input_type must be an instance of InputType Enum, got {type(value)}")
        if value == InputType.SET:
            self._values = list(set(self._values))
            self._group = "-1"
        if value == InputType.LIST:
            self._range_data["min"] = self.min
            self._range_data["max"] = self.max
            self._range_data["num_values"] = len(self._values)
        if value == InputType.RANGE:
            self._range_data["min"] = self.min
            self._range_data["max"] = self.max
            self._range_data["num_values"] = len(self._values)
        self._input_type = value

    @property
    def value(self):
        return self._values

    @value.setter
    def value(self, new_values):
        if new_values is None:
            new_values = []
        elif not isinstance(new_values, (list, tuple)):
            new_values = [new_values]
        values = []
        set_values = set()
        try:
            for value in new_values:
                new_value = self._coerce(value)
                values.append(new_value)
                set_values.add(new_value)
        except Exception as e:
            raise ValueError(f"Error coercing value for {self.code}: {e}") from

        if self.min_value is not None and min(set_values) < self.min_value:
            raise ValueError(f"Value {value} is less than the minimum value {self.min_value} for {self.code}.")
        if self.max_value is not None and max(set_values) > self.max_value:
            raise ValueError(f"Value {value} is greater than the maximum value {self.max_value} for {self.code}.")
        
        self._values = values

    def __repr__(self):
        return f"code: {self.code}, value: {self.value}, description: {self.description}, min_value: {self.min_value}, max_value: {self.max_value}"

    def _validate(self, value):
        if not super()._validate(value):
            return False
        if self.min_value is not None and value < self.min_value:
            print(f"Value {value} is less than the minimum value {self.min_value} for {self.code}.")
            return False
        if self.max_value is not None and value > self.max_value:
            print(f"Value {value} is greater than the maximum value {self.max_value} for {self.code}.")
            return False
        return True