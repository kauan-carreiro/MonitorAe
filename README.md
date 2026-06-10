# MonitorAê — Plataforma Educacional

> Conectando alunos e monitores de forma simples, direto pelo terminal.

---

## Sobre o projeto

O **MonitorAê** é uma plataforma educacional desenvolvida em Python que roda **inteiramente no terminal de comando**. Ele permite que alunos e monitores se cadastrem, se encontrem e pratiquem conteúdos de Matemática e Português por meio de questões organizadas por descritores e níveis de dificuldade.

O projeto nasceu com o objetivo de ajudar os alunos de escolas públicas estaduais a se prepararem de maneira fácil, centralizada e gratuita. Todos os conteúdos em um só lugar de maneira rápida e eficaz.

---

## 📁 Documentação

👉 [Acessar pasta no Google Drive](https://drive.google.com/drive/folders/1TWGYSU8sIXvJbo6uLz8xbIwCzJFnt4F6?usp=sharing)

---

## Funcionalidades

### Tela Inicial
- **Login** — Aluno ou Monitor (com verificação de ID extra para monitores)
- **Cadastro** — Aluno ou Monitor, com validações em todos os campos (nome, e-mail, senha, escola, etc.)
- **Esqueci minha senha** — Redefinição por e-mail + confirmação de nome
- **Sair** — Encerra o programa

### Menu Principal (pós-login)
Após fazer login, o usuário vê a saudação `Olá, {nome}! 👋` e acessa as funcionalidades de acordo com seu tipo:

| Opção (Aluno) | Opção (Monitor) | Descrição |
|---|---|---|
| 👤 Meu Perfil | 👤 Meu Perfil | Dados do usuário + opção de deletar conta + desempenho detalhado |
| 🔍 Monitores | 🔍 Monitores | Lista todos os monitores com filtros e possibilidade de avaliar (alunos) |
| 🏫 Alunos Próximos | 🏫 Alunos Próximos | Alunos cadastrados na mesma escola |
| 📚 Biblioteca | 📚 Biblioteca | Questões de Matemática e Português por descritor/dificuldade |
| 🎲 Simulado | 🎲 Simulado | Personalize seu simulado (descritores, nível, quantidade de questões) |
| 📖 FAQ | 📖 FAQ | Perguntas frequentes com busca local + assistente IA (Groq) |
| — | ✍️ Aprovar Sugestões da FAQ | Monitores revisam e aprovam sugestões enviadas pelos usuários |
| — | 💬 Minhas Conversas | Lista de conversas ativas com alunos |
| 🚪 Sair da conta | 🚪 Sair da conta | Desconecta e retorna à tela inicial |

### 🔍 Monitores
- Lista todos os monitores cadastrados com suas respectivas **notas médias** (avaliações dos alunos)
- **Filtro por matéria** (Matemática ou Português)
- **Filtro por escola**
- **Busca por nome** (parcial, sem diferenciar maiúsculas)
- Filtros podem ser combinados e limpos
- Ao selecionar um monitor, é possível:
  - **Visualizar perfil completo** com nota média
  - **Avaliar** (apenas alunos da mesma escola, nota 0 a 10, podendo alterar depois)
  - **Iniciar conversa** (alunos) – veja seção de Chat

### 💬 Chat entre Aluno e Monitor
- **Aluno** pode iniciar conversa com qualquer monitor
- **Monitor** vê suas conversas ativas no menu e pode respondê-las
- Envio e recebimento de mensagens em tempo real (dentro da mesma sessão)
- Monitor pode **encerrar a conversa** quando a dúvida for resolvida
- Após o encerramento, o aluno é convidado a **avaliar o monitor** (dúvida sanada? sim/não) e, se quiser, pode iniciar uma **nova conversa** com o mesmo monitor
- Toda conversa fica armazenada para histórico

### 📚 Biblioteca de Questões
- Matérias disponíveis: **Matemática** e **Português**
- 5 descritores por matéria, exibidos **5 a 5** com botão de avançar
- 3 níveis de dificuldade: 😊 Fácil, 😐 Médio, 😤 Difícil
- 5 questões por nível com verificação de resposta em tempo real
- **Placar** ao final com mensagem de desempenho

### 🎲 Simulado Personalizado
- Permite ao usuário **combinar múltiplos descritores e níveis** de dificuldade
- Opções disponíveis:
  - Adicionar descritor (escolhe matéria → descritor → nível)
  - Remover descritor
  - Definir quantidade de questões: 5, 10, 15, 20 ou **todas as disponíveis**
- As questões são **embaralhadas aleatoriamente** a partir dos blocos selecionados
- Ao final, o desempenho é **registrado automaticamente** (acertos por matéria/descritor)
- Exibe resultado com percentual e mensagem motivacional

### 📊 Desempenho Detalhado
- Acessível pelo **Meu Perfil** → "Mais detalhes"
- Mostra:
  - Total de questões respondidas, acertos, erros e percentual geral
  - Desempenho por assunto (Matemática/Português ou descritor)
  - Assunto com mais acertos e com mais erros
- Baseado nos simulados realizados (atualização automática)

### ❓ FAQ com Assistente IA
- **Busca local**: digite uma dúvida e o sistema procura palavras-chave nas perguntas cadastradas (ignora acentos e palavras genéricas)
- **Resultados**: exibe perguntas encontradas; o usuário pode escolher uma para ver a resposta
- **Sem resultados**: oferece três opções:
  1. Buscar novamente
  2. **Consultar assistente IA** (integração com Groq – modelo Llama 3.1 8B)
  3. Ver todas as perguntas cadastradas
- A resposta da IA pode ser **sugerida para a FAQ** – a sugestão fica pendente para aprovação de um monitor
- **Monitores** têm uma opção extra no menu: **Aprovar Sugestões da FAQ**
  - Visualizam sugestões pendentes
  - Podem **aceitar, editar pergunta/resposta ou rejeitar**
  - Quando aprovada, a pergunta entra na FAQ oficial

### 👤 Perfil
- Exibe todos os dados do usuário logado (nome, e-mail, escola, etc.)
- Mostra também estatísticas resumidas de desempenho
- **Deletar conta** com dupla confirmação (confirmação + senha) – ação irreversível

### ⭐ Avaliação de Monitores
- Apenas alunos podem avaliar
- Só é permitido avaliar monitores da **mesma escola** do aluno
- Nota inteira de 0 a 10
- Um aluno pode avaliar o mesmo monitor várias vezes, mas a nota anterior é **substituída**
- A nota média é exibida na lista de monitores e no perfil do monitor

---

## Estrutura de Pastas

```
monitora_ae/
│
├── app.py                    ← Ponto de entrada. Execute: python app.py
├── router.py                 ← Controla a navegação entre telas
│
├── telas/
│   ├── auth.py               ← Login, Cadastro e Redefinir senha
│   ├── menu.py               ← Menu principal pós-login
│   ├── perfil.py             ← Perfil e deletar conta + desempenho detalhado
│   ├── monitores.py          ← Listagem de monitores com filtros e avaliação
│   ├── alunos_proximos.py    ← Alunos da mesma escola
│   ├── biblioteca.py         ← Descritores e questões fixas
│   ├── simulado.py           ← Simulado personalizado (com registro de desempenho)
│   ├── faq.py                ← FAQ com busca local + IA (Groq) e aprovação de sugestões
│   ├── chat.py               ← Chat entre aluno e monitor
│   ├── lista_conversas.py    ← Lista de conversas ativas para monitores
│   └── desempenho_detalhes.py← Estatísticas avançadas de desempenho
│
├── utils/
│   ├── terminal.py           ← Funções de formatação do terminal (cores, menus)
│   ├── usuarios.py           ← Leitura/escrita do banco de usuários
│   ├── chat.py               ← Gerenciamento de conversas (criar, adicionar mensagem, encerrar)
│   ├── avaliacoes.py         ← Registro e cálculo de avaliações de monitores
│   └── desempenho.py         ← Registro e consulta de desempenho em simulados
│
├── validacoes/
│   └── validadores.py        ← Todas as regras de validação centralizadas
│
├── data/
│   ├── usuarios.json         ← Banco de dados de usuários
│   ├── ids_validos.json      ← IDs de monitor autorizados
│   ├── avaliacoes.json       ← Avaliações dos monitores (aluno → monitor, nota)
│   ├── conversas.json        ← Histórico de conversas (mensagens, status)
│   ├── faq.json              ← Perguntas frequentes oficiais
│   └── sugestoes_faq.json    ← Sugestões de perguntas/respostas (pendentes de aprovação)
│
└── questoes/
    └── banco_questoes.json   ← 150 questões (5 desc × 3 níveis × 5 questões × 2 matérias)
```

---

## Como executar

### Pré-requisitos
- Python **3.8** ou superior
- Nenhuma biblioteca externa obrigatória – usa apenas módulos da biblioteca padrão (`json`, `os`, `re`, `getpass`, `unicodedata`, `urllib`)
- Para a funcionalidade de **Assistente IA** (FAQ) é necessário uma **chave de API do Groq** (opcional – sem ela a busca local continua funcionando)

### Passos

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/monitora_ae.git

# 2. Entre na pasta do projeto
cd monitora_ae

# 3. (Opcional) Configure a chave da API Groq para o assistente IA
#    Crie um arquivo .env na raiz com: GROQ_API_KEY=sua_chave_aqui

# 4. Execute
python app.py
```

> ⚠️ No Windows, use `python app.py`. No Linux/Mac, pode ser necessário `python3 app.py`.

---

## Regras de Cadastro

Todas as validações ficam centralizadas em `validacoes/validadores.py`.

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

## Banco de Dados

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

### `data/avaliacoes.json`
Armazena as avaliações feitas por alunos a monitores.

```json
{
  "avaliacoes": [
    {
      "email_avaliador": "aluno@email.com",
      "email_monitor": "monitor@email.com",
      "nota": 9
    }
  ]
}
```

### `data/conversas.json`
Histórico completo de conversas (aluno, monitor, mensagens, status, timestamps).

### `data/faq.json` e `data/sugestoes_faq.json`
Perguntas frequentes oficiais e sugestões pendentes de aprovação.

### `data/ids_validos.json`
Lista dos IDs de monitor autorizados. Edite este arquivo para adicionar ou remover IDs.

```json
{
  "ids": ["MON001", "MON002", "MON003"]
}
```

### `questoes/banco_questoes.json`
Banco com 600 questões organizadas por matéria, descritor e dificuldade. Você pode adicionar novas questões seguindo a estrutura:

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

## Como o código está organizado

O projeto usa **Programação Orientada a Objetos (POO)**:

- **Classes** (`class`) — agrupam dados e funções relacionadas. Cada tela é uma classe.
- **Métodos** (`def` dentro de uma classe) — são as funções da classe.
- **`self`** — referência ao próprio objeto, como dizer "eu mesmo".
- **`__init__`** — método construtor, chamado ao criar um objeto da classe.

O **Router** (`router.py`) é responsável por saber qual tela está ativa e quem está logado, funcionando como um controlador de navegação.

---

## Personalizações rápidas

| O que mudar | Onde mexer |
|---|---|
| Lista de escolas | `validacoes/validadores.py` → `ESCOLAS_PERMITIDAS` |
| Matérias dos monitores | `validacoes/validadores.py` → `MATERIAS_PERMITIDAS` |
| IDs de monitor válidos | `data/ids_validos.json` |
| Adicionar questões | `questoes/banco_questoes.json` |
| Regras de senha | `validacoes/validadores.py` → `validar_senha()` |
| FAQ inicial | `data/faq.json` |
| Chave da API Groq (IA) | Arquivo `.env` na raiz do projeto |

---

## Tipos de usuário

### Aluno
- Cadastra-se com nome, escola, e-mail e senha
- Acessa a biblioteca de questões e simulados
- Vê monitores disponíveis e alunos da mesma escola
- Pode iniciar conversa com qualquer monitor
- Pode avaliar monitores (da mesma escola)
- Tem seu desempenho registrado e pode visualizá-lo

### Monitor
- Além dos dados do aluno, precisa de: matéria que monitora e ID de monitor
- O ID é validado contra a lista em `data/ids_validos.json`
- Pode responder conversas de alunos (menu "Minhas Conversas")
- Pode encerrar conversas
- Pode aprovar/rejeitar sugestões de FAQ enviadas pelos usuários

---

## Tecnologias utilizadas

- **Python 3** — linguagem principal
- **JSON** — armazenamento de dados
- **Módulos nativos**: `os`, `re`, `json`, `getpass`, `unicodedata`, `urllib`
- **API Groq** (opcional) — para o assistente de IA na FAQ
- Sem dependências externas obrigatórias — basta ter o Python instalado

---

## Funcionalidades já implementadas (status atual)

### ✅ Totalmente implementadas
- Sistema completo de autenticação (login, cadastro, redefinição de senha)
- Menu dinâmico para Aluno e Monitor
- Perfil com exclusão de conta e desempenho detalhado
- Listagem de monitores com filtros e avaliação (com média)
- Listagem de alunos da mesma escola
- Biblioteca de questões com 150 questões (5 descritores × 3 níveis × 5 questões × 2 matérias)
- Simulado personalizado (escolha de descritores, nível, quantidade) com registro de desempenho
- Chat entre aluno e monitor (criação, envio de mensagens, encerramento, avaliação pós-conversa)
- FAQ com busca local inteligente (ignora acentos, palavras genéricas, busca por raiz)
- Integração com IA (Groq) para responder dúvidas não encontradas na FAQ
- Sugestão de novas perguntas/respostas para a FAQ
- Aprovação de sugestões por monitores (edição, aceite, rejeição)
- Acompanhamento de desempenho (total de questões, acertos, erros, percentual, assuntos com mais acertos/erros)

---

## Próximos passos (planejados)

| Funcionalidade | Descrição |
|---|---|
| Ranking de Alunos | Classificação baseada em desempenho geral |
| Solicitação de Material | Aluno pede conteúdo específico, monitor responde |
| Seleção de Monitores Preferidos | Vínculo aluno-monitor para acompanhamento contínuo |
| Sistema de Bolsas | Incentivos baseados em desempenho ou participação |
| Notificações | Alertas sobre novas mensagens, avaliações, etc. |

---

*Desenvolvido como projeto educacional. 📖*
