# Contrato para agentes — leitura obrigatória antes de alterar `harness/`

## Missão
Implementar features usando eventos imutáveis, projeção determinística e limites claros entre domínio e infraestrutura.

## Regras vinculantes
1. Eventos são dataclasses imutáveis (`frozen=True`); nunca os modifique.
2. O domínio é puro: `reduce(state, event) -> state`; sem `print`, I/O, relógio, rede, banco ou variáveis globais mutáveis.
3. Transições válidas: ausente → criado → pago → enviado. Não permitir pular estados.
4. Reprocessar um `event_id` não causa alteração (idempotência).
5. Erros de transição lançam `DomainError` e preservam o estado anterior.
6. A camada de aplicação pode coordenar eventos, mas nunca alterar atributos de `OrderState` diretamente.
7. Não importar `baseline` a partir de `harness`; não introduzir dependência externa no domínio.
8. Toda feature precisa de teste para caminho feliz, ordem inválida e duplicidade.

## Fluxo de trabalho
1. Leia `docs/ARCHITECTURE.md`.
2. Faça mudanças pequenas e localizadas.
3. Rode `python scripts/validate.py` e corrija toda falha.
4. Registre no PR testes adicionados, invariantes e decisão arquitetural.

## Definição de pronto
Todos os testes do harness passam; checks estáticos passam; nenhuma regra é violada; eventos permanecem serializáveis por campos primitivos.
