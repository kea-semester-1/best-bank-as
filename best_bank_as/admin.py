from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from best_bank_as.db_models.account import Account
from best_bank_as.db_models.bank import Bank
from best_bank_as.db_models.customer import Customer
from best_bank_as.db_models.ledger import Ledger
from best_bank_as.db_models.loan import Loan
from best_bank_as.db_models.loan_application import LoanApplication
from best_bank_as.db_models.transaction import Transaction
from best_bank_as.models import CustomUser

# Register your models here.


admin.site.register(Customer)
admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Ledger)
admin.site.register(LoanApplication)
admin.site.register(Loan)
admin.site.register(Bank)
admin.site.register(CustomUser, UserAdmin)
