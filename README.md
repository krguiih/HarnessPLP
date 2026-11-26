# Harness para agentes de IA — Programação Reativa / Orientada a Eventos

Projeto de backend em Python 3.11+ usando **somente biblioteca padrão**. Duas implementações do mesmo caso de uso, processamento de pedidos via eventos, permitem comparar regras arquiteturais, defeitos detectados e esforço de correção.

> **Importante:** a versão `baseline/` é um **controle didático intencionalmente defeituoso**. Isto **não** constitui um ensaio independente com agentes de IA. Os resultados são mensurações do código incluído. Intervenções humanas de agentes reais são **não observadas**, não zero.

## Fluxo

`OrderPlaced` → `PaymentConfirmed` → `OrderShipped`.

Requisitos comuns: um pedido deve ser criado antes de receber pagamento; envio só após pagamento; eventos duplicados não devem alterar o estado; tentativa inválida não pode mudar o estado; fluxo não deve depender de rede ou banco.

## Estrutura

- `baseline/`: lógica imperativa sem barreiras de arquitetura; falhas intencionais para exercício.
- `harness/`: domínio funcional (redutor puro), eventos imutáveis e camada explícita de aplicação.
- `AGENTS.md`: contrato para agentes, checklist e definição de pronto.
- `docs/ARCHITECTURE.md`: decisões arquiteturais e invariantes.
- `tests/`: testes comportamentais compartilhados + testes de arquitetura.
- `scripts/validate.py`: execução de testes, lint e geração de relatório JSON.
- `scripts/experiment.py`: benchmark reproduzível de falhas por caso, controle e harness.
- `.github/workflows/ci.yml`: validação automática.

## Executar

```bash
python scripts/validate.py
python scripts/experiment.py
```

O comando `validate.py` verifica o **harness** (deve passar). `experiment.py` roda ambos e grava `results/comparison.json`. Python 3.11+ exigido, sem instalação de dependências. Opcional: `python -m pip install ruff` e `ruff check harness tests scripts`.

## Como conduzir uma comparação real com agentes

1. Crie duas cópias limpas do mesmo starter (sem soluções nem testes visíveis ao agente), mesmo modelo, mesmo prompt, limite de tempo, ferramentas e orçamento.
2. **Grupo A:** entregue apenas o enunciado, sem `AGENTS.md`, validação nem guia arquitetural. **Grupo B:** entregue as regras e scripts do harness.
3. Peça a implementação do mesmo comportamento. Salve commits, saídas de testes, transcrições e intervenções humanas em `results/runs.csv`.
4. Rode o mesmo avaliador externo oculto nas duas saídas; repita em várias seeds/rodadas e compare distribuição, não apenas um caso.
5. Registre como intervenção humana qualquer orientação corretiva dada durante a geração, além do prompt inicial; quando não houver registro, marque `NA`.

O relatório local compara artefatos **preparados**, não mede diretamente o desempenho de agentes. A pasta de slides fornecida foi acessada via link público, mas os arquivos internos não estavam disponíveis para leitura automatizada; as regras seguem conceitos gerais de programação reativa.
