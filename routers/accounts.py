from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Account

router = APIRouter(prefix="/accounts", tags=["accounts"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class AccountCreateRequest(BaseModel):
    account_number: str
    balance: int = Field(default=0)
    customer_id: int = Field(gt=0)


class AmountRequest(BaseModel):
    amount: int


@router.get("/", status_code=status.HTTP_200_OK)
async def get_accounts(db: db_dependency):
    return db.query(Account).all()


@router.get("/{account_id}", status_code=status.HTTP_200_OK)
async def get_account(db: db_dependency, account_id: int = Path(gt=0)):
    account_model = db.query(Account).filter(Account.id == account_id).first()
    if account_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="account not found"
        )
    return account_model


@router.post("/create_account", status_code=status.HTTP_201_CREATED)
async def create_account(
    db: db_dependency, account_create_request: AccountCreateRequest
):
    account_model = Account(
        account_number=account_create_request.account_number,
        balance=account_create_request.balance,
        customer_id=account_create_request.customer_id,
    )
    db.add(account_model)
    db.commit()


@router.put("/refill/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def refill_account(
    db: db_dependency, amount: AmountRequest, account_id: int = Path(gt=0)
):
    account_model = db.query(Account).filter(Account.id == account_id).first()
    if account_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    account_model.balance = account_model.balance + amount.amount
    db.add(account_model)
    db.commit()


@router.put("/withdraw/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def withdraw_account(
    db: db_dependency, amount: AmountRequest, account_id: int = Path(gt=0)
):
    account_model = db.query(Account).filter(Account.id == account_id).first()
    if account_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if account_model.is_blocked:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Ваш аккаунт заблокирован"
        )
    account_model.balance = account_model.balance - amount.amount
    if account_model.balance < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Недостаточно средств"
        )
    db.add(account_model)
    db.commit()


@router.put("/tranfer", status_code=status.HTTP_204_NO_CONTENT)
def tranfer_operation_by_id(
    db: db_dependency, from_account: int, to_account: int, amount: AmountRequest
):
    from_account_model = db.query(Account).filter(Account.id == from_account).first()
    from_account_model.balance = from_account_model.balance - amount.amount
    if from_account_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if from_account_model.is_blocked:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Ваш аккаунт заблокирован"
        )
    if from_account_model.balance < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Недостаточно средств"
        )
    db.add(from_account_model)
    db.commit()
    to_account_model = db.query(Account).filter(Account.id == to_account).first()
    if to_account_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    to_account_model.balance = to_account_model.balance + amount.amount
    db.add(to_account_model)
    db.commit()
