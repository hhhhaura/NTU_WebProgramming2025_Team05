from rest_framework import serializers
from Transaction.models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    creditor = serializers.CharField(source='creditor.username')
    debtor = serializers.CharField(source='debtor.username')

    class Meta:
        model = Transaction
        fields = ['creditor', 'debtor', 'amount', 'created_at', 'slug']

class DebtSerializer(serializers.Serializer):
    debtor = serializers.CharField()
    creditor = serializers.CharField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

class TotalDebtSerializer(serializers.Serializer):
    user = serializers.CharField()
    net_balance = serializers.DecimalField(max_digits=10, decimal_places=2)