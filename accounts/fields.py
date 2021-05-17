class CurrentProfileDefault:

    requires_context = True

    def __call__(self, serializer_field):
        request = serializer_field.context['request']
        return request.user.profile

    def __repr__(self):
        return '%s()' % self.__class__.__name__
