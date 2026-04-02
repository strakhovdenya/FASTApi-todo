import pytest



def test_equal_or_not_equal():
    assert 3 == 3
    assert 3 != 1

def test_is_instance():
    assert isinstance('3', str)
    assert not isinstance('3', int)
    assert ('hello' == 'world') is False

def test_type():
    assert type('hello' is str)
    assert type('hello' is not int)

def test_list():
    num_list = [1,2,3]
    any_list = [False, False]
    assert all(num_list)
    assert not any(any_list)

class Student:
    def __init__(self, first_name:str, last_name:str, major: str, years:int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years

@pytest.fixture
def default_employee():
    return Student('John', 'Doe', 'Computer Science', 3)

def test_person_initialisation(default_employee):
    assert default_employee.first_name == 'John', 'First name should be "John"'
    assert default_employee.last_name == 'Doe', 'Last name should be "Doe"'
    assert default_employee.major == 'Computer Science'
    assert default_employee.years == 3