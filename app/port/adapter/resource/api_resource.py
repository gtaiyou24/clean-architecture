import abc

from fastapi import APIRouter


class APIResource(abc.ABC):
    router: APIRouter
