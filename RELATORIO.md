# Relatório - Escolhedor de Algoritmo de Ordenação

**Dupla:** Matheus Martins Pagel e Daniel Bernardes Araújo

## 1. Comparação nos quatro cenários

Os tempos abaixo foram obtidos rodando `python testes/medir.py`, que calcula a mediana de 5 execuções com `time.perf_counter()` e semente fixa (`random.seed(42)`). Nos três primeiros cenários usamos listas de tamanho $n = 10\,000$; no cenário de lista minúscula usamos $n = 12$ (tirando a média de 500 listas por repetição para reduzir o ruído da medição).

| Cenário | `insercao` | `intercalacao` | `rapido` | `hibrido` | `contagem` | `base` | `ordenar` | Escolha feita |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Aleatório com chaves grandes ($n = 10\,000$, valores em $[0, 10^{12}]$) | 1435,71 ms | 14,40 ms | 14,45 ms | 11,88 ms | MemError* | 4,21 ms | 4,51 ms | `base` |
| Faixa estreita ($n = 10\,000$, valores em $[0, 100]$) | 1239,93 ms | 12,97 ms | 4,82 ms | 4,55 ms | 0,44 ms | 1,04 ms | 0,54 ms | `contagem` |
| Quase ordenado ($n = 10\,000$, 25 trocas de vizinhos) | 0,56 ms | 8,59 ms | 12,59 ms | 10,46 ms | 1,47 ms | 1,74 ms | 0,80 ms | `insercao` |
| Lista minúscula ($n = 12$, valores em $[0, 1000]$) | 2,25 µs | 6,40 µs | 5,16 µs | 2,34 µs | 18,81 µs | 28,21 µs | 2,39 µs | `insercao` |

*\*No cenário de chaves grandes, a amplitude $k = \text{maior} - \text{menor} + 1$ fica na casa de $10^{12}$. A contagem tentaria alocar um vetor desse tamanho em memória (vários terabytes), causando `MemoryError`.*

Olhando para a tabela, fica evidente que nenhum método fixo é o melhor em todas as situações: a inserção é ótima quando a lista é minúscula ou quase ordenada, mas leva mais de 1 segundo nas listas aleatórias maiores; a contagem é a mais rápida na faixa estreita, mas estoura a memória quando as chaves são grandes; a ordenação por base vai muito bem nas chaves grandes, mas tem muito custo fixo nas listas pequenas. O `ordenar(v)` consegue escolher o método vencedor em todos os quatro cenários e fica com tempo muito próximo do melhor de cada linha.

## 2. Qual venceu cada cenário e por quê

**Aleatório com chaves grandes (`base`, 4,21 ms):**
Nesse cenário a contagem não pode ser usada por causa do consumo de memória $O(k)$. Entre os demais, a ordenação por base (implementada com Radix Sort LSD em base 256, olhando 1 byte por vez) venceu porque chaves de até $10^{12}$ cabem em 40 bits, exigindo apenas 5 passadas lineares sobre o vetor com operações bit a bit. Já os métodos por comparação (`intercalacao`, `rapido` e `hibrido`) têm custo $\Theta(n \log n)$ e sofrem mais com o custo de recursão e comparações no interpretador do Python, ficando entre 11,88 ms e 14,45 ms.

**Faixa estreita (`contagem`, 0,44 ms):**
Com valores restritos ao intervalo $[0, 100]$, a faixa $k = 101$ é muito menor que $n = 10\,000$. A contagem aloca uma lista pequena de 101 posições, conta as ocorrências em uma passada e monta a resposta repetindo os elementos de cada posição. Vale notar que o `rapido` e o `hibrido` caíram de ~14 ms para ~4,6 ms nesse cenário porque implementamos a partição em três vias (menores, iguais e maiores que o pivô), que descarta todas as cópias iguais ao pivô de uma vez só, mas ainda assim a contagem linear é dez vezes mais rápida.

**Quase ordenado (`insercao`, 0,56 ms):**
O custo da ordenação por inserção é $O(n + \text{inversões})$. Como a entrada foi gerada a partir de uma lista ordenada com apenas 25 trocas entre elementos vizinhos, quase todos os elementos já estão no lugar certo e o laço interno (`while`) raramente executa. Por isso ela percorre o vetor praticamente uma única vez, ganhando até da contagem (1,47 ms) e da base (1,74 ms), que precisam achar `min` e `max` e alocar listas auxiliares mesmo quando a entrada já está quase pronta.

**Lista minúscula (`insercao`, 2,25 µs):**
Para $n = 12$, a diferença assintótica entre $O(n^2)$ e $O(n \log n)$ é irrelevante perto do custo constante de cada algoritmo. A inserção usa apenas dois laços simples sobre uma cópia da lista, sem chamadas recursivas, sem sorteio de pivô (`random.randint`) e sem alocar baldes ou vetores de contagem. O `hibrido` (2,34 µs) praticamente empata com ela justamente porque seu corte interno (`LIMITE_INSERCAO = 16`) manda listas de tamanho 12 direto para a rotina de inserção.

## 3. Regras do `escolher` e de onde vieram

A função `escolher(v)` em `src/seletor/escolhedor.py` testa três condições, na ordem da mais barata para a mais custosa:

1. **Tamanho até 16 (`n <= 16` $\rightarrow$ `insercao`):**
   Testamos vários tamanhos pequenos e vimos que até por volta de 16 elementos a inserção empata ou ganha da ordenação rápida por ter menos overhead por chamada (o mesmo corte foi usado no algoritmo híbrido). Como `len(v)` é $O(1)$, essa checagem é imediata.

2. **Proporção de descidas até 1% (`descidas <= 0.01 * n` $\rightarrow$ `insercao`):**
   Para saber se a lista está quase ordenada sem gastar $O(n \log n)$ contando inversões, contamos quantas vezes um elemento é menor que o anterior ($v[i] < v[i-1]$). Se essa quantidade não passar de 1% do tamanho da lista, devolvemos `insercao`.
   Para atender ao aviso do enunciado e não percorrer a lista inteira à toa, o laço para com `break` assim que o número de descidas passa do limite de 1%. Numa lista aleatória de $10\,000$ elementos, metade dos pares vizinhos sobe e metade desce, então o limite de 100 descidas estoura perto da posição 200. Ou seja: em listas embaralhadas o laço olha apenas ~200 elementos antes de desistir, e só percorre tudo quando a lista realmente é quase ordenada (caso em que já retorna `insercao` sem fazer mais nada).

3. **Faixa de valores (`maior - menor + 1 <= 4 * n` $\rightarrow$ `contagem`, senão `base`):**
   Se a lista não é pequena nem quase ordenada, calculamos `min(v)` e `max(v)`. Optamos pelas funções embutidas do Python porque elas rodam em C e, nos testes, foram bem mais rápidas do que escrever um `for` em Python para achar o menor e o maior ao mesmo tempo.
   Se a faixa $k = \text{maior} - \text{menor} + 1$ for de no máximo $4n$, o consumo de memória da contagem permanece linear em $n$ e ela é mais rápida que os outros métodos, então devolvemos `contagem`. Se a faixa passar de $4n$, evitamos a contagem (prevenindo tanto lentidão quanto estouro de memória em chaves grandes) e devolvemos `base`, que superou o `hibrido` e o `rapido` nas nossas medições com inteiros.

## 4. Quanto custa rodar o `escolher` — ele compensa?

Para verificar o peso da decisão, o script `testes/medir.py` também mede o tempo de chamar apenas `escolher(v)` em comparação com o tempo total de `ordenar(v)`:

| Cenário | Tempo do `escolher(v)` | Tempo do `ordenar(v)` | Peso no tempo total |
| :--- | :---: | :---: | :---: |
| Aleatório com chaves grandes ($n = 10\,000$) | 0,119 ms | 4,273 ms | 2,8% |
| Faixa estreita ($n = 10\,000$) | 0,108 ms | 0,525 ms | 20,6% |
| Quase ordenado ($n = 10\,000$) | 0,161 ms | 0,738 ms | 21,8% |
| Lista minúscula ($n = 12$) | 0,04 µs | 2,31 µs | 1,9% |

O custo do `escolher` compensa claramente em todos os casos. Na lista minúscula, ele gasta 0,04 µs (só checa `len(v)`). Nos cenários aleatório e de faixa estreita, o laço de descidas aborta logo no começo e o `min`/`max` em C gasta cerca de 0,11 ms; na faixa estreita isso representa ~20% do tempo total porque a contagem em si é muito rápida (0,44 ms), mas o total de ~0,54 ms ainda é quase a metade do tempo da `base` (1,04 ms) e oito vezes menor que o `hibrido` (4,55 ms). No quase ordenado, percorrer a lista no `escolher` custa 0,16 ms, mas economiza mais de 9 ms em relação ao `hibrido` ou `rapido`.

## 5. Um cenário em que o `escolher` erra a decisão

O ponto fraco do `escolher` está na segunda regra: olhar apenas para pares adjacentes ($v[i] < v[i-1]$) não mede a distância que os elementos fora de lugar precisam percorrer. Uma lista pode ter pouquíssimas descidas e, mesmo assim, ter um número quadrático de inversões.

Um exemplo direto para $n = 10\,000$ é colocar os valores de $100$ até $9\,999$ em ordem crescente e deixar os $100$ menores valores no final, em ordem decrescente:

```python
v = list(range(100, 10_000)) + list(range(100, 0, -1))
```

Nessa lista existem exatamente 100 descidas (1% de $n$), todas concentradas no final. Como não ultrapassa a tolerância de 1%, o `escolher(v)` acha que a lista está quase ordenada e devolve `insercao`. Porém, na hora de ordenar, cada um desses 100 elementos pequenos que estão no fim precisa ser deslocado para o início da lista, passando por quase todos os $9\,900$ elementos maiores ($\approx 990\,000$ trocas no laço interno).

Medindo essa entrada no `testes/medir.py`, temos:

- Escolha do `escolher(v)`: **`insercao`**, levando **49,27 ms**.
- Se tivesse escolhido **`contagem`**: levaria **1,43 ms** (cerca de 34 vezes mais rápido).
- Se tivesse escolhido **`base`**: levaria **2,05 ms**.
- Mesmo **`intercalacao`** (8,50 ms), **`hibrido`** (10,13 ms) e **`rapido`** (12,32 ms) seriam de 4 a 6 vezes mais rápidos que a escolha feita.

*(Nota: o mesmo problema ocorre até com uma única descida se a lista for rotacionada, como `list(range(100, 10_000)) + list(range(100))`, pois os 100 menores elementos continuam no final precisando atravessar o vetor inteiro na inserção.)*
