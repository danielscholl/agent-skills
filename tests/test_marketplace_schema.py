"""
Marketplace schema validation tests.

Validates that marketplace.json, plugin.json, and SKILL.md files conform
to Claude Code plugin marketplace specifications.
"""
# /// script
# dependencies = [
#   "pytest>=7.4.0",
#   "pyyaml>=6.0",
# ]
# ///

import json
import re
from pathlib import Path
from typing import Any, Dict

import pytest
import yaml


# Path constants
PROJECT_ROOT = Path(__file__).parent.parent
MARKETPLACE_FILE = PROJECT_ROOT / ".claude-plugin" / "marketplace.json"
PLUGINS_DIR = PROJECT_ROOT / "plugins"


def load_json(path: Path) -> Dict[str, Any]:
    """Load and parse JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_skill_frontmatter(path: Path) -> Dict[str, Any]:
    """Extract and parse YAML frontmatter from SKILL.md."""
    content = path.read_text(encoding="utf-8")

    # Match YAML frontmatter between --- delimiters
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        raise ValueError(f"No frontmatter found in {path}")

    frontmatter = match.group(1)
    return yaml.safe_load(frontmatter)


class TestMarketplaceManifest:
    """Test marketplace.json structure and content."""

    def test_marketplace_file_exists(self):
        """Marketplace manifest file should exist."""
        assert MARKETPLACE_FILE.exists(), f"Missing {MARKETPLACE_FILE}"

    def test_marketplace_valid_json(self):
        """Marketplace manifest should be valid JSON."""
        data = load_json(MARKETPLACE_FILE)
        assert isinstance(data, dict)

    def test_marketplace_required_fields(self):
        """Marketplace manifest should have all required fields."""
        data = load_json(MARKETPLACE_FILE)

        required_fields = ["name", "displayName", "owner", "plugins"]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"

    def test_marketplace_plugins_array(self):
        """Plugins field should be a non-empty array."""
        data = load_json(MARKETPLACE_FILE)

        assert "plugins" in data
        assert isinstance(data["plugins"], list)
        assert len(data["plugins"]) > 0, "Plugins array should not be empty"

    def test_marketplace_plugin_entries(self):
        """Each plugin entry should have required fields."""
        data = load_json(MARKETPLACE_FILE)

        required_plugin_fields = ["name", "path", "description"]

        for plugin in data["plugins"]:
            for field in required_plugin_fields:
                assert field in plugin, f"Plugin missing field: {field}"

            # Validate plugin path points to existing directory
            plugin_path = PROJECT_ROOT / plugin["path"]
            assert plugin_path.exists(), f"Plugin directory not found: {plugin_path}"


class TestPluginManifests:
    """Test plugin.json files for each plugin."""

    @pytest.fixture
    def plugin_dirs(self):
        """Get all plugin directories."""
        if not PLUGINS_DIR.exists():
            pytest.skip("Plugins directory does not exist")

        return [d for d in PLUGINS_DIR.iterdir() if d.is_dir()]

    def test_plugin_manifests_exist(self, plugin_dirs):
        """Each plugin should have a plugin.json file."""
        for plugin_dir in plugin_dirs:
            manifest = plugin_dir / "plugin.json"
            assert manifest.exists(), f"Missing plugin.json in {plugin_dir.name}"

    def test_plugin_manifests_valid_json(self, plugin_dirs):
        """Plugin manifests should be valid JSON."""
        for plugin_dir in plugin_dirs:
            manifest = plugin_dir / "plugin.json"
            if manifest.exists():
                data = load_json(manifest)
                assert isinstance(data, dict)

    def test_plugin_manifests_required_fields(self, plugin_dirs):
        """Plugin manifests should have all required fields."""
        required_fields = [
            "name", "displayName", "version", "description",
            "author", "license", "skills"
        ]

        for plugin_dir in plugin_dirs:
            manifest = plugin_dir / "plugin.json"
            if manifest.exists():
                data = load_json(manifest)

                for field in required_fields:
                    assert field in data, f"{plugin_dir.name}: Missing field {field}"

    def test_plugin_semantic_versioning(self, plugin_dirs):
        """Plugin versions should follow semantic versioning."""
        semver_pattern = r'^\d+\.\d+\.\d+$'

        for plugin_dir in plugin_dirs:
            manifest = plugin_dir / "plugin.json"
            if manifest.exists():
                data = load_json(manifest)
                version = data.get("version", "")

                assert re.match(semver_pattern, version), \
                    f"{plugin_dir.name}: Invalid version format '{version}' (expected X.Y.Z)"

    def test_plugin_author_fields(self, plugin_dirs):
        """Plugin author should have required fields."""
        for plugin_dir in plugin_dirs:
            manifest = plugin_dir / "plugin.json"
            if manifest.exists():
                data = load_json(manifest)
                author = data.get("author", {})

                assert isinstance(author, dict), f"{plugin_dir.name}: Author should be object"
                assert "name" in author, f"{plugin_dir.name}: Author missing name"

    def test_plugin_skills_array(self, plugin_dirs):
        """Plugin skills should be a non-empty array."""
        for plugin_dir in plugin_dirs:
            manifest = plugin_dir / "plugin.json"
            if manifest.exists():
                data = load_json(manifest)
                skills = data.get("skills", [])

                assert isinstance(skills, list), f"{plugin_dir.name}: Skills should be array"
                assert len(skills) > 0, f"{plugin_dir.name}: Skills array should not be empty"


class TestSkillManifests:
    """Test SKILL.md files in plugin skill directories."""

    @pytest.fixture
    def skill_files(self):
        """Get all SKILL.md files."""
        if not PLUGINS_DIR.exists():
            pytest.skip("Plugins directory does not exist")

        return list(PLUGINS_DIR.glob("*/skills/*/SKILL.md"))

    def test_skill_files_exist(self, skill_files):
        """Skills should have SKILL.md files."""
        assert len(skill_files) > 0, "No SKILL.md files found"

    def test_skill_frontmatter_valid(self, skill_files):
        """SKILL.md frontmatter should be valid YAML."""
        for skill_file in skill_files:
            data = load_skill_frontmatter(skill_file)
            assert isinstance(data, dict)

    def test_skill_required_fields(self, skill_files):
        """SKILL.md frontmatter should have required fields."""
        required_fields = ["name", "description", "version", "allowed-tools"]

        for skill_file in skill_files:
            data = load_skill_frontmatter(skill_file)

            for field in required_fields:
                assert field in data, f"{skill_file.name}: Missing field {field}"

    def test_skill_name_format(self, skill_files):
        """Skill names should be lowercase with hyphens."""
        name_pattern = r'^[a-z][a-z0-9-]*$'

        for skill_file in skill_files:
            data = load_skill_frontmatter(skill_file)
            name = data.get("name", "")

            assert re.match(name_pattern, name), \
                f"{skill_file.name}: Invalid name format '{name}' (use lowercase-with-hyphens)"
            assert len(name) <= 64, f"{skill_file.name}: Name too long (max 64 chars)"

    def test_skill_description_length(self, skill_files):
        """Skill descriptions should not exceed 1024 characters."""
        for skill_file in skill_files:
            data = load_skill_frontmatter(skill_file)
            description = data.get("description", "")

            assert len(description) <= 1024, \
                f"{skill_file.name}: Description too long ({len(description)} > 1024 chars)"

    def test_skill_version_format(self, skill_files):
        """Skill versions should follow semantic versioning."""
        semver_pattern = r'^\d+\.\d+\.\d+$'

        for skill_file in skill_files:
            data = load_skill_frontmatter(skill_file)
            version = data.get("version", "")

            assert re.match(semver_pattern, version), \
                f"{skill_file.name}: Invalid version format '{version}' (expected X.Y.Z)"

    def test_skill_allowed_tools(self, skill_files):
        """Allowed-tools should be a string or list."""
        for skill_file in skill_files:
            data = load_skill_frontmatter(skill_file)
            allowed_tools = data.get("allowed-tools")

            assert allowed_tools is not None, f"{skill_file.name}: Missing allowed-tools"
            assert isinstance(allowed_tools, (str, list)), \
                f"{skill_file.name}: allowed-tools should be string or array"


class TestDirectoryStructure:
    """Test plugin directory structure compliance."""

    def test_plugins_directory_exists(self):
        """Plugins directory should exist."""
        assert PLUGINS_DIR.exists(), "plugins/ directory should exist"
        assert PLUGINS_DIR.is_dir(), "plugins/ should be a directory"

    def test_plugin_skills_subdirectory(self):
        """Each plugin should have a skills/ subdirectory."""
        if not PLUGINS_DIR.exists():
            pytest.skip("Plugins directory does not exist")

        for plugin_dir in PLUGINS_DIR.iterdir():
            if plugin_dir.is_dir():
                skills_dir = plugin_dir / "skills"
                assert skills_dir.exists(), f"{plugin_dir.name}: Missing skills/ subdirectory"

    def test_skill_scripts_directory(self):
        """Each skill should have a scripts/ directory."""
        if not PLUGINS_DIR.exists():
            pytest.skip("Plugins directory does not exist")

        for skill_dir in PLUGINS_DIR.glob("*/skills/*"):
            if skill_dir.is_dir():
                scripts_dir = skill_dir / "scripts"
                assert scripts_dir.exists(), f"{skill_dir.name}: Missing scripts/ directory"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
