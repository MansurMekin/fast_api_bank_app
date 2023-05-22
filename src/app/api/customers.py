from fastapi import APIRouter, Depends, Path, Response, status

from app.api.schemas import CustomerCreateRequest
from app.services.customers import CustomerService

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("/", status_code=status.HTTP_200_OK)
async def get_customers(service: CustomerService = Depends()):
    return service.get_list()


@router.get("/{customer_id}", status_code=status.HTTP_200_OK)
async def get_customer(
    customer_id: int = Path(gt=0), service: CustomerService = Depends()
):
    return service.get(customer_id=customer_id)


@router.post(
    "/", response_model=CustomerCreateRequest, status_code=status.HTTP_201_CREATED
)
async def create_customer(
    customer_data: CustomerCreateRequest, service: CustomerService = Depends()
):
    return service.create(customer_data=customer_data)


@router.put("/{customer_id}", status_code=status.HTTP_200_OK)
async def update_customer(
    customer_data: CustomerCreateRequest,
    customer_id: int = Path(gt=0),
    service: CustomerService = Depends(),
):
    return service.update(customer_id=customer_id, customer_data=customer_data)


@router.delete("/{customer_id}", status_code=status.HTTP_200_OK)
async def delete_customer(
    customer_id: int = Path(gt=0), service: CustomerService = Depends()
):
    service.delete(customer_id=customer_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
