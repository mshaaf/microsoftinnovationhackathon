import os

APP_MODES = frozenset({"mock", "live"})


def get_app_mode() -> str:
    mode = os.getenv("APP_MODE", "mock").strip().lower()
    if mode not in APP_MODES:
        raise ValueError("APP_MODE must be 'mock' or 'live'")
    return mode


APP_MODE = get_app_mode()
