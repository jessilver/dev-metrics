# 📊 Dev Metrics

Sistema completo para calcular e gerar métricas de desenvolvimento do GitHub. Analisa pull requests de repositórios específicos e gera relatórios automáticos com métricas de produtividade, qualidade e entrega.

## 🎯 Funcionalidades

- ✅ Análise automática de PRs merged
- ✅ Cálculo de métricas de desenvolvimento
- ✅ Cálculo de métricas de qualidade e entrega
- ✅ Geração automática de relatórios mensais
- ✅ Identificação de deploys via Git Flow
- ✅ Criação automática de issues com métricas
- ✅ Configuração via arquivo YAML
- ✅ Argumentos de linha de comando
- ✅ Filtros de período flexíveis
- ✅ Inputs manuais para GitHub Actions

## 📈 Métricas Calculadas

### Métricas de Desenvolvimento

- **Média de Tempo Codificando**: Tempo médio (em horas) entre o primeiro e último commit de cada PR
- **Média de Intervalo entre Commits**: Tempo médio (em horas) entre commits consecutivos
- **Média de Tempo Total (Cycle Time)**: Tempo médio (em horas) da criação do PR até o merge
- **Flow Efficiency**: Porcentagem de tempo efetivamente codificando vs. tempo total do PR
  - Fórmula: `(Tempo Codificando / Tempo Total) × 100`

### Métricas de Qualidade e Entrega

- **Lead Time médio até deploy**: Tempo médio (em horas) da criação do PR até o deploy em produção
- **Change Failure Rate (CFR)**: Porcentagem de deploys que resultaram em falha
  - Identifica PRs com labels: `bug`, `hotfix`, `revert`

## ⚙️ Configuração

### Arquivo de Configuração (config.yaml)

O sistema suporta configuração via arquivo YAML. Copie o arquivo de exemplo e ajuste conforme necessário:

```bash
cp config.example.yaml config.yaml
```

#### Estrutura do config.yaml

```yaml
# Repositórios a serem analisados
repositories:
  - MellloJ/Inclusiv
  - Coutinhopmw/awtkd_django

# Autor dos PRs a serem analisados
author: jessilver

# Período de análise
period:
  type: "all"  # Opções: "all", "last_month", "last_3_months", "last_6_months", "custom"
  start_date: ""  # Formato: YYYY-MM-DD (apenas para type: "custom")
  end_date: ""    # Formato: YYYY-MM-DD (apenas para type: "custom")
```

#### Exemplos de Configuração

**Análise do último mês:**
```yaml
period:
  type: "last_month"
```

**Análise dos últimos 6 meses:**
```yaml
period:
  type: "last_6_months"
```

**Período personalizado:**
```yaml
period:
  type: "custom"
  start_date: "2025-01-01"
  end_date: "2025-12-31"
```

**Múltiplos repositórios:**
```yaml
repositories:
  - microsoft/vscode
  - facebook/react
  - vercel/next.js
```

## 🚀 Uso

### Pré-requisitos

- Python 3.11 ou superior
- Token de acesso pessoal do GitHub com permissões:
  - `repo` (acesso total a repositórios)
  - `read:org` (se repositórios forem de organizações privadas)

### Instalação Local

1. Clone o repositório:
```bash
git clone https://github.com/jessilver/dev-metrics.git
cd dev-metrics
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure o token do GitHub:
```bash
cp .env.example .env
# Edite .env e adicione seu token
```

4. Configure os repositórios (opcional):
```bash
cp config.example.yaml config.yaml
# Edite config.yaml para personalizar repositórios, autor e período
```

### Uso Básico

**Usando arquivo de configuração:**
```bash
export GITHUB_TOKEN="seu_token_aqui"
python generate_metrics.py
```

**Especificando repositórios via linha de comando:**
```bash
python generate_metrics.py --repos "owner/repo1" "owner/repo2"
```

### Argumentos de Linha de Comando

| Argumento | Tipo | Descrição | Exemplo |
|-----------|------|-----------|---------|
| `--config` | `PATH` | Caminho para arquivo de configuração | `--config custom.yaml` |
| `--repos` | `REPO [REPO ...]` | Lista de repositórios (formato: owner/repo) | `--repos "user/repo1" "user/repo2"` |
| `--author` | `USERNAME` | Autor dos PRs a analisar | `--author jessilver` |
| `--period` | `TYPE` | Tipo de período | `--period last_month` |
| `--start` | `YYYY-MM-DD` | Data inicial (para período custom) | `--start 2025-01-01` |
| `--end` | `YYYY-MM-DD` | Data final (para período custom) | `--end 2025-12-31` |

#### Tipos de Período

- `all` - Todo o histórico disponível
- `last_month` - Último mês (últimos 30 dias)
- `last_3_months` - Últimos 3 meses (últimos 90 dias)
- `last_6_months` - Últimos 6 meses (últimos 180 dias)
- `custom` - Período personalizado (requer `--start` e `--end`)

### Exemplos de Uso

**1. Usar configuração padrão (config.yaml):**
```bash
python generate_metrics.py
```

**2. Analisar apenas o último mês:**
```bash
python generate_metrics.py --period last_month
```

**3. Período personalizado:**
```bash
python generate_metrics.py --period custom --start 2025-01-01 --end 2025-12-31
```

**4. Analisar repositórios específicos:**
```bash
python generate_metrics.py --repos "MellloJ/Inclusiv"
```

**5. Múltiplos repositórios:**
```bash
python generate_metrics.py --repos "MellloJ/Inclusiv" "Coutinhopmw/awtkd_django"
```

**6. Analisar outro autor:**
```bash
python generate_metrics.py --author outro-usuario
```

**7. Combinar múltiplos parâmetros:**
```bash
python generate_metrics.py \
  --repos "owner/repo1" "owner/repo2" \
  --author jessilver \
  --period last_3_months
```

**8. Usar arquivo de configuração personalizado:**
```bash
python generate_metrics.py --config custom-config.yaml --period last_month
```

### Prioridade de Configuração

O sistema aplica configurações na seguinte ordem de prioridade:

1. **Argumentos de linha de comando** (maior prioridade)
2. **Arquivo config.yaml**
3. **Valores padrão** (menor prioridade)

**Exemplo:** Se você tiver `author: jessilver` no `config.yaml` mas executar com `--author outro-usuario`, o sistema usará `outro-usuario`.

### Saída do Programa

Ao iniciar, o programa exibe a configuração sendo utilizada:

```
📊 Configuração de Análise de Métricas
==================================================
Repositórios:
  - MellloJ/Inclusiv
  - Coutinhopmw/awtkd_django

Autor: jessilver
Período: Último mês (2025-12-01 a 2025-12-31)
==================================================
```

### Execução com Variável de Ambiente

```bash
# Usando GITHUB_TOKEN
GITHUB_TOKEN="seu_token_aqui" python generate_metrics.py

# Ou usando METRICS_TOKEN
METRICS_TOKEN="seu_token_aqui" python generate_metrics.py
```

## 🤖 GitHub Action Automatizada

O sistema inclui um workflow que executa automaticamente no GitHub Actions.

### Execução Automática

- **Agendamento**: Todo dia 1 de cada mês às 09:00 UTC
- **Ação**: Cria automaticamente uma issue com as métricas do mês anterior

### Configuração do Workflow

1. **Adicione o secret no repositório**:
   - Vá em: `Settings` → `Secrets and variables` → `Actions`
   - Clique em `New repository secret`
   - Nome: `METRICS_TOKEN`
   - Valor: Seu token pessoal do GitHub

2. **O workflow criará automaticamente**:
   - Uma issue com o título: `📊 Métricas de Desenvolvimento - [Mês/Ano]`
   - Labels: `metrics`, `automated`
   - Conteúdo: Relatório completo das métricas

### Execução Manual com Inputs

Você pode executar o workflow manualmente com parâmetros personalizados:

1. Vá para a aba `Actions` do repositório
2. Selecione o workflow `Monthly Dev Metrics`
3. Clique em `Run workflow`
4. Configure os inputs desejados:

#### Inputs Disponíveis

| Input | Descrição | Padrão | Opções |
|-------|-----------|--------|--------|
| **period** | Período de análise | `last_month` | `all`, `last_month`, `last_3_months`, `last_6_months`, `custom` |
| **start_date** | Data inicial (YYYY-MM-DD) | - | Qualquer data válida |
| **end_date** | Data final (YYYY-MM-DD) | - | Qualquer data válida |
| **repositories** | Repositórios (separados por espaço) | config.yaml | `owner/repo1 owner/repo2` |

#### Exemplos de Execução Manual

**1. Analisar todo o histórico:**
- period: `all`
- repositories: (deixe vazio para usar config.yaml)

**2. Analisar últimos 3 meses:**
- period: `last_3_months`

**3. Período personalizado:**
- period: `custom`
- start_date: `2025-01-01`
- end_date: `2025-03-31`

**4. Repositórios específicos no último mês:**
- period: `last_month`
- repositories: `MellloJ/Inclusiv Coutinhopmw/awtkd_django`

**5. Análise completa customizada:**
- period: `custom`
- start_date: `2025-01-01`
- end_date: `2025-12-31`
- repositories: `owner/repo1 owner/repo2`

### Relatório Gerado

O workflow cria uma issue com:
- Título do mês/ano
- Configuração utilizada (repositórios e período)
- Métricas calculadas
- Timestamp da geração

## 🏗️ Identificação de Deploys

O sistema segue o Git Flow e identifica deploys através de:

1. **PRs de Release → Main**: PRs que fazem merge de branches `release` ou `release/*` para `main`
2. **Tags de Release**: Tags criadas no GitHub marcando versões de release

## 📊 Formato de Saída

```
📊 Configuração de Análise de Métricas
==================================================
Repositórios:
  - owner/repo

Autor: username
Período: Último mês (2025-12-01 a 2025-12-31)
==================================================

--- Processando repositório: owner/repo ---
PRs contabilizados: X
----------------------------------------
MÉTRICAS DE DESENVOLVIMENTO:
Média Tempo Codificando:     XX.XX h
Média Intervalo entre Commits: XX.XX h
Média Tempo Total (Cycle):   XX.XX h
Flow Efficiency (Tarefa):    XX.XX%
----------------------------------------
MÉTRICAS DE QUALIDADE E ENTREGA:
Lead time médio (até deploy): XXXX.XX h
Change Failure Rate (CFR):    X.XX%
----------------------------------------

==================================================
Análise concluída. Total de repositórios processados: X
==================================================
```

## 🔧 Personalização

### Modificar Repositórios Padrão

Edite o arquivo `config.yaml`:

```yaml
repositories:
  - owner/repo1
  - owner/repo2
  - owner/repo3
```

### Modificar Autor Padrão

Edite o arquivo `config.yaml`:

```yaml
author: seu_usuario
```

### Modificar Período Padrão

Edite o arquivo `config.yaml`:

```yaml
period:
  type: "last_3_months"  # ou outra opção
```

## 📋 Estrutura do Projeto

```
dev-metrics/
├── .github/
│   └── workflows/
│       └── monthly-metrics.yml   # Workflow automático com inputs
├── generate_metrics.py            # Script principal com CLI
├── requirements.txt               # Dependências Python (inclui pyyaml)
├── config.yaml                    # Configuração principal
├── config.example.yaml            # Template de configuração
├── .env.example                   # Template de variáveis de ambiente
├── .gitignore                     # Arquivos ignorados
└── README.md                      # Documentação completa
```

## 🔍 Troubleshooting

### Erro: "Token do GitHub não encontrado"

**Solução**: Configure a variável de ambiente `GITHUB_TOKEN` ou `METRICS_TOKEN`:
```bash
export GITHUB_TOKEN="seu_token_aqui"
```

### Erro: "Erro ao acessar repositório"

**Causas possíveis**:
- Token sem permissões adequadas
- Nome do repositório incorreto (deve ser `owner/repo`)
- Repositório privado sem acesso

**Solução**: Verifique as permissões do token e o acesso aos repositórios.

### Erro: "Repositório não está no formato correto"

**Solução**: Use o formato `owner/repo`:
```bash
python generate_metrics.py --repos "username/repository"
```

### Erro: "Datas devem estar no formato YYYY-MM-DD"

**Solução**: Use o formato correto de data:
```bash
python generate_metrics.py --period custom --start 2025-01-01 --end 2025-12-31
```

### Erro: "start_date deve ser anterior a end_date"

**Solução**: Certifique-se de que a data inicial é anterior à data final.

### Nenhum PR encontrado

**Causas possíveis**:
- Autor não possui PRs merged no repositório
- Filtro de autor incorreto
- Período filtrado não contém PRs

**Solução**: Verifique o username do autor, o período selecionado e se existem PRs merged no período.

### Rate Limiting

A API do GitHub tem limites de requisições. Com autenticação:
- 5.000 requisições por hora

**Solução**: O script inclui tratamento básico de erros. Para grandes volumes, considere adicionar delays entre requisições.

## 🆕 Novidades da Versão Atual

- ✨ Suporte a configuração via arquivo YAML
- ✨ Argumentos de linha de comando completos
- ✨ Filtros de período (últimos 30/90/180 dias ou custom)
- ✨ Inputs manuais no GitHub Actions
- ✨ Validação de formato de repositórios e datas
- ✨ Exibição clara da configuração utilizada
- ✨ Prioridade de configuração (CLI > config.yaml > padrão)

## 📝 Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abrir um Pull Request

## 📧 Contato

Para dúvidas ou sugestões, abra uma issue neste repositório.

---

Feito com ❤️ por [@jessilver](https://github.com/jessilver)
