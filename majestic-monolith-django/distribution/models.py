import uuid
import logging

from django.db import models

logger = logging.getLogger("django.eventlogger")


class DistributionCenter(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    center_code = models.CharField(max_length=16, db_index=True)
    name = models.CharField(max_length=64, db_index=True)
    # use Arrayfield if using postgresql
    staff_members = models.JSONField(default=dict, blank=True, null=True,
                                     help_text="{'uuid': ['uuid','uuid']}")

    class Meta:
        app_label = "distribution"
        db_table = "distribution_distribution_center"

    def __str__(self):
        return f"[DistributionCenter:{self.center_code}]{self.name}"
