from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models
from app.api.schemas import AccountCreateRequest
from app.db import get_session



class AccountService:
    def __init__(self, session: Session = Depends(get_session)) -> None:
        self.session = session

    
    def _get(self, account_id: int):
        account = (
            self.session.query(models.Account)
            .filter(models.Account.id == account_id)
            .first()
        )
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"account with id: {account_id} not found",
            )
        return account
    
    def get_list(self):
        accounts = self.session.query(models.Account).all()
        return accounts
    
    def get(self, account_id: int):
        return self._get(account_id)
    
    def create(self, account_data: AccountCreateRequest):
        account = models.Account(**account_data.dict())
        self.session.add(account)
        self.session.commit()
        return account
    
    def update(self, account_id: int, account_data: AccountCreateRequest):
        account = self._get(account_id)
        for field, value in account_data:
            setattr(account, field, value)
        self.session.add(account)
        self.session.commit()
        return account
    
    def delete(self, account_id: int):
        account = self._get(account_id)
        self.session.delete(account)
        self.session.commit()

    