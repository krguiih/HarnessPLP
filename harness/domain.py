"""Núcleo puro e imutável de um fluxo orientado a eventos."""
from dataclasses import dataclass, replace


class DomainError(ValueError):
    """Evento viola uma invariante do domínio."""


@dataclass(frozen=True)
class OrderPlaced:
    event_id: str
    order_id: str
    amount: int


@dataclass(frozen=True)
class PaymentConfirmed:
    event_id: str
    order_id: str


@dataclass(frozen=True)
class OrderShipped:
    event_id: str
    order_id: str


@dataclass(frozen=True)
class OrderState:
    order_id: str
    amount: int
    status: str
    seen_ids: frozenset[str]


def reduce(state: OrderState | None, event: OrderPlaced | PaymentConfirmed | OrderShipped) -> OrderState:
    """Transição determinística: nenhum efeito e nenhuma mutação de entrada."""
    if state is not None and event.event_id in state.seen_ids:
        return state
    if state is None:
        if not isinstance(event, OrderPlaced):
            raise DomainError("O primeiro evento deve ser OrderPlaced")
        if event.amount <= 0:
            raise DomainError("amount deve ser positivo")
        return OrderState(event.order_id, event.amount, "created", frozenset({event.event_id}))
    if event.order_id != state.order_id:
        raise DomainError("Evento pertence a outro pedido")
    if isinstance(event, OrderPlaced):
        raise DomainError("Pedido já criado")
    if isinstance(event, PaymentConfirmed) and state.status == "created":
        new_status = "paid"
    elif isinstance(event, OrderShipped) and state.status == "paid":
        new_status = "shipped"
    else:
        raise DomainError("Transição inválida")
    return replace(state, status=new_status, seen_ids=state.seen_ids | {event.event_id})
