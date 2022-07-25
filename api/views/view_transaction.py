from rest_framework import viewsets

from api.controller import transaction_get_all
from api.serializers import TransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = transaction_get_all()
    serializer_class = TransactionSerializer
