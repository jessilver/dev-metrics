# 📊 Dev Metrics

Sistema completo para calcular e gerar métricas de desenvolvimento do GitHub. Analisa pull requests de repositórios específicos e gera relatórios automáticos com métricas de produtividade, qualidade e entrega.

## 🎯 Funcionalidades

- ✅ Análise automática de PRs merged
- ✅ Cálculo de métricas de desenvolvimento
- ✅ Cálculo de métricas de qualidade e entrega
- ✅ Geração automática de relatórios mensais
- ✅ Identificação de deploys via Git Flow
- ✅ Criação automática de issues com métricas

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

## 🚀 Como Usar

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

4. Execute o script:
```bash
export GITHUB_TOKEN="seu_token_aqui"
python generate_metrics.py
```

### Execução com Variável de Ambiente

```bash
# Usando GITHUB_TOKEN
GITHUB_TOKEN="seu_token_aqui" python generate_metrics.py

# Ou usando METRICS_TOKEN
METRICS_TOKEN="seu_token_aqui" python generate_metrics.py
```

## 🤖 GitHub Action Automatizada

O sistema inclui um workflow que executa automaticamente:

- **Agendamento**: Todo dia 1 de cada mês às 09:00 UTC
- **Manual**: Via interface do GitHub Actions (workflow_dispatch)

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

### Executar Manualmente

1. Vá para a aba `Actions` do repositório
2. Selecione o workflow `Monthly Dev Metrics`
3. Clique em `Run workflow`
4. Selecione a branch e confirme

## 🏗️ Identificação de Deploys

O sistema segue o Git Flow e identifica deploys através de:

1. **PRs de Release → Main**: PRs que fazem merge de branches `release` ou `release/*` para `main`
2. **Tags de Release**: Tags criadas no GitHub marcando versões de release

## 📊 Formato de Saída

```
==================================================
Métricas de desenvolvimento
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

## 🔧 Configuração

### Repositórios Analisados

Por padrão, o script analisa:
- `MellloJ/Inclusiv`
- `Coutinhopmw/awtkd_django`

Para modificar os repositórios, edite a lista `repositories` em `generate_metrics.py`:

```python
repositories = [
    'owner/repo1',
    'owner/repo2'
]
```

### Filtro de Autor

Por padrão, apenas PRs do autor `jessilver` são analisados. Para modificar, altere a variável `author` em `generate_metrics.py`:

```python
author = 'seu_usuario'
```

## 📋 Estrutura do Projeto

```
dev-metrics/
├── .github/
│   └── workflows/
│       └── monthly-metrics.yml   # Workflow automático
├── generate_metrics.py            # Script principal
├── requirements.txt               # Dependências Python
├── .env.example                   # Template de configuração
├── .gitignore                     # Arquivos ignorados
└── README.md                      # Documentação
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
- Nome do repositório incorreto
- Repositório privado sem acesso

**Solução**: Verifique as permissões do token e o acesso aos repositórios.

### Nenhum PR encontrado

**Causas possíveis**:
- Autor não possui PRs merged no repositório
- Filtro de autor incorreto

**Solução**: Verifique o username do autor e se existem PRs merged.

### Rate Limiting

A API do GitHub tem limites de requisições. Com autenticação:
- 5.000 requisições por hora

**Solução**: O script inclui tratamento básico de erros. Para grandes volumes, considere adicionar delays entre requisições.

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
