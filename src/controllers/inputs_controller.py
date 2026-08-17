from src.models.string_input import ParseError, StringInput as StringInput
from src.views.string_input_view import Widget as StringInputView
from src.controllers.controller import BaseController
from src.models.input import Input, InputType
from src.views.input_view import InputView, GroupFrame, InputWidget
from src.controllers.data_controller import DataController

import tkinter as tk
from pathlib import Path
from enum import Enum

class MultiType(Enum):
    LIST = "List"
    SET = "Set"
    RANGE = "Range"
    SINGLE = "Single"

    @property
    def open_char(self):
        match self:
            case MultiType.LIST:
                return "["
            case MultiType.SET:
                return "{"
            case MultiType.RANGE:
                return "("
            case MultiType.SINGLE:
                return "["
            case _:
                raise ValueError(f"Invalid MultiType '{self}'.")
            
    @property
    def close_char(self):
        match self:
            case MultiType.LIST:
                return "]"
            case MultiType.SET:
                return "}"
            case MultiType.RANGE:
                return ")"
            case MultiType.SINGLE:
                return "]"
            case _:
                raise ValueError(f"Invalid MultiType '{self}'.")

class _Input():
    def __init__(self, input: Input, controller: BaseController):
        self.controller = controller
        self.input = input
        self._state = _MultiStateSingle(self)
        self.group = "0"
        self.values = []
        self.view = None

    def handle_state_change(self, event):
        new_type = MultiType(event.widget.get())
        self.state = new_type

    def handle_group_change(self, event):
        new_group = event.widget.get()
        self.group = new_group    

    def handle_value_change(self, event):
        entry = self.view.entry.entry.get()
        group = self.view.group.value
        multi_type = MultiType(self.view.multi_type.value)
        text = ""
        if multi_type != MultiType.SET:
            text = group
        text += multi_type.open_char + entry + multi_type.close_char
        self.view.error_label.clear()
        try:
            self.controller.string_input.validate_input(self.input.code, text)
            self.values = self.controller.string_input.set_values_for_input(self.input.code, text)
        except ParseError as e:
            self.view.error_label.message = e.message

        print(f"Input '{self.input.code}' values: {self.values}")
        

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value: MultiType):
        if not isinstance(value, MultiType):
            raise ValueError(f"State must be an instance of MultiType Enum, got {type(value)}")
        self.state.exit()
        match value:
            case MultiType.LIST:
                self._state = _MultiStateList(self)
            case MultiType.SET:
                self._state = _MultiStateSet(self)
            case MultiType.RANGE:
                self._state = _MultiStateRange(self)
            case MultiType.SINGLE:
                self._state = _MultiStateSingle(self)
            case _:
                raise ValueError(f"Invalid state '{value}' for input '{self.input.code}'.")
        self.state.enter()

class InputsController(BaseController):
    def __init__(self, model: list[Input]|Input, view: InputView, input_data: DataController):
        super().__init__()
        self.view = view
        if isinstance(model, Input):
            model = [model]

        self._category_views = self._factory_category_frames(model)
        self.model = self._factory_inputs(model)
        self.string_input = StringInput(input_data)

    def _get_category_view(self, category: str) -> GroupFrame:
        if category is None:
            category = "None"
        if category not in self._category_views:
            raise ValueError(f"Category '{category}' not found in category views.")
        return self._category_views[category]
        
    def _factory_category_frames(self, inputs: list[Input]) -> dict[str, GroupFrame]:
        s = set(input.cat if input.cat is not None else "None" for input in inputs)
        categories: dict[str, GroupFrame] = {}
        for category in sorted(s):
            categories[category] = GroupFrame(self.view.scrollable_frame, group=category)
            self.view.add_category(category, categories[category])
        return categories

    def _factory_inputs(self, inputs: list[Input]) -> dict[str, _Input]:
        model: dict[str, _Input] = {}
        for input in inputs:
            _input = _Input(input, self)
            _input.view = InputWidget(self._get_category_view(input.cat), text=input.code)
            _input.view.multi_type.options = [e.value for e in MultiType]
            _input.view.multi_type.value = _input.state.type.value
            _input.view.group.options = [str(i) for i in range(10)]
            _input.view.group.value = _input.group
            _input.view.description.config(text=input.description)
            _input.view.bind_multi_type_callback(_input.handle_state_change)
            _input.view.bind_group_change(_input.handle_group_change)
            _input.view.bind_modified_callback(_input.handle_value_change)
            self.view.add_input(input.code, _input.view, input.cat)
            model[input.code] = _input
        return model


            

class _MultiState():
    def __init__(self, parent: _Input):
        self.parent = parent
        self._type = MultiType.SINGLE
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

    @values.setter
    def values(self, value: list):
        if not isinstance(value, list):
            raise ValueError(f"Values must be a list, got {type(value)}")
        self.parent.values = value

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
        if self.range["START"] is None or self.range["STOP"] is None or self.range["NUM"] is None:
            self.values = []
            return
        self.values = fixed_range(self.range["START"], self.range["STOP"], self.range["NUM"])
            

class _MultiStateSingle(_MultiState):
    def enter(self):
        self.group = "0"
        self.values = [self.values[0]] if self.values else []

            
if __name__ == "__main__":
    from src.models.aevap import AEVAP
    from src.models.acond import ACOND
    from src.models.asys import ASYS_DX, ASYS_HP
    from src.models.input import Input
    from src.controllers.data_controller import DataController

    root = tk.Tk()
    root.title("Input View Test")
    input_view = InputView(root)
    input_view.pack(fill="both", expand=True)

    inputs = []
    aevap = AEVAP()
    acond = ACOND()
    asys_hp = ASYS_HP()
    asys_dx = ASYS_DX()
    for i, row in enumerate(asys_dx.input_sequence):
        for col, input in enumerate(row):
            input._category = f"Row {i+1}"
            inputs.append(input)

    data_controller = DataController(asys_dx)
    controller = InputsController(inputs, input_view, data_controller)

    root.mainloop()

    