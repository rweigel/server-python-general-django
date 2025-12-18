
def django_app():
  import os
  import importlib
  from django.core.wsgi import get_wsgi_application
  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

  # Load the Django settings module and tweak values before ASGI app is created
  _settings = importlib.import_module(os.environ["DJANGO_SETTINGS_MODULE"])
  _settings.DEBUG = False
  _settings.ALLOWED_HOSTS = ["*"]
  return get_wsgi_application()

def fastapi_app():
  import fastapi
  import a2wsgi

  # FastAPI ASGI app, converted to WSGI
  fastapi_asgi = fastapi.FastAPI()
  @fastapi_asgi.get("/", response_class=fastapi.responses.PlainTextResponse)
  async def hello():
      return "hello world"

  fastapi_wsgi = a2wsgi.ASGIMiddleware(fastapi_asgi)

  return fastapi_wsgi

def combine_apps(fastapi_app, django_app):
  from werkzeug.middleware.dispatcher import DispatcherMiddleware
  # Add /hapi endpoint
  application = DispatcherMiddleware(django_app, {
      "/hapi": fastapi_app
  })
  return application

application = combine_apps(fastapi_app(), django_app())

# Start server using gunicorn -w 1 wsgi_hapi:application -b 0.0.0.0:8877

print("Serving /hapi and /polls")