from src.models.string_input import StringInput as StringInput
from src.views.string_input_view import Widget as StringInputView
from src.controllers.controller import BaseController
from src.models.input import Input, InputType
from src.views.input_view import InputView, GroupFrame, InputWidget

import tkinter as tk
from pathlib import Path
from enum import Enum

class MultiType(Enum):
    LIST = "_InputStateList"
    SET = "_InputStateSet"
    RANGE = "_InputStateRange"
    SINGLE = "_InputStateSingle"

class _Input():
    def __init__(self, input: Input):
        self.input = input
        self.cat = None
        self.state = _MultiState(self)
        self.group = "0"
        self.values = []
        

    @property
    def state(self):
        return self.multi.state

    @state.setter
    def state(self, value: MultiType):
        if not isinstance(value, MultiType):
            raise ValueError(f"State must be an instance of MultiType Enum, got {type(value)}")
        self.multi.exit()
        match value:
            case MultiType.LIST:
                self.multi = _MultiStateList(self)
            case MultiType.SET:
                self.multi = _MultiStateSet(self)
            case MultiType.RANGE:
                self.multi = _MultiStateRange(self)
            case MultiType.SINGLE:
                self.multi = _MultiStateSingle(self)
            case _:
                raise ValueError(f"Invalid state '{value}' for input '{self.input.code}'.")
        self.multi.enter()

class InputsController(BaseController):
    def __init__(self, model: list[Input]|Input, view: InputView):
        super().__init__()
        self.model: dict[str, _Input] = {}
        if isinstance(model, Input):
            model = [model]
        for input in model:
            self.model[input.code] = _Input(input)
        self.view = view


    def _set_state(self, input: Input, state: MultiType):
        if input.code not in self.model:
            raise ValueError(f"Input code '{input.code}' not found in model.")

        if not isinstance(state, MultiType):
            raise ValueError(f"State must be an instance of MultiType Enum, got {type(state)}")
        
        self.model[input.code].multi.exit()
        match state:
            case MultiType.LIST:
                self.model[input.code]["state"] = _MultiStateList()
            case MultiType.SET:
                self.model[input.code]["state"] = _MultiStateSet()
            case MultiType.RANGE:
                self.model[input.code]["state"] = _MultiStateRange()
            case MultiType.SINGLE:
                self.model[input.code]["state"] = _MultiStateSingle()
            case _:
                raise ValueError(f"Invalid state '{state}' for input '{input.code}'.")
            

class _MultiState():
    def __init__(self, parent: _Input):
        self.parent = parent
        self._type = None
        self._range = {
            "START": None,
            "STOP": None,
            "NUM": 1
        }


    @property
    def range(self):
        if self.values is None or len(self.values) == 0:
            return {"START": None, "STOP": None, "NUM": 1}
        start = self.values[0]
        stop = self.values[-1]
        num = len(self.values)
        return {"START": start, "STOP": stop, "NUM": num}
    
    @property
    def values(self):
        return self.parent.values

    @property
    def type(self):
        return self._type

    @property
    def group(self):
        return self.parent.group

    @group.setter
    def group(self, value):
        self.parent.group = value

    def enter(self):
        pass

    def exit(self):
        pass

def fixed_range(start, stop, num) -> list[float]:
    if num <= 0:
        return []
    step = (stop - start) / (num - 1)
    result = [start + i * step for i in range(num)]
    result[num-1] = stop  # Ensure no floating point error at the end
    return result
    
class _MultiStateSet(_MultiState):
    def enter(self):
        self._type = MultiType.SET
        self.values = list(set(self.values))
        self.group = "-1"

class _MultiStateList(_MultiState):
    def enter(self):
        self._type = MultiType.LIST
        if int(self.group) < 0:
            self.group = "0"

class _MultiStateRange(_MultiState):
    @property
    def range(self):
        return self._range

    def enter(self):
        self._type = MultiType.RANGE
        if int(self.group) < 0:
            self.group = "0"

        if self._type == MultiType.RANGE:
            return
        
        num_values = len(self.values)
        self._range["NUM"] = num_values

        if self._type == MultiType.LIST:
            self._range["START"] = self.values[0] if num_values > 0 else 0
            self._range["STOP"] = self.values[-1] if num_values > 0 else 0

        if self._type == MultiType.SET:
            self._range["START"] = min(self.values) if num_values > 0 else 0
            self._range["STOP"] = max(self.values) if num_values > 0 else 0

    def exit(self):
        self.values = fixed_range(self.range["START"], self.range["STOP"], self.range["NUM"])
            

class _MultiStateSingle(_MultiState):
    def enter(self):
        self.group = "0"
        self.values = [self.values[0]] if self.values else []

            


    