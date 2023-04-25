from fastapi import FastAPI
from routers import customers, accounts, admin
import models
from database import engine

app = FastAPI(
    title='KaspiBank'
)


models.Base.metadata.create_all(bind=engine)

app.include_router(admin.router)
app.include_router(customers.router)
app.include_router(accounts.router)