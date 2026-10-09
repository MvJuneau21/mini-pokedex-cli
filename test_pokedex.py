"""Testes offline: nenhuma chamada real à internet."""

import io
import unittest
import urllib.error
from contextlib import redirect_stderr, redirect_stdout
from unittest import mock

import pokeapi
import pokedex


def fake_pokemon(nome="pikachu", id_=25, hp=35, ataque=55):
    nomes = ["hp", "attack", "defense", "special-attack", "special-defense", "speed"]
    valores = [hp, ataque, 40, 50, 50, 90]
    return {
        "id": id_,
        "name": nome,
        "height": 4,
        "weight": 60,
        "types": [{"type": {"name": "electric"}}],
        "abilities": [
            {"ability": {"name": "static"}, "is_hidden": False},
            {"ability": {"name": "lightning-rod"}, "is_hidden": True},
        ],
        "stats": [
            {"base_stat": v, "stat": {"name": n}} for n, v in zip(nomes, valores)
        ],
    }


class TestNormalizar(unittest.TestCase):
    def test_minusculas_e_espacos(self):
        self.assertEqual(pokeapi.normalizar("  Mr Mime "), "mr-mime")

    def test_numero(self):
        self.assertEqual(pokeapi.normalizar(25), "25")


class TestGetJson(unittest.TestCase):
    def setUp(self):
        pokeapi._cache.clear()

    def test_404_vira_nao_encontrado(self):
        erro = urllib.error.HTTPError("url", 404, "Not Found", {}, None)
        with mock.patch("urllib.request.urlopen", side_effect=erro):
            with self.assertRaises(pokeapi.NaoEncontrado):
                pokeapi.get_json("/pokemon/xxx")

    def test_erro_de_rede(self):
        with mock.patch(
            "urllib.request.urlopen", side_effect=urllib.error.URLError("sem rede")
        ):
            with self.assertRaises(pokeapi.PokeAPIError) as ctx:
                pokeapi.get_json("/pokemon/pikachu")
        self.assertIn("internet", str(ctx.exception))

    def test_timeout_na_conexao(self):
        erro = urllib.error.URLError(TimeoutError("timed out"))
        with mock.patch("urllib.request.urlopen", side_effect=erro):
            with self.assertRaises(pokeapi.PokeAPIError) as ctx:
                pokeapi.get_json("/pokemon/pikachu")
        self.assertIn("demorou", str(ctx.exception))

    def test_conexao_interrompida(self):
        with mock.patch("urllib.request.urlopen", side_effect=ConnectionResetError()):
            with self.assertRaises(pokeapi.PokeAPIError):
                pokeapi.get_json("/pokemon/pikachu")

    def test_cache_evita_segunda_chamada(self):
        pokeapi._cache["/pokemon/pikachu"] = {"id": 25}
        with mock.patch("urllib.request.urlopen") as urlopen:
            self.assertEqual(pokeapi.get_json("/pokemon/pikachu"), {"id": 25})
            urlopen.assert_not_called()


class TestBuscar(unittest.TestCase):
    def test_entrada_vazia(self):
        with self.assertRaises(pokeapi.PokeAPIError):
            pokeapi.get_pokemon("   ")

    def test_normaliza_antes_de_chamar(self):
        with mock.patch("pokeapi.get_json", return_value={}) as get_json:
            pokeapi.get_pokemon("Mr Mime")
        get_json.assert_called_once_with("/pokemon/mr-mime")


class TestFormatacao(unittest.TestCase):
    def test_barra(self):
        self.assertEqual(pokedex.barra(0), "." * pokedex.LARGURA_BARRA)
        self.assertEqual(pokedex.barra(255), "#" * pokedex.LARGURA_BARRA)

    def test_info(self):
        texto = pokedex.formatar_info(fake_pokemon())
        self.assertIn("#25 Pikachu", texto)
        self.assertIn("Altura: 0.4 m", texto)
        self.assertIn("Peso: 6.0 kg", texto)
        self.assertIn("lightning-rod (oculta)", texto)

    def test_tipo_respeita_limite(self):
        tipo = {
            "name": "fire",
            "pokemon": [{"pokemon": {"name": f"p{i}"}} for i in range(10)],
        }
        texto = pokedex.formatar_tipo(tipo, 3)
        self.assertIn("10 Pokémon (mostrando 3)", texto)
        self.assertIn("- p2", texto)
        self.assertNotIn("- p3", texto)

    def test_comparacao_indica_maior(self):
        a = fake_pokemon("a", hp=100)
        b = fake_pokemon("b", hp=10)
        texto = pokedex.formatar_comparacao(a, b)
        self.assertIn("Maior total: A", texto)

    def test_comparacao_empate(self):
        texto = pokedex.formatar_comparacao(fake_pokemon("a"), fake_pokemon("b"))
        self.assertIn("Empate", texto)


class TestMain(unittest.TestCase):
    def rodar(self, argv):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            codigo = pokedex.main(argv)
        return codigo, out.getvalue(), err.getvalue()

    def test_info_ok(self):
        with mock.patch("pokeapi.get_json", return_value=fake_pokemon()):
            codigo, out, _ = self.rodar(["info", "pikachu"])
        self.assertEqual(codigo, 0)
        self.assertIn("Pikachu", out)

    def test_pokemon_inexistente_retorna_1(self):
        with mock.patch("pokeapi.get_json", side_effect=pokeapi.NaoEncontrado("x")):
            codigo, out, err = self.rodar(["info", "naoexiste"])
        self.assertEqual(codigo, 1)
        self.assertEqual(out, "")
        self.assertIn("Erro:", err)

    def test_comparar_ok(self):
        respostas = {
            "/pokemon/a": fake_pokemon("a", hp=100),
            "/pokemon/b": fake_pokemon("b"),
        }
        with mock.patch("pokeapi.get_json", side_effect=respostas.get):
            codigo, out, _ = self.rodar(["comparar", "a", "b"])
        self.assertEqual(codigo, 0)
        self.assertIn("Maior total: A", out)

    def test_ctrl_c_sem_traceback(self):
        with mock.patch("pokeapi.get_json", side_effect=KeyboardInterrupt):
            codigo, _, err = self.rodar(["info", "pikachu"])
        self.assertEqual(codigo, 1)
        self.assertIn("Cancelado", err)

    def test_limite_invalido(self):
        codigo, _, err = self.rodar(["tipo", "fire", "--limite", "0"])
        self.assertEqual(codigo, 1)
        self.assertIn("--limite", err)


if __name__ == "__main__":
    unittest.main()
