from fastapi import FastAPI, Depends

from .db_utils.database_handler import DatabaseHandler
from .endpoints.endpoints import router, set_db_handler

db_handler = DatabaseHandler("config/config.ini")
app = FastAPI()

set_db_handler(db_handler)
app.include_router(router, dependencies=[Depends(lambda: db_handler)]) 
