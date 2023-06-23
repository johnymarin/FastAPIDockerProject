import os
from importlib.util import find_spec

from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.staticfiles import StaticFiles

import sys
from pathlib import Path

# Get the parent directory of django_project
django_app_parent_dir = str(Path(__file__).resolve().parent.parent)

# Add django_app_parent_dir to sys.path
sys.path.insert(0, django_app_parent_dir)

from django.core.wsgi import get_wsgi_application



# Create a FastAPI instance
app = FastAPI()


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.django_app.settings")


# Create a Django application instance
#django_project = WSGIHandler()
django_app = get_wsgi_application()

# Mount the Django app on the FastAPI app
app.mount("/django", WSGIMiddleware(django_app))
app.mount("/static",
    StaticFiles(
         directory=os.path.normpath(
              os.path.join(find_spec("django.contrib.admin").origin, "..", "static")
         )
   ),
   name="static",
)


# Define a FastAPI route
@app.get("/fastapi")
async def fastapi_route():
    return {"message": "Hello from FastAPI!"}


if __name__ == "__main__":
    import uvicorn

    # Start the FastAPI server
    uvicorn.run(app, host="0.0.0.0", port=8000)

    