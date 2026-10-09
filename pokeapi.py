"""Cliente mínimo da PokéAPI. Única camada do projeto que acessa a rede."""

import http.client
import json
import urllib.error
import urllib.request

BASE_URL = "https://pokeapi.co/api/v2"
TIMEOUT = 10
USER_AGENT = "mini-pokedex-cli/1.0 (projeto de aula)"
MSG_TIMEOUT = "A PokéAPI demorou demais para responder."

_cache: dict[str, dict] = {}


class PokeAPIError(Exception):
    """Erro com mensagem já pronta para mostrar ao usuário."""


class NaoEncontrado(PokeAPIError):
    """O recurso pedido não existe (HTTP 404)."""


def normalizar(texto: str) -> str:
    """Minúsculas, sem espaços nas pontas, espaços internos viram '-'."""
    return "-".join(str(texto).strip().lower().split())


def get_json(path: str) -> dict:
    """GET em BASE_URL + path. Devolve o JSON; usa cache em memória."""
    if path in _cache:
        return _cache[path]

    req = urllib.request.Request(
        f"{BASE_URL}{path}", headers={"User-Agent": USER_AGENT}
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            dados = json.load(resp)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise NaoEncontrado("Não encontrado na PokéAPI.") from e
        raise PokeAPIError(f"Erro da PokéAPI (HTTP {e.code}).") from e
    except urllib.error.URLError as e:
        # timeout na conexão chega embrulhado em URLError
        if isinstance(e.reason, TimeoutError):
            raise PokeAPIError(MSG_TIMEOUT) from e
        raise PokeAPIError(
            "Não foi possível conectar à PokéAPI. Verifique sua internet."
        ) from e
    except TimeoutError as e:
        raise PokeAPIError(MSG_TIMEOUT) from e
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        raise PokeAPIError("Resposta inválida da PokéAPI.") from e
    except (OSError, http.client.HTTPException) as e:
        # ex.: conexão caiu no meio da leitura da resposta
        raise PokeAPIError("A conexão com a PokéAPI foi interrompida.") from e

    _cache[path] = dados
    return dados


def _buscar(recurso: str, rotulo: str, nome_ou_id: str) -> dict:
    """recurso = caminho na API ("pokemon"); rotulo = nome nas mensagens ("Pokémon")."""
    chave = normalizar(nome_ou_id)
    if not chave:
        raise PokeAPIError(f"{rotulo} não informado.")
    try:
        return get_json(f"/{recurso}/{chave}")
    except NaoEncontrado as e:
        raise NaoEncontrado(f"{rotulo} não encontrado: '{chave}'.") from e


def get_pokemon(nome_ou_id: str) -> dict:
    return _buscar("pokemon", "Pokémon", nome_ou_id)


def get_tipo(tipo: str) -> dict:
    return _buscar("type", "Tipo", tipo)
