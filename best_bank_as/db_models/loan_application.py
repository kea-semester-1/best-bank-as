from typing import Any
from django.db import models

from best_bank_as import enums
from best_bank_as.db_models.core import base_model


class LoanApplication(base_model.BaseModel):
    """Model for loan_application."""

    reason = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.IntegerField(
        choices=enums.ApplicationStatus.choices,
        default=enums.ApplicationStatus.PENDING,
    )
    customer = models.ForeignKey(
        "Customer", on_delete=models.CASCADE, null=True, blank=True
    )

    # test

    @property
    def status_name(self) -> str:
        """Get status name."""
        return enums.ApplicationStatus.int_to_enum(self.status)
    
    @staticmethod
    def formatted_by_filter(**kwargs: Any) -> list[tuple["LoanApplication", str]]:
        loan_applications = LoanApplication.objects.filter(**kwargs)
        statuses = [
            enums.ApplicationStatus.int_to_enum(application.status)
            for application in loan_applications
        ]

        return list(zip(loan_applications, statuses))

    def __str__(self) -> str:
        return f"{self.customer} - {self.amount}"
