from fastapi import APIRouter, HTTPException, Path, status

from dependencies import db_dependency
from models import Customer
from schemas import CustomerCreateRequest

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("/", status_code=status.HTTP_200_OK)
async def get_customers(db: db_dependency):
    return db.query(Customer).all()


@router.get("/{customer_id}", status_code=status.HTTP_200_OK)
async def get_customer(db: db_dependency, customer_id: int = Path(gt=0)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    return customer


@router.post("/create_customer", status_code=status.HTTP_201_CREATED)
async def create_customer(
    db: db_dependency, customer_create_request: CustomerCreateRequest
):
    customer_model = Customer(
        name=customer_create_request.name,
        email=customer_create_request.email,
        phone_number=customer_create_request.phone_number,
    )
    db.add(customer_model)
    db.commit()


@router.get("/{customer_id}/accounts", status_code=status.HTTP_200_OK)
def get_customer_accounts(db: db_dependency, customer_id: int):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    return customer.accounts.all()
