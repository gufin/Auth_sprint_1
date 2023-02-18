import logging


def backoff_handler(details):
    logging.error(
        "Backing off {wait:0.1f} seconds after {tries} tries "
        "calling function {target} with args {args} and kwargs "
        "{kwargs}".format(**details)
    )


def get_user_id(data: list[dict[str, str]], user_name: str) -> str | None:
    for user_data in data:
        if user_name in user_data:
            return user_data[user_name]


def get_role_id(data: list[dict[str, str]], role: str) -> str | None:
    for role_data in data:
        if role in role_data:
            return role_data[role]
