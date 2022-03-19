import pytest


@pytest.fixture
def existing_shipping_item():
    return {
        "uuid": "48574f05-a29e-4735-a817-839b228c3e82",
        "tracking_number": "202201011234",
        "sku": "123211"
    }


@pytest.fixture
def new_shipping_item():
    return {
        "sku": "123211231",
    }


@pytest.fixture
def new_batch():
    return {
        "alias": "AB-132",
    }


@pytest.fixture
def new_transport():
    return {
        "distribution_center_code_source": "ABC001",
        "distribution_center_code_destination": "ABC002",
    }
