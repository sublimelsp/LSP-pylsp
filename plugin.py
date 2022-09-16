from LSP.plugin.core.typing import Dict
from lsp_utils.pip_client_handler import PipClientHandler
from sublime_lib import ResourcePath
import os


class Pylsp(PipClientHandler):
    package_name = __package__
    requirements_txt_path = "requirements.txt"
    server_filename = "pylsp"

    @classmethod
    def get_additional_variables(cls) -> Dict[str, str]:
        variables = super().get_additional_variables()
        variables.update({
            "sublime_stubs_dir": os.path.join(cls.package_storage(), 'stubs', 'sublime_text'),
        })
        return variables

    @classmethod
    def install_or_update(cls) -> None:
        super().install_or_update()
        # Copy stubs
        src = 'Packages/{}/stubs/'.format(cls.package_name)
        dest = os.path.join(cls.package_storage(), 'stubs')
        ResourcePath(src).copytree(dest, exist_ok=True)


def plugin_loaded() -> None:
    Pylsp.setup()


def plugin_unloaded() -> None:
    Pylsp.cleanup()
