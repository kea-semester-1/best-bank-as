from typing import Any

from django.contrib.auth.models import User
from django.db import models

from best_bank_as import enums
from best_bank_as.db_models.core import base_model
from best_bank_as.models import CustomUser


class LoanApplication(base_model.BaseModel):
    """Model for customer_application."""

    reason = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=15, decimal_places=2)

    status = models.IntegerField(
        choices=enums.ApplicationStatus.choices,
        default=enums.ApplicationStatus.PENDING,
    )
    customer = models.ForeignKey(
        "Customer", on_delete=models.CASCADE, null=True, blank=True
    )

    employee_approved = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="employee",
    )
    supervisor_approved = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="supervisor",
    )

    @property
    def status_name(self) -> str:
        """Get status name."""
        return enums.ApplicationStatus.int_to_enum(self.status)

    @property
    def approved(self) -> bool:
        """Check if the loan application is approved."""
        return self.employee_approved and self.supervisor_approved

    def reject(self) -> None:
        """Soft delete the loan application."""
        self.status = enums.ApplicationStatus.REJECTED
        self.save()

    def employee_approve(self, user: User) -> None:
        """Employee approve the loan application."""
        if self.status != enums.ApplicationStatus.PENDING:
            raise ValueError("Cannot approve a non-pending application.")

        self.status = enums.ApplicationStatus.EMPLOYEE_APPROVED
        self.employee_approved = user
        self.save()

    def supervisor_approve(self, user: User) -> None:
        """Supervisor approve the loan application."""
        if self.status != enums.ApplicationStatus.EMPLOYEE_APPROVED:
            raise ValueError("Cannot approve a non-employee approved application.")

        self.status = enums.ApplicationStatus.SUPERVISOR_APPROVED
        self.supervisor_approved = user
        self.save()

    @classmethod
    def filter_fmt(
        cls, **filter_params: dict[str, Any]
    ) -> list[tuple["LoanApplication", str]]:
        """Filter and format loan applications."""
        loan_applications = cls.objects.filter(**filter_params)
        statuses = [
            enums.ApplicationStatus.int_to_enum(application.status)
            for application in loan_applications
        ]
        return list(zip(loan_applications, statuses, strict=True))

    def __str__(self) -> str:
        return f"{self.customer} - {self.amount}"
