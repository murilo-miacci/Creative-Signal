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
    CTA (Call To Action) x Score
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
    plt.title("Score por Presença de CTA")
    plt.suptitle("")
    plt.xlabel("CTA?")
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
# agexscore(dados)  #  Gráfico Boxplot + Estatísticas (Terminal)
# retargetingxscore(dados)  # Gráfico Boxplot + Estatísticas (Terminal)
# videodurationxscore(dados)  #  Gráfico Scatter + Pearson e Spearman (Terminal)
ctaxscore(dados)  #  Gráfico Boxplot + Estatísticas (Terminal)
