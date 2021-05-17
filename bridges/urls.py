from django.urls import path

from . import views


app_name = 'bridges'

urlpatterns = [
    path(
        'transactions/<str:transaction_id>',
        views.TransactionDetailView.as_view(),
        name='transaction_detail'),
]
