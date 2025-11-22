import os
import hapiserver


def django_app():
  import importlib
  from django.core.asgi import get_asgi_application
  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

  # Load the Django settings module and tweak values before ASGI app is created
  _settings = importlib.import_module(os.environ["DJANGO_SETTINGS_MODULE"])
  _settings.DEBUG = False
  _settings.ALLOWED_HOSTS = ["*"]
  return get_asgi_application()

def combine_apps(fastapi_app, django_app):
  # Create the main Starlette application
  from starlette.applications import Starlette
  from starlette.routing import Mount
  # Serve HAPI routes under data/ path.
  routes = [ Mount("/data/", app=fastapi_app), Mount("/", app=django_app) ]
  return Starlette(routes=routes)


config = "../server-python-general/bin/psws/config.json"
fastapi_app = hapiserver.app(config)
combined_apps = combine_apps(fastapi_app, django_app())
host = "0.0.0.0"
port = 8000
print(f"Starting HAPI server at http://{host}:{port}/data/hapi")
import uvicorn
uvicorn.run(combined_apps, host=host, port=port)