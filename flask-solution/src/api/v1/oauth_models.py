import json

from flask import current_app, redirect, request, url_for, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from rauth import OAuth2Service


class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config["OAUTH_CREDENTIALS"][provider_name]
        self.consumer_id = credentials["client_id"]
        self.consumer_secret = credentials["client_secret"]

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for(
            "oauth_helper.oauth_callback",
            provider=self.provider_name,
            _external=True,
        )

    @staticmethod
    def create_tokens(identity: str):
        access_token = create_access_token(
            identity=identity, additional_claims={"is_administrator": False}
        )
        refresh_token = create_refresh_token(identity=identity)
        return jsonify(access_token=access_token, refresh_token=refresh_token)

    @classmethod
    def get_provider(cls, provider_name):
        if cls.providers is None:
            cls.providers = {}
            for provider_class in cls.__subclasses__():
                provider = provider_class()
                cls.providers[provider.provider_name] = provider
        return cls.providers[provider_name]


class YandexSignIn(OAuthSignIn):
    def __init__(self):
        super(YandexSignIn, self).__init__("yandex")
        self.service = OAuth2Service(
            name="yandex",
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url="https://oauth.yandex.ru/authorize",
            access_token_url="https://oauth.yandex.ru/token",
            base_url="https://oauth.yandex.ru",
        )

    def authorize(self):
        print(self.get_callback_url())
        return redirect(
            self.service.get_authorize_url(
                scope="login:email login:info",
                response_type="code",
                redirect_uri=self.get_callback_url(),
            )
        )

    def callback(self):
        def decode_json(payload):
            return json.loads(payload.decode("utf-8"))

        if "code" not in request.args:
            return None, None, None
        oauth_session = self.service.get_auth_session(
            data={
                "code": request.args["code"],
                "response_type": "code",
                "grant_type": "authorization_code",
                "redirect_uri": self.get_callback_url(),
            },
            decoder=decode_json,
        )
        info = oauth_session.get(url="https://login.yandex.ru/info").json()
        social_id = info.get("id")
        login = info.get("login")
        email = info.get("default_email")
        return social_id, login, email


class GoogleSignIn(OAuthSignIn):

    def __init__(self):
        super(GoogleSignIn, self).__init__('google')
        self.service = OAuth2Service(
            name='google',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://accounts.google.com/o/oauth2/auth',
            access_token_url='https://accounts.google.com/o/oauth2/token',
            base_url='https://www.googleapis.com/plus/v1/people/'
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='email',
            response_type='code',
            redirect_uri=self.get_callback_url())
        )

    def callback(self):
        if 'code' not in request.args:
            return None, None, None
        oauth_session = self.service.get_auth_session(
            data={'code': request.args['code'],
                  'grant_type': 'authorization_code',
                  'redirect_uri': self.get_callback_url()},
            decoder=json.loads
        )
        user = oauth_session.get('https://www.googleapis.com/oauth2/v1/userinfo').json()
        social_id = user.get("sub")
        email = user.get("email")
        login = user.get("sub")
        return social_id, login, email