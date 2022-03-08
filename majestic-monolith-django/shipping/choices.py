# -*- coding: utf-8 -*-
from django.db import models


class ShippingItemStatus(models.TextChoices):
    CREATED = "CREATED", "Created"
    MOVING = "MOVING", "Moving"
    COMPLETED = "COMPLETED", "Completed"
    DAMAGED = "DAMAGED", "Damaged"
    LOST = "LOST", "Lost"
