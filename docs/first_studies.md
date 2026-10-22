# Estudo sobre tópicos e abordagens

O seguinte documento tem por função servir de anotação, guia de estudos e estruturação de uma possível solução para o desafio. Busquei escrever a maior parte disso de forma autoral, preservando o meu raciocínio ao máximo, salvo momentos em que peço para a IA me explicar determinados tópicos que desconheço e quando coloco códigos de exemplos.

Utilizarei a biblioteca Pandas em Python.

## Como fazer um perfil geral dos dados?

Analisaria as informações estruturais e diretas que o dataframe pode me dar como `df.head()`, `df.shape()`, `df.info()`, `df.isna().sum()` e `df.describe()`.

Logo após já saber como estão estruturados as 500 linhas, veria uma parte mais generalista dos dados, como média, mediana, outliers, contagens, NAs nas colunas, por meio de `df.groupby()`, `df.agg()`, `df.sort_values()` e parâmetros úteis.

## Como conectar dados de uma coluna com outra de forma proveitosa? Quais são os padrões de generalização? Como relacionar o score?

| Relação                 | Abordagem                                                |
| ----------------------- | -------------------------------------------------------- |
| Numérica x Numérica     | Correlação (Dispersão)                                   |
| Categórica x Numérica   | Estatísticas por grupo e distribuição de notas (boxplot) |
| Categórica x Categórica | Tabela de frequências cruzadas (bar, heat map)           |
| Tempo x Numérica        | Evolução ao do tempo (Linha)                             |

Preciso estudar todas as variáveis presentes e ver quais mais se relacionam com o klike score.

## Como criar um modelo preditivo? O que é um modelo de regressão? Como treiná-lo?

Pelo meu entendimento, uma forma de fazer uma previsão a partir de dados numéricos é pela regressão linear, em que se obtém uma função do primeiro grau que mais se aproxima da relação dos dados.
Utiliza-se a biblioteca scikit-learn para isso. `.fit()` é um comando que faz essa regressão linear, junto de `LinearRegression`.

Um exemplo de modelo (MAE - erro absoluto médio) é:

```python
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline

# Precisamos conhecer a resposta dos exemplos de treinamento.
dados = df.dropna(subset=["score"])

X = dados[["duracao", "ano"]]
y = dados["score"]

# 60% para treino; 40% ficam reservados.
X_treino, X_reserva, y_treino, y_reserva = train_test_split(
    X,
    y,
    test_size=0.40,
    random_state=42,
)

# Metade dos 40% para validação; metade para teste.
X_validacao, X_teste, y_validacao, y_teste = train_test_split(
    X_reserva,
    y_reserva,
    test_size=0.50,
    random_state=42,
)

modelo = make_pipeline(
    SimpleImputer(strategy="median"),
    LinearRegression(),
)

modelo.fit(X_treino, y_treino)

previsoes_validacao = modelo.predict(X_validacao)

mae_validacao = mean_absolute_error(
    y_validacao,
    previsoes_validacao,
)

print("MAE na validação:", mae_validacao)
```

Uma baseline é necessária para que se valide os dados usados como evidência

```python
previsoes_baseline = [
    y_treino.median()
] * len(y_validacao)

mae_baseline = mean_absolute_error(
    y_validacao,
    previsoes_baseline,
)

print("MAE do baseline:", mae_baseline)

previsoes_teste = modelo.predict(X_teste)

print(
    "MAE no teste:",
    mean_absolute_error(y_teste, previsoes_teste),
)
```

## Como fazer a Engine? Qual será a divisão do dataset?

Uma possível divisão é: 60% treino, 20% validação e 20% teste

Uma engine responde perguntas como: "Qual filme esta pessoa vai provavelmente querer assistir?". Tem mais a ver com uma recomendação com base em uma análise de perfil do que simplesmente a melhor estatística.

Adiciona-se uma nova tabela para guardar informações relevantes de determinado perfil, pois é a parte crucial da Engine.

Um exemplo de recomendação:

```python
generos_preferidos = ["Drama", "Ficção científica"]
filmes_ja_vistos = [1, 8, 15]

filtro = (
    df["genero"].isin(generos_preferidos)
    & ~df["filme_id"].isin(filmes_ja_vistos)
    & df["score"].notna()
)

recomendacoes = (
    df.loc[filtro]
    .sort_values("score", ascending=False)
    .head(5)
)

print(recomendacoes[["titulo", "genero", "score"]])
```

| O que eu quero avaliar                    | Abordagem de separação                    |
| ----------------------------------------- | ----------------------------------------- |
| Prever notas de outros filmes semelhantes | Divisão aleatória                         |
| Recomendar próximas interações            | Treinar com passado e avaliar com recente |
| Recomendar para usuários novos            | Reservar dados de outros usuários         |
| Recomendar itens novos                    | Reservar dados de outros itens            |

### Extra

Preciso avaliar se outras métricas de modelagem seriam melhores que MAE.

Preciso construir todo o escopo do dataframe (dataset) antes de começar a trabalhar nos modelos e, principalmente, engine.

## Consolidação da estrutura

Começarei vendo os dados diretos do dataframe. Então atacarei cada relação das variáveis mais relevantes e depois atacarei com o score, fazendo relações tanto matemáticas quanto gráficas e guardando todos os resultados de forma a tornar o mais útil possível cada valor e representação de relação, assim como descartarei o que não for relevante.

Após isso, iniciarei o modelo com a métrica MAE, mas também testarei para outras métricas a fim de conhecer o propósito de cada uma. Logo após a consolidação de um modelo funcional para certas variáveis, irei fazer o treinamento + validação + testes.

Por fim, com tudo isso feito, irei explorar as melhores formas de construir uma engine funcional que faça exatamente o que eu quero. Disso, quero que entregue uma resposta simples com base em um cenário não tão simples. A ideia que eu vou correr atrás para por em prática é: quanto menos complicada for a resolução da Engine, melhor será. Mas, simples não implica em pouco ou fraco e sim em preciso e assertivo, com fundamentação e base bem formulada.

Mãos à obra!
