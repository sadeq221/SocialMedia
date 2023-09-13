from django.urls import reverse
from django.test import Client


api_client = Client()

# Logs the user in using the cridentials (email and password) and returs f"Bearer {access token}"
def get_bearer(cridentials: dict) -> str:
    
    # Login in
    tokens = api_client.post(reverse("login"), data=cridentials).json()

    # Get access token
    access = tokens["access"]

    # Return Bearer auth
    return f"Bearer {access}"


# Logs the user in using the cridentials (email and password) and returs refresh and access tokens
def get_tokens(cridentials: dict) -> dict:
    
    # Login in
    tokens = api_client.post(reverse("login"), data=cridentials).json()

    return tokens