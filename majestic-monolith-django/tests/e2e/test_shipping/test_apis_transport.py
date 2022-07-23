import pytest
from django.apps import apps
from django.shortcuts import resolve_url
from rest_framework import status

from shipping.choices import ShippingItemStatus
from tests.conftest import CustomClient

DistributionCenter = apps.get_model("distribution", "DistributionCenter")
ShippingItem = apps.get_model("shipping", "ShippingItem")
ShippingBatch = apps.get_model("shipping", "ShippingBatch")
ShippingTransport = apps.get_model("shipping", "ShippingTransport")


@pytest.mark.django_db
class TestTransportScenario:
    """
    testing only working scenarios

    1. create transport (ABC001 -> ABC002)
    2. create batch
    3. add existing item to batch
    4. add batch to transport
    5. assign driver to transport
    5. start transport
    6. end transport
    """

    def test_normal_transport(
        self, staff_user, new_transport, new_batch, existing_shipping_item
    ):
        client = CustomClient()
        client.force_login(staff_user)

        # 1. create transport (ABC001 -> ABC002)
        url = resolve_url("transport-list")
        response = client.post(
            url,
            {
                "distribution_center_code_source": new_transport[
                    "distribution_center_code_source"
                ],
                "distribution_center_code_destination": new_transport[
                    "distribution_center_code_destination"
                ],
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        transport_uuid = response.json()["uuid"]

        # 2. create batch
        url = resolve_url("batch-list")
        response = client.post(
            url,
            {
                "alias": new_batch["alias"],
            },
        )

        assert response.status_code == status.HTTP_201_CREATED
        batch_alias = response.json()["alias"]

        # 3. add existing item to batch
        url = resolve_url("batch_shippingitem_add", alias=batch_alias)
        post_param = {
            "tracking_number": existing_shipping_item["tracking_number"],
        }
        response = client.post(url, post_param)
        # print(response.json())
        assert response.status_code == status.HTTP_200_OK

        url = resolve_url("batch_shippingitems", alias=batch_alias)
        response = client.get(url)
        assert len(response.json()["results"]) == 1

        # 4. add batch to transport
        url = resolve_url("transport_batches_add", uuid=transport_uuid)
        post_param = {
            "alias": batch_alias,
        }
        response = client.post(url, post_param)
        assert response.status_code == status.HTTP_200_OK

        url = resolve_url("transport_batches", uuid=transport_uuid)
        response = client.get(url)
        assert len(response.json()["results"]) == 1

        # 5. assign driver to transport
        # TODO api not available yet
        # adddding driver with ORM
        url = resolve_url("transport_batches_start", uuid=transport_uuid)
        response = client.post(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        ShippingTransport.objects.filter(uuid=transport_uuid).update(
            driver_uuid="d916bff8-19b2-40c0-b8f7-46a35f60c511"  # staff user for now
        )
        url = resolve_url("transport_batches_start", uuid=transport_uuid)
        response = client.post(url)
        assert response.status_code == status.HTTP_200_OK

        # 6. end transport
        url = resolve_url("transport_batches_complete", uuid=transport_uuid)
        response = client.post(url)
        assert response.status_code == status.HTTP_200_OK

        # check shipping item and batch data
        batch = ShippingBatch.objects.get(alias=batch_alias)
        assert batch.timestamp_completed
        assert str(batch.shipping_transport.uuid) == transport_uuid
        assert batch.completed

        item = ShippingItem.objects.get(
            tracking_number=existing_shipping_item["tracking_number"]
        )
        assert item.status == ShippingItemStatus.MOVING
        assert (
            item.current_distribution_center_code
            == new_transport["distribution_center_code_destination"]
        )
