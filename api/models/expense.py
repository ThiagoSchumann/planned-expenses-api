from calendar import monthrange
from datetime import date

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now

from api.utils import diff_month
from api.models import User, Periodicity, ExpenseType, TransactionType, TransactionStatus, BankAccount


class Expense(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.PROTECT,
                                verbose_name='Usuário')
    name = models.CharField(max_length=155,
                            verbose_name='Nome')
    expense_type = models.IntegerField(default=ExpenseType.EXPENSE,
                                       choices=ExpenseType.choices,
                                       verbose_name='Tipo de Despesa')
    next_occurrence = models.DateField(verbose_name='Data da próxima ocorrência')
    periodicity_occurrence = models.IntegerField(default=Periodicity.ANNUAL,
                                                 choices=Periodicity.choices,
                                                 verbose_name='Periodicidade')
    include_current_month = models.BooleanField(default=True,
                                                verbose_name='Inclúir mês atual no cálculo da recorrência')
    value = models.FloatField(validators=[MinValueValidator(0.0)],
                              verbose_name='Valor')
    observations = models.TextField(null=True,
                                    blank=True,
                                    max_length=5000,
                                    verbose_name='Observações')

    class Meta:
        verbose_name = 'Despesa'

    def __str__(self):
        return "[{} / {}]".format(self.name, self.expense_type)


@receiver(post_save, sender=Expense)
def expense_pre_save(sender, instance, **kwargs):
    months_to_next_occurrence = diff_month(instance.next_occurrence, now())
    if instance.include_current_month:
        months_to_next_occurrence += 1
        next_month = now().month
    else:
        next_month = now().month + 1

    year_occurrence = now().year
    transaction_value = round(instance.value / months_to_next_occurrence)
    bank_account = BankAccount.objects.get(id=1)

    for month in range(months_to_next_occurrence):
        try:
            due_date = date(year=year_occurrence, month=next_month, day=instance.next_occurrence.day)
        except ValueError:
            due_date = date(year=year_occurrence, month=next_month, day=monthrange(year_occurrence, next_month)[1])

        from api.models import Transaction
        Transaction.objects.update_or_create(
            expanse=instance,
            bank_account_id=bank_account.id,
            transaction_type=TransactionType.CREDIT,
            creation_date_time=now(),
            due_date=due_date,
            payment_date=None,
            value=transaction_value,
            status=TransactionStatus.PENDING
        )

        if next_month == 12:
            next_month = 1
            year_occurrence += 1
        else:
            next_month += 1

    Transaction.objects.update_or_create(
        expanse=instance,
        bank_account_id=bank_account.id,
        transaction_type=TransactionType.DEBIT,
        creation_date_time=now(),
        due_date=instance.next_occurrence,
        payment_date=None,
        value=instance.value,
        status=TransactionStatus.PENDING
    )
