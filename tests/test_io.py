import os
import pytest
from datagen import generate_profiles, save_data

def test_save_data_csv(tmp_path):
    df = generate_profiles(n=5)
    file_path = tmp_path / "test.csv"
    saved_path = save_data(df, str(file_path))
    assert os.path.exists(saved_path)

def test_save_data_json(tmp_path):
    df = generate_profiles(n=5)
    file_path = tmp_path / "test.json"
    saved_path = save_data(df, str(file_path))
    assert os.path.exists(saved_path)