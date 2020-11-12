from LSP.plugin.core.typing import Any, Dict, List, Optional
from lsp_utils import GenericClientHandler
from lsp_utils import ServerResourceInterface
from lsp_utils import ServerStatus
from lsp_utils.helpers import run_command_sync
import operator
import os
import shutil
import sublime
import subprocess


class PylsServerResource(ServerResourceInterface):

    @classmethod
    def file_extension(cls) -> str:
        return ".exe" if sublime.platform() == "windows" else ""

    @classmethod
    def pyls_version_str(cls) -> str:
        settings = sublime.load_settings("LSP-pyls.sublime-settings")
        return str(settings.get("pyls_version"))

    @classmethod
    def black_version_str(cls) -> str:
        settings = sublime.load_settings("LSP-pyls.sublime-settings")
        return str(settings.get("pyls_black_version"))

    @classmethod
    def isort_version_str(cls) -> str:
        settings = sublime.load_settings("LSP-pyls.sublime-settings")
        return str(settings.get("pyls_isort_version"))

    @classmethod
    def python_exe(cls) -> str:
        return "python" if sublime.platform() == "windows" else "python3"

    @classmethod
    def run(cls, *args: Any, **kwargs: Any) -> bytes:
        if sublime.platform() == "windows":
            startupinfo = subprocess.STARTUPINFO()  # type: ignore
            flag = subprocess.STARTF_USESHOWWINDOW  # type: ignore
            startupinfo.dwFlags |= flag
        else:
            startupinfo = None
        return subprocess.check_output(args=args, cwd=kwargs.get("cwd"), startupinfo=startupinfo,
                                       stderr=subprocess.STDOUT)

    def __init__(self, storage_path: str) -> None:
        self._storage_path = storage_path
        self._status = ServerStatus.UNINITIALIZED

    # --- ServerResourceInterface handlers ----------------------------------------------------------------------------

    @property
    def binary_path(self) -> str:
        return self.server_exe()

    def needs_installation(self) -> bool:
        if os.path.exists(self.server_exe()) and os.path.exists(self.pip_exe()):
            if not os.path.exists(self.python_version()):
                return True
            with open(self.python_version(), 'rb') as f:
                if f.readline() != self.run(self.python_exe(), '--version'):
                    return True
            requirements = {
                "pyls": [True, "python-language-server"],
                "black": [True, "pyls-black"],
                "isort": [True, "pyls-isort"]
            }  # type: Dict[str, List[Any]]
            for line in self.run(self.pip_exe(), "freeze").decode("ascii").splitlines():
                for name, requirement in requirements.items():
                    prefix = requirement[1] + "=="
                    if line.startswith(prefix):
                        stored_version_str = line[len(prefix):].strip()
                        attr = "{}_version_str".format(name)
                        version_str = getattr(self, attr)
                        assert callable(version_str)
                        if stored_version_str == version_str():
                            requirement[0] = False
                            continue
            if not any(map(operator.itemgetter(0), requirements.values())):
                self._status = ServerStatus.READY
                return False
        return True

    def install_or_update(self) -> None:
        shutil.rmtree(self.basedir(), ignore_errors=True)
        try:
            os.makedirs(self.basedir(), exist_ok=True)
            self.run(self.python_exe(), "-m", "venv", "LSP-pyls", cwd=self._storage_path)
            pyls = "python-language-server[all]=={}".format(self.pyls_version_str())
            black = "pyls-black=={}".format(self.black_version_str())
            isort = "pyls-isort=={}".format(self.isort_version_str())
            mypy = "git+https://github.com/tomv564/pyls-mypy.git"
            self.run(self.pip_exe(), "install", pyls, black, mypy, isort)
            with open(self.python_version(), 'wb') as f:
                f.write(self.run(self.python_exe(), '--version'))
        except Exception:
            shutil.rmtree(self.basedir(), ignore_errors=True)
            raise
        self._status = ServerStatus.READY

    def get_status(self) -> int:
        return self._status

    # --- internal handlers -------------------------------------------------------------------------------------------

    def basedir(self) -> str:
        return os.path.join(self._storage_path, "LSP-pyls")

    def bindir(self) -> str:
        bin_dir = "Scripts" if sublime.platform() == "windows" else "bin"
        return os.path.join(self.basedir(), bin_dir)

    def server_exe(self) -> str:
        return os.path.join(self.bindir(), "pyls" + self.file_extension())

    def pip_exe(self) -> str:
        return os.path.join(self.bindir(), "pip" + self.file_extension())

    def python_version(self) -> str:
        return os.path.join(self.basedir(), 'python_version')


class Pyls(GenericClientHandler):
    package_name = __package__
    _server = None  # type: Optional[ServerResourceInterface]

    @classmethod
    def get_displayed_name(cls) -> str:
        return "pyls"

    @classmethod
    def get_additional_variables(cls) -> Optional[Dict[str, str]]:
        variables = super().get_additional_variables()
        variables.update({
            'sublime_py_files_dir': os.path.dirname(sublime.__file__),
        })
        return variables

    @classmethod
    def manages_server(cls) -> bool:
        return True

    @classmethod
    def get_server(cls) -> Optional[ServerResourceInterface]:
        if not cls._server:
            cls._server = PylsServerResource(cls.storage_path())
        return cls._server


def plugin_loaded() -> None:
    Pyls.setup()


def plugin_unloaded() -> None:
    Pyls.cleanup()
