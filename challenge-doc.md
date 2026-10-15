# 🎯 Klike Data Science Challenge

## Sobre a Millai e o Klike

A **Millai** é uma consultoria especializada em Marketing e Inteligência Artificial. Nosso principal produto, o [**Klike**](https://www.klike.ai), é uma plataforma de análise de anúncios em vídeo que utiliza IA para pontuar criativos, identificar oportunidades de melhoria e apoiar decisões estratégicas de marketing.

Neste desafio, você vai trabalhar com um dataset simulado inspirado em dados reais da plataforma.

## 📋 Contexto

Você recebeu um dataset (klike_challenge_dataset.csv) contendo **500 registros de campanhas de vídeo** veiculadas em diferentes plataformas. Cada registro representa um criativo de vídeo com seus atributos e métricas de performance.

O **Klike Score** (coluna klike_score) é uma pontuação de 0 a 100 que representa a qualidade geral do criativo, calculada por nosso sistema de IA com base em múltiplos fatores.

### Dicionário de dados

| **Coluna**          | **Descrição**                                                                   |
| ------------------- | ------------------------------------------------------------------------------- |
| campaign_id         | Identificador único da campanha                                                 |
| date                | Data de veiculação                                                              |
| platform            | Plataforma (Meta, TikTok, LinkedIn)                                             |
| category            | Categoria do anunciante (E-commerce, SaaS, App Install, Branding, Lead Gen)     |
| objective           | Objetivo da campanha (awareness, traffic, conversions, engagement, app_install) |
| target_audience_age | Faixa etária do público-alvo (18-24, 25-34, 35-44, 45+)                         |
| is_retargeting      | Se a campanha é de retargeting (True) ou prospecção (False)                     |
| video_duration_s    | Duração do vídeo em segundos                                                    |
| format              | Formato do vídeo (vertical, horizontal, quadrado)                               |
| has_subtitle        | Se o vídeo possui legendas                                                      |
| has_cta             | Se o vídeo possui call-to-action                                                |
| has_hook            | Se o vídeo possui hook nos primeiros 3 segundos                                 |
| has_face            | Se o vídeo apresenta rosto humano                                               |
| text_density        | Quantidade de texto on-screen (low, medium, high)                               |
| music_voice_ratio   | Proporção música/voz (0 = só voz, 1 = só música)                                |
| impressions         | Número de impressões                                                            |
| clicks              | Número de cliques                                                               |
| ctr                 | Click-through rate                                                              |
| cpc                 | Custo por clique (R\$)                                                          |
| spend               | Gasto total (R\$)                                                               |
| conversions         | Número de conversões                                                            |
| revenue             | Receita gerada (R\$)                                                            |
| roas                | Return on Ad Spend                                                              |
| avg_watch_time_s    | Tempo médio de visualização do vídeo (segundos)                                 |
| engagement_rate     | Taxa de engajamento (likes + comentários + compartilhamentos / impressões)      |
| klike_score         | Score de qualidade do criativo (0-100) — **target**                             |

## 🧩 O Desafio

### Parte 1 — Análise Exploratória (EDA)

Explore o dataset e responda:

1. **Qual o perfil geral dos dados?** Distribuições, valores faltantes, outliers — como você trataria cada caso?

2. **Quais atributos do criativo mais se correlacionam com boas métricas de performance?** (CTR, ROAS, conversões, etc.)

3. **Existem padrões diferentes por plataforma?** O que funciona no TikTok funciona no LinkedIn?

4. **Crie pelo menos 3 visualizações** que você usaria para apresentar insights a um time de marketing.

### Parte 2 — Modelagem

Construa um modelo preditivo para o klike_score:

1. **Feature engineering:** quais features você escolheu e por quê? Criou alguma feature nova?

2. **Modelo:** treine pelo menos um modelo de regressão. Explique sua escolha.

3. **Avaliação:** use métricas apropriadas (RMSE, MAE, R², etc.) e interprete os resultados.

4. **Feature importance:** quais variáveis mais influenciam o score? Isso faz sentido do ponto de vista de negócio?

### Parte 3 — Recommendations Engine

Usando os insights das Partes 1 e 2, construa um sistema simples de recomendações que analisa uma campanha e gera sugestões de melhoria.

**Requisitos mínimos:**

1. **Input:** o sistema recebe os dados de uma campanha (uma linha do dataset) e gera pelo menos **3 recomendações específicas** de melhoria.

2. **Recomendações devem ser acionáveis e quantificadas** — não basta dizer "melhore o hook"; diga algo como: _"Adicionar um hook nos primeiros 3 segundos poderia aumentar o CTR em aproximadamente X% com base nos padrões observados no dataset."_

3. **Recomendações devem ser contextuais** — considere a plataforma, categoria e outros atributos da campanha. O que funciona no TikTok pode não funcionar no LinkedIn.

4. **Priorização:** ordene as recomendações por impacto estimado na performance.

5. **Protótipo funcional** — pode ser uma função Python, um notebook interativo ou uma CLI simples. Não precisa ser bonito, precisa funcionar.

**Exemplos do tipo de recomendação esperada:**

- _"Reduzir a duração do vídeo de 45s para ~20s poderia aumentar o CTR em aproximadamente 18% no TikTok, com base na análise de duração ideal por plataforma."_

- _"Incluir rosto humano no criativo poderia elevar a taxa de engajamento em ~35%, especialmente para a faixa etária 25-34."_

- _"A text density 'high' está penalizando o desempenho no Meta. Reduzir para 'medium' poderia melhorar o klike_score em ~8 pontos."_

### Parte 4 — Visão de Produto (respostas abertas)

Responda em texto (no README ou em um documento separado):

1. Se você tivesse acesso ao vídeo original (não só metadados), **que features adicionais você extrairia** para melhorar o modelo e as recomendações?

2. **Como você colocaria o seu Recommendations Engine em produção?** Pense em arquitetura, escalabilidade e como ele se integraria a um produto real. (não precisa implementar — queremos entender seu raciocínio)

3. **O que mais você faria se tivesse mais tempo?** Que análises, experimentos ou melhorias no engine ficaram de fora?

## 📦 Entrega

- **Repositório Git** (GitHub, GitLab ou similar) contendo:
  - Código organizado e reproduzível (Python)

  - **README.md** explicando suas decisões, processo de pensamento e conclusões

  - Instruções para rodar o projeto (dependências, etc.)

- **Prazo:** 03/04/2026 (sexta-feira) até às 23h59

### O que valorizamos

- **Raciocínio analítico** — mais do que acertar, queremos entender como você pensa

- **Comunicação** — código limpo, visualizações claras, explicações que um não-técnico entenderia

- **Criatividade** — ir além do pedido é bem-vindo: análises extras, features inesperadas, abordagens diferentes

- **Pragmatismo** — soluções simples e bem executadas valem mais que complexidade desnecessária

Boa sorte! 🚀

_Em caso de dúvidas, entre em contato conosco._
