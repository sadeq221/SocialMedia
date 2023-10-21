from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import NotFound

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def get_object_or_404(model, pk):
    try:
        return model.objects.get(pk=pk)
    except model.DoesNotExist:
        raise NotFound(detail=f"{model.__name__} not found")