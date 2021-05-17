from django.urls import path

from .consumers import TransactionConsumer


urlpatterns = [
    path('transactions/<str:transaction_id>', TransactionConsumer),
]
