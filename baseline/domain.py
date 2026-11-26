"""Controle didático deliberadamente frágil; não usar em produção."""
from dataclasses import dataclass


class DomainError(ValueError):
    pass


@dataclass
class OrderPlaced:
    event_id: str
    order_id: str
    amount: int


@dataclass
class PaymentConfirmed:
    event_id: str
    order_id: str


@dataclass
class OrderShipped:
    event_id: str
    order_id: str


@dataclass
class OrderState:
    order_id: str
    amount: int
    status: str
    seen_ids: set[str]


def reduce(state, event):
    # Baseline sem regras: aceita eventos fora de ordem e não deduplica.
    if state is None:
        if isinstance(event, OrderPlaced):
            return OrderState(event.order_id, event.amount, "created", {event.event_id})
        return OrderState(event.order_id, 0, "paid" if isinstance(event, PaymentConfirmed) else "shipped", {event.event_id})
    if isinstance(event, PaymentConfirmed):
        state.status = "paid"
    elif isinstance(event, OrderShipped):
        state.status = "shipped"
    elif isinstance(event, OrderPlaced):
        state.amount = event.amount
    state.seen_ids.add(event.event_id)
    return state
