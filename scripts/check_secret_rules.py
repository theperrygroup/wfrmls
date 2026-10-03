"""Check pinned Gitleaks rules using generated, noncredential input only."""

import argparse
import json
import secrets
import string
import subprocess
import tempfile
from pathlib import Path

EXPECTED_VERSION = "8.30.1"
CUSTOM_RULE = "wfrmls-bearer-token"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gitleaks", default="gitleaks")
    args = parser.parse_args()
    version = subprocess.run(
        [args.gitleaks, "version"], capture_output=True, text=True, check=True
    ).stdout.strip()
    if version != EXPECTED_VERSION:
        raise SystemExit("Use the pinned Gitleaks " + EXPECTED_VERSION + " release.")

    root = Path(__file__).resolve().parent.parent
    token = secrets.token_hex(16)
    low_entropy = "01" * 16
    github_token = "ghp_" + "".join(
        secrets.choice(string.ascii_letters + string.digits) for _ in range(36)
    )
    cases = [
        (
            "environment assignment",
            "os.environ['WFRMLS_BEARER_TOKEN'] = '" + token + "'",
            CUSTOM_RULE,
        ),
        (
            "constructor keyword",
            "WFRMLSClient(bearer_token='" + token + "')",
            CUSTOM_RULE,
        ),
        ("bare dotenv value", "WFRMLS_BEARER_TOKEN=" + token, CUSTOM_RULE),
        (
            "multiline assignment",
            "os.environ[\n'WFRMLS_BEARER_TOKEN'\n] =\n'" + token + "'",
            CUSTOM_RULE,
        ),
        ("authorization header", "Authorization: Bearer " + token, CUSTOM_RULE),
        ("low entropy", "bearer_token='" + low_entropy + "'", CUSTOM_RULE),
        (
            "inline allow comment",
            "bearer_token='" + token + "' # gitleaks:allow",
            CUSTOM_RULE,
        ),
        ("default GitHub rule", "github_token='" + github_token + "'", "github-pat"),
        ("test sentinel", "bearer_token='test_token'", None),
        ("invalid sentinel", "bearer_token='invalid_token'", None),
        ("documentation placeholder", "bearer_token='documentation-test-token'", None),
        (
            "dotenv placeholder",
            "WFRMLS_BEARER_TOKEN=replace-with-your-issued-token",
            None,
        ),
        ("environment lookup", "token = os.environ['WFRMLS_BEARER_TOKEN']", None),
        (
            "Actions secret reference",
            "WFRMLS_BEARER_TOKEN: ${{ secrets.WFRMLS_BEARER_TOKEN }}",
            None,
        ),
    ]
    with tempfile.TemporaryDirectory(prefix="wfrmls-gitleaks-ignore-") as ignore_path:
        command = [
            args.gitleaks,
            "stdin",
            "--config",
            str(root / ".gitleaks.toml"),
            "--redact=100",
            "--no-banner",
            "--no-color",
            "--ignore-gitleaks-allow",
            "--gitleaks-ignore-path",
            ignore_path,
            "--report-format=json",
            "--report-path=-",
        ]
        for label, content, expected_rule in cases:
            result = subprocess.run(
                command, input=content + "\n", text=True, capture_output=True
            )
            expected_status = 1 if expected_rule else 0
            if result.returncode != expected_status:
                raise SystemExit(label + ": unexpected scanner exit status.")
            if any(
                value in result.stdout + result.stderr
                for value in (token, low_entropy, github_token)
            ):
                raise SystemExit(label + ": scanner output was not fully redacted.")
            findings = json.loads(result.stdout)
            rules = {item["RuleID"] for item in findings}
            if expected_rule and expected_rule not in rules:
                raise SystemExit(
                    label + ": expected rule did not detect the synthetic input."
                )
            if not expected_rule and findings:
                raise SystemExit(label + ": ordinary placeholder was rejected.")
    print("Passed " + str(len(cases)) + " secret-rule checks; synthetic input only.")


if __name__ == "__main__":
    main()
