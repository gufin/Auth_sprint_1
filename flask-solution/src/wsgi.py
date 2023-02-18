from gevent import monkey

monkey.patch_all()

from core.app_init import create_app
from core.settings import get_settings

settings = get_settings()

app = create_app(settings)
