"""Mini-Pokédex: consulta Pokémon na PokéAPI pelo terminal."""

import argparse
import sys

import pokeapi

LARGURA_BARRA = 20
STAT_MAX = 255  # maior valor base possível de um stat
NOMES_STATS = {
    "hp": "HP",
    "attack": "Ataque",
    "defense": "Defesa",
    "special-attack": "Atq. Esp.",
    "special-defense": "Def. Esp.",
    "speed": "Veloc.",
}


def barra(valor: int) -> str:
    cheios = round(valor / STAT_MAX * LARGURA_BARRA)
    return "#" * cheios + "." * (LARGURA_BARRA - cheios)


def stats_de(pokemon: dict) -> dict[str, int]:
    return {s["stat"]["name"]: s["base_stat"] for s in pokemon["stats"]}


def formatar_info(pokemon: dict) -> str:
    tipos = ", ".join(t["type"]["name"] for t in pokemon["types"])
    habilidades = ", ".join(
        a["ability"]["name"] + (" (oculta)" if a["is_hidden"] else "")
        for a in pokemon["abilities"]
    )
    linhas = [
        f"#{pokemon['id']} {pokemon['name'].capitalize()}",
        f"Tipos: {tipos}",
        f"Altura: {pokemon['height'] / 10} m",
        f"Peso: {pokemon['weight'] / 10} kg",
        f"Habilidades: {habilidades}",
        "Stats base:",
    ]
    for chave, valor in stats_de(pokemon).items():
        nome = NOMES_STATS.get(chave, chave)
        linhas.append(f"  {nome:<10} {valor:>3} {barra(valor)}")
    return "\n".join(linhas)


def formatar_tipo(tipo: dict, limite: int) -> str:
    nomes = [p["pokemon"]["name"] for p in tipo["pokemon"]]
    mostrados = nomes[:limite]
    linhas = [f"Tipo {tipo['name']}: {len(nomes)} Pokémon (mostrando {len(mostrados)})"]
    linhas += [f"  - {n}" for n in mostrados]
    return "\n".join(linhas)


def formatar_comparacao(a: dict, b: dict) -> str:
    sa, sb = stats_de(a), stats_de(b)
    nome_a, nome_b = a["name"].capitalize(), b["name"].capitalize()
    linhas = [f"{'':<10} {nome_a:>12} {nome_b:>12}"]
    for chave in sa:
        va, vb = sa[chave], sb.get(chave, 0)
        marca_a = "*" if va > vb else " "
        marca_b = "*" if vb > va else " "
        nome = NOMES_STATS.get(chave, chave)
        linhas.append(f"{nome:<10} {va:>11}{marca_a} {vb:>11}{marca_b}")
    ta, tb = sum(sa.values()), sum(sb.values())
    linhas.append(f"{'Total':<10} {ta:>11}{'*' if ta > tb else ' '} {tb:>11}{'*' if tb > ta else ' '}")
    if ta == tb:
        linhas.append("Empate no total.")
    else:
        linhas.append(f"Maior total: {nome_a if ta > tb else nome_b} (*)")
    return "\n".join(linhas)


def criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pokedex", description="Mini-Pokédex usando a PokéAPI."
    )
    sub = parser.add_subparsers(dest="comando", required=True)

    p_info = sub.add_parser("info", help="mostra dados de um Pokémon")
    p_info.add_argument("pokemon", help="nome ou número (ex.: pikachu, 25)")

    p_tipo = sub.add_parser("tipo", help="lista Pokémon de um tipo")
    p_tipo.add_argument("tipo", help="ex.: fire, water, grass")
    p_tipo.add_argument("--limite", type=int, default=20, help="máximo de itens (padrão 20)")

    p_comp = sub.add_parser("comparar", help="compara os stats de dois Pokémon")
    p_comp.add_argument("a")
    p_comp.add_argument("b")
    return parser


def executar(args: argparse.Namespace) -> str:
    if args.comando == "info":
        return formatar_info(pokeapi.get_pokemon(args.pokemon))
    if args.comando == "tipo":
        if args.limite < 1:
            raise pokeapi.PokeAPIError("--limite deve ser pelo menos 1.")
        return formatar_tipo(pokeapi.get_tipo(args.tipo), args.limite)
    return formatar_comparacao(pokeapi.get_pokemon(args.a), pokeapi.get_pokemon(args.b))


def main(argv: list[str] | None = None) -> int:
    args = criar_parser().parse_args(argv)
    try:
        print(executar(args))
    except pokeapi.PokeAPIError as e:
        print(f"Erro: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Cancelado.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
