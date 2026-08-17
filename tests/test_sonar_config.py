"""Tests for sonar-project.properties, this repo's SonarQube scanner config.

Regression coverage for two distinct problems:

1. This repo previously had no sonar-project.properties at all, so even a
   correctly-authenticated scan would have had no declared project identity
   (project key / name) and no sources to scan. test_sonar_config_declares_
   project_identity and test_sonar_sources_root_is_a_real_path lock that
   scanner metadata in.

2. The actual reported failure ("No SonarQube token configured ...") is a
   CI-secrets problem, not something a config file committed to this repo
   can fix — the autopilot pipeline's secret store has to inject
   SONAR_TOKEN at scan time. The tempting wrong fix is to hardcode a token
   (or otherwise make the scan report a fake success) so the pipeline stops
   complaining. test_sonar_config_never_embeds_a_credential locks in that
   sonar-project.properties must never contain
   sonar.login/sonar.token/sonar.password/sonar.token.name, so SONAR_TOKEN
   stays something injected at scan time, never something committed.

Uses only the standard library (unittest) since this repo has no existing
test framework or dependency manifest to build on top of.
"""

from __future__ import annotations

import unittest
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SONAR_PROPERTIES_PATH = _REPO_ROOT / "sonar-project.properties"

# Credential-shaped keys that must never be committed to this file. SonarQube
# accepts several spellings/aliases for the same secret; block them all.
_FORBIDDEN_CREDENTIAL_KEYS = {
    "sonar.login",
    "sonar.token",
    "sonar.password",
    "sonar.token.name",
}


def _load_sonar_properties() -> dict:
    assert (
        _SONAR_PROPERTIES_PATH.is_file()
    ), "sonar-project.properties is missing from the repo root"

    properties = {}
    for raw_line in _SONAR_PROPERTIES_PATH.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or line.startswith("!"):
            continue
        assert "=" in line, f"malformed properties line (no '='): {raw_line!r}"
        key, _, value = line.partition("=")
        properties[key.strip()] = value.strip()
    return properties


class SonarConfigTests(unittest.TestCase):
    def test_sonar_config_declares_project_identity(self):
        properties = _load_sonar_properties()

        self.assertTrue(
            properties.get("sonar.projectKey"),
            "sonar.projectKey must be set so scans attach to the right project",
        )
        self.assertTrue(
            properties.get("sonar.sources"),
            "sonar.sources must be set so the scanner knows what to analyze",
        )

    def test_sonar_config_never_embeds_a_credential(self):
        properties = _load_sonar_properties()

        present_credential_keys = _FORBIDDEN_CREDENTIAL_KEYS & properties.keys()
        self.assertFalse(
            present_credential_keys,
            "sonar-project.properties must never hardcode a credential "
            f"(found: {sorted(present_credential_keys)}) — SONAR_TOKEN has "
            "to come from the CI/autopilot secrets store at scan time, not "
            "from a committed file",
        )

    def test_sonar_sources_root_is_a_real_path(self):
        properties = _load_sonar_properties()

        for source in properties.get("sonar.sources", "").split(","):
            source = source.strip()
            self.assertTrue(source, "sonar.sources must not contain an empty entry")
            resolved = (_REPO_ROOT / source).resolve()
            self.assertTrue(
                resolved.exists(),
                f"sonar.sources entry {source!r} does not exist at {resolved}",
            )

    def test_sonar_properties_file_has_no_duplicate_keys(self):
        # A duplicate key silently shadows the earlier value, which is easy
        # to introduce by accident when hand-editing this file later.
        keys = []
        for raw_line in _SONAR_PROPERTIES_PATH.read_text().splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or line.startswith("!"):
                continue
            key, _, _value = line.partition("=")
            keys.append(key.strip())

        duplicates = {key for key in keys if keys.count(key) > 1}
        self.assertFalse(
            duplicates,
            f"sonar-project.properties has duplicate keys: {sorted(duplicates)}",
        )


if __name__ == "__main__":
    unittest.main()
