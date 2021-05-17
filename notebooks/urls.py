from django.urls import path

from . import views


app_name = 'notebooks'

urlpatterns = [
    path(
        'records/transaction/<str:transaction_id>/confirm',
        views.RecordConfirmView.as_view(),
        name='record_confirm'),
    path(
        'records',
        views.RecordListView.as_view(),
        name='record_list'),
    path(
        'records/<int:record_id>',
        views.RecordDetailView.as_view(),
        name='record_detail'),
    path(
        'sheets/transaction/<str:transaction_id>/confirm',
        views.SheetConfirmView.as_view(),
        name='sheet_confirm'),
    path(
        'sheets',
        views.SheetListView.as_view(),
        name='sheet_list'),
    path(
        'sheets/<int:sheet_id>',
        views.SheetDetailView.as_view(),
        name='sheet_detail'),
    path(
        'sheets/<int:sheet_id>/profile/<int:profile_id>',
        views.SheetManageProfileView.as_view(),
        name='sheet_manage_profile'),
]
