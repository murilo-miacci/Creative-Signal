"""Exploratory Data Analysis."""

import matplotlib.pyplot as plt
import pandas as pd

dados = pd.read_csv("data/campaigns.csv")

# print(dados.shape)
# 500 x 26

# dados.to_html("dados.html")
# Melhor pra vizualização o tempo todo em live server

# print(dados.dtypes)
# campaign_id                str
# date                       str
# platform                   str
# category                   str
# objective                  str
# target_audience_age        str
# is_retargeting            bool
# video_duration_s       float64
# format                     str
# has_subtitle            object
# has_cta                   bool
# has_hook                  bool
# has_face                  bool
# text_density               str
# music_voice_ratio      float64
# impressions              int64
# clicks                   int64
# ctr                    float64
# cpc                    float64
# spend                  float64
# conversions              int64
# revenue                float64
# roas                   float64
# avg_watch_time_s       float64
# engagement_rate        float64
# klike_score            float64

# print(dados.isna().sum())
# nºNA > 0
# video_duration_s   39
# has_subtitle       46
# music_voice_radio  38
# cpc                28
# revenue            25
# avg_watch_time_s   27
# engagement_rate    32

# print(dados["klike_score"].describe())
# count    500.0000
# mean      60.1568
# std       15.5891
# min       10.4000
# 25%       49.7750
# 50%       60.5500
# 75%       71.9250
# max       99.1000

# =============================================================================
#                         Modificações na base de dados
# =============================================================================

dados["date"] = pd.to_datetime(dados["date"])

# =============================================================================
#                             Funções EDA (Score)
# =============================================================================


def platformxscore(raw: pd.DataFrame) -> None:
    """
    ———————————————————————————————————————————————————————————————————————————
    Plataforma x Score
    (Meta, TikTok, LinkedIn)
    ———————————————————————————————————————————————————————————————————————————
    Meta apresenta mais observações e menor dispersão dos scores. Sua média
    amostral é 1,25 ponto inferior à do TikTok.
    As diferenças entre médias das plataformas representam apenas 1,35% da
    variação do score (eta² = 0,0135), indicando pequena associação nessa
    amostra. Os 98,65% restantes correspondem à variação dentro das próprias
    plataformas. Esses resultados não implicam causalidade.

    """
    df = raw[["platform", "klike_score"]].dropna()
    df["platform"] = pd.Categorical(
        df["platform"], categories=["Meta", "TikTok", "LinkedIn"]
    )
    groups = df.groupby("platform", observed=True)["klike_score"]
    resume = groups.agg(["count", "mean", "median", "std"])
    print(resume)

    mean = df["klike_score"].mean()
    ss_effect = (resume["count"] * (resume["mean"] - mean) ** 2).sum()
    ss_total = ((df["klike_score"] - mean) ** 2).sum()
    eta2 = ss_effect / ss_total if ss_total > 0 else float("nan")

    ax = df.boxplot(column="klike_score", by="platform", grid=False)
    ax.set_title(f"Score por Plataforma (η² = {eta2:.4f})")
    ax.set_xlabel("Plataforma")
    ax.set_ylabel("Klike score")
    ax.figure.suptitle("")
    plt.show()


def formatxscore(raw: pd.DataFrame) -> None:
    """
    ———————————————————————————————————————————————————————————————————————————
    Formato x Score
    (Vertical, Horizontal, Quadrado)
    ———————————————————————————————————————————————————————————————————————————
    Os formatos não apresentam forte associação com o score, sendo pouco
    relevante o maior valor observado no formato vertical.
    """
    df = raw[["format", "klike_score"]]
    df["format"] = pd.Categorical(
        df["format"], categories=["vertical", "horizontal", "quadrado"]
    )
    groups = df.groupby("format", observed=True)["klike_score"]
    resume = groups.agg(["count", "mean", "median", "std"])
    print(resume)

    df.boxplot(column="klike_score", by="format", grid=False)
    plt.title("Score por Formato de Criativo")
    plt.suptitle("")
    plt.xlabel("Formato")
    plt.ylabel("Score")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()


def subtitlexscore(raw: pd.DataFrame) -> None:
    """
    ———————————————————————————————————————————————————————————————————————————
    Legenda x Score
    (True, False)
    ———————————————————————————————————————————————————————————————————————————
    A presença de legenda é um bom indicativo de aumento no score, uma vez que
    sua média e mediana são relativamente maiores.
    """
    df = raw[["has_subtitle", "klike_score"]].dropna()
    groups = df.groupby("has_subtitle", observed=True)
    resume = groups.agg(["count", "mean", "median", "std"])
    print(resume)

    df.boxplot(column="klike_score", by="has_subtitle", grid=False)
    plt.title("Score por Presença de Legenda")
    plt.suptitle("")
    plt.xlabel("Possui legenda?")
    plt.ylabel("Score")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()


def categoryxscore(raw: pd.DataFrame) -> None:
    """
    ———————————————————————————————————————————————————————————————————————————
    Category x Score
    (Branding, App Install, SaaS, Lead Gen, E-commerce)
    ———————————————————————————————————————————————————————————————————————————
    Saas e E-commerce aparecem com valores de média e mediana insuficientemente
    maiores para uma conclusão de associação com o score.
    """
    df = raw[["category", "klike_score"]]
    df["category"] = pd.Categorical(
        df["category"],
        categories=["Branding", "App Install", "SaaS", "Lead Gen", "E-commerce"],
    )
    groups = df.groupby("category", observed=True)
    resume = groups.agg(["count", "mean", "median", "std"])
    print(resume)

    df.boxplot(column="klike_score", by="category", grid=False)
    plt.title("Score por Categoria de Criativo de Anúncio")
    plt.suptitle("")
    plt.xlabel("Categoria")
    plt.ylabel("Score")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()


def objectivexscore(raw: pd.DataFrame) -> None:
    """
    ———————————————————————————————————————————————————————————————————————————
    Objetivo x Score
    (awareness, traffic, conversions, engagement, app_install)
    ———————————————————————————————————————————————————————————————————————————
    Conversions aparece com maior média e mediana, mas é um dado quase
    irrelevante dado a proximidade com os outros valores extremamente próximos.
    """
    df = raw[["objective", "klike_score"]]
    df["objective"] = pd.Categorical(
        df["objective"],
        categories=["awareness", "traffic", "conversions", "engagement", "app_install"],
    )
    groups = df.groupby("objective", observed=True)
    resume = groups.agg(["count", "mean", "median", "std"])
    print(resume)

    df.boxplot(column="klike_score", by="objective", grid=False)
    plt.title("Score por Objetivo do Criativo")
    plt.suptitle("")
    plt.xlabel("Objetivo")
    plt.ylabel("Score")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()


def agexscore(raw: pd.DataFrame) -> None:
    """
    ———————————————————————————————————————————————————————————————————————————
    Faixa de Idade Alvo x Score
    (18-24, 25-34, 35-44, 45+)
    ———————————————————————————————————————————————————————————————————————————
    É aparente que o público com as idades entre 25-34 são dos criativos que
    obtêm melhores scores. Não é uma relação forte, mas é relevante.
    """
    df = raw[["target_audience_age", "klike_score"]]
    df["target_audience_age"] = pd.Categorical(
        df["target_audience_age"],
        categories=["18-24", "25-34", "35-44", "45+"],
    )
    groups = df.groupby("target_audience_age", observed=True)
    resume = groups.agg(["count", "mean", "median", "std"])
    print(resume)

    df.boxplot(column="klike_score", by="target_audience_age", grid=False)
    plt.title("Score por Faixa de Idade Alvo")
    plt.suptitle("")
    plt.xlabel("Faixa de Idade")
    plt.ylabel("Score")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()


def retargetingxscore(raw: pd.DataFrame) -> None:
    """
    ———————————————————————————————————————————————————————————————————————————
    Retargeting x Score
    (True, False)
    ———————————————————————————————————————————————————————————————————————————
    Quando o anúncio do criativo é visto mais de uma vez, o score tende a haver
    um aumento, porém, não tão significante a ponto de deixar clara uma relação.
    """
    df = raw[["is_retargeting", "klike_score"]]
    groups = df.groupby("is_retargeting", observed=True)
    resume = groups.agg(["count", "mean", "median", "std"])
    print(resume)

    df.boxplot(column="klike_score", by="is_retargeting", grid=False)
    plt.title("Score por Retargeting")
    plt.suptitle("")
    plt.xlabel("Retarget?")
    plt.ylabel("Score")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()


def videodurationxscore(raw: pd.DataFrame) -> None:
    """
    ———————————————————————————————————————————————————————————————————————————
    Duração do Vídeo x Score
    (Duração em segundos [s])
    ———————————————————————————————————————————————————————————————————————————
    É observado pelas correlações de Pearson e Spearman que com o aumento da
    duração do vídeo há uma ligeira diminuição do score (~1,4%) e a tendência é
    diminuir o score (~3,8%), respectivamente.
    """
    df = raw[["video_duration_s", "klike_score"]].dropna()

    pearson = df["video_duration_s"].corr(df["klike_score"])
    print(f"Correlação (Pearson): {pearson}")
    spearman = df["video_duration_s"].corr(df["klike_score"], method="spearman")
    print(f"Correlação (Spearman): {spearman}")

    df.plot.scatter(x="video_duration_s", y="klike_score", alpha=0.5)
    plt.title("Score por Duração de Vídeo")
    plt.suptitle("")
    plt.xlabel("Tempo [s]")
    plt.ylabel("Score")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()


def ctaxscore(raw: pd.DataFrame) -> None:
    """
    ———————————————————————————————————————————————————————————————————————————
    Presentça de CTA (Call To Action) x Score
    (True, False)
    ———————————————————————————————————————————————————————————————————————————
    A presença de CTA no criativo se relaciona com uma maior taxa de score
    observado.
    """
    df = raw[["has_cta", "klike_score"]]
    groups = df.groupby("has_cta", observed=True)
    resume = groups.agg(["count", "mean", "median", "std"])
    print(resume)

    df.boxplot(column="klike_score", by="has_cta", grid=False)
    plt.title("Score por Presença de CTA no Criativo")
    plt.suptitle("")
    plt.xlabel("CTA?")
    plt.ylabel("Score")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()


def hookxscore(raw: pd.DataFrame) -> None:
    """
    ———————————————————————————————————————————————————————————————————————————
    Presença de Hook x Score
    (True, False)
    ———————————————————————————————————————————————————————————————————————————
    A presença de hook no criativo se relaciona com o aumento do score.
    """
    df = raw[["has_hook", "klike_score"]]
    groups = df.groupby("has_hook", observed=True)
    resume = groups.agg(["count", "mean", "median", "std"])
    print(resume)

    df.boxplot(column="klike_score", by="has_hook", grid=False)
    plt.title("Score por Presença de Hook no Criativo")
    plt.suptitle("")
    plt.xlabel("Hook?")
    plt.ylabel("Score")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()


def facexscore(raw: pd.DataFrame) -> None:
    """
    ———————————————————————————————————————————————————————————————————————————
    Presença de Rosto x Score
    (True, False)
    ———————————————————————————————————————————————————————————————————————————
    A presença de rosto no criativo se relaciona com o aumento do score.
    """
    df = raw[["has_face", "klike_score"]]
    groups = df.groupby("has_face", observed=True)
    resume = groups.agg(["count", "mean", "median", "std"])
    print(resume)

    df.boxplot(column="klike_score", by="has_face", grid=False)
    plt.title("Score por Presença de Rosto no Criativo")
    plt.suptitle("")
    plt.xlabel("Rosto?")
    plt.ylabel("Score")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()


def textxscore(raw: pd.DataFrame) -> None:
    """
    ———————————————————————————————————————————————————————————————————————————
    Densidade de Texto x Score
    (low, medium, high)
    ———————————————————————————————————————————————————————————————————————————
    É fortemente observado um maior score na densidade média de texto no
    criativo, seguido de densidade baixa e alta, com intervalos grandes entre
    os marcadores (65, 59 e 60, respectivamente).
    """
    df = raw[["text_density", "klike_score"]]
    df["text_density"] = pd.Categorical(
        df["text_density"],
        categories=["low", "medium", "high"],
    )
    groups = df.groupby("text_density", observed=True)
    resume = groups.agg(["count", "mean", "median", "std"])
    print(resume)

    df.boxplot(column="klike_score", by="text_density", grid=False)
    plt.title("Score por Densidade de Texto")
    plt.suptitle("")
    plt.xlabel("Densidade")
    plt.ylabel("Score")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()


def musicvoicexscore(raw: pd.DataFrame) -> None:
    """
    ———————————————————————————————————————————————————————————————————————————
    Relação Música e Voz x Score
    (Duração em segundos [s])
    ———————————————————————————————————————————————————————————————————————————
    É visto uma baixa, porém levemente considerável, tendência de que com o
    aumento da Música com a Voz no criativo, há uma diminuição do score.
    """
    df = raw[["music_voice_ratio", "klike_score"]].dropna()

    pearson = df["music_voice_ratio"].corr(df["klike_score"])
    print(f"Correlação (Pearson): {pearson}")
    spearman = df["music_voice_ratio"].corr(df["klike_score"], method="spearman")
    print(f"Correlação (Spearman): {spearman}")

    df.plot.scatter(x="music_voice_ratio", y="klike_score", alpha=0.5)
    plt.title("Score pela Relação de Música e Voz no criativo")
    plt.suptitle("")
    plt.xlabel("Relação Musica x Voz")
    plt.ylabel("Score")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()


def impressionsxscore(raw: pd.DataFrame) -> None:
    """
    ———————————————————————————————————————————————————————————————————————————
    Impressões x Score
    (Número de impressões)
    ———————————————————————————————————————————————————————————————————————————
    O número de impressões apresenta correlações muito próximas de zero com o
    score, sendo levemente negativa em Pearson (-0,080) e positiva em
    Spearman (0,032). Não é observada uma relação relevante nessa amostra.
    """
    df = raw[["impressions", "klike_score"]].dropna()

    pearson = df["impressions"].corr(df["klike_score"])
    print(f"Correlação (Pearson): {pearson}")
    spearman = df["impressions"].corr(df["klike_score"], method="spearman")
    print(f"Correlação (Spearman): {spearman}")

    df.plot.scatter(x="impressions", y="klike_score", alpha=0.5)
    plt.title("Score por Número de Impressões")
    plt.suptitle("")
    plt.xlabel("Impressões")
    plt.ylabel("Score")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()


def clicksxscore(raw: pd.DataFrame) -> None:
    """
    ———————————————————————————————————————————————————————————————————————————
    Cliques x Score
    (Número de cliques)
    ———————————————————————————————————————————————————————————————————————————
    É observada uma relação positiva entre o número de cliques e o score,
    fraca em Pearson (0,152) e mais evidente em Spearman (0,303). A tendência
    é de scores maiores nos criativos com mais cliques, porém com dispersão.
    """
    df = raw[["clicks", "klike_score"]].dropna()

    pearson = df["clicks"].corr(df["klike_score"])
    print(f"Correlação (Pearson): {pearson}")
    spearman = df["clicks"].corr(df["klike_score"], method="spearman")
    print(f"Correlação (Spearman): {spearman}")

    df.plot.scatter(x="clicks", y="klike_score", alpha=0.5)
    plt.title("Score por Número de Cliques")
    plt.suptitle("")
    plt.xlabel("Cliques")
    plt.ylabel("Score")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()


def ctrxscore(raw: pd.DataFrame) -> None:
    """
    ———————————————————————————————————————————————————————————————————————————
    CTR x Score
    (Taxa de cliques)
    ———————————————————————————————————————————————————————————————————————————
    A taxa de cliques apresenta uma associação positiva moderada com o score,
    tanto em Pearson (0,503) quanto em Spearman (0,539). É observado que
    criativos com maior CTR tendem a apresentar scores maiores.
    """
    df = raw[["ctr", "klike_score"]].dropna()

    pearson = df["ctr"].corr(df["klike_score"])
    print(f"Correlação (Pearson): {pearson}")
    spearman = df["ctr"].corr(df["klike_score"], method="spearman")
    print(f"Correlação (Spearman): {spearman}")

    df.plot.scatter(x="ctr", y="klike_score", alpha=0.5)
    plt.title("Score por Taxa de Cliques")
    plt.suptitle("")
    plt.xlabel("CTR")
    plt.ylabel("Score")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()


def cpcxscore(raw: pd.DataFrame) -> None:
    """
    ———————————————————————————————————————————————————————————————————————————
    CPC x Score
    (Custo por clique [R$])
    ———————————————————————————————————————————————————————————————————————————
    O custo por clique apresenta uma relação negativa fraca com o score,
    com Pearson de -0,105 e Spearman de -0,089. É vista uma ligeira tendência
    de scores menores com o aumento do CPC, porém pouco relevante.
    """
    df = raw[["cpc", "klike_score"]].dropna()

    pearson = df["cpc"].corr(df["klike_score"])
    print(f"Correlação (Pearson): {pearson}")
    spearman = df["cpc"].corr(df["klike_score"], method="spearman")
    print(f"Correlação (Spearman): {spearman}")

    df.plot.scatter(x="cpc", y="klike_score", alpha=0.5)
    plt.title("Score por Custo por Clique")
    plt.suptitle("")
    plt.xlabel("CPC [R$]")
    plt.ylabel("Score")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()


def spendxscore(raw: pd.DataFrame) -> None:
    """
    ———————————————————————————————————————————————————————————————————————————
    Gasto Total x Score
    (Gasto total [R$])
    ———————————————————————————————————————————————————————————————————————————
    O gasto total apresenta uma correlação linear muito baixa com o score
    (Pearson de 0,052), mas uma tendência positiva fraca em Spearman (0,237).
    Maiores gastos se associam levemente a scores maiores, com dispersão.
    """
    df = raw[["spend", "klike_score"]].dropna()

    pearson = df["spend"].corr(df["klike_score"])
    print(f"Correlação (Pearson): {pearson}")
    spearman = df["spend"].corr(df["klike_score"], method="spearman")
    print(f"Correlação (Spearman): {spearman}")

    df.plot.scatter(x="spend", y="klike_score", alpha=0.5)
    plt.title("Score por Gasto Total")
    plt.suptitle("")
    plt.xlabel("Gasto [R$]")
    plt.ylabel("Score")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()


def revenuexscore(raw: pd.DataFrame) -> None:
    """
    ———————————————————————————————————————————————————————————————————————————
    Receita x Score
    (Receita gerada [R$])
    ———————————————————————————————————————————————————————————————————————————
    A receita apresenta uma relação positiva fraca em Pearson (0,137),
    sendo mais evidente em Spearman (0,320). É observada uma tendência de
    scores maiores nos criativos com maior receita, porém com dispersão.
    """
    df = raw[["revenue", "klike_score"]].dropna()

    pearson = df["revenue"].corr(df["klike_score"])
    print(f"Correlação (Pearson): {pearson}")
    spearman = df["revenue"].corr(df["klike_score"], method="spearman")
    print(f"Correlação (Spearman): {spearman}")

    df.plot.scatter(x="revenue", y="klike_score", alpha=0.5)
    plt.title("Score por Receita Gerada")
    plt.suptitle("")
    plt.xlabel("Receita [R$]")
    plt.ylabel("Score")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()


def roasxscore(raw: pd.DataFrame) -> None:
    """
    ———————————————————————————————————————————————————————————————————————————
    ROAS x Score
    (Retorno sobre o gasto com anúncios)
    ———————————————————————————————————————————————————————————————————————————
    O retorno sobre o gasto com anúncios apresenta uma associação positiva
    fraca com o score, com Pearson de 0,189 e Spearman de 0,247. É vista uma
    ligeira tendência de scores maiores nos criativos com maior ROAS.
    """
    df = raw[["roas", "klike_score"]].dropna()

    pearson = df["roas"].corr(df["klike_score"])
    print(f"Correlação (Pearson): {pearson}")
    spearman = df["roas"].corr(df["klike_score"], method="spearman")
    print(f"Correlação (Spearman): {spearman}")

    df.plot.scatter(x="roas", y="klike_score", alpha=0.5)
    plt.title("Score por Retorno sobre o Gasto com Anúncios")
    plt.suptitle("")
    plt.xlabel("ROAS")
    plt.ylabel("Score")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()


# =============================================================================
#                              Painel EDA (Score)
# =============================================================================
# On/Off -> '#'

# platformxscore(dados)  # Gráfico Boxplot + Estatísticas (Terminal)
# formatxscore(dados)  # Gráfico Boxplot + Estatísticas (Terminal)
# subtitlexscore(dados)  # Gráfico Boxplot + Estatísticas (Terminal)
# categoryxscore(dados)  # Gráfico Boxplot + Estatísticas (Terminal)
# objectivexscore(dados)  # Gráfico Boxplot + Estatísticas (Terminal)
# agexscore(dados)  # Gráfico Boxplot + Estatísticas (Terminal)
# retargetingxscore(dados)  # Gráfico Boxplot + Estatísticas (Terminal)
# videodurationxscore(dados)  # Gráfico Scatter + Pearson e Spearman (Terminal)
# ctaxscore(dados)  # Gráfico Boxplot + Estatísticas (Terminal)
# hookxscore(dados)  # Gráfico Boxplot + Estatísticas (Terminal)
# facexscore(dados)  # Gráfico Boxplot + Estatísticas (Terminal)
# textxscore(dados)  # Gráfico Boxplot + Estatísticas (Terminal)
# musicvoicexscore(dados)  # Gráfico Scatter + Pearson e Spearman (Terminal)
# impressionsxscore(dados)  # Gráfico Scatter + Pearson e Spearman (Terminal)
# clicksxscore(dados)  # Gráfico Scatter + Pearson e Spearman (Terminal)
# ctrxscore(dados)  # Gráfico Scatter + Pearson e Spearman (Terminal)
# cpcxscore(dados)  # Gráfico Scatter + Pearson e Spearman (Terminal)
# spendxscore(dados)  # Gráfico Scatter + Pearson e Spearman (Terminal)
# revenuexscore(dados)  # Gráfico Scatter + Pearson e Spearman (Terminal)
roasxscore(dados)  # Gráfico Scatter + Pearson e Spearman (Terminal)
