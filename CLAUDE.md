# CLAUDE.md — Mini-Pokédex CLI

## Resumo
CLI em Python que consulta a PokéAPI (https://pokeapi.co/api/v2/) e mostra dados de Pokémon no terminal.
Projeto de aula: o foco é código simples, legível e funcional, não features.
O plano completo e o status das etapas estão em `plan.md` — **leia antes de mudar qualquer coisa**.

## Comandos
```bash
python pokedex.py info <nome|id>
python pokedex.py tipo <tipo> [--limite N]
python pokedex.py comparar <a> <b>
python -m unittest -v          # rodar testes (offline)
```

## Arquitetura
- `pokeapi.py` — única camada que acessa a rede. Expõe `get_json`, `get_pokemon`, `get_tipo`, `normalizar` e `PokeAPIError`.
- `pokedex.py` — CLI (`argparse`). Funções `formatar_*` recebem dicts e retornam strings (sem I/O), para serem testáveis.
- `test_pokedex.py` — testes `unittest`; sempre mockam `pokeapi.get_json`, nunca chamam a internet.

## Regras para o Claude
- **Só biblioteca padrão do Python.** Não adicionar `requests` nem qualquer `pip install`.
- Siga o `plan.md`: execute **uma etapa por vez** e pare para aprovação antes da próxima. Marque `[x]` ao concluir.
- Não adicione funcionalidades fora do `plan.md` sem perguntar.
- Toda chamada de rede passa por `pokeapi.get_json` (timeout de 10s, header `User-Agent`).
- Erros para o usuário: mensagem curta em português no stderr + `exit code 1`. Nada de traceback.
- Textos da interface em português; nomes de Pokémon/tipos como vêm da API (inglês).
- Depois de alterar código, rode `python -m unittest -v` e confirme que passa.

## Convenções
- Python 3.10+, funções pequenas, nomes em português (`buscar_`, `formatar_`), type hints simples.
- Sem classes desnecessárias; módulos curtos.
