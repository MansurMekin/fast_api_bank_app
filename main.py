from fastapi import FastAPI

import models
from database import engine
from routers import accounts, admin, customers

app = FastAPI(
    title="KaspiBank",
)


models.Base.metadata.create_all(bind=engine)

app.include_router(admin.router)
app.include_router(customers.router)
app.include_router(accounts.router)
