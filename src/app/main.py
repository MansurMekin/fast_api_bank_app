from fastapi import FastAPI

import app.models as models
from app.api import accounts, admin, customers
from app.db import engine

app = FastAPI(
    title="KaspiBank",
)


models.Base.metadata.create_all(bind=engine)


app.include_router(admin.router)
app.include_router(customers.router)
app.include_router(accounts.router)
