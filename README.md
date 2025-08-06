# README.md
```markdown
# Show do Milhão Dinâmico

Este é um jogo estilo “Show do Milhão” que usa a API da OpenAI para criar perguntas dinâmicas e evita repetições usando um cache local.

## Pré-requisitos
- Python 3.8+
- Editor de texto ou IDE (VSCode, PyCharm, etc.)
- Conta na OpenAI

## Passo a passo para iniciantes

1. **Clone o repositório**
   ```bash
   git clone https://github.com/seu-usuario/show_do_milhao.git
   cd show_do_milhao
   ```

2. **Obtenha sua chave de API da OpenAI**
   - Acesse https://platform.openai.com/
   - Faça login ou crie uma conta gratuita.
   - No painel, vá em **API Keys** (Menu lateral).
   - Clique em **Create new secret key**.
   - Copie a chave gerada (começa com `sk-`).

3. **Crie um arquivo `.env` na pasta `show_do_milhao/`**
   ```text
   OPENAI_API_KEY=sk-sua_chave_aqui
   ```

4. **Adicione o `.env` ao `.gitignore`**
   ```text
   .env
   ```

5. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

6. **Estrutura de arquivos**
   ```
   show_do_milhao/
   ├── .env
   ├── README.md
   ├── requirements.txt
   ├── data/
   │   ├── perguntas.json
   │   ├── cache.json
   │   └── stats.json
   ├── ui/
   │   ├── __init__.py
   │   ├── menu.py
   │   ├── game.py
   │   └── result.py
   ├── logic/
   │   ├── __init__.py
   │   ├── game_logic.py
   │   ├── question_manager.py
   │   ├── help_manager.py
   │   ├── stats_manager.py
   │   └── api_manager.py
   ├── config.py
   ├── main.py
   └── tests/
      ├── test_game_logic.py
      └── test_question_manager.py
   ```

7. **Execute o jogo**
   ```bash
   python main.py
   ```

Divirta-se respondendo perguntas e veja seu conhecimento crescer!
```