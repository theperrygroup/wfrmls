---
title: "Install the WFRMLS Python package"
description: "Install wfrmls in a Python virtual environment, verify the installed version, and set up separate contributor and docs tooling."
---

# Install the WFRMLS Python package

Install `wfrmls` in the Python environment that will run your application.
The package requires Python 3.8 or later and depends on `requests` and
`python-dotenv`. The repository's test matrix covers Python 3.8–3.12.

## Create a virtual environment

Check your interpreter with `python --version`, then create an environment:

```bash
python -m venv .venv
```

=== "macOS or Linux"

    ```bash
    source .venv/bin/activate
    ```

=== "Windows PowerShell"

    ```powershell
    .venv\Scripts\Activate.ps1
    ```

If activation is restricted by your environment, invoke the environment's
Python executable directly. Use the same interpreter for installation and execution.

## Install and verify

```bash
python -m pip install --upgrade pip
python -m pip install wfrmls
python -m pip check
python -c "import wfrmls; print(wfrmls.__version__)"
```

The import check verifies the package installation. It does not use a token or
validate API access. For repeatable deployments, pin the version you have tested
in your application's dependency manifest.

## Install a local checkout

For source changes, install the checkout in editable mode:

```bash
git clone https://github.com/theperrygroup/wfrmls.git
cd wfrmls
python -m pip install -e ".[dev]"
```

The `dev` extra adds testing and code-quality tools. Documentation dependencies
live separately in `docs/requirements.txt`; there is no `docs` extra. Use
Python 3.11 for the current docs toolchain and follow the
[contributor setup](../development/index.md).

## Resolve installation problems

| Symptom | Check |
| --- | --- |
| `ModuleNotFoundError: wfrmls` | Run `python -m pip show wfrmls` with the interpreter that runs your script. |
| Package resolution fails | Check the Python version and dependency constraints shown by pip. |
| TLS certificate verification fails | Repair your interpreter's certificate store or configured proxy certificates. |
| The IDE cannot import the package | Select the interpreter from the environment where you installed it. |

Keep certificate verification enabled. A package installation error is separate
from a provider authentication error during an API request.

## Next step

[Configure your bearer token](authentication.md), then run the
[quick start](quickstart.md).
