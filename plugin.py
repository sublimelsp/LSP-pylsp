from __future__ import annotations

from lsp_utils import GenericClientHandler
from lsp_utils import UvVenvManager
from pathlib import Path
from typing import final
from typing_extensions import override
import sublime


@final
class Pylsp(GenericClientHandler):
    package_name = str(__package__)
    uv_venv_manager: UvVenvManager | None = None

    # --- GenericClientHandler handlers --------------------------------------------------------------------------------

    @classmethod
    @override
    def needs_update_or_installation(cls) -> bool:
        if not cls.uv_venv_manager:
            cls.uv_venv_manager = UvVenvManager(cls.package_name, 'server/pyproject.toml', Path(cls.storage_path()))
        return cls.uv_venv_manager.needs_install_or_update()

    @classmethod
    @override
    def install_or_update(cls) -> None:
        if not cls.uv_venv_manager:
            raise Exception('Expected UvVenvManager to be initialized')
        cls.uv_venv_manager.install()

    @classmethod
    @override
    def get_additional_variables(cls) -> dict[str, str]:
        variables = super().get_additional_variables()
        variables.update({
            'sublime_py_files_dir': str(Path(sublime.__file__).parent),
        })
        if cls.uv_venv_manager:
            variables.update({
                'server_path': str(cls.uv_venv_manager.venv_bin_path / 'pylsp'),
            })
        return variables

    @classmethod
    @override
    def get_additional_paths(cls) -> list[str]:
        if uv_venv_manager := cls.uv_venv_manager:
            return [str(uv_venv_manager.venv_bin_path)]
        return []


def plugin_loaded() -> None:
    Pylsp.setup()


def plugin_unloaded() -> None:
    Pylsp.cleanup()
