from dataclasses import dataclass
from typing import Any

@dataclass
class Transaction:
    amount: float
    currency: str
    user_id: int

@dataclass
class Account:
    country: str
    age: int
    is_active: bool

@dataclass
class Device:
    ip_address: str
    device_type: str  # например: mobile, desktop
    is_trusted: bool

@dataclass
class Rule:
    id: int
    target: str
    field: str
    operator: str
    value: Any