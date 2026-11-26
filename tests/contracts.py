"""Contrato idêntico executado contra cada implementação."""
from importlib import import_module


def scenarios(variant: str) -> dict[str, callable]:
    domain = import_module(f"{variant}.domain")
    app = import_module(f"{variant}.application")

    def create():
        service = app.OrderService()
        service.handle(domain.OrderPlaced("e1", "o1", 100))
        assert service.state.status == "created"
        assert service.state.amount == 100

    def flow():
        service = app.OrderService()
        service.handle(domain.OrderPlaced("e1", "o1", 100))
        service.handle(domain.PaymentConfirmed("e2", "o1"))
        service.handle(domain.OrderShipped("e3", "o1"))
        assert service.state.status == "shipped"
        assert len(service.events) == 3

    def no_payment_before_create():
        service = app.OrderService()
        try:
            service.handle(domain.PaymentConfirmed("e1", "o1"))
        except domain.DomainError:
            assert service.state is None
        else:
            raise AssertionError("Pagamento antes de criar pedido foi aceito")

    def no_shipping_before_payment():
        service = app.OrderService()
        service.handle(domain.OrderPlaced("e1", "o1", 100))
        before = service.state
        try:
            service.handle(domain.OrderShipped("e2", "o1"))
        except domain.DomainError:
            assert service.state == before
            assert len(service.events) == 1
        else:
            raise AssertionError("Envio antes do pagamento foi aceito")

    def idempotent():
        service = app.OrderService()
        event = domain.OrderPlaced("e1", "o1", 100)
        service.handle(event)
        first = service.state
        service.handle(event)
        assert service.state == first
        assert len(service.events) == 1

    def immutable_events():
        service = app.OrderService()
        event = domain.OrderPlaced("e1", "o1", 100)
        service.handle(event)
        try:
            event.amount = 900
        except (AttributeError, TypeError):
            pass
        else:
            raise AssertionError("Evento permitiu mutação")

    def positive_amount():
        service = app.OrderService()
        try:
            service.handle(domain.OrderPlaced("e1", "o1", -10))
        except domain.DomainError:
            assert service.state is None
        else:
            raise AssertionError("Valor negativo foi aceito")

    def no_cross_order():
        service = app.OrderService()
        service.handle(domain.OrderPlaced("e1", "o1", 100))
        try:
            service.handle(domain.PaymentConfirmed("e2", "o2"))
        except domain.DomainError:
            assert service.state.status == "created"
        else:
            raise AssertionError("Evento de outro pedido foi aceito")

    return {k: v for k, v in locals().items() if callable(v) and k not in {"scenarios"}}
