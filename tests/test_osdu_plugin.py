"""
OSDU Plugin Tests

Tests for the osdu plugin that wraps osdu-quality CLI tool for GitLab CI/CD
test quality analysis.

Tests cover:
- Script functionality (help output, CLI options)
- Error handling (missing prerequisites)
- PEP 723 dependency declarations
- CLI wrapper pattern implementation
- Dual output mode support (JSON and TTY)
"""
# /// script
# dependencies = [
#   "pytest>=7.4.0",
# ]
# ///

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict

import pytest


# Path constants
PROJECT_ROOT = Path(__file__).parent.parent
OSDU_PLUGIN_DIR = PROJECT_ROOT / "plugins" / "osdu"
OSDU_SKILL_DIR = OSDU_PLUGIN_DIR / "skills" / "osdu"
OSDU_SCRIPTS_DIR = OSDU_SKILL_DIR / "scripts"
STATUS_SCRIPT = OSDU_SCRIPTS_DIR / "status.py"
ANALYZE_SCRIPT = OSDU_SCRIPTS_DIR / "analyze.py"


class TestOSDUPluginStructure:
    """Test OSDU plugin directory structure and files."""

    def test_plugin_directory_exists(self):
        """OSDU plugin directory should exist."""
        assert OSDU_PLUGIN_DIR.exists(), f"Missing {OSDU_PLUGIN_DIR}"
        assert OSDU_PLUGIN_DIR.is_dir()

    def test_skill_directory_exists(self):
        """OSDU skill directory should exist."""
        assert OSDU_SKILL_DIR.exists(), f"Missing {OSDU_SKILL_DIR}"
        assert OSDU_SKILL_DIR.is_dir()

    def test_scripts_directory_exists(self):
        """Scripts directory should exist."""
        assert OSDU_SCRIPTS_DIR.exists(), f"Missing {OSDU_SCRIPTS_DIR}"
        assert OSDU_SCRIPTS_DIR.is_dir()

    def test_required_scripts_exist(self):
        """Required Python scripts should exist."""
        assert STATUS_SCRIPT.exists(), f"Missing {STATUS_SCRIPT}"
        assert ANALYZE_SCRIPT.exists(), f"Missing {ANALYZE_SCRIPT}"
        assert STATUS_SCRIPT.is_file()
        assert ANALYZE_SCRIPT.is_file()


class TestPEP723Dependencies:
    """Test PEP 723 inline script metadata (dependency declarations)."""

    def test_status_script_has_pep723_metadata(self):
        """status.py should have PEP 723 dependency declaration."""
        content = STATUS_SCRIPT.read_text(encoding="utf-8")

        # Check for PEP 723 metadata block
        assert "# /// script" in content, "Missing PEP 723 opening marker"
        assert "# ///" in content, "Missing PEP 723 closing marker"
        assert '# dependencies = [' in content, "Missing dependencies declaration"

    def test_analyze_script_has_pep723_metadata(self):
        """analyze.py should have PEP 723 dependency declaration."""
        content = ANALYZE_SCRIPT.read_text(encoding="utf-8")

        # Check for PEP 723 metadata block
        assert "# /// script" in content, "Missing PEP 723 opening marker"
        assert "# ///" in content, "Missing PEP 723 closing marker"
        assert '# dependencies = [' in content, "Missing dependencies declaration"

    def test_scripts_declare_click_dependency(self):
        """Both scripts should declare click as a dependency."""
        for script in [STATUS_SCRIPT, ANALYZE_SCRIPT]:
            content = script.read_text(encoding="utf-8")
            assert '"click"' in content or "'click'" in content, \
                f"{script.name} should declare click dependency"


class TestScriptSyntax:
    """Test Python syntax validation for all scripts."""

    def test_status_script_syntax(self):
        """status.py should have valid Python syntax."""
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(STATUS_SCRIPT)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"Syntax error in status.py: {result.stderr}"

    def test_analyze_script_syntax(self):
        """analyze.py should have valid Python syntax."""
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(ANALYZE_SCRIPT)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"Syntax error in analyze.py: {result.stderr}"


class TestScriptHelpOutput:
    """Test CLI help functionality for both scripts."""

    @pytest.fixture
    def uv_available(self):
        """Check if uv is available."""
        try:
            subprocess.run(
                ["uv", "--version"],
                capture_output=True,
                check=True,
            )
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            return False

    def test_status_script_help(self, uv_available):
        """status.py should display help message."""
        if not uv_available:
            pytest.skip("uv not available")

        result = subprocess.run(
            ["uv", "run", str(STATUS_SCRIPT), "--help"],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT),
        )

        assert result.returncode == 0, f"Help command failed: {result.stderr}"

        # Verify help content includes key options
        help_text = result.stdout
        assert "--pipelines" in help_text, "Missing --pipelines option"
        assert "--project" in help_text, "Missing --project option"
        assert "--venus" in help_text, "Missing --venus option"
        assert "--no-release" in help_text, "Missing --no-release option"
        assert "--json" in help_text, "Missing --json option"
        assert "GITLAB_TOKEN" in help_text, "Missing GITLAB_TOKEN requirement"

    def test_analyze_script_help(self, uv_available):
        """analyze.py should display help message."""
        if not uv_available:
            pytest.skip("uv not available")

        result = subprocess.run(
            ["uv", "run", str(ANALYZE_SCRIPT), "--help"],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT),
        )

        assert result.returncode == 0, f"Help command failed: {result.stderr}"

        # Verify help content includes key options
        help_text = result.stdout
        assert "--pipelines" in help_text, "Missing --pipelines option"
        assert "--project" in help_text, "Missing --project option"
        assert "--stage" in help_text, "Missing --stage option"
        assert "--provider" in help_text, "Missing --provider option"
        assert "--json" in help_text, "Missing --json option"
        assert "GITLAB_TOKEN" in help_text, "Missing GITLAB_TOKEN requirement"


class TestErrorHandling:
    """Test error handling for missing prerequisites."""

    @pytest.fixture
    def clean_env(self):
        """Provide clean environment without GITLAB_TOKEN."""
        original_token = os.environ.get("GITLAB_TOKEN")

        # Remove GITLAB_TOKEN if present
        if "GITLAB_TOKEN" in os.environ:
            del os.environ["GITLAB_TOKEN"]

        yield

        # Restore original token
        if original_token:
            os.environ["GITLAB_TOKEN"] = original_token

    @pytest.fixture
    def uv_available(self):
        """Check if uv is available."""
        try:
            subprocess.run(
                ["uv", "--version"],
                capture_output=True,
                check=True,
            )
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            return False

    def test_status_missing_gitlab_token(self, uv_available, clean_env):
        """status.py should error when GITLAB_TOKEN is missing."""
        if not uv_available:
            pytest.skip("uv not available")

        result = subprocess.run(
            ["uv", "run", str(STATUS_SCRIPT), "--json"],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT),
        )

        # Should exit with error code
        assert result.returncode != 0, "Should fail without GITLAB_TOKEN"

        # Check for error message in JSON output
        try:
            error_data = json.loads(result.stdout)
            assert "error" in error_data, "Missing error field in JSON output"
            assert "GITLAB_TOKEN" in error_data["error"], \
                "Error should mention GITLAB_TOKEN"
        except json.JSONDecodeError:
            # If not JSON, check stderr for error message
            error_output = result.stderr or result.stdout
            assert "GITLAB_TOKEN" in error_output, \
                "Error message should mention GITLAB_TOKEN"

    def test_analyze_missing_gitlab_token(self, uv_available, clean_env):
        """analyze.py should error when GITLAB_TOKEN is missing."""
        if not uv_available:
            pytest.skip("uv not available")

        result = subprocess.run(
            ["uv", "run", str(ANALYZE_SCRIPT), "--json"],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT),
        )

        # Should exit with error code
        assert result.returncode != 0, "Should fail without GITLAB_TOKEN"

        # Check for error message in JSON output
        try:
            error_data = json.loads(result.stdout)
            assert "error" in error_data, "Missing error field in JSON output"
            assert "GITLAB_TOKEN" in error_data["error"], \
                "Error should mention GITLAB_TOKEN"
        except json.JSONDecodeError:
            # If not JSON, check stderr for error message
            error_output = result.stderr or result.stdout
            assert "GITLAB_TOKEN" in error_output, \
                "Error message should mention GITLAB_TOKEN"


class TestCLIWrapperPattern:
    """Test CLI wrapper implementation patterns."""

    def test_status_script_has_prerequisite_check(self):
        """status.py should have check_prerequisites function."""
        content = STATUS_SCRIPT.read_text(encoding="utf-8")

        assert "def check_prerequisites()" in content, \
            "Missing check_prerequisites function"
        assert "GITLAB_TOKEN" in content, "Missing GITLAB_TOKEN check"
        assert "osdu-quality" in content, "Missing osdu-quality CLI check"

    def test_analyze_script_has_prerequisite_check(self):
        """analyze.py should have check_prerequisites function."""
        content = ANALYZE_SCRIPT.read_text(encoding="utf-8")

        assert "def check_prerequisites()" in content, \
            "Missing check_prerequisites function"
        assert "GITLAB_TOKEN" in content, "Missing GITLAB_TOKEN check"
        assert "osdu-quality" in content, "Missing osdu-quality CLI check"

    def test_status_script_wraps_cli_command(self):
        """status.py should wrap osdu-quality status command."""
        content = STATUS_SCRIPT.read_text(encoding="utf-8")

        assert "osdu-quality" in content, "Should reference osdu-quality CLI"
        assert "status" in content, "Should reference status command"
        assert "subprocess" in content, "Should use subprocess for CLI execution"

    def test_analyze_script_wraps_cli_command(self):
        """analyze.py should wrap osdu-quality analyze command."""
        content = ANALYZE_SCRIPT.read_text(encoding="utf-8")

        assert "osdu-quality" in content, "Should reference osdu-quality CLI"
        assert "analyze" in content, "Should reference analyze command"
        assert "subprocess" in content, "Should use subprocess for CLI execution"

    def test_scripts_use_click_for_cli(self):
        """Scripts should use click for CLI interface."""
        for script in [STATUS_SCRIPT, ANALYZE_SCRIPT]:
            content = script.read_text(encoding="utf-8")

            assert "import click" in content, f"{script.name} should import click"
            assert "@click.command()" in content, \
                f"{script.name} should use click.command decorator"
            assert "@click.option" in content, \
                f"{script.name} should use click.option decorators"


class TestDualOutputMode:
    """Test dual output mode support (JSON and TTY)."""

    def test_status_script_has_json_option(self):
        """status.py should support --json option."""
        content = STATUS_SCRIPT.read_text(encoding="utf-8")

        # Check for JSON option definition
        assert '--json' in content or '"output_json"' in content, \
            "Missing --json option"
        assert "output_json" in content, "Missing output_json parameter"

    def test_analyze_script_has_json_option(self):
        """analyze.py should support --json option."""
        content = ANALYZE_SCRIPT.read_text(encoding="utf-8")

        # Check for JSON option definition
        assert '--json' in content or '"output_json"' in content, \
            "Missing --json option"
        assert "output_json" in content, "Missing output_json parameter"

    def test_status_script_handles_json_errors(self):
        """status.py should format errors as JSON when --json is used."""
        content = STATUS_SCRIPT.read_text(encoding="utf-8")

        # Check for JSON error handling
        assert "import json" in content, "Should import json module"
        assert 'json.dumps' in content, "Should use json.dumps for output"
        assert '"error"' in content or "'error'" in content, \
            "Should include error field in JSON output"

    def test_analyze_script_handles_json_errors(self):
        """analyze.py should format errors as JSON when --json is used."""
        content = ANALYZE_SCRIPT.read_text(encoding="utf-8")

        # Check for JSON error handling
        assert "import json" in content, "Should import json module"
        assert 'json.dumps' in content, "Should use json.dumps for output"
        assert '"error"' in content or "'error'" in content, \
            "Should include error field in JSON output"


class TestScriptOptions:
    """Test that scripts implement all documented options."""

    def test_status_script_options(self):
        """status.py should implement all documented options."""
        content = STATUS_SCRIPT.read_text(encoding="utf-8")

        required_options = [
            "--pipelines",
            "--project",
            "--venus",
            "--no-release",
            "--json",
        ]

        for option in required_options:
            assert option in content, f"Missing option: {option}"

    def test_analyze_script_options(self):
        """analyze.py should implement all documented options."""
        content = ANALYZE_SCRIPT.read_text(encoding="utf-8")

        required_options = [
            "--pipelines",
            "--project",
            "--stage",
            "--provider",
            "--json",
        ]

        for option in required_options:
            assert option in content, f"Missing option: {option}"

    def test_analyze_stage_choices(self):
        """analyze.py should validate stage choices."""
        content = ANALYZE_SCRIPT.read_text(encoding="utf-8")

        # Should have choice validation for stage
        assert "unit" in content, "Missing 'unit' stage option"
        assert "integration" in content, "Missing 'integration' stage option"
        assert "acceptance" in content, "Missing 'acceptance' stage option"

    def test_analyze_provider_choices(self):
        """analyze.py should validate provider choices."""
        content = ANALYZE_SCRIPT.read_text(encoding="utf-8")

        # Should have choice validation for provider
        assert "azure" in content, "Missing 'azure' provider option"
        assert "aws" in content, "Missing 'aws' provider option"
        assert "gcp" in content, "Missing 'gcp' provider option"
        assert "ibm" in content, "Missing 'ibm' provider option"


class TestScriptExecutability:
    """Test that scripts are executable."""

    def test_status_script_has_shebang(self):
        """status.py should have Python shebang."""
        with open(STATUS_SCRIPT, 'r', encoding='utf-8') as f:
            first_line = f.readline()

        assert first_line.startswith("#!"), "Missing shebang"
        assert "python" in first_line.lower(), "Shebang should reference python"

    def test_analyze_script_has_shebang(self):
        """analyze.py should have Python shebang."""
        with open(ANALYZE_SCRIPT, 'r', encoding='utf-8') as f:
            first_line = f.readline()

        assert first_line.startswith("#!"), "Missing shebang"
        assert "python" in first_line.lower(), "Shebang should reference python"

    def test_status_script_has_main_guard(self):
        """status.py should have __main__ guard."""
        content = STATUS_SCRIPT.read_text(encoding="utf-8")

        assert 'if __name__ == "__main__"' in content, \
            "Missing __main__ guard"

    def test_analyze_script_has_main_guard(self):
        """analyze.py should have __main__ guard."""
        content = ANALYZE_SCRIPT.read_text(encoding="utf-8")

        assert 'if __name__ == "__main__"' in content, \
            "Missing __main__ guard"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
