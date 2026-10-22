# Bizus de gráficos de acordo com tipos de variáveis

## Numérica x Numérica -> Dispersão

```python
df.plot.scatter(x="investimento", y="receita", alpha=0.5)
plt.title("Investimento × receita")
plt.show()
```

Se houver muitos pontos:

```python
df.plot.hexbin(
    x="investimento",
    y="receita",
    gridsize=25,
    cmap="viridis",
)
plt.show()
```

**MATEMÁTICA:** Correlação de Pearson (Ordenado para `method='spearman'`)

```python
r = df["investimento"].corr(df["receita"])
print(r)
```

## Categórica x Numérica -> Boxplot

```python
df.boxplot(column="score", by="tipo", grid=False)
plt.title("Score por tipo de anunciante")
plt.suptitle("")
plt.xlabel("Tipo")
plt.ylabel("Score")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()
```

Se for especificamente sobre média ou mediana:

```python
medianas = df.groupby("tipo")["score"].median().sort_values()
medianas.plot.barh()
plt.xlabel("Mediana do score")
plt.ylabel("Tipo")
plt.tight_layout()
plt.show()
```

**MATEMÁTICA:** Ponto bisserial

```python
from scipy.stats import pointbiserialr
dados = df[["score", "converteu"]].dropna()
r, p = pointbiserialr(
    dados["converteu"].astype(int),
    dados["score"],
)
print("Correlação:", r)
print("Valor-p:", p)
```

Apenas o coeficiente:

```python
r = dados["score"].corr(dados["converteu"].astype(int))
```

## Categórica x Categórica -> Barras de proporções

```python
tabela = pd.crosstab(
    df["tipo"],
    df["plataforma"],
    normalize="index",
).mul(100)
tabela.plot.bar(stacked=True, rot=0)
plt.xlabel("Tipo de anunciante")
plt.ylabel("Proporção (%)")
plt.legend(title="Plataforma")
plt.tight_layout()
plt.show()
```

> [!NOTE]
> normalize pode ser ='index', ='columns' ou =True

**MATEMÁTICA:** Eta quadrado

```python
dados = df[["tipo", "score"]].dropna()
grupos = dados.groupby("tipo", observed=True)["score"]
medias = grupos.mean()
tamanhos = grupos.size()
media_geral = dados["score"].mean()
variacao_entre = (
    tamanhos * (medias - media_geral) ** 2
).sum()
variacao_total = (
    (dados["score"] - media_geral) ** 2
).sum()
eta2 = (
    variacao_entre / variacao_total
    if variacao_total > 0
    else float("nan")
)
print("Eta quadrado:", eta2)
```

## Numérica x Booleana -> Proporção por faixa

```python
dados = df.dropna(subset=["score", "converteu"]).copy()
dados["faixa"] = pd.cut(
    dados["score"],
    bins=[0, 20, 40, 60, 80, 100],
    include_lowest=True,
)
resumo = (
    dados.groupby("faixa", observed=True)["converteu"]
    .agg(proporcao="mean", quantidade="size")
)
resumo["proporcao"].mul(100).plot.bar(rot=30)
plt.xlabel("Faixa de score")
plt.ylabel("Conversão (%)")
plt.ylim(0, 100)
plt.tight_layout()
plt.show()
print(resumo)
```

**MATEMÁTICA:** Tabela de Contingência & V de Cramér

```python
import pandas as pd
from scipy.stats.contingency import association
tabela = pd.crosstab(df["tipo"], df["plataforma"])
v = association(
    tabela.to_numpy(),
    method="cramer",
    correction=False,
)
print("V de Cramér:", v)
```

## Data x Numérica -> Linha

```python
dados = df.copy()
dados["data"] = pd.to_datetime(dados["data"])
receita_diaria = (
    dados.set_index("data")["receita"]
    .resample("D")
    .sum(min_count=1) # Modificável para .mean(), .count(), etc.
)
receita_diaria.plot()
plt.xlabel("Data")
plt.ylabel("Receita diária")
plt.tight_layout()
plt.show()
```

## Data x Booleana -> Linha da proporção

```python
dados = df.copy()
dados["data"] = pd.to_datetime(dados["data"])
taxa_semanal = (
    dados.set_index("data")["converteu"]
    .resample("W")
    .mean()
    .mul(100)
)
taxa_semanal.plot(marker="o")
plt.xlabel("Semana")
plt.ylabel("Conversão (%)")
plt.ylim(0, 100)
plt.tight_layout()
plt.show()
```

## Booleana x Booleana

**MATEMÁTICA:** phi (equivalente à correlação de Pearson, mas como 0 e 1)

```python
dados = df[["clicou", "comprou"]].dropna().astype(int)
phi = dados["clicou"].corr(dados["comprou"])
print("Phi:", phi)
```

Comparar a proporção:

```python
print(df.groupby("clicou")["comprou"].mean())
```
