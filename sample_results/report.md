# Relatório — Testes Não Funcionais (E-commerce Black Friday)

**Data:** 2025-10-31 05:37

## Metas e Resultados

| Tipo | Métrica | Meta | Resultado | Status |
|---|---|---:|---:|:--:|
| Desempenho | P95 (ms) | < 500 | 420 | ✅ |
| Carga | Throughput sustentado (req/s) | > 2000 | 2450 | ✅ |
| Estresse | Ponto de quebra (usuários) | > 15000 | 15000 | ⚠️ (limite) |
| Escalabilidade | Eficiência horizontal (%) | > 80 | 80.6 (média) | ✅ |
| Segurança | Rate limiting (429 em 100+ req/min/IP) | Ativo | 22 respostas 429 | ✅ |

### Observações
- **Estresse:** o ponto de quebra ocorreu **por volta de 15k usuários** com P95 ≈ 5,2s e queda na taxa de sucesso para 94,6%. Recomenda-se **tuning** de pool de conexões e caching de catálogo para ultrapassar com folga a meta (> 18k).
- **Escalabilidade:** eficiência entre **95% (2 nós)** e **80,6% (8 nós)** — bom, mas já mostra sobrecarga de coordenação no balanceador/sessões. Avaliar **stateless sessions** e sticky condicional.
- **Segurança:** rate limiting responde com 429 conforme esperado; RBAC nega acesso sem token e permite com token válido.

## Artefatos
- `perf_results.json`, `load_results.json`, `stress_results.json`, `scalability_output.csv`, `security_results.json`.
- Scripts para repetir os testes com seu `BASE_URL`.

---

> Este relatório segue o escopo da atividade de Aula 11 (Testes não funcionais: desempenho, carga, estresse, escalabilidade e segurança).
