from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app import models
from app.api.schemas import CustomerCreateRequest
from app.db import get_session


class CustomerService:
    def __init__(self, session: Session = Depends(get_session)) -> None:
        self.session = session

    def _get(self, customer_id: int):
        customer = (
            self.session.query(models.Customer)
            .options(joinedload(models.Customer.accounts))
            .filter(models.Customer.id == customer_id)
            .first()
        )
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"customer with id: {customer_id} not found",
            )
        return customer

    def get_list(self):
        customers = self.session.query(models.Customer).all()
        return customers

    def get(self, customer_id: int):
        return self._get(customer_id)

    def create(self, customer_data: CustomerCreateRequest):
        customer = models.Customer(**customer_data.dict())
        self.session.add(customer)
        self.session.commit()
        return customer

    def update(self, customer_id: int, customer_data: CustomerCreateRequest):
        customer = self._get(customer_id)
        for field, value in customer_data:
            setattr(customer, field, value)
        self.session.add(customer)
        self.session.commit()
        return customer

    def delete(self, customer_id: int):
        customer = self._get(customer_id)
        self.session.delete(customer)
        self.session.commit()
