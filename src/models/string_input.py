from enum import Enum, auto


class State(Enum):
    INITIALIZING = "_Initializing"
    APPENDING_VALUE = "_AppendingValue"
    SETTING_VALUE = "_SettingValue"
    CREATING_LIST = "_CreatingList"
    CREATING_RANGE = "_CreatingRange"
    CREATING_SET = "_CreatingSet"
    APPENDING_LIST_VALUE = "_AppendingListValue"
    APPENDING_LIST = "_AppendingList"
    CLOSING_LIST = "_ClosingList"
    SETTING_VALUE_AFTER_NEW_LINE = "_SettingValueAfterNewLine"
    APPENDING_VALUE_AFTER_NEW_LINE = "_AppendingValueAfterNewLine"
    ENDING = "_Ending"

class ParseError(Exception):
    def __init__(self, position: int, message: str):
        super().__init__()
        self._position = position
        self._message = message

    @property
    def position(self):
        return self._position

    @property
    def message(self):
        return self._message

from src.models.rr_data import InputData
class StringInput():
    def __init__(self, data: InputData):
        self._data = data
        self._executable = data.parent
        self._text = ""
        self._initialize()
        self._create_input_list()
        self.input = _Input(self)
        self.cursor_position = 1

    def validate_input(self, input, text: str):
        """
        Validates the input text against the expected input sequence for a specific input.
        Raises a ParseError if any validation fails.
        """
        try:
            fix = 1/0
        except Exception as e:
            print("=================This hasn't been debugged yet.=================")
            raise e
        self._enter_state(State.INITIALIZING)

        while self._iter_position < len(text):
            self._state.enter()
            self._state.validate()
            self._state.exit()
        if self._state.name != State.SETTING_VALUE.value:
            raise ParseError(self.iter_position, f"Unexpected end of input for '{self._input.code}'.")

    def set_values_for_input(self, input, text: str):
        """
        Sets the values for the current input in the data object using the provided text.
        Raises a ParseError if any validation fails.
        """
        try:
            fix = 1/0
        except Exception as e:
            print("=================This hasn't been debugged yet.=================")
            raise e
        
        self._enter_state(State.INITIALIZING)

        while self._iter_position < len(text):
            self._state.enter()
            self._state.set_values()
            self._state.exit()

    def validate(self):
        """
        Validates the input text against the expected input sequence.
        Raises a ParseError if any validation fails.
        """
        self._enter_state(State.INITIALIZING)
        while self._iter_position < len(self._text):
            self._state.enter()
            self._state.validate()
            self._state.exit()
            

        self._is_validated = True

    def set_values(self):
        """
        Sets the values for the current input in the data object using the current text.
        Raises a ParseError if any validation fails.
        """
        if not self._is_validated:
            raise ParseError(self.iter_position, "Input text has not been validated yet.")
        
        self._enter_state(State.INITIALIZING)
        while self._iter_position < len(self._text):
            self._state.enter()
            self._state.set_values()
            self._state.exit()

    @property
    def is_validated(self):
        return self._is_validated

    @property
    def _input(self):
        return self._input_list[self._input_index][0]

    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, value: str):
        self._text = value
        self._is_validated = False

    @property
    def iter_position(self):
        return self._iter_position

    @iter_position.setter
    def iter_position(self, value: int):
        if value < 1 or value > len(self._text) + 1:
            return
        self._iter_position = value

    def _initialize(self):
        """
        Initializes the input text processing by resetting the cursor position, values list, group, and stack.
        """
        self._iter_position = -1
        self._values = []
        self._char = ""
        self._stack = ""
        self._input_index = 0
        self._is_validated = False
        self._reset_group()

    def _enter_state(self, state: State):
        self._set_state(state)
        self._state.enter()

    def _set_state(self, state: State):
        match state:
            case State.INITIALIZING:
                self._state = _Initializing(self)
            case State.APPENDING_VALUE:
                self._state = _AppendingValue(self)
            case State.SETTING_VALUE:
                self._state = _SettingValue(self)
            case State.CREATING_LIST:
                self._state = _CreatingList(self)
            case State.CREATING_RANGE:
                self._state = _CreatingRange(self)
            case State.APPENDING_LIST_VALUE:
                self._state = _AppendingListValue(self)
            case State.CREATING_SET:
                self._state = _CreatingSet(self)
            case State.APPENDING_LIST:
                self._state = _AppendingList(self)
            case State.CLOSING_LIST:
                self._state = _ClosingList(self)
            case State.SETTING_VALUE_AFTER_NEW_LINE:
                self._state = _SettingValueAfterNewLine(self)
            case State.APPENDING_VALUE_AFTER_NEW_LINE:
                self._state = _AppendingValueAfterNewLine(self)
            case State.ENDING:
                self._state = _Ending(self)

    def _create_input_list(self):
        self._input_list = []
        current_input = None
        number_of_lines = len(self._executable.input_sequence)
        for row, line in enumerate(self._executable.input_sequence):
            for col, input in enumerate(line):
                next_input = input
                if col < len(line) and current_input is not None:
                    self._input_list.append((current_input, "input"))
                current_input = next_input
            if row < number_of_lines - 1:
                self._input_list.append((current_input, "newline"))
                current_input = None
        self._input_list.append((current_input, "end"))

    def _read(self):
        """
        Reads the next character from the input text and updates the cursor position.
        If the cursor position exceeds the length of the text, sets the character to an empty string.
        """
        self._iter_position += 1
        if self._iter_position >= len(self._text):
            self._char = ""
        else:
            self._char = self._text[self._iter_position]

    def _push_to_stack(self):
        """
        Appends the current character to the stack.
        """
        self._stack += self._pop_char

    def _next_input(self):
        """
        Moves to the next input in the input list and updates the current input.
        If the end of the input list is reached, sets the current input to None and resets the input index.
        """
        self._values = []
        self._reset_group()
        self._input_index += 1
        if self._input_index >= len(self._input_list):
            self._input_index = 0
            return

    def _validate_value(self):
        """
        Validates the current value in the stack against the current input's validation rules.
        """
        # if self._input is None:
        #     raise ParseError(self.parent.iter_position, "No input is currently being processed.")
        try:
            if self._input.validate(self._stack) is False:
                raise ParseError(self.iter_position, f"Invalid value '{self._stack}' for input '{self._input.code}'")
        except Exception as e:
            raise ParseError(self.iter_position, f"Invalid value '{self._stack}' for input '{self._input.code}': {str(e)}")

    def _validate_group(self):
        """
        Validates the current group in the stack.
        """

        print(f"{self._stack=}", f"{self._iter_position=}")
        if self._stack.isdigit():
            if int(self._stack) < 0:
                raise ParseError(self.iter_position, f"Invalid group '{self._stack}'")
            return
        raise ParseError(self.iter_position, f"Invalid group '{self._stack}'")

    def _push_stack_to_value(self):
        """
        Appends the current value in the stack to the values list.
        """
        self._values.append(self._pop_stack)

    def _set_values(self):
        """
        Sets the values for the current input in the data object using the current stack and group.
        """
        if self._input is None:
            raise ParseError(self.iter_position, "No input is currently being processed.")
        self._data.set_values(self._input.code, self._values, self._group, force=True)


    def _set_group(self):
        """
        Sets the current group to the value in the stack.
        """
        self._group = self._pop_stack

    def _reset_group(self):
        """
        Resets the current group to "0".
        """
        self._group = "0"
    
    def _validate(self):
        """
        Check if the state is a final state.
        """
        if not self._state.final:
            raise ParseError(self.iter_position, f"Missing input for '{self._input.code}'.")

    def _validate_terminal(self):
        """
        Checks if the current character is the expected terminal character for the current input.
        """
        # if self._input is None:
        #     raise ParseError(self.iter_position, "No input is currently being processed.")
        next_expected = self._input_list[self._input_index][1]
        match next_expected:
            case "input":
                expected_terminal = ","
            case "newline":
                expected_terminal = "\n"
            case _:
                return
        char = self._pop_char
        if char != expected_terminal:
            if char == "\n":
                raise ParseError(self.iter_position, f"Unexpected newline for input '{self._input.code}'.")
            raise ParseError(self.iter_position, f"Expected comma for input '{self._input.code}'.")


    @property
    def _pop_char(self):
        """
        Pops the current character and returns its value.
        """
        value = self._char
        self._char = ""
        return value
    
    @property
    def _pop_stack(self):
        """
        Pops the current stack and returns its value.
        """
        value = self._stack
        self._stack = ""
        return value

    @property
    def _pop_value(self):
        """
        Pops the last value from the values list and returns it.
        """
        if not self._values:
            raise ValueError("No values to pop.")
        return self._values.pop()

class _Input():
    def __init__(self, parent: StringInput):
        self.parent = parent

    @property
    def index(self):
        """
        returns the index of the current group or value for the current cursor position.
        """
        splits = 0
        text = self.parent.text
        for idx, chr in enumerate(text, start=1):
            if chr in [",", "\n", "[", "(", "{", "]", ")", "}"]:
                splits += 1
            if idx >= self.parent.cursor_position:
                break
        return splits

    def current(self) -> tuple[int, int]:
        """
        Returns the start and end position of the current input or group. \n
        If the end of the input list is reached, returns the start and end position of the last input.
        """
        try:
            start = self._get_start_of_value(self.index)
            end = self._get_end_of_value(self.index)
            return (start, end)
        except ValueError:
            start = self._get_start_of_value(0)
            end = self._get_end_of_value(0)
            return (start, end)

    def next(self) -> tuple[int, int]:
        """
        Returns the start and end position of the next input or group. \n
        If the end of the input list is reached, returns the start and end position of the last input.
        """
        try:
            start = self._get_start_of_value(self.index+1)
            end = self._get_end_of_value(self.index+1)
            return (start, end)
        except ValueError:
            start = self._get_start_of_value(self.index)
            end = self._get_end_of_value(self.index)
            return (start, end)

    def prev(self) -> tuple[int, int]:
        """
        Returns the start and end position of the previous input. \n
        If the beginning of the input list is reached, returns the start and end position of the first input.
        """
        try:
            start = self._get_start_of_value(self.index-1)
            end = self._get_end_of_value(self.index-1)
            return (start, end)
        except ValueError:
            start = self._get_start_of_value(0)
            end = self._get_end_of_value(0)
            return (start, end)

    def _get_start_of_value(self, index: int) -> int:
        """
        Returns the start position of the value at the given index in the input text. \n
        If the index is out of bounds, raises a ValueError.
        """
        if index <= 0:
            return 0
        index -=1
        for start, char in enumerate(self.parent._text, start=1):
            if char in [",", "\n", "[", "(", "{", "]", ")", "}"]:
                index -= 1
            if index < 0:
                return start
        raise ValueError("Index out of bounds.")

    def _get_end_of_value(self, index: int) -> int:
        """
        Returns the end position of the value at the given index in the input text. \n
        If the index is out of bounds, raises a ValueError.
        """
        # index += 1
        for end, char in enumerate(self.parent._text, start=0):
            if char in [",", "\n", "[", "(", "{", "]", ")", "}"]:
                index -= 1
            if index < 0:
                return end
        raise ValueError("Index out of bounds.")
            
class _State():
    def __init__(self, parent: StringInput):
        self.parent = parent

    @property
    def name(self):
        return self.__class__.__name__
    
    def enter(self):
        # if self.parent._char == "\n":
        #     char = "newline"
        # else:
        #     char = self.parent._char
        # print(f"{self.__class__.__name__} for {self.parent.input.code}: Position: {self.parent.iter_position}, char='{char}', stack='{self.parent._stack}', values={self.parent._values}, group='{self.parent._group}'")
        pass

    def exit(self):
        pass

    def validate(self):
        pass

    def set_values(self):
        pass

    @property
    def final(self):
        return False

class _Initializing(_State):
    def enter(self):
        super().enter()
        self.parent._initialize()
        self.parent._set_state(State.APPENDING_VALUE)

class _AppendingValue(_State):
    def enter(self):
        super().enter()
        self.parent._push_to_stack()
        self.parent._read()

    def exit(self):
        match self.parent._char:
            case ",":
                self.parent._set_state(State.SETTING_VALUE)
            case "\n":
                self.parent._set_state(State.SETTING_VALUE_AFTER_NEW_LINE)
            case "[":
                self.parent._set_state(State.CREATING_LIST)
            case "(":
                self.parent._set_state(State.CREATING_RANGE)
            case "{":
                self.parent._set_state(State.CREATING_SET)
            case "]" | ")" | "}":
                raise ParseError(self.parent.iter_position, f"Unexpected closing bracket '{self.parent._char}'.")
            case _:
                self.parent._set_state(State.APPENDING_VALUE)
                
class _SettingValue(_State):
    def enter(self):
        super().enter()
        self.parent._validate_terminal()

    def validate(self):
        self.parent._validate_value()
        self.parent._push_stack_to_value()

    def set_values(self):
        self.parent._push_stack_to_value()
        self.parent._set_values()

    def exit(self):
        self.parent._next_input()
        self.parent._read()
        match self.parent._char:
            case ",":
                self.parent._set_state(State.SETTING_VALUE)
            case "\n":
                self.parent._set_state(State.SETTING_VALUE_AFTER_NEW_LINE)
            case "[" | "(" | "{":
                raise ParseError(self.parent.iter_position, f"Unnamed group for code '{self.parent.input.code}'.")
            case "]" | ")" | "}":
                raise ParseError(self.parent.iter_position, f"Unexpected closing bracket '{self.parent._char}'.")
            case _:
                self.parent._set_state(State.APPENDING_VALUE)

class _SettingValueAfterNewLine(_State):
    def enter(self):
        super().enter()
        self.parent._validate_terminal()

    def validate(self):
        self.parent._validate_value()
        self.parent._push_stack_to_value()

    def set_values(self):
        self.parent._push_stack_to_value()
        self.parent._set_values()

    def exit(self):
        self.parent._next_input()
        self.parent._read()
        match self.parent._char:
            case ",":
                self.parent._set_state(State.SETTING_VALUE)
            case "\n":
                self.parent._set_state(State.SETTING_VALUE_AFTER_NEW_LINE)
            case "0":
                self.parent._set_state(State.APPENDING_VALUE_AFTER_NEW_LINE)
            case _:
                self.parent._set_state(State.APPENDING_VALUE)

class _CreatingList(_State):
    def enter(self):
        super().enter()
        self.parent._validate_group()
        self.parent._set_group()

    def exit(self):
        self.parent._read()
        match self.parent._char:
            case "]":
                self.parent._set_state(State.CLOSING_LIST)
            case ",":
                self.parent._set_state(State.APPENDING_LIST)
            case "\n":
                raise ParseError(self.parent.iter_position, f"Unexpected newline while creating list for code '{self.parent.input.code}'.")
            case "[" | "(" | "{":
                raise ParseError(self.parent.iter_position, f"Unexpected opening bracket '{self.parent._char}' while creating list for code '{self.parent.input.code}'.")
            case ")" | "}":
                raise ParseError(self.parent.iter_position, f"Unexpected closing bracket '{self.parent._char}' while creating list for code '{self.parent.input.code}'.")
            case _:
                self.parent._set_state(State.APPENDING_LIST_VALUE)

class _AppendingListValue(_State):
    def enter(self):
        super().enter()
        self.parent._push_to_stack()

    def exit(self):
        self.parent._read()
        match self.parent._char:
            case ",":
                self.parent._set_state(State.APPENDING_LIST)
            case "\n":
                raise ParseError(self.parent.iter_position, f"Unexpected newline while creating list for code '{self.parent.input.code}'.")
            case "[" | "(" | "{":
                raise ParseError(self.parent.iter_position, f"Unexpected opening bracket '{self.parent._char}' while creating group for code '{self.parent.input.code}'.")
            case "]":
                self.parent._set_state(State.CLOSING_LIST)
            case ")" | "}":
                raise ParseError(self.parent.iter_position, f"Unexpected closing bracket '{self.parent._char}' while creating group for code '{self.parent.input.code}'.")
            case _:
                self.parent._set_state(State.APPENDING_LIST_VALUE)

class _AppendingList(_State):
    def enter(self):
        super().enter()

    def validate(self):
        self.parent._validate_value()

    def exit(self):
        self.parent._push_stack_to_value()
        self.parent._read()
        match self.parent._char:
            case ",":
                self.parent._set_state(State.APPENDING_LIST)
            case "\n":
                raise ParseError(self.parent.iter_position, f"Unexpected newline while creating list for code '{self.parent.input.code}'.")
            case "[" | "(" | "{":
                raise ParseError(self.parent.iter_position, f"Unexpected opening bracket '{self.parent._char}' while creating group for code '{self.parent.input.code}'.")
            case "]":
                self.parent._set_state(State.CLOSING_LIST)
            case ")" | "}":
                raise ParseError(self.parent.iter_position, f"Unexpected closing bracket '{self.parent._char}' while creating group for code '{self.parent.input.code}'.")
            case _:
                self.parent._set_state(State.APPENDING_LIST_VALUE)

class _ClosingList(_State):
    def exit(self):
        self.parent._read()
        match self.parent._char:
            case ",":
                self.parent._set_state(State.SETTING_VALUE)
            case "\n":
                self.parent._set_state(State.SETTING_VALUE_AFTER_NEW_LINE)
            case _:
                raise ParseError(self.parent.iter_position, f"Unexpected character '{self.parent._char}' after closing list for code '{self.parent.input.code}'.")

class _AppendingValueAfterNewLine(_State):
    def final(self):
        return True
    
    def enter(self):
        super().enter()
        self.parent._push_to_stack()

    def exit(self):
        self.parent._read()
        match self.parent._char:
            case ",":
                self.parent._set_state(State.SETTING_VALUE)
            case "\n":
                self.parent._set_state(State.ENDING)
            case _:
                self.parent._set_state(State.APPENDING_VALUE)

class _CreatingRange(_State):
    def enter(self):
        super().enter()
        raise NotImplementedError("Creating range is not implemented yet.")

class _CreatingSet(_State):
    def enter(self):
        super().enter()
        raise NotImplementedError("Creating set is not implemented yet.")

class _Ending(_State):
    def final(self):
        return True
    
    def enter(self):
        super().enter()
        if self.parent._input_index != 0:
            raise ParseError(self.parent.iter_position, f"Unexpected input '{self.parent._input.code}' after end of input text.")

    def exit(self):
        self.parent._read()
        match self.parent._char:
            case "":
                return
            case _:
                raise ParseError(self.parent.iter_position, f"Multi input text is not implemented yet. Unexpected character '{self.parent._char}' after end of input text.")