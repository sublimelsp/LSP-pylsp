import operator
import os
import shutil
import subprocess

import sublime
from LSP.plugin import AbstractPlugin
from LSP.plugin import register_plugin
from LSP.plugin import unregister_plugin
from LSP.plugin.core.typing import Any, Dict, Optional


class Pyls(AbstractPlugin):
    @classmethod
    def name(cls) -> str:
        return "pyls"

    @classmethod
    def additional_variables(cls) -> Optional[Dict[str, str]]:
        variables = {}
        variables['sublime_py_files_dir'] = os.path.dirname(sublime.__file__)
        return variables

    @classmethod
    def basedir(cls) -> str:
        return os.path.join(sublime.cache_path(), "LSP-pyls")

    @classmethod
    def bindir(cls) -> str:
        return os.path.join(cls.basedir(), "bin")

    @classmethod
    def server_exe(cls) -> str:
        return os.path.join(cls.bindir(), "pyls")

    @classmethod
    def pip_exe(cls) -> str:
        return os.path.join(cls.bindir(), "pip")

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

    @classmethod
    def needs_update_or_installation(cls) -> bool:
        if os.path.exists(cls.server_exe()) and os.path.exists(cls.pip_exe()):
            requirements = {
                "pyls": [True, "python-language-server"],
                "black": [True, "pyls-black"],
                "isort": [True, "pyls-isort"]
            }  # type: Dict[str, List[Any]]
            for line in cls.run(cls.pip_exe(), "freeze").decode("ascii").splitlines():
                for name, requirement in requirements.items():
                    prefix = requirement[1] + "=="
                    if line.startswith(prefix):
                        stored_version_str = line[len(prefix):].strip()
                        attr = "{}_version_str".format(name)
                        version_str = getattr(cls, attr)
                        assert callable(version_str)
                        if stored_version_str == version_str():
                            requirement[0] = False
                            continue
            return any(map(operator.itemgetter(0), requirements.values()))
        return True

    @classmethod
    def install_or_update(cls) -> None:
        shutil.rmtree(cls.basedir(), ignore_errors=True)
        try:
            os.makedirs(cls.basedir(), exist_ok=True)
            cls.run(cls.python_exe(), "-m", "venv", "LSP-pyls", cwd=sublime.cache_path())
            pyls = "python-language-server[all]=={}".format(cls.pyls_version_str())
            black = "pyls-black=={}".format(cls.black_version_str())
            isort = "pyls-isort=={}".format(cls.isort_version_str())
            mypy = "git+https://github.com/tomv564/pyls-mypy.git"
            cls.run(cls.pip_exe(), "install", pyls, black, mypy, isort)
        except Exception:
            shutil.rmtree(cls.basedir(), ignore_errors=True)
            raise


# def plugin_loaded() -> None:
#     register_plugin(Pyls)


# def plugin_unloaded() -> None:
#     unregister_plugin(Pyls)
