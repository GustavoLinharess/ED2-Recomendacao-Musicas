# Motor de recomendação

É a etapa final do pipeline: junta tudo que as estruturas anteriores produziram e devolve uma
lista ordenada de músicas para o usuário. Implementado em `src/structures/recomendador.py`.

## Usuário existente

Para quem já tem histórico, a recomendação acontece em cinco passos:

1. **Sementes** — pega as músicas que o usuário melhor avaliou (notas altas) como ponto de partida.
2. **Travessia** — roda BFS ou DFS na projeção música-música a partir de cada semente, até
   profundidade 2, acumulando peso ao longo do caminho.
3. **Similaridade de atributos** — para cada candidato, mede a proximidade de conteúdo (cosseno do
   vetor sonoro) com as sementes. Isso reforça candidatos parecidos no "som".
4. **Combinação** — o score final mistura as duas medidas:

   ```
   score = 0,7 × travessia + 0,3 × similaridade_de_atributos
   ```

5. **Limpeza e ranking** — remove o que o usuário já ouviu e devolve o Top N.

## Cold-start (usuário novo)

Um usuário recém-criado não tem histórico, então a travessia não tem de onde partir. Nesse caso:

1. o usuário informa seus **gêneros preferidos**;
2. o sistema calcula o **centroide** (vetor médio) das músicas desses gêneros;
3. ordena as músicas pela proximidade ao centroide e devolve o Top N.

Assim, mesmo sem nenhuma interação registrada, o usuário já recebe recomendações coerentes com
o gosto declarado.

## Por que combinar as duas medidas

- A **travessia** captura padrões reais de comportamento (o que é ouvido junto), mas não funciona
  para músicas novas ou pouco avaliadas.
- A **similaridade de atributos** cobre essa lacuna (cold-start), mas tende a favorecer músicas do
  mesmo gênero.

Juntas, uma compensa a fraqueza da outra.
