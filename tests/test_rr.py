import pytest

@pytest.fixture
def sample_data():
    return (True, True)

def test_process_data(sample_data):
    assert sample_data[0], "This is a placeholder test. Replace with actual test logic using sample_data."

def test_input_data(sample_data):
    assert sample_data[1], "This is a placeholder test. Replace with actual test logic using sample_data."