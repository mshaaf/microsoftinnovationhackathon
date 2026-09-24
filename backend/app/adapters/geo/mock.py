from app.adapters.base import MockAdapter

from .base import lookup


class Adapter(MockAdapter):
    def lookup(self, zip_code: str):
        return lookup(zip_code)
