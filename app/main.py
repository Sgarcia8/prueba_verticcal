# app/main.py
from fastapi import FastAPI
from routers.jsonPlaceHolderApi.JsonPlaceHolderRouter import router

app = FastAPI()

# Incluye el router
app.include_router(router)