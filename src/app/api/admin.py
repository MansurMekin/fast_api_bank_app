import services
from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Account

router = APIRouter(prefix="/admin", tags=["admin"])


@router.put("/block/{account_id}", status_code=status.HTTP_200_OK)
async def block_account(db: Session = Depends(get_db), account_id: int = Path(gt=0)):
    account_model = db.query(Account).filter(Account.id == account_id).first()
    if account_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="account not found"
        )
    account_model.is_blocked = True
    db.add(account_model)
    db.commit()
    return {"account_blocked": account_model.id}


@router.put("/unblock/{account_id}", status_code=status.HTTP_200_OK)
async def unblock_account(db: Session = Depends(get_db), account_id: int = Path(gt=0)):
    account_model = db.query(Account).filter(Account.id == account_id).first()
    if account_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="account not found"
        )
    account_model.is_blocked = False
    db.add(account_model)
    db.commit()
    return {"account_unblocked": account_model.id}
