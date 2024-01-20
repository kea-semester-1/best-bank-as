from django.db import models

from best_bank_as import enums
from best_bank_as.models.core import base_model


class Loan(base_model.BaseModel):
    """Model for loan."""

    customer = models.OneToOneField(
        "Customer", on_delete=models.CASCADE, null=True, blank=True
    )
    loan_application = models.OneToOneField(
        "LoanApplication", on_delete=models.CASCADE, null=True, blank=True
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.IntegerField(
        choices=enums.LoanStatus.choices,
        default=enums.LoanStatus.IN_PROGRESS,
    )
