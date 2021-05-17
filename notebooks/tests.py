from django.urls import reverse, resolve

from . import views


class TestsUrlResolve:

    def test_resolve_record_confirm(self):
        kwargs = {'version': 'v1', 'transaction_id': 'uuid'}
        r = self.resolve_by_name('notebooks:record_confirm', **kwargs)
        assert r.func.cls == views.RecordConfirmView  # nosec

    def test_resolve_record_list(self):
        kwargs = {'version': 'v1'}
        r = self.resolve_by_name('notebooks:record_list', **kwargs)
        assert r.func.cls == views.RecordListView  # nosec

    def test_resolve_record_detail(self):
        kwargs = {'version': 'v1', 'record_id': 1}
        r = self.resolve_by_name('notebooks:record_detail', **kwargs)
        assert r.func.cls == views.RecordDetailView  # nosec

    def test_resolve_sheet_confirm(self):
        kwargs = {'version': 'v1', 'transaction_id': 'uuid'}
        r = self.resolve_by_name('notebooks:sheet_confirm', **kwargs)
        assert r.func.cls == views.SheetConfirmView  # nosec

    def test_resolve_sheet_list(self):
        kwargs = {'version': 'v1'}
        r = self.resolve_by_name('notebooks:sheet_list', **kwargs)
        assert r.func.cls == views.SheetListView  # nosec

    def test_resolve_sheet_detail(self):
        kwargs = {'version': 'v1', 'sheet_id': 1}
        r = self.resolve_by_name('notebooks:sheet_detail', **kwargs)
        assert r.func.cls == views.SheetDetailView  # nosec

    def test_resolve_sheet_manage_profile(self):
        kwargs = {'version': 'v1', 'sheet_id': 1, 'profile_id': 1}
        r = self.resolve_by_name('notebooks:sheet_manage_profile', **kwargs)
        assert r.func.cls == views.SheetManageProfileView  # nosec

    @classmethod
    def resolve_by_name(cls, name, **kwargs):
        url = reverse(name, kwargs=kwargs)
        return resolve(url)
