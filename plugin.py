from __future__ import annotations

from LSP.plugin import LspPlugin
from LSP.plugin import OnPreStartContext
from lsp_utils import UvVenvManager
from pathlib import Path
from sublime_lib import ResourcePath
from typing import final
from typing_extensions import override
import sublime


@final
class Pylsp(LspPlugin):

    @classmethod
    @override
    def on_pre_start_async(cls, context: OnPreStartContext) -> None:
        package_name = cls.plugin_storage_path.name
        UvVenvManager.on_pre_start_async(
            context, cls.plugin_storage_path, ResourcePath('Packages', package_name, 'server'), 'pylsp')
        context.variables.update({
            'sublime_py_files_dir': str(Path(sublime.__file__).parent),
        })


def plugin_loaded() -> None:
    Pylsp.register()


def plugin_unloaded() -> None:
    Pylsp.unregister()
