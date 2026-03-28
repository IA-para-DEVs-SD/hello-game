"""Testes para o sistema de save/load."""

from pathlib import Path

import pytest

from pyblaze.utils.save_system import SaveSystem


class TestSaveSystem:
    """Testes para a classe SaveSystem."""

    def test_save_system_creates_directory(self, tmp_path: Path) -> None:
        """Testa que SaveSystem cria o diretório se não existir."""
        save_dir = tmp_path / "saves"
        assert not save_dir.exists()

        save_system = SaveSystem(save_dir)

        assert save_dir.exists()
        assert save_system.save_dir == save_dir

    def test_save_game_creates_file(self, tmp_path: Path) -> None:
        """Testa que save_game cria um arquivo."""
        save_system = SaveSystem(tmp_path)
        player_data = {"lives": 3, "rings": 10, "checkpoint_x": 100.0}

        result = save_system.save_game(player_data)

        assert result is True
        assert save_system.save_file.exists()

    def test_load_game_returns_saved_data(self, tmp_path: Path) -> None:
        """Testa que load_game retorna os dados salvos."""
        save_system = SaveSystem(tmp_path)
        original_data = {
            "lives": 3,
            "rings": 25,
            "checkpoint_x": 500.0,
            "checkpoint_y": 300.0,
        }

        save_system.save_game(original_data)
        loaded_data = save_system.load_game()

        assert loaded_data == original_data

    def test_load_game_without_save_returns_none(self, tmp_path: Path) -> None:
        """Testa que load_game retorna None se não houver save."""
        save_system = SaveSystem(tmp_path)

        loaded_data = save_system.load_game()

        assert loaded_data is None

    def test_delete_save_removes_file(self, tmp_path: Path) -> None:
        """Testa que delete_save remove o arquivo."""
        save_system = SaveSystem(tmp_path)
        save_system.save_game({"lives": 3})

        assert save_system.save_file.exists()

        result = save_system.delete_save()

        assert result is True
        assert not save_system.save_file.exists()

    def test_delete_save_without_file_returns_false(self, tmp_path: Path) -> None:
        """Testa que delete_save retorna False se não houver arquivo."""
        save_system = SaveSystem(tmp_path)

        result = save_system.delete_save()

        assert result is False

    def test_has_save_returns_true_when_exists(self, tmp_path: Path) -> None:
        """Testa has_save com save existente."""
        save_system = SaveSystem(tmp_path)

        assert save_system.has_save() is False

        save_system.save_game({"lives": 3})

        assert save_system.has_save() is True

    def test_get_save_info_returns_metadata(self, tmp_path: Path) -> None:
        """Testa que get_save_info retorna metadados do save."""
        save_system = SaveSystem(tmp_path)
        save_system.save_game({"lives": 3, "rings": 10})

        info = save_system.get_save_info()

        assert info is not None
        assert info["exists"] is True
        assert info["size"] > 0
        assert "modified" in info
        assert "path" in info

    def test_get_save_info_without_save_returns_none(self, tmp_path: Path) -> None:
        """Testa get_save_info sem save."""
        save_system = SaveSystem(tmp_path)

        info = save_system.get_save_info()

        assert info is None

    def test_save_game_with_complex_data(self, tmp_path: Path) -> None:
        """Testa save_game com dados complexos."""
        save_system = SaveSystem(tmp_path)
        complex_data = {
            "lives": 3,
            "rings": 50,
            "checkpoint_x": 1000.5,
            "checkpoint_y": 500.25,
            "level": "zone_1",
            "time_played": 123.45,
            "achievements": ["speed_demon", "ring_collector"],
        }

        save_system.save_game(complex_data)
        loaded_data = save_system.load_game()

        assert loaded_data == complex_data

    def test_save_overwrites_previous_save(self, tmp_path: Path) -> None:
        """Testa que save sobrescreve o save anterior."""
        save_system = SaveSystem(tmp_path)

        save_system.save_game({"lives": 3})
        save_system.save_game({"lives": 5})

        loaded_data = save_system.load_game()

        assert loaded_data == {"lives": 5}

    def test_multiple_saves_and_loads(self, tmp_path: Path) -> None:
        """Testa múltiplos ciclos de save/load."""
        save_system = SaveSystem(tmp_path)

        for i in range(5):
            data = {"lives": i, "rings": i * 10}
            save_system.save_game(data)
            loaded = save_system.load_game()
            assert loaded == data
