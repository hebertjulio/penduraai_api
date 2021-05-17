from django.urls import reverse, resolve

from . import views


class TestsUrlResolve:

    def test_resolve_token_obtain_pair(self):
        kwargs = {'version': 'v1'}
        r = self.resolve_by_name('auths:token_obtain_pair', **kwargs)
        assert r.func.cls == views.TokenObtainPairView  # nosec

    def test_resolve_token_refresh(self):
        kwargs = {'version': 'v1'}
        r = self.resolve_by_name('auths:token_refresh', **kwargs)
        assert r.func.cls == views.TokenRefreshView  # nosec

    @classmethod
    def resolve_by_name(cls, name, **kwargs):
        url = reverse(name, kwargs=kwargs)
        return resolve(url)
