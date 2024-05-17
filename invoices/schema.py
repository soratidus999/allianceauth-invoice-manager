from datetime import datetime
from typing import Optional

from ninja import Schema


class Message(Schema):
    message: str


class WalletEvent(Schema):
    amount: int
    date: datetime


class Character(Schema):
    character_name: str
    corporation_name: str
    alliance_name: Optional[str]


class Corporation(Schema):
    corporation_name: str
    alliance_name: Optional[str]
    corporation_id: int
    alliance_id: Optional[int]


class Invoice(Schema):
    pk: int
    due_date: datetime
    paid: bool
    note: str
    invoice_ref: str
    amount: float
    character: Character
    payment: Optional[WalletEvent]
    action: Optional[bool]
