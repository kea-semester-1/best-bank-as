from django.contrib import admin
from best_bank_as.models import  Customer, CustomerLevel, Account, AccountType, TransactionTable, Ledger

# Register your models here.


admin.site.register(Customer)
admin.site.register(CustomerLevel)
admin.site.register(Account)
admin.site.register(AccountType)
admin.site.register(TransactionTable)
admin.site.register(Ledger)