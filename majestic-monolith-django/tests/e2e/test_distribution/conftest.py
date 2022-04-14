import pytest


@pytest.fixture
def new_center_param():
    return {
        "center_code": "NEWYORK001",
        "name": "NewYork 001",
        "staff_members": {
            "uuid": ['b77a1d4f921d460a9eb179d45ba56f51']
        }
    }


@pytest.fixture
def existing_center():
    return {
        "uuid": "48574f05-a29e-4735-a817-839b228c3e82",
        "center_code": "ABC001",
        "name": "CENTER-ABC",
    }
