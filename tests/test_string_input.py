import pytest
from src.controllers.string_inputs_controller import InputText

def test_all():
    from src.models.aevap import AEVAP
    from src.controllers.data_controller import InputData
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
    except Exception as e:
        assert False, f"Validation or setting values failed: {e}"
    
    for cursor_position in range(35,41,1):
        print(f"Cursor position: {cursor_position} -> {state_machine.get_input(cursor_position).code}")

    cursor_positions = [0, 1, 4, 5, 17, 18]
    expected_index = [0, 0, 1, 2, 6, 7]
    expected_codes = ["TAE", "TAE", "TAE", "TAE", "TAE", "TWB"]

    for cursor_position in [0,1,4,5,17,18]:
        state_machine.cursor_position = cursor_position
        assert state_machine.input.index == expected_index[cursor_positions.index(cursor_position)]
        assert state_machine.get_input().code == expected_codes[cursor_positions.index(cursor_position)]


    state_machine.cursor_position = 27
    assert state_machine.input.next() == (29, 31), "Next input position is incorrect."
    assert state_machine.input.prev() == (23, 25), "Previous input position is incorrect."
    assert state_machine.get_input().code == "TWB", "Current input code is incorrect."
    assert input_data.number_of_runs() == 3750, "Number of runs is incorrect."