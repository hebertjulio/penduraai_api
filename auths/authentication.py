from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTAuthentication(JWTAuthentication):

    def authenticate(self, request):
        authenticate = super().authenticate(request)
        if not authenticate:
            return None

        user, validated_token = authenticate

        try:
            profile_id = validated_token['profile_id']
            user.profile = user.userprofiles.get(id=profile_id)
        except (KeyError, user.DoesNotExist):
            pass

        return user, validated_token
