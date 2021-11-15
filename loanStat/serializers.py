from rest_framework import serializers
from .models import Borrowers

class BorrowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowers
        fields = ['id', 'name', 'loan_id', 'state', 'loan_amt', 'amt_paid']
    