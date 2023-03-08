from flask import request
from opentelemetry import trace

from core.app_init import create_app
from core.settings import get_settings
from core.tracer import configure_tracer

settings = get_settings()
app = create_app(settings)

if settings.TRACER_ENABLED:
    configure_tracer()

if settings.TRACER_ENABLED:
    @app.before_request
    def before_request():
        request_id = request.headers.get('X-Request-Id')
        if not request_id:
            raise RuntimeError('request id is required')
        tracer = trace.get_tracer(__name__)
        span = tracer.start_span('auth')
        span.set_attribute('http.request_id', request_id)
        span.end()


if __name__ == "__main__":
    app.run(port=app.config["AUTH_PORT"], host="0.0.0.0")


