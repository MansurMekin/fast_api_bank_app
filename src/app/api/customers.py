from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from app.api.schemas import CustomerCreateRequest
from app.db import get_db
from app.models import Customer
from app.services.customers import CustomerService

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("/", status_code=status.HTTP_200_OK)
async def get_customers(service: CustomerService = Depends()):
    return service.get_list()


@router.get("/{customer_id}", status_code=status.HTTP_200_OK)
async def get_customer(customer_id: int = Path(gt=0), db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    return customer


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_customer(
    customer_create_request: CustomerCreateRequest, db: Session = Depends(get_db)
):
    customer_model = Customer(
        name=customer_create_request.name,
        email=customer_create_request.email,
        phone_number=customer_create_request.phone_number,
    )
    db.add(customer_model)
    db.commit()


@router.get("/{customer_id}/accounts", status_code=status.HTTP_200_OK)
def get_customer_accounts(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    return customer.accounts.all()
