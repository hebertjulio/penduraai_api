from django.urls import reverse, resolve

from . import views


class TestsUrlResolve:

    def test_resolve_user_list(self):
        kwargs = {'version': 'v1'}
        r = self.resolve_by_name('accounts:user_list', **kwargs)
        assert r.func.cls == views.UserListView  # nosec

    def test_resolve_user_current(self):
        kwargs = {'version': 'v1'}
        r = self.resolve_by_name('accounts:user_current', **kwargs)
        assert r.func.cls == views.UserCurrentView  # nosec

    def test_resolve_profile_confirm(self):
        kwargs = {'version': 'v1', 'transaction_id': 'uuid'}
        r = self.resolve_by_name('accounts:profile_confirm', **kwargs)
        assert r.func.cls == views.ProfileConfirmView  # nosec

    def test_resolve_profile_list(self):
        kwargs = {'version': 'v1'}
        r = self.resolve_by_name('accounts:profile_list', **kwargs)
        assert r.func.cls == views.ProfileListView  # nosec

    def test_resolve_profile_detail(self):
        kwargs = {'version': 'v1', 'profile_id': 1}
        r = self.resolve_by_name('accounts:profile_detail', **kwargs)
        assert r.func.cls == views.ProfileDetailView  # nosec

    def test_resolve_profile_roles(self):
        kwargs = {'version': 'v1'}
        r = self.resolve_by_name('accounts:profile_roles', **kwargs)
        assert r.func.cls == views.ProfileRolesView  # nosec

    def test_resolve_profile_unlock(self):
        kwargs = {'version': 'v1', 'profile_id': 1}
        r = self.resolve_by_name('accounts:profile_unlock', **kwargs)
        assert r.func.cls == views.ProfileUnlockView  # nosec

    def test_resolve_profile_current(self):
        kwargs = {'version': 'v1'}
        r = self.resolve_by_name('accounts:profile_current', **kwargs)
        assert r.func.cls == views.ProfileCurrentView  # nosec

    @classmethod
    def resolve_by_name(cls, name, **kwargs):
        url = reverse(name, kwargs=kwargs)
        return resolve(url)
