from rest_framework import serializers

from api.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'expanse', 'bank_account', 'transaction_type', 'creation_date_time', 'payment_date', 'value',
                  'status')
