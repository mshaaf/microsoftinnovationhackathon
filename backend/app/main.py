import importlib
import pkgutil
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

FRONTEND_DIST = Path(__file__).resolve().parents[2] / "frontend" / "dist"


def register_feature_routers(
    application: FastAPI, package_name: str = "app.features"
) -> None:
    features = importlib.import_module(package_name)
    for feature in pkgutil.iter_modules(features.__path__):
        if not feature.ispkg:
            continue
        router_name = f"{package_name}.{feature.name}.router"
        try:
            module = importlib.import_module(router_name)
        except ModuleNotFoundError as error:
            if error.name != router_name:
                raise
            continue
        router = getattr(module, "router", None)
        if router is not None:
            application.include_router(router, prefix="/api")


def create_app() -> FastAPI:
    application = FastAPI(title="Survivor Journey Navigator", version="0.1.0")
    register_feature_routers(application)

    index = FRONTEND_DIST / "index.html"
    if index.is_file():

        @application.get("/", include_in_schema=False)
        def frontend_index() -> FileResponse:
            return FileResponse(index)

        @application.get("/{path:path}", include_in_schema=False)
        def frontend_path(path: str) -> FileResponse:
            if path == "api" or path.startswith("api/"):
                raise HTTPException(status_code=404)
            frontend_root = FRONTEND_DIST.resolve()
            candidate = (frontend_root / path).resolve()
            try:
                candidate.relative_to(frontend_root)
            except ValueError as error:
                raise HTTPException(status_code=404) from error
            return FileResponse(candidate if candidate.is_file() else index)

    return application


app = create_app()
