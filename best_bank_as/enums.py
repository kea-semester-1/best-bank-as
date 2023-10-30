from django.db.models import IntegerChoices


class BaseEnum(IntegerChoices):
    """Base enum class."""

    @classmethod
    def int_to_enum(cls, value: int) -> str:
        """Convert an integer to a string representation of an enum."""
        return cls.choices[value - 1][1]


class ApplicationStatus(BaseEnum):
    """
    Application status enum.

    - `PENDING` - Application is pending.
    - `APPROVED` - Application is approved.
    - `REJECTED` - Application is rejected.
    """

    PENDING = 1
    APPROVED = 2
    REJECTED = 3


class ApplicationType(BaseEnum):
    """
    Application type enum.

    - `LOAN` - Application is for a loan.
    """

    LOAN = 1


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
    """ Account status type
    
    - `Active` - Account is active
    - `Inactive` - Account is inactive due to a deletion
    - `Pending` - After customer has requested new account
    """
    ACTIVE = 1
    INACTIVE = 2
    PENDING = 3


class CustomerStatus(BaseEnum):
    """Customer status enum.

    - `PENDING` - Customer is pending
    - `APPROVED` - Customer is approved
    - `REJECTED` - Customer is rejected
    """

    PENDING = 1
    APPROVED = 2
    REJECTED = 3
