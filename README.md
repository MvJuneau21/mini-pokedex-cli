# Mini-Pokédex CLI

Ferramenta de linha de comando que consulta a [PokéAPI](https://pokeapi.co/) e mostra informações de Pokémon no terminal.

Projeto de aula: usa apenas a biblioteca padrão do Python, então não há nada para instalar.

## Requisitos

- Python 3.10 ou superior
- Conexão com a internet (os dados vêm da PokéAPI)

Para verificar a versão instalada:

```bash
python --version
```

## Como usar

Execute os comandos a partir da pasta do projeto.

### Ver os dados de um Pokémon

```bash
python pokedex.py info pikachu
python pokedex.py info 25
```

Mostra número, nome, tipos, altura, peso, habilidades e stats base com barra ASCII.

### Listar Pokémon de um tipo

```bash
python pokedex.py tipo fire
python pokedex.py tipo water --limite 5
```

Mostra quantos Pokémon existem no tipo e lista os primeiros. O padrão é 20 itens; use `--limite N` para mudar.

### Comparar dois Pokémon

```bash
python pokedex.py comparar charizard blastoise
```

Mostra os stats lado a lado, o total de cada um e indica o maior (`*`).

### Ajuda

```bash
python pokedex.py -h
python pokedex.py info -h
```

## Dicas de entrada

- Não diferencia maiúsculas de minúsculas: `Pikachu` e `pikachu` dão o mesmo resultado.
- Espaços viram hífen automaticamente, mas **nomes com espaço precisam de aspas**, senão o terminal os separa em argumentos:

  ```bash
  python pokedex.py info "mr mime"    # correto
  python pokedex.py info mr mime      # erro: argumento extra
  ```

## Erros

Quando algo dá errado, a mensagem curta aparece no erro padrão (`stderr`) e o programa termina com código de saída `1`. Por exemplo:

```bash
python pokedex.py info naoexiste
# Erro: Pokémon não encontrado: 'naoexiste'.
```

Casos tratados: Pokémon ou tipo inexistente, entrada vazia, sem internet, tempo esgotado e `--limite` menor que 1.

## Testes

Os testes não acessam a internet; a rede é simulada (mock).

```bash
python -m unittest -v
```

## Estrutura

| Arquivo | Função |
|---|---|
| `pokedex.py` | Ponto de entrada: comandos e formatação da saída |
| `pokeapi.py` | Cliente HTTP da PokéAPI, com cache em memória |
| `test_pokedex.py` | Testes offline |
| `plan.md` | Plano do projeto, com as etapas |
| `CLAUDE.md` | Regras e resumo do projeto para o Claude |
| `RESPOSTAS.md` | Documento de reflexão da atividade |
