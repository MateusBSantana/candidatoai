# CandidatoIA

Assistente pessoal de apoio à busca de emprego. Analisa a compatibilidade (aderência) entre meu perfil profissional e vagas reais, e evolui progressivamente para incluir histórico de candidaturas, integração com IA/LLM e análise de dados.

Este é meu projeto de estudo prático de Python, SQL, Dados e IA — construído com apoio de um instrutor de IA que me guia por perguntas, sem entregar código pronto (ver `prompt-instrutor-candidatoia.md`, se disponível no repositório).

## Status atual

- ✅ **V1 — Python puro**: leitura de perfil (JSON) e vaga (texto), comparação de habilidades, cálculo de aderência, relatório no terminal
- 🚧 **V2 — Banco de dados (SQLite)**: modelagem completa (5 tabelas) e criação das tabelas concluídas; inserção de dados (`INSERT`) em andamento
- ⏳ **V3 — IA/LLM**: análise mais inteligente de vaga/currículo, sugestões de melhoria (planejado)
- ⏳ **V4 — Pandas**: análise agregada do histórico de candidaturas (planejado)
- ⏳ **V5 — Machine Learning**: previsão/análise baseada nos dados coletados (planejado)

Funcionalidades mais avançadas (multiusuário, deploy em produção, scraping de vagas, integrações com WhatsApp/Telegram) estão documentadas em `requisitos.md` como visão de longo prazo, organizadas por fase, mas conscientemente adiadas.

## Como rodar

Pré-requisitos: Python 3.10+

```bash
# Clone o repositório
git clone https://github.com/MateusBSantana/CandidatoIA.git
cd CandidatoIA

# Crie e ative o ambiente virtual
python -m venv venv

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Ative o ambiente virtual (Mac/Linux)
# source venv/bin/activate

# Rode o script principal
cd src
python candidatura.py
```

## Como usar

1. Edite `dados/perfil.json` com suas habilidades reais
2. Cole o texto de uma vaga real em `dados/vagas.txt`
3. Rode `python candidatura.py`
4. O terminal mostra a lista de habilidades compatíveis e o percentual de aderência

## Estrutura do projeto

```
CandidatoIA/
├── dados/
│   ├── perfil.json         # dados do candidato
│   └── vagas.txt            # texto da vaga a ser analisada
├── src/
│   └── candidatura.py       # script principal
├── candidatoIA.db            # banco de dados SQLite (gerado automaticamente)
├── requisitos.md             # documento de requisitos funcionais (RF)
├── venv/                     # ambiente virtual (não versionado)
└── README.md
```

## Modelagem do banco de dados (V2)

5 tabelas, com relacionamentos um-para-muitos e muitos-para-muitos:

- **vagas** — dados da vaga (entidade forte)
- **requisitos** — lista mestre de requisitos técnicos únicos (entidade forte)
- **requisito_vaga** — associativa entre vaga e requisito, guarda prioridade (obrigatório/desejável)
- **candidaturas** — cada análise realizada, com aderência calculada
- **requisitos_candidatura** — associativa entre candidatura e requisito, guarda se cada requisito foi cumprido naquela análise específica

## Stack

Python · SQLite · SQL

*(Em evolução: LLM/API, Pandas, Scikit-learn — conforme roadmap V1→V7)*

## Sobre este projeto

Desenvolvido como parte da minha transição de carreira para Dados e Inteligência Artificial. Documentação de requisitos, decisões arquiteturais e progresso seguem o mesmo padrão de rigor que usei no meu projeto anterior, [HospedaFacil](https://github.com/MateusBSantana/HospedaFacil).