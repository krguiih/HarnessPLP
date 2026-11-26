"""Orquestração em memória; nunca altera o estado diretamente."""
from harness.domain import OrderState, OrderPlaced, PaymentConfirmed, OrderShipped, reduce


class OrderService:
    def __init__(self) -> None:
        self.state: OrderState | None = None
        self.events: list[OrderPlaced | PaymentConfirmed | OrderShipped] = []

    def handle(self, event: OrderPlaced | PaymentConfirmed | OrderShipped) -> OrderState:
        next_state = reduce(self.state, event)
        if next_state is not self.state:
            self.events.append(event)
        self.state = next_state
        return next_state
