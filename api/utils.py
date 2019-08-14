from django.conf import settings
import jwt
from jwt.algorithms import RSAAlgorithm
import requests
import json

def verify_and_decode_jwt(id_token):
    # Get and public key from Twitch
    r = requests.get(settings.WELL_KNOWN_URL)
    if r.status_code == 200:
        keys = r.content[9:-3]

        # Verify and decode ID Token from public key
        try:
            public_key = RSAAlgorithm.from_jwk(keys)
            decoded = jwt.decode(id_token, public_key, algorithms='RS256', audience=settings.CLIENT_ID, options={'verify_exp': False})
            return decoded

        except Exception as e:
            # TODO: Raise appropriate error
            return None
    else:
        return None
        # TODO: Raise appropriate error

def get_id_from_request(request):
    # Extract jwt from request cookies and decode
    token = request.COOKIES.get('token')
    decoded = verify_and_decode_jwt(token)

    # Extract and return Twitch ID portion
    twitch_id = decoded['sub']
    return twitch_id