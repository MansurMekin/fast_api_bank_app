from fastapi import Depends, Query
from sqlalchemy.orm import Session

from app.db import get_db

# def block_account(account_id: int = Query(gt=0)):
