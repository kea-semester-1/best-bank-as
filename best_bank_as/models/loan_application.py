from django.contrib.auth.models import User
from django.db import models

from best_bank_as import enums
from best_bank_as.models.core import base_model


class LoanApplication(base_model.BaseModel):
    """Model for customer_application."""

    reason = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.IntegerField(
        choices=enums.ApplicationStatus.choices,
        default=enums.ApplicationStatus.PENDING,
    )
    customer = models.ForeignKey(
        "Customer", on_delete=models.CASCADE, null=True, blank=True
    )

    employee_approved = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="employee"
    )
    supervisor_approved = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="supervisor"
    )

    @property
    def status_name(self) -> str:
        """Get status name."""
        return enums.ApplicationStatus.int_to_enum(self.status)

    def __str__(self) -> str:
        return f"{self.customer} - {self.amount}"
