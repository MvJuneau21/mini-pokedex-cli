# plan.md — Mini-Pokédex CLI (PokéAPI + Python)

> Plano gerado em **plan mode** no Claude Code, antes de qualquer arquivo de código existir.
> Cada etapa é executada só depois de aprovada. Marque `[x]` ao concluir.

## Objetivo
Uma ferramenta de linha de comando que consulta a [PokéAPI](https://pokeapi.co/) (gratuita, sem chave)
e mostra informações de Pokémon no terminal.

## Decisões técnicas
| Decisão | Escolha | Motivo |
|---|---|---|
| API | PokéAPI v2 | Gratuita, sem autenticação, estável, dados ricos |
| Linguagem | Python 3.10+ | Já instalado; fácil de ler e corrigir |
| Dependências | Só biblioteca padrão (`urllib`, `json`, `argparse`, `unittest`) | Roda em qualquer máquina sem `pip install` |
| Cache | Dicionário em memória | Evita requisição repetida no mesmo comando (ex.: `comparar`) |
| Testes | `unittest` + `unittest.mock` | Testam sem depender da internet |

## Estrutura
```
mini-projeto-api/
├── CLAUDE.md          # resumo e regras do projeto para o Claude
├── plan.md            # este arquivo
├── README.md          # como rodar
├── pokedex.py         # CLI (argparse) — ponto de entrada
├── pokeapi.py         # cliente HTTP da PokéAPI
├── test_pokedex.py    # testes offline
└── RESPOSTAS.md       # documento de reflexão da atividade
```

## Funcionalidades
- `python pokedex.py info <nome|id>` → nº, nome, tipos, altura (m), peso (kg), habilidades e stats base com barra ASCII.
- `python pokedex.py tipo <tipo> [--limite N]` → lista Pokémon de um tipo (padrão 20).
- `python pokedex.py comparar <a> <b>` → stats lado a lado + total, indicando o maior.
- Erros amigáveis: Pokémon/tipo inexistente (404), sem internet/timeout, entrada vazia → exit code 1.
- Entrada normalizada (minúsculas, espaços → `-`).

## Etapas

### [x] Etapa 1 — Estrutura e documentação · modelo: **Opus**
- Criar pasta, `plan.md` e `CLAUDE.md`.
- Critério de pronto: os dois arquivos existem e descrevem o projeto.

### [x] Etapa 2 — Cliente da API (`pokeapi.py`) · modelo: **Sonnet**
- `get_json(path)` com `urllib.request`, timeout 10s, header `User-Agent`, cache em dict.
- `get_pokemon(nome_ou_id)`, `get_tipo(tipo)`, `normalizar(texto)`.
- Exceção `PokeAPIError` para 404 / erro de rede / JSON inválido.
- Critério de pronto: `python -c "import pokeapi; print(pokeapi.get_pokemon('pikachu')['id'])"` imprime `25`.

### [x] Etapa 3 — CLI (`pokedex.py`) · modelo: **Sonnet**
- `argparse` com subcomandos `info`, `tipo`, `comparar`.
- Funções de formatação separadas das funções que chamam a API (facilita teste).
- Critério de pronto: os 3 comandos funcionam com dados reais.

### [x] Etapa 4 — Testes (`test_pokedex.py`) · modelo: **Sonnet** (ou Haiku)
- Mock de `pokeapi.get_json` com JSON fixo; testar formatação, normalização, 404 e comparação.
- Critério de pronto: `python -m unittest -v` passa sem internet.

### [x] Etapa 5 — Revisão · modelo: **Opus**
- Rodar testes + comandos reais; revisar casos de erro, nomes, duplicação.
- Critério de pronto: nenhum problema pendente na revisão.

### [x] Etapa 6 — README e RESPOSTAS · modelo: **Haiku**
- `README.md` com instruções de uso; esqueleto do `RESPOSTAS.md` (o texto final é escrito pelo aluno).

## Verificação final
```bash
python -m unittest -v
python pokedex.py info pikachu
python pokedex.py info 25
python pokedex.py tipo fire --limite 5
python pokedex.py comparar charizard blastoise
python pokedex.py info naoexiste      # erro amigável, exit code 1
```

## Riscos e mitigação
- **Rate limit / API fora do ar** → timeout + mensagem clara; testes não dependem da rede.
- **Escopo crescer** (Pokémon evolutions, imagens, GUI…) → fora do escopo; só depois de tudo pronto.
- **Contexto longo na sessão** → `/compact` ao fim de cada etapa grande; `/clear` antes da revisão.
