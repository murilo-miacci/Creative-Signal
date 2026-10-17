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
