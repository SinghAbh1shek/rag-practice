from pydantic import Field
from typing import TypedDict
from pymongo.asynchronous.collection import AsyncCollection
from ..db import database

class FileSchema(TypedDict):
    name: str = Field(..., discription="Name of the file")
    status: str = Field(..., discription="Status of the file")

COLLECTION_NAME = "files"
files_collection: AsyncCollection = database[COLLECTION_NAME]