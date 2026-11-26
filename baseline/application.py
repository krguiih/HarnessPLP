"""Camada de aplicação da implementação sem harness."""
from baseline.domain import OrderPlaced, PaymentConfirmed, OrderShipped, reduce


class OrderService:
    def __init__(self):
        self.state = None
        self.events = []

    def handle(self, event: OrderPlaced | PaymentConfirmed | OrderShipped):
        self.state = reduce(self.state, event)
        self.events.append(event)
        return self.state
