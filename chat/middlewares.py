'''
In asgi.py, we do not use the default AuthMiddlewareStack.
This is because it is helpful when serving the ASGI app from the same application or templating engine.
It stores the data in the sessions.
Instead, we define new middleware that add the user to the scope based on the token provided.
'''
import jwt
from django.contrib.auth.models import AnonymousUser
from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from app.models import User

import environ
env = environ.Env()
environ.Env.read_env()


@database_sync_to_async
def return_user(token):
    try:
        decoded_token = jwt.decode(token, env('JWT_SECRET'), algorithms=['HS256'])
        return User.objects.get(id=decoded_token['user_id'])
    except:
        return AnonymousUser()
    

class TokenAuthMiddleWare:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, recieve, send):
        query_string = scope['query_string']
        # convert query_string from b'' (byte string) to '' (python string)
        query_string = query_string.decode()
        # decode the string and adds it to the Python dictionary
        query_dict = parse_qs(query_string)

        # Let's add the user to the scope based on the token
        try:
            token = query_dict['token'][0]
            scope['user'] = await return_user(token)
        except:
            scope['user'] = AnonymousUser()

        return await self.app(scope, recieve, send)
