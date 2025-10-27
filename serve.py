import os
import hapiserver
base_dir = "../server-python-general"
config = {
    "index.html": os.path.join(base_dir, "html", "index.html"),
    "path": "",
    "HAPI": "3.3",
    "scripts": {
      "catalog": os.path.join(base_dir, "bin", "psws", "catalog.py"),
      "info": os.path.join(base_dir, "bin", "psws", "info.py"),
      "data": os.path.join(base_dir, "bin", "psws", "data.py")
    }
  }
fastapi_app = hapiserver.app(config)

from django.core.asgi import get_asgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
application = get_asgi_application()

#uvicorn mysite.asgi:app --reload
# Create the main Starlette application
from starlette.applications import Starlette
from starlette.routing import Mount
app = Starlette(
    routes=[
        Mount("/hapi", app=fastapi_app),
        Mount("/", app=application),
    ]
)
import uvicorn
uvicorn.run(app, host="0.0.0.0", port=8000)