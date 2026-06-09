#  MonitorAê — Plataforma Educacional 

> Conectando alunos e monitores de forma simples, direto pelo terminal.

---

##  Sobre o projeto

O **MonitorAê** é uma plataforma educacional desenvolvida em Python que roda **inteiramente no terminal de comando**. Ele permite que alunos e monitores se cadastrem, se encontrem e pratiquem conteúdos de Matemática e Português por meio de questões organizadas por descritores e níveis de dificuldade.

O projeto nasceu com o objetivo de ajudar os alunos de escolas públicas estaduais a se prepararem de maneira fácil, centralizada e gratuita. Todos os conteúdos em um só lugar de maneira rápida e eficaz.

---

## 📁 Documentação

👉 [Acessar pasta no Google Drive](https://drive.google.com/drive/folders/1TWGYSU8sIXvJbo6uLz8xbIwCzJFnt4F6?usp=sharing)

---

##  Funcionalidades

### Tela Inicial
- **Login** — Aluno ou Monitor (com verificação de ID extra para monitores)
- **Cadastro** — Aluno ou Monitor, com validações em todos os campos
- **Esqueci minha senha** — Redefinição por e-mail + confirmação de nome
- **Sair** — Encerra o programa

### Menu Principal (pós-login)
Após fazer login, o usuário vê a saudação `Olá, {nome}! 👋` e acessa:

| Opção | Descrição |
|---|---|
| 👤 Meu Perfil | Dados do usuário + opção de deletar conta |
| 🔍 Monitores | Lista todos os monitores com filtros |
| 🏫 Alunos Próximos | Alunos cadastrados na mesma escola |
| 📚 Biblioteca | Questões de Matemática e Português |

### Monitores
- Lista todos os monitores cadastrados
- **Filtro por matéria** (Matemática ou Português)
- **Filtro por escola**
- **Busca por nome** (parcial, sem diferenciar maiúsculas)
- Filtros podem ser combinados e limpos

### Biblioteca de Questões
- Matérias disponíveis: **Matemática** e **Português**
- 5 descritores por matéria, exibidos **5 a 5** com botão de avançar
- 3 níveis de dificuldade: 😊 Fácil, 😐 Médio, 😤 Difícil
- 5 questões por nível com verificação de resposta em tempo real
- **Placar** ao final com mensagem de desempenho

### Perfil
- Exibe todos os dados do usuário logado
- **Deletar conta** com dupla confirmação (confirmação + senha)

---

##  Estrutura de Pastas

```
monitora_ae/
│
├── app.py                  <- Ponto de entrada. Execute: python app.py
├── README.md               <- Documentação principal do projeto
├── router.py               <- Controla a navegação entre as telas do terminal
│
├── data/
│   ├── avaliacoes.json     <- Logs e notas das avaliações dos monitores
│   ├── conversas.json      <- Histórico das mensagens trocadas no chat
│   ├── desempenho.json     <- Dados de acertos/erros dos estudantes
│   ├── faq.json            <- Banco de perguntas e respostas frequentes
│   ├── ids_validos.json    <- IDs de monitor autorizados para cadastro
│   ├── sugestoes_faq.json  <- Sugestões enviadas pelos usuários para o FAQ
│   └── usuarios.json       <- Banco de dados de usuários (gerado automaticamente)
│
├── questoes/
│   └── banco_questoes.json <- 150 questões (5 desc × 3 níveis × 5 questões × 2 matérias)
│
├── telas/
│   ├── alunos_proximos.py  <- Visualização de alunos da mesma escola
│   ├── auth.py             <- Telas de Login, Cadastro e Redefinição de senha
│   ├── biblioteca.py       <- Menu de descritores e banco de questões
│   ├── chat.py             <- Interface de chat ativo entre alunos e monitores
│   ├── desempenho_detalhes.py <- Gráficos e relatórios de evolução do aluno
│   ├── faq.py              <- Central de ajuda e dúvidas frequentes
│   ├── lista_conversas.py  <- Histórico de chats abertos para o usuário
│   ├── menu.py             <- Menu principal pós-login (Aluno / Monitor)
│   ├── monitores.py        <- Listagem e busca de monitores com filtros
│   ├── perfil.py           <- Detalhes do perfil e opção de deletar conta
│   └── simulado.py         <- Inicialização e execução de simulados
│
├── utils/
│   ├── avaliacoes.py       <- Funções lógicas para cálculo e salvamento de notas
│   ├── chat.py             <- Regras de negócio e envio de mensagens
│   ├── desempenho.py       <- Processamento de estatísticas e rendimento
│   ├── emojis.py           <- Central de mapeamento de ícones e emojis para o terminal
│   ├── terminal.py         <- Formatação visual do terminal (cores, cabeçalhos, menus)
│   └── usuarios.py         <- Manipulação e persistência do banco de usuários
│
└── validacoes/
    └── validadores.py      <- Regras de validação centralizadas (CPF, e-mail, senhas)

```

---

##  Como executar

### Pré-requisitos
- Python **3.8** ou superior
- Nenhuma biblioteca externa — usa apenas módulos da biblioteca padrão do Python (`json`, `os`, `re`, `getpass`)

### Passos

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/monitora_ae.git

# 2. Entre na pasta do projeto
cd monitora_ae

# 3. Execute
python app.py
```

> ⚠️ No Windows, use `python app.py`. No Linux/Mac, pode ser necessário `python3 app.py`.

---

##  Regras de Cadastro

Todas as validações ficam centralizadas em `validacoes/validadores.py`, o que facilita encontrar e alterar qualquer restrição.

### Nome
- Mínimo de 3 caracteres
- Não pode conter números

### E-mail
- Deve seguir o formato `exemplo@dominio.com`

### Senha
- Mínimo de 6 caracteres
- Pelo menos 1 número
- Pelo menos 1 letra maiúscula
- Pelo menos 1 caractere especial (`!@#$%...`)

### Escolas disponíveis (podem ser editadas em `validacoes/validadores.py`)
1. EREM Edson Moury Fernandes
2. EREM Adelaide Pessoa Câmara
3. EREM Cabo De Santo Agostinho
4. EREM Diário de Pernambuco
5. EREM Justino Ferreira Gomes

### Matérias para monitores
- Matemática
- Português

### ID de Monitor
- Deve constar no arquivo `data/ids_validos.json`
- IDs padrão: `MON001` até `MON005`, `MON123`, `MON456`, `MON789`, `...`

---

##  Banco de Dados

O sistema usa arquivos **JSON** como banco de dados local — sem necessidade de instalar nenhum banco de dados externo.

### `data/usuarios.json`
Armazena todos os usuários cadastrados. Criado automaticamente no primeiro cadastro.

```json
{
  "usuarios": [
    {
      "tipo": "Aluno",
      "nome": "Ana Paula Silva",
      "escola": "EREM Adelaide Pessoa Câmara",
      "email": "ana@email.com",
      "senha": "Senha1!"
    },
    {
      "tipo": "Monitor",
      "nome": "Carlos Andrade",
      "escola": "EREM Edson Moury Fernandes",
      "materia": "Matemática",
      "id": "MON001",
      "email": "carlos@email.com",
      "senha": "Senha1!"
    }
  ]
}
```

### `data/ids_validos.json`
Lista dos IDs de monitor autorizados. Edite este arquivo para adicionar ou remover IDs.

```json
{
  "ids": ["MON001", "MON002", "MON003"]
}
```

### `questoes/banco_questoes.json`
Banco com 150 questões organizadas por matéria, descritor e dificuldade. Você pode adicionar novas questões seguindo a estrutura:

```json
{
  "Matematica": {
    "D01": {
      "nome": "Nome do Descritor",
      "facil": [
        {
          "id": 1,
          "enunciado": "Texto da pergunta?",
          "alternativas": ["A) ...", "B) ...", "C) ...", "D) ..."],
          "resposta": "B"
        }
      ],
      "medio": [ ... ],
      "dificil": [ ... ]
    }
  }
}
```

---

##  Como o código está organizado

O projeto usa alguns conceitos de **Programação Orientada a Objetos (POO)**:

- **Classes** (`class`) — agrupam dados e funções relacionadas. Cada tela é uma classe.
- **Métodos** (`def` dentro de uma classe) — são as funções da classe.
- **`self`** — referência ao próprio objeto, como dizer "eu mesmo".
- **`__init__`** — método construtor, chamado ao criar um objeto da classe.

O **Router** (`router.py`) é responsável por saber qual tela está ativa e quem está logado, funcionando como um controlador de navegação.

---

##  Personalizações rápidas

| O que mudar | Onde mexer |
|---|---|
| Lista de escolas | `validacoes/validadores.py` → `ESCOLAS_PERMITIDAS` |
| Matérias dos monitores | `validacoes/validadores.py` → `MATERIAS_PERMITIDAS` |
| IDs de monitor válidos | `data/ids_validos.json` |
| Adicionar questões | `questoes/banco_questoes.json` |
| Regras de senha | `validacoes/validadores.py` → `validar_senha()` |

---

##  Tipos de usuário

### Aluno
- Cadastra-se com nome, escola, e-mail e senha
- Acessa a biblioteca de questões
- Vê monitores disponíveis e alunos da mesma escola

### Monitor
- Além dos dados do aluno, precisa de: matéria que monitora e ID de monitor
- O ID é validado contra a lista em `data/ids_validos.json`

---

##  Tecnologias utilizadas

- **Python 3** — linguagem principal
- **JSON** — armazenamento de dados
- **Módulos nativos**: `os`, `re`, `json`, `getpass`
- Sem dependências externas — basta ter o Python instalado

---

## Conteúdo das VAs

---

## ✅ 1VA - Desenvolvido e Lançado

### Funcionalidades implementadas:

### Sistema de Autenticação

- Login (Aluno e Monitor)
- Cadastro com validações completas
- Redefinição de senha (e-mail + nome)
- Validação de ID para monitores

### Tela Inicial

- Opções: Login, Cadastro, Esqueci minha senha, Sair
- Navegação por fluxo controlado

### Menu Principal

- Saudação personalizada ao usuário
- Acesso às funcionalidades principais

### Busca de Monitores

- Listagem de monitores cadastrados
- Filtros por:
  - Matéria
  - Escola
  - Nome (busca parcial)
  - Combinação e limpeza de filtros

### Biblioteca de Questões

- Matérias: Matemática e Português
- Descritores organizados com paginação
- Níveis de dificuldade:
  -😊 Fácil
  -😐 Médio
  -😤 Difícil
- Execução de questões com correção imediata
- Resultado final com desempenho

### Perfil do Usuário

- Visualização dos dados cadastrados
- Exclusão de conta com confirmação dupla

---

## 🚧 2VA - Em Desenvolvimento

### Funcionalidades em desenvolvimento:

### Chat entre usuários
- Comunicação entre aluno e monitor
- Envio e recebimento de mensagens
- Tratamento de erros (mensagem vazia, falhas, etc.)

### FAQ (Perguntas Frequentes)
- Lista de dúvidas comuns
- Busca por perguntas
- Sugestão de suporte adicional

### Avaliação de Monitores
- Sistema de notas (0 a 10)
- Cálculo de média automática
- Restrições:
   - Não é permitido se autoavaliar
   - Apenas uma avaliação por monitor

### Simulados

- Configuração personalizada:
   - Matéria
   - Dificuldade
   - Quantidade de questões
   - Geração aleatória de questões
   - Resultado com porcentagem de acertos

### Acompanhamento de Desempenho

- Histórico baseado nos simulados realizados
- Métricas:
   - Total de questões
   - Taxa de acertos
   - Atualização automática

---

## 🚧 3VA - Em Desenvolvimento

## Funcionalidades planejadas:

#### Solicitação de Material
- Solicitação de conteúdos por alunos
- Resposta por monitores

#### Ranking de Alunos
- Classificação baseada em desempenho
- Comparação entre usuários

#### Seleção de Monitores
- Escolha de monitores preferidos
- Possível vínculo aluno-monitor

#### Sistema de Bolsas
- Incentivos baseados em desempenho ou participação

#### Notificações
- Alertas do sistema:
- Novas mensagens
- Avaliações
- Atualizações importantes

---

*Desenvolvido como projeto educacional. 📖*
