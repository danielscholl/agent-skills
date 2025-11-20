#!/usr/bin/env bash
#
# Plugin structure validation script
#
# Validates:
# - Directory structure (plugins/*/skills/*/)
# - Required files (plugin.json, SKILL.md, scripts/)
# - YAML frontmatter syntax in SKILL.md
# - JSON syntax in manifests
#
# Usage: bash scripts/validate-plugins.sh
# Exit: 0 on success, 1 on validation failure

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
ERRORS=0
WARNINGS=0

# Helper functions
error() {
    echo -e "${RED}ERROR: $1${NC}" >&2
    ((ERRORS++))
}

warning() {
    echo -e "${YELLOW}WARNING: $1${NC}" >&2
    ((WARNINGS++))
}

success() {
    echo -e "${GREEN}✓ $1${NC}"
}

info() {
    echo "INFO: $1"
}

# Validation functions
validate_marketplace_manifest() {
    local marketplace_file=".claude-plugin/marketplace.json"

    info "Validating marketplace manifest..."

    if [[ ! -f "$marketplace_file" ]]; then
        error "Missing marketplace manifest: $marketplace_file"
        return
    fi

    # Validate JSON syntax
    if ! jq empty "$marketplace_file" 2>/dev/null; then
        error "Invalid JSON syntax in $marketplace_file"
        return
    fi

    # Check required fields
    if ! jq -e '.name' "$marketplace_file" >/dev/null 2>&1; then
        error "Marketplace manifest missing 'name' field"
    fi

    if ! jq -e '.owner' "$marketplace_file" >/dev/null 2>&1; then
        error "Marketplace manifest missing 'owner' field"
    fi

    if ! jq -e '.plugins | length > 0' "$marketplace_file" >/dev/null 2>&1; then
        error "Marketplace manifest missing or empty 'plugins' array"
    fi

    success "Marketplace manifest validation passed"
}

validate_plugin_manifest() {
    local plugin_dir="$1"
    local manifest="${plugin_dir}/plugin.json"

    if [[ ! -f "$manifest" ]]; then
        error "Missing plugin manifest: $manifest"
        return
    fi

    # Validate JSON syntax
    if ! jq empty "$manifest" 2>/dev/null; then
        error "Invalid JSON syntax in $manifest"
        return
    fi

    # Check required fields
    local required_fields=("name" "displayName" "version" "description" "author" "license" "skills")

    for field in "${required_fields[@]}"; do
        if ! jq -e ".$field" "$manifest" >/dev/null 2>&1; then
            error "$manifest missing required field: $field"
        fi
    done

    # Validate semantic versioning
    local version
    version=$(jq -r '.version' "$manifest" 2>/dev/null || echo "")
    if [[ ! "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        error "$manifest has invalid version format: $version (expected X.Y.Z)"
    fi

    success "Plugin manifest validation passed: $manifest"
}

validate_skill_manifest() {
    local skill_file="$1"

    if [[ ! -f "$skill_file" ]]; then
        error "Missing SKILL.md: $skill_file"
        return
    fi

    # Extract YAML frontmatter (between first two --- lines)
    local frontmatter
    frontmatter=$(sed -n '/^---$/,/^---$/p' "$skill_file" | sed '1d;$d')

    if [[ -z "$frontmatter" ]]; then
        error "$skill_file missing YAML frontmatter"
        return
    fi

    # Validate YAML syntax using Python (portable across systems)
    if command -v python3 >/dev/null 2>&1; then
        # Try with installed PyYAML, fall back to UV if not available
        if ! echo "$frontmatter" | python3 -c "import sys, yaml; yaml.safe_load(sys.stdin)" 2>/dev/null; then
            # Try with UV if available
            if command -v uv >/dev/null 2>&1; then
                if ! echo "$frontmatter" | uv run --with pyyaml python3 -c "import sys, yaml; yaml.safe_load(sys.stdin)" 2>/dev/null; then
                    error "$skill_file has invalid YAML frontmatter syntax"
                    return
                fi
            else
                warning "PyYAML not installed and UV not found, skipping YAML syntax validation for $skill_file"
            fi
        fi
    else
        warning "Python3 not found, skipping YAML syntax validation for $skill_file"
    fi

    # Check required fields (basic grep check)
    local required_fields=("name:" "description:" "version:" "allowed-tools:")

    for field in "${required_fields[@]}"; do
        if ! grep -q "^${field}" "$skill_file"; then
            error "$skill_file missing required field: ${field%:}"
        fi
    done

    success "SKILL.md validation passed: $skill_file"
}

validate_plugin_structure() {
    local plugin_dir="$1"
    local plugin_name
    plugin_name=$(basename "$plugin_dir")

    info "Validating plugin: $plugin_name"

    # Check plugin.json
    validate_plugin_manifest "$plugin_dir"

    # Check skills/ subdirectory
    if [[ ! -d "${plugin_dir}/skills" ]]; then
        error "Plugin missing skills/ subdirectory: $plugin_dir"
        return
    fi

    # Validate each skill
    local skill_count=0
    for skill_dir in "${plugin_dir}"/skills/*; do
        if [[ -d "$skill_dir" ]]; then
            skill_count=$((skill_count + 1))
            validate_skill_structure "$skill_dir"
        fi
    done

    if [[ $skill_count -eq 0 ]]; then
        warning "Plugin has no skills: $plugin_dir"
    fi
}

validate_skill_structure() {
    local skill_dir="$1"
    local skill_name
    skill_name=$(basename "$skill_dir")

    # Check SKILL.md
    local skill_md="${skill_dir}/SKILL.md"
    validate_skill_manifest "$skill_md"

    # Check scripts/ directory
    if [[ ! -d "${skill_dir}/scripts" ]]; then
        error "Skill missing scripts/ directory: $skill_dir"
        return
    fi

    # Check for at least one script
    local script_count
    script_count=$(find "${skill_dir}/scripts" -type f -name "*.py" | wc -l)

    if [[ $script_count -eq 0 ]]; then
        warning "Skill has no Python scripts: $skill_dir"
    fi
}

# Main validation
main() {
    echo "========================================="
    echo "Plugin Marketplace Validation"
    echo "========================================="
    echo

    # Check for required tools
    if ! command -v jq >/dev/null 2>&1; then
        error "jq is required but not installed. Please install jq."
        exit 1
    fi

    # Validate marketplace manifest
    validate_marketplace_manifest
    echo

    # Validate plugins directory
    if [[ ! -d "plugins" ]]; then
        error "plugins/ directory not found"
        exit 1
    fi

    # Validate each plugin
    local plugin_count=0
    for plugin_dir in plugins/*; do
        if [[ -d "$plugin_dir" ]]; then
            plugin_count=$((plugin_count + 1))
            validate_plugin_structure "$plugin_dir"
            echo
        fi
    done

    if [[ $plugin_count -eq 0 ]]; then
        error "No plugins found in plugins/ directory"
    fi

    # Summary
    echo "========================================="
    echo "Validation Summary"
    echo "========================================="
    echo "Plugins validated: $plugin_count"
    echo "Errors: $ERRORS"
    echo "Warnings: $WARNINGS"
    echo

    if [[ $ERRORS -gt 0 ]]; then
        echo -e "${RED}Validation FAILED with $ERRORS error(s)${NC}"
        exit 1
    elif [[ $WARNINGS -gt 0 ]]; then
        echo -e "${YELLOW}Validation PASSED with $WARNINGS warning(s)${NC}"
        exit 0
    else
        echo -e "${GREEN}Validation PASSED - all checks successful!${NC}"
        exit 0
    fi
}

# Run main function
main
