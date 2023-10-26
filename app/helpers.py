from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import NotFound

import hashlib


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
    

def hash_security_answer(answer):
    """Hashes a security answer using a strong cryptographic hash function.

    Args:
        answer: The security answer to be hashed.

    Returns:
        The hashed security answer.
    """

    return hashlib.sha256(answer.encode()).hexdigest()