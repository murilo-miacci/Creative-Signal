"""Exploratory Data Analysis."""

import matplotlib.pyplot as plt
import pandas as pd

dados = pd.read_csv("data/campaigns.csv")

# print(dados.shape)
# 500 x 26

# dados.to_html("dados.html")
# Melhor pra vizualização o tempo todo em live server

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


# =============================================================================
#                              Painel EDA (Score)
# =============================================================================
# On/Off -> '#'

platformxscore(dados)  # Gráfico Boxplot + Estatísticas
