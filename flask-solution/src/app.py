from core.app_init import create_app
from core.settings import get_settings

settings = get_settings()
app = create_app(settings)


if __name__ == "__main__":
    app.run(port=app.config["AUTH_PORT"], host='0.0.0.0')
