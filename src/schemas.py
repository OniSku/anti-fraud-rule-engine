from pydantic import BaseModel, Field
from typing import Any, List, Optional

class RuleSchema(BaseModel):
    """
    Схема для создания и редактирования правил администратором.
    Использую её для автоматической валидации входящих JSON-данных.
    """
    target: str = Field(..., description="Тип объекта: Transaction, Account или Device")
    field: str = Field(..., description="Поле объекта для проверки")
    operator: str = Field(..., description="Оператор сравнения: >, <, ==, in")
    value: Any = Field(..., description="Значение для сравнения")

    model_config = {
        "json_schema_extra": {
            "example": {
                "target": "Transaction",
                "field": "amount",
                "operator": ">",
                "value": 10000
            }
        }
    }

class TransactionSchema(BaseModel):
    """Схема входных данных для транзакции"""
    amount: float
    currency: str
    user_id: int

class AccountSchema(BaseModel):
    """Схема входных данных для аккаунта"""
    country: str
    age: int
    is_active: bool

class DeviceSchema(BaseModel):
    """Схема входных данных для устройства"""
    ip_address: str
    device_type: str
    is_trusted: bool

class CheckResultSchema(BaseModel):
    """Схема ответа системы после проверки объекта по правилам"""
    status: str
    errors: List[str] = []