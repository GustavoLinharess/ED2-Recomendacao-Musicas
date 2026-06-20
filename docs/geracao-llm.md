# Geração via LLM

Os dados foram gerados com apoio de um LLM (Claude, modelo Opus 4.8). Esta seção registra
o que foi feito com o modelo e o que foi ajustado à mão, atendendo ao critério de indicação
explícita do uso de LLM.

## Feito com o LLM

- definição do schema das três coleções e da convenção de pesos por tipo de interação;
- construção das faixas de atributos por gênero (os intervalos de energia, dançabilidade,
  valência, BPM e ano que mantêm cada gênero plausível);
- listas-semente de gêneros, artistas fictícios e fragmentos de títulos;
- a rotina que materializa as três coleções aplicando essas regras e a validação final.

## Ajustado à mão

- revisão dos intervalos por gênero para evitar combinações estranhas;
- ajuste das quantidades (60 músicas, 25 usuários) e da concentração das interações para
  garantir coocorrência;
- mudança da escala da nota para 0–10;
- conferência final dos CSVs gerados.

## Reprodutibilidade

A semente aleatória é fixa, então rodar a geração novamente produz exatamente a mesma base.
