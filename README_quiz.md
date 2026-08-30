# Quiz em Python 3 com Adição de Novas Perguntas no Banco de Dados

Aplicação de quiz interativo sobre programação Python, com interface gráfica e banco de dados próprio, desenvolvida em parceria com o Claude (Anthropic) como parte dos meus estudos.

## Sobre o projeto

Um quiz com interface gráfica (Tkinter) que testa conhecimentos de Python através de perguntas de múltipla escolha, com as perguntas armazenadas em um banco de dados SQLite — permitindo adicionar novas perguntas sem alterar o código.

## Funcionalidades

- **Quiz interativo**: sorteia 10 perguntas aleatórias do banco de dados a cada rodada, com barra de progresso e pontuação em tempo real.
- **Gerenciamento de perguntas**: tela dedicada para adicionar novas perguntas (com 5 alternativas cada) sem precisar mexer no código-fonte.
- **Listagem de perguntas**: visualização de todas as perguntas cadastradas, com a resposta correta destacada.
- **Persistência com SQLite**: as perguntas ficam salvas em `quiz.db`, então tudo que você adiciona continua disponível na próxima vez que abrir o programa.
- **Feedback de desempenho**: ao final do quiz, uma mensagem de resultado varia conforme a pontuação obtida.

## Tecnologias utilizadas

- **Python 3**
- **Tkinter** — interface gráfica nativa do Python
- **SQLite3** — banco de dados embutido, sem necessidade de instalação de servidor

## Estrutura do banco de dados

Tabela `perguntas`:

| Coluna | Descrição |
|---|---|
| `id` | Identificador único (auto-incremento) |
| `pergunta` | Texto da pergunta |
| `opcao1` a `opcao5` | As cinco alternativas de resposta |
| `correta` | Número (1 a 5) indicando qual opção é a correta |

## Como executar

```bash
python quizpython3.py
```

Na primeira execução, o banco de dados é criado automaticamente com 15 perguntas iniciais sobre fundamentos de Python.

## O que pratiquei neste projeto

- Interfaces gráficas com Tkinter (janelas, frames, botões, formulários)
- Integração com banco de dados SQLite (criação de tabelas, inserção, consulta)
- Lógica de quiz: seleção aleatória de perguntas, controle de pontuação e progresso
- Validação de formulário (campos obrigatórios, faixa de valores aceitos)
- Organização de uma aplicação com múltiplas telas dentro de uma única janela
