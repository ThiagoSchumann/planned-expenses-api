from django.core.validators import MinValueValidator
from django.db import models
from api.models import Expense, BankAccount, TransactionType, TransactionStatus


class Transaction(models.Model):
    expanse = models.ForeignKey(Expense,
                                on_delete=models.PROTECT,
                                verbose_name='Despesa')
    bank_account = models.ForeignKey(BankAccount,
                                     null=False,
                                     on_delete=models.PROTECT,
                                     verbose_name='Conta Bancária')
    transaction_type = models.IntegerField(default=TransactionType.DEBIT,
                                           choices=TransactionType.choices,
                                           verbose_name='Tipo de transação')
    creation_date_time = models.DateTimeField(auto_now=True,
                                              verbose_name='Data/hora criação')
    due_date = models.DateTimeField(verbose_name='Data de Vencimento')
    payment_date = models.DateField(default=None,
                                    null=True,
                                    blank=True,
                                    verbose_name='Data pagamento')
    value = models.FloatField(validators=[MinValueValidator(0.0)],
                              verbose_name='Valor')
    status = models.IntegerField(default=TransactionStatus.PENDING,
                                 choices=TransactionStatus.choices,
                                 verbose_name='status de transação')

    class Meta:
        verbose_name = 'Transaction'

    def __str__(self):
        return "[{} / {}]".format(self.expanse.name, self.transaction_type)
