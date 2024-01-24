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
        return [(choice.name, choice.value) for choice in cls]  # type: ignore


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
    - `LOAN` - Account is a loan account.
    - `INTERNAL` - Account is an internal account,
    meaning that it belongs to the bank.
    """

    SAVINGS = 1
    CHECKING = 2
    LOAN = 3
    INTERNAL = 4


class AccountStatus(BaseEnum):
    """Account status type.

    - `ACTIVE` - Account is active & is approved by employee and supervisor
    - `INACTIVE` - Account is inactive due to a deletion
    - `PENDING` - After customer has requested new account
    - `REJECTED` - Rejected by either employee or supervisor
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


class TransactionStatus(BaseEnum):
    """Status for transactions.

    - `PENDING` - Transaction is pending
    - `PROCESSED` - Transaction is approved
    - `REJECTED` - Transaction is rejected
    """

    PENDING = 1
    PROCESSED = 2
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
