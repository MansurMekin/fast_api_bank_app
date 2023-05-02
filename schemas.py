from pydantic import BaseModel, Field


class AccountCreateRequest(BaseModel):
    account_number: str
    balance: int = Field(default=0)
    customer_id: int = Field(gt=0)


class AmountRequest(BaseModel):
    amount: int


class CustomerCreateRequest(BaseModel):
    name: str = Field(min_length=3)
    email: str = Field(min_length=10, default="example@mail.com")
    phone_number: str = Field(min_length=8, default="87076165139")
