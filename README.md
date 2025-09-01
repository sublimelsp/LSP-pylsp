# LSP-pylsp

This is a helper package that automatically installs and updates the
[Python LSP Server](https://github.com/python-lsp/python-lsp-server) (pylsp) for you.

To use this package, you must have:

- An executable `python` (on Windows) or `python3` (on Linux/macOS)
- The [LSP](https://packagecontrol.io/packages/LSP) package
- For Ubuntu and Debian users, you must also install `python3-venv` with `apt`
- It's recommended to also install the `LSP-json` package which will provide auto-completion and validation for this package's settings.

## Applicable Selectors

This language server operates on views with the `source.python` base scope.

## Installation Location

The server is installed in the `$CACHE/Package Storage/LSP-pylsp` directory, where `$CACHE` is the base data path of Sublime Text.
For instance, `$CACHE` is `~/.cache/sublime-text` on a Linux system. If you want to force a re-installation of the server,
you can delete the entire `$CACHE/Package Storage/LSP-pylsp` directory or just reinstall the package. The installation is done through a virtual environment, using
pip. Therefore, you must have at least the `python` executable installed and it must be present in your `$PATH`.

Like any helper package, installation starts when you open a view that is suitable for this language server. In this
case, that means that when you open a view with the `source.python` base scope, installation commences.

## Running alongside LSP-pyright

[`LSP-pyright`](https://packagecontrol.io/packages/LSP-pyright) is a more modern, faster and actively supported alternative to `LSP-pylsp`. While it's arguably much better solution for validating the code and type-checking, it doesn't support linters or code formatters like `flake8`, `pyflakes`, `pydocstyle`, `yapf` or `black`. The solution to that could be to run them alongside each other with code-checking features disabled in `LSP-pylsp`. To achieve that, open `Preferences: LSP-pylsp Settings` from the _Command Palette_ and add the following user settings:

```js
{
    "disabled_capabilities": {
        "completionProvider": true,
        "definitionProvider": true,
        "documentHighlightProvider": true,
        "documentSymbolProvider": true,
        "hoverProvider": true,
        "referencesProvider": true,
        "renameProvider": true,
        "signatureHelpProvider": true,
    },
    "settings": {
        "pylsp.plugins.jedi_completion.enabled": false,
        "pylsp.plugins.jedi_definition.enabled": false,
        "pylsp.plugins.jedi_hover.enabled": false,
        "pylsp.plugins.jedi_references.enabled": false,
        "pylsp.plugins.jedi_signature_help.enabled": false,
        "pylsp.plugins.jedi_symbols.enabled": false,
    },
}
```

## Configuration

Configure the Python LSP Server by accessing `Preferences > Package Settings > LSP > Servers > LSP-pylsp`.

### Python Binary

The underlying `pylsp` server will be installed inside a virtual environment created using a system-default Python interpreter (by default `python` on Windows and `python3` on other platforms). If you want to, for example, develop code that requires a newer version of Python than the one installed by default, you can override the path to the Python interpreter (binary) by changing the `python_binary` setting. For example:

```jsonc
// Settings in here override those in "LSP-pylsp/LSP-pylsp.sublime-settings"
{
    "python_binary": "/opt/homebrew/bin/python3",
}
```

### Virtual environments

If your project needs to run and be validated within a virtual environment, point to the environment using the `pylsp.plugins.jedi.environment` setting. For example, if your virtual environment lives in `.venv/myproject` within the project directory then run `Project: Edit Project` from the Command Palette and add the setting like so:

```jsonc
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

You can also set it in the `LSP-pylsp` global settings but it's more likely that you'd want this to be overridden per-project.

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
- pylsp_mypy (`"pylsp.plugins.pylsp_mypy.enabled"` in the settings)
- ruff (`"pylsp.plugins.ruff.enabled"` in the settings)

After changing a linter, you must restart Sublime Text.

## Formatters

The default formatter is `autopep8`. The possible formatters are:

| Name           | Setting | Note |
|:---------------|:--------|:-----|
| autopep8       | `pylsp.plugins.autopep8.enabled` | |
| black          | `pylsp.plugins.black.enabled` | When enabling also make sure that `autopep8` and `yapf` are disabled. |
| ruff           | `pylsp.plugins.ruff.formatEnabled` | Make sure to also enable `pylsp.plugins.ruff.enabled` and disable other formatters and linters. |
| yapf           | `pylsp.plugins.yapf.enabled` | |

## Sorting import statements

To sort your import statements, you can enable `isort`. The relevant setting is `"pylsp.plugins.pyls_isort.enabled"` in
the settings. Sorting is done through the "LSP: Format Document" option in the Context Menu by right-clicking within the
view with your mouse.

## Sublime Text Plugin Development

By default, the environment of pylsp is adjusted so that the `PYTHONPATH` includes the directory where `sublime.py` and
`sublime_plugin.py` live, as well as the $DATA/Packages directory. This enables accurate code completion for these
files.
