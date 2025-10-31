# Testes Não Funcionais — E-commerce (Black Friday)

Projeto pronto para executar exemplos de **Desempenho, Carga, Estresse, Escalabilidade e Segurança** em Python.
Defina a variável de ambiente `BASE_URL` (ex.: `http://localhost:8000`) ou edite o arquivo `.env.example` e renomeie para `.env`.

## Estrutura
- `perf_test.py` — teste de **desempenho** (tempo de resposta / P95).
- `locustfile.py` — teste de **carga** (throughput sustentado) usando **Locust**.
- `stress_test.py` — teste de **estresse** (rampa/spike e ponto de quebra).
- `scalability_analysis.py` — **escala horizontal** (eficiência) com planilha/CSV de resultados.
- `security_tests.py` — **segurança** (rate limiting, auth, RBAC básico).
- `sample_results/` — métricas sintéticas e **relatório** `report.md` demonstrando a análise e o “aprovado/reprovado”.
- `requirements.txt` — dependências.
- `.env.example` — configuração padrão.

## Pré-requisitos
Python 3.10+ recomendado.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Como executar (sugestão)
- **Desempenho:** `python perf_test.py`
- **Carga (Locust):** `locust -f locustfile.py --headless -u 2000 -r 200 --run-time 10m --host $BASE_URL`
- **Estresse:** `python stress_test.py`
- **Escalabilidade:** `python scalability_analysis.py`
- **Segurança:** `python security_tests.py`

> Ajuste `BASE_URL` (ex.: `export BASE_URL=http://localhost:8000`). Endpoints esperados:
> `/api/catalog`, `/api/cart/add`, `/api/checkout`, `/auth/login`, `/admin`.

## Metas (da atividade)
- P95 < 500ms (desempenho)
- Throughput sustentado > 2000 req/s (carga)
- Ponto de quebra > 15000 usuários (estresse)
- Eficiência horizontal > 80% (escalabilidade)
- Rate limiting: 100 req/min/IP (segurança)

> Os códigos coletam métricas em `./results` (criado automaticamente) e geram `sample_results/report.md` como exemplo.
