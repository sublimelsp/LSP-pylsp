from LSP.plugin.core.typing import Dict
from lsp_utils.pip_client_handler import PipClientHandler
import os
import sublime


class Pyls(PipClientHandler):
    package_name = __package__
    requirements_txt_path = 'requirements.txt'
    server_filename = 'pyls'

    @classmethod
    def get_displayed_name(cls) -> str:
        return "pyls"

    @classmethod
    def get_additional_variables(cls) -> Dict[str, str]:
        variables = super().get_additional_variables()
        variables.update({
            'sublime_py_files_dir': os.path.dirname(sublime.__file__),
        })
        return variables


def plugin_loaded() -> None:
    Pyls.setup()


def plugin_unloaded() -> None:
    Pyls.cleanup()
