from enum import Enum, auto
class State(Enum):
    INITIALIZING = auto()
    APPENDING_VALUE = auto()
    SETTING_VALUE = auto()
    CREATING_LIST = auto()
    CREATING_RANGE = auto()
    CREATING_SET = auto()
    APPENDING_LIST_VALUE = auto()
    APPENDING_LIST = auto()
    CLOSING_LIST = auto()
    SETTING_VALUE_AFTER_NEW_LINE = auto()
    APPENDING_VALUE_AFTER_NEW_LINE = auto()
    ENDING = auto()

class ParseError(Exception):
    def __init__(self, position: int, message: str):
        self._position = position
        super().__init__(message)

    @property
    def position(self):
        return self._position

from RRData import InputData
class InputText():
    def __init__(self, data: InputData):
        self._data = data
        self._executable = data.parent
        self._text = ""
        self._initialize()
        self._create_input_list()
        self.input = _Input(self)
        self.cursor_position = 1

    from RR import Input

    def get_input(self, cursor_position: int = None) -> Input:
        """
        Returns the input at the given cursor position. \n
        Args:
            cursor_position (int): The position of the cursor in the input text. If None, uses the current cursor position.
        Returns:
            Input: The input at the given cursor position.
        Raises:
            ValueError: If the cursor position is out of bounds.
        """
        if cursor_position is None or cursor_position < 1 or cursor_position > len(self._text):
            cursor_position = self.cursor_position
        
        self._enter_state(State.INITIALIZING)
        while self._iter_position < cursor_position:
            self._state.enter()
            self._state.validate()
            self._state.exit()

        return self._input

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
    def __init__(self, parent: InputText):
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
    def __init__(self, parent: InputText):
        self.parent = parent
        
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

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from pathlib import Path
from RRData import InputData
from tkinterdnd2 import DND_FILES, TkinterDnD

# from rr_input_text import InputText

class Information(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.label = tk.Label(self, text="Current Code: None")
        self.label.pack(side="top", fill="x")

        self.description_label = tk.Label(self, text="Description: None")
        self.description_label.pack(side="top", fill="x")

        self._input = None

    @property
    def input(self):
        return self._input

    @input.setter
    def input(self, value):
        self._input = value
        if value is not None:
            self.label.config(text=f"Current Code: {value.code}")
            self.description_label.config(text=f"Description: {value.description}")
        else:
            self.label.config(text="Current Code: None")
            self.description_label.config(text="Description: None")
        
class StringInput(ttk.Frame):
    def __init__(self, string_input: InputText, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.string_input = string_input
        self._inserting = False
        self._updating = False

        # Create the scrollbar
        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side="right", fill="y")

        self.text_widget = tk.Text(
            self,
            wrap="none",
            yscrollcommand=scrollbar.set,
            font=("Arial", 10),
            padx=10,
            pady=10,
        )
        self.text_widget.pack(side="bottom", fill="both", expand=True)

        scrollbar.config(command=self.text_widget.yview)
        
        self.text_widget.bind("<<Modified>>", self.on_text_change)
        self.text_widget.bind("<FocusIn>", self.start_update)
        self.text_widget.bind("<FocusOut>", self.end_update)
        self.text_widget.bind("<ButtonRelease-1>", self.on_click)

        self.text_widget.drop_target_register(DND_FILES)
        self.text_widget.dnd_bind("<<Drop>>", self.handle_drop)

        self.suppress_modified = False

    def on_click(self, event=None):
        self.start_update(event)
        self.text_widget.focus_set()
        self.set_cursor_position()
        print(f"{self.cursor_position=}, {self.string_input.cursor_position=}, {self.string_input.input.index=}")
        self.update_input_label()
        if self._inserting:
            start, end = self.string_input.input.current()
            self.select(start, end)

    def start_update(self, event=None):
        if self._updating:
            return

        self._updating = True
        #self.text_widget.bind("<KeyPress-Up>", self.do_nothing)
        self.text_widget.bind("<KeyRelease-Up>", self.move_cursor)

        #self.text_widget.bind("<KeyPress-Down>", self.do_nothing)
        self.text_widget.bind("<KeyRelease-Down>", self.move_cursor)

        self.text_widget.bind("<KeyPress-Left>", self.start_move_cursor)
        self.text_widget.bind("<KeyRelease-Left>", self.end_move_cursor_left)

        self.text_widget.bind("<KeyPress-Right>", self.start_move_cursor)
        self.text_widget.bind("<KeyRelease-Right>", self.end_move_cursor_right)

        self.text_widget.bind("<KeyPress-Tab>", self.do_nothing)
        self.text_widget.bind("<KeyRelease-Tab>", self.tab_cursor_right)

        self.text_widget.bind("<<Paste>>", self.on_paste)

    def do_nothing(self, event=None):
        if self._inserting:
            return "break"

        if self._updating:
            #remove focus from the text_widget to trigger the end_update method
            self.text_widget.focus_set()        

    def on_paste(self, event=None):
        self.start_update(event)
        self.text_widget.after(1, self.end_update)
    
    def end_update(self, event=None):
        if not self._updating:
            return

        self.text_widget.unbind("<KeyPress-Up>")
        self.text_widget.unbind("<KeyRelease-Up>")
        self.text_widget.unbind("<KeyPress-Down>")
        self.text_widget.unbind("<KeyRelease-Down>")
        self.text_widget.unbind("<KeyPress-Left>")
        self.text_widget.unbind("<KeyRelease-Left>")
        self.text_widget.unbind("<KeyPress-Right>")
        self.text_widget.unbind("<KeyRelease-Right>")
        self.text_widget.unbind("<KeyPress-Tab>")
        self.text_widget.unbind("<KeyRelease-Tab>")
        self.text_widget.unbind("<<Paste>>")

        self.on_text_change(force=True)
        self._updating = False

    def on_text_change(self, event=None, force=False):
        if self.suppress_modified:
            self.text_widget.edit_modified(False)
            return
        
        if not force and not self.text_widget.edit_modified():
            return
        
        self.text_widget.edit_modified(False)
        self._flush()

    def set_cursor_position(self):
        self.string_input.cursor_position = self.cursor_position

    def start_move_cursor(self, event):
        self.set_cursor_position()
        self._current_input_index = self.string_input.input.index

    def move_cursor(self, event):
        self.set_cursor_position()
        self.update_input_label()
        if self._inserting:
            start, end = self.string_input.input.current()
            self.select(start, end)

    def end_move_cursor_left(self, event):
        self.set_cursor_position()
        if self._inserting:
            if self._current_input_index == self.string_input.input.index:
                start, end = self.string_input.input.prev()
            else:
                start, end = self.string_input.input.current()
            self.select(start, end)
        self.update_input_label()

    def end_move_cursor_right(self, event):
        self.set_cursor_position()
        if self._inserting:
            if self._current_input_index == self.string_input.input.index:
                start, end = self.string_input.input.next()
            else:
                start, end = self.string_input.input.current()
            self.select(start, end)
        self.update_input_label()

    def tab_cursor_right(self, event):
        self.set_cursor_position()
        start, end = self.string_input.input.next()
        if self._inserting:
            self.select(start, end)
        else:
            self.text_widget.mark_set("insert", f"1.0 + {start} chars")
        self.update_input_label()
        return "break"

    def update_input_label(self):
        input = self.string_input.get_input()
        self.master.information.input = input

    @property
    def cursor_position(self) -> int:
        try:
            return int(self.text_widget.count("1.0", "insert", "chars")[0])
        except Exception:
            return 0

    def select(self, start: int, end: int):
        start_idx = f"1.0 + {start} chars"
        end_idx = f"1.0 + {end} chars"

        self.text_widget.tag_remove("sel", "1.0", tk.END)
        self.text_widget.tag_add("sel", start_idx, end_idx)

        self.text_widget.mark_set("insert", start_idx)
        self.text_widget.see(start_idx)


    def _flush(self):
        self.text_widget.tag_remove("red", "1.0", tk.END)
        self.text_widget.tag_remove("black", "1.0", tk.END)
        self.string_input.text = self.text_widget.get("1.0", tk.END)
        try:
            self.string_input.validate()
            self.string_input.set_values()
            self.master.error_label.clear_error()
        except Exception as e:
            message = e.__str__()
            position = e.position
            self.show_error(message, position)

    def show_error(self, message: str, position: int):
        self.master.error_label.set_error(message)
        self.text_widget.tag_add("black", "1.0", f"1.0 + {position-1} chars")
        self.text_widget.tag_add("red", f"1.0 + {position-1} chars", tk.END)
        self.text_widget.tag_configure("red", foreground="red")
        self.text_widget.tag_configure("black", foreground="black")
        self.text_widget.mark_set("insert", f"1.0 + {position} chars")

    def handle_drop(self, event):
        file_path = event.data
        if file_path.startswith("{") and file_path.endswith("}"):
            file_path = file_path[1:-1]
        file=Path(file_path)
        if file.is_file():
            try:
                self.end_update()
                self.input_data.set_data(data = file)
                self.master.refresh()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load data from {file_path}: {e}")


class Commands(ttk.Frame):
    def __init__(self, text_frame: StringInput, input_data: InputData, string_input, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_frame = text_frame
        self.input_data = input_data
        self.string_input = string_input

        self.toggle_button = tk.Button(self, text="Toggle Inserting Mode", command=self.toggle_inserting_mode)
        self.toggle_button.pack(side="left", fill="x", expand=True)

        self.write_button = tk.Button(self, text="Write Input File", command=self.input_data.write_input_file)
        self.write_button.pack(side="left", fill="x", expand=True)

        self.set_file_button = tk.Button(self, text="Set Input File Name", command=self.set_input_file_name)
        self.set_file_button.pack(side="left", fill="x", expand=True)

        self.export_button = tk.Button(self, text="Export Input File")
        self.export_button.pack(side="left", fill="x", expand=True)

    def set_input_file_name(self):
        current_name = self.input_data.input_file

        new_name = tk.filedialog.asksaveasfilename(
            initialfile=Path(current_name).name if current_name else "",
            defaultextension=".dat",
            filetypes=[
                ("DAT files", "*.dat"),
                ("All files", "*.*")    
            ]
        )
        try:
            if new_name:
                self.input_data.set_input_file_name(Path(new_name).name)
        except ValueError as e:
            tk.messagebox.showerror("Invalid Input File Name", str(e))

    def toggle_inserting_mode(self):
        self.text_frame._inserting = not self.text_frame._inserting
        if self.text_frame._inserting:
            self.toggle_button.config(text="Inserting Mode: ON")
            start, end = self.string_input.input.current()
            self.text_frame.select(start, end)
        else:
            self.toggle_button.config(text="Inserting Mode: OFF")
            self.text_frame.text_widget.tag_remove("sel", "1.0", tk.END)

class ErrorLabel(ttk.Label):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(text="", foreground="red")

    def set_error(self, message: str):
        self.config(text=message)

    def clear_error(self):
        self.config(text="")

class Widget(ttk.Frame):
    def __init__(self, input_data: InputData, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_data = input_data
        self.string_input = self.input_data.string_input
        self.information = Information(master=self)
        self.text = StringInput(master=self, string_input=self.string_input)
        self.commands = Commands(master=self, text_frame=self.text, input_data=self.input_data, string_input=self.string_input)
        self.error_label = ErrorLabel(master=self)

        self.information.pack(side="top", fill="x")
        self.text.pack(side="top", fill="both", expand=True)
        self.error_label.pack(side="bottom", fill="x")
        self.commands.pack(side="bottom", fill="x")

        # add a margin to the frame
        self.pack(padx=10, pady=10)

        # self.text._set_text_without_trigger(str(self.input_data))

    # def set(self, text: str):
    #     self.text._set_text_without_trigger(text)

    # def get(self) -> str:
    #     return self.text.text_widget.get("1.0", tk.END)

    # def refresh(self):
    #     self.text._set_text_without_trigger(str(self.input_data))

if __name__ == "__main__":
    from AEVAP import AEVAP
    from RRData import InputData
    aevap = AEVAP()
    input_data = aevap.data.input

    state_machine = InputText(input_data)

    text = "2[80,70,68,60,59],3[70,60,50,59,58],5[105,106,107,108,109],40,50,5,53,,,,\n"
    text +=  "1[417,135,100,200,300],1,12,6,30,46,4[4000,4100,4200,4300,4400,4500],S,24,0,0,0,10,-1,75,0,Z16,0,0,0,0,11S,11,,,\n0\n"

    state_machine.text = text

    try:
        state_machine.validate()
        print("Input text is valid.")
        state_machine.set_values()
        print("Values set in the data object.")
    except ParseError as e:
        print(f"Parse error at position {e.position}: {e}")
        print(f"{state_machine.text[:e.position]}")

    print(f"Total number of runs: {aevap.data.input.number_of_runs()}")
    # state_machine.input.next()
    
    for cursor_position in range(35,41,1):
        print(f"Cursor position: {cursor_position} -> {state_machine.get_input(cursor_position).code}")

    for cursor_position in range(0, 40, 1):
        state_machine.cursor_position = cursor_position
        print(f"Cursor position: {cursor_position} -> {state_machine.input.index}")


    state_machine.cursor_position = 27
    print(f"Setting cursor position to {state_machine.cursor_position}")
    print(f"Cursor position: {state_machine.cursor_position} -> {state_machine.get_input().code}")
    print(f"Next cursor position: {state_machine.input.next()}")
    print(f"Previous cursor position: {state_machine.input.prev()}")

    assert state_machine.input.next() == (29, 31), "Next input position is incorrect."
    assert state_machine.input.prev() == (23, 25), "Previous input position is incorrect."
    assert state_machine.get_input().code == "TWB", "Current input code is incorrect."
    assert input_data.number_of_runs() == 3750, "Number of runs is incorrect."