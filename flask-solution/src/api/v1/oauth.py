from http import HTTPStatus

from flask import Blueprint

from api.v1.oauth_models import OAuthSignIn
from db.db_init import get_db
from core.rate_limiter import rate_limit
from models.users import SocialAccount, User

db = get_db()
oauth = Blueprint("oauth_helper", __name__)


@oauth.route("/authorize/<provider>")
@rate_limit()
def oauth_authorize(provider):
    oauth_provider = OAuthSignIn.get_provider(provider)
    return oauth_provider.authorize()


@oauth.route("/callback/<provider>")
@rate_limit()
def oauth_callback(provider):
    oauth_provider = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth_provider.callback()
    if social_id is None:
        return {"msg": "Account not found"}, HTTPStatus.CONFLICT
    social_account = SocialAccount.query.filter(
        (SocialAccount.social_id == social_id)
        | (SocialAccount.social_name == provider)
    ).first()
    if social_account is None:
        user = User(login=username, email=email)
        user.set_password("password")
        db.session.add(user)
        db.session.commit()
        new_social_account = SocialAccount(
            social_id=social_id,
            social_name=provider,
            user_id=str(user.id),
        )
        db.session.add(new_social_account)
        db.session.commit()
    else:
        user = social_account.user
    return oauth_provider.create_tokens(identity=user.id)
