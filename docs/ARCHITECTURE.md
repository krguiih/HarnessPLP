# Arquitetura orientada a eventos

## Modelo

`Evento externo` → `ApplicationService.handle` → `reduce` (núcleo puro) → `OrderState`.

O fluxo implementa uma **projeção/event reducer**, e não um broker assíncrono de produção. A mesma sequência de eventos sempre gera o mesmo estado. O histórico é mantido em memória; persistência e entrega ao menos uma vez seriam adaptadores externos em uma evolução futura.

## Invariantes
- `OrderPlaced` inicia pedido com estado `created`.
- `PaymentConfirmed` requer `created`.
- `OrderShipped` requer `paid`.
- `event_id` duplicado é ignorado sem mutar o estado.
- Evento rejeitado não entra no log e não altera a projeção.
- Estado e eventos são imutáveis.

## Decisões
- IDs e valores em strings/int simplificam um exercício sem dependências.
- A validação arquitetural usa AST e verifica classes congeladas, ausência de imports I/O no núcleo e ausência de manipulação de estado fora do redutor. É intencionalmente limitada: não substitui revisão humana.
- Testes compartilhados implementam o mesmo contrato para as duas variantes.

## Extensões futuras
Outbox transacional, observabilidade, versionamento de esquema, snapshots, broker de mensagens, concorrência otimista e testes de carga.
