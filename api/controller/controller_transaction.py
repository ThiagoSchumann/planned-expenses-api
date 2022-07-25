from api.models import Transaction


def transaction_get_all():
    return Transaction.objects.all()
