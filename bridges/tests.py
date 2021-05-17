from django.urls import reverse, resolve

from . import views


class TestsUrlResolve:

    def test_resolve_transaction_detail(self):
        kwargs = {'version': 'v1', 'transaction_id': 'uuid'}
        r = self.resolve_by_name('bridges:transaction_detail', **kwargs)
        assert r.func.cls == views.TransactionDetailView  # nosec

    @classmethod
    def resolve_by_name(cls, name, **kwargs):
        url = reverse(name, kwargs=kwargs)
        return resolve(url)
