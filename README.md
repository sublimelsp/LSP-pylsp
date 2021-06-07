# LSP-pylsp

This is a helper package that automatically installs and updates the
[Python LSP Server](https://github.com/python-lsp/python-lsp-server) (pylsp) for you.

To use this package, you must have:

- An executable `python` (on Windows) or `python3` (on Linux/macOS)
- The [LSP](https://packagecontrol.io/packages/LSP) package
- For Ubuntu and Debian users, you must also install `python3-venv` with `apt`
- It's recommended to also install the `LSP-json` package which will provide autocompletion and validation for this package's settings.

## Applicable Selectors

This language server operates on views with the `source.python` base scope.

## Installation Location

The server is installed in the `$CACHE/Package Storage/LSP-pylsp` directory, where `$CACHE` is the base data path of Sublime Text.
For instance, `$CACHE` is `~/.cache/sublime-text` on a Linux system. If you want to force a re-installation of the server,
you can delete the entire `$CACHE/Package Storage/LSP-pylsp` directory or just reinstall the package. The installation is done through a virtual environment, using
pip. Therefore, you must have at least the `python` executable installed and it must be present in your `$PATH`.

Like any helper package, installation starts when you open a view that is suitable for this language server. In this
case, that means that when you open a view with the `source.python` base scope, installation commences.

## Configuration

Configure the Python LSP Server by accessing `Preferences > Package Settings > LSP > Servers > LSP-pylsp`.

### Virtual environments

If your project needs to run and be validated within a virtual environment, point to the environment using the `pylsp.plugins.jedi.environment` setting. For example if your virtual environment lives in `.venv/myproject` within the the project directory then run `Project: Edit Project` from the Command Palette and add the setting like so:

```json
{
    // "folders": [
    //     ...
    // ]
    "settings":
    {
        "LSP":
        {
            "LSP-pylsp":
            {
                "settings":
                {
                    "pylsp.plugins.jedi.environment": "./.venv/myproject"
                }
            }
        }
    }
}
```

You can also set it in the `LSP-pylsp` global settings but it's more likely that you'd want this to be overriden per-project.

## Code Completion

This language server provides code completion through JEDI.

## Signature Help

This language server provides signature help through JEDI.

## Goto

This language server provides "goto definition" through JEDI.

## Find References

This language server provides "find references" through JEDI.

## Rename

This language server provides "rename word/symbol" through JEDI.

## Linters

The default linter is `pycodestyle`. The possible linters are:

- pycodestyle (`"pylsp.plugins.pycodestyle.enabled"` in the settings)
- pydocstyle (`"pylsp.plugins.pydocstyle.enabled"` in the settings)
- flake8 (`"pylsp.plugins.flake8.enabled"` in the settings)
  For flake8 to work, you must also modify `"pylsp.configurationSources"` to be `["flake8"]` instead of the default
  `["pycodestyle"]`.
- pyflakes (`"pylsp.plugins.pyflakes.enabled"` in the settings)
- pylint (`"pylsp.plugins.pylint.enabled"` in the settings)
- mypy_ls (`"pylsp.plugins.mypy_ls.enabled"` in the settings)

After changing a linter, you must restart Sublime Text.

## Formatters

The default formatter is `autopep8`. The possible formatters are:

- yapf (`"pylsp.plugins.yapf.enabled"` in the settings)
- autopep8 (`"pylsp.plugins.autopep8.enabled"` in the settings)
- black (`"pylsp.plugins.pylsp_black.enabled"` in the settings)

After changing a formatter, you must restart Sublime Text.

## Sorting import statements

To sort your import statements, you can enable `isort`. The relevant setting is `"pylsp.plugins.pyls_isort.enabled"` in
the settings. Sorting is done through the "LSP: Format Document" option in the Context Menu by right-clicking in the
view with your mouse.

## Sublime Text Plugin Development

By default, the environment of pylsp is adjusted so that the `PYTHONPATH` includes the directory where `sublime.py` and
`sublime_plugin.py` live, as well as the $DATA/Packages directory. This enables accurate code completion for these
files.
