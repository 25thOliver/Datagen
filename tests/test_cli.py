import subprocess
import pytest

def test_cli_help():
    result = subprocess.run(["datagen", "--help"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "DataGen CLI" in result.stdout

def test_cli_profiles():
    result = subprocess.run(["datagen", "profiles", "--count", "5", "--seed", "42"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "full_name" in result.stdout