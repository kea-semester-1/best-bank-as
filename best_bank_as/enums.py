from django.db.models import IntegerChoices


class BaseEnum(IntegerChoices):
    """Base enum class."""

    @classmethod
    def int_to_enum(cls, value: int) -> str:
        """Convert an integer to a string representation of an enum."""
        return cls.choices[value - 1][1]

    @classmethod
    def name_value_pairs(cls) -> list[tuple[str, int]]:
        """Get name value pairs."""
        return [(name, value) for name, value in cls.choices]


class ApplicationStatus(BaseEnum):
    """
    Application status enum.

    - `PENDING` - Application is pending
    - `EMPLOYEE_APPROVED` - Application is approved by employee
    - `SUPERVISOR_APPROVED` - Application is approved by supervisor
    - `REJECTED` - Application is rejected
    """

    PENDING = 1
    EMPLOYEE_APPROVED = 2
    SUPERVISOR_APPROVED = 3
    REJECTED = 4


class CustomerRank(BaseEnum):
    """Customer rank enum.

    - `BLUE` - Customer is a blue rank.
    - `SILVER` - Customer is a silver rank.
    - `GOLD` - Customer is a gold rank.
    """

    BLUE = 1
    SILVER = 2
    GOLD = 3


class AccountType(BaseEnum):
    """Account type enum.

    - `SAVINGS` - Account is a savings account.
    - `CHECKING` - Account is a checking account.
    """

    SAVINGS = 1
    CHECKING = 2


class AccountStatus(BaseEnum):
    """Account status type.

    - `Active` - Account is active & is approved by staff and supervisor
    - `Inactive` - Account is inactive due to a deletion
    - `Pending` - After customer has requested new account
    - `Rejected` - Rejected by either staff or supervisor
    """

    ACTIVE = 1
    INACTIVE = 2
    PENDING = 3
    REJECTED = 4


class CustomerStatus(BaseEnum):
    """Customer status enum.

    - `PENDING` - Customer is pending
    - `APPROVED` - Customer is approved
    - `REJECTED` - Customer is rejected
    """

    PENDING = 1
    APPROVED = 2
    REJECTED = 3


class LoanStatus(BaseEnum):
    """Loan status enum.

    - `IN_PROGRESS` - Loan is in progress
    - `PAID` - Loan is paid
    - `ABORTED` - Loan is aborted
    """

    IN_PROGRESS = 1
    PAID = 2
    ABORTED = 3
