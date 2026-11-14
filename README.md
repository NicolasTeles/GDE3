# GDE3 (exploratório)

Implementação **exploratória e incompleta** em Python do GDE3 (*Generalized Differential Evolution 3*), um algoritmo evolutivo multiobjetivo baseado em evolução diferencial. Foi um estudo pessoal, iniciado em outubro de 2025 e **interrompido no meio**: o código roda, mas é uma versão simplificada do algoritmo e não foi validado contra a versão original nem contra outros métodos.

## O problema de teste

Cada indivíduo é um veículo elétrico fictício com três variáveis:

| Variável | Intervalo |
|---|---|
| Diâmetro da roda | 10 a 30 |
| Potência do motor | 50 a 200 |
| Capacidade da bateria | 100 a 500 |

Dois objetivos são calculados a partir delas (as fórmulas são inventadas, só para ter um problema de duas dimensões):

- **Autonomia** = `capacidade_bateria / (potencia_motor * diametro_roda)`, a ser **maximizada**;
- **Tempo de aceleração** = `(capacidade_bateria + diametro_roda) / potencia_motor`, a ser **minimizado**.

## O que o código faz

1. Gera uma população inicial aleatória (`random.seed(42)`, 3000 indivíduos).
2. A cada geração (1200 no total), para cada indivíduo cria um vetor de teste por evolução diferencial: `alvo + F * (aleatório1 - aleatório2)`, com `F = 0,5`, refazendo o sorteio enquanto alguma variável sair do intervalo.
3. Cruza o pai com o vetor de teste, escolhendo cada variável de um dos dois com probabilidade 50%.
4. Compara pelo critério de dominância de Pareto: se o filho domina o pai, fica o filho; se o pai domina, fica o pai; se nenhum domina o outro, os dois são guardados como par.
5. Para os pares, calcula a distância de aglomeração (*crowding distance*) e mantém o de maior distância.
6. Ao final, salva dois gráficos de dispersão (autonomia x tempo de aceleração): `populacao inicial.png` e `nova populacao.png`.

## Executar

Requisitos: Python 3.10 ou superior (usa a sintaxe `int | float`) e `matplotlib`.

```
pip install matplotlib
python main.py
```

O programa imprime todos os indivíduos iniciais e uma linha por geração, e no fim o tempo de CPU. Os valores padrão (3000 indivíduos e 1200 gerações) são muito maiores do que o necessário: foram valores de teste, usados para forçar uma execução pesada e observar o comportamento do algoritmo. Por isso a execução com eles é demorada. Reduza `NUM_INDIVIDUOS` e `GERACOES` no início do `main.py` para rodar rápido. As imagens geradas são ignoradas pelo Git (`.gitignore`).

## Estado atual e limitações

- Não é um GDE3 completo: não há seleção por não dominância seguida de truncamento da população inteira, e a distância de aglomeração só é calculada para os indivíduos que formaram pares.
- O cruzamento troca variáveis com probabilidade fixa de 50%, sem parâmetro de taxa de cruzamento.
- O cálculo da distância de aglomeração é lento (buscas lineares na lista a cada geração) e não foi otimizado.
- Os parâmetros ficam no código e não há argumentos de linha de comando.
- Não há testes nem análise dos resultados.
