import pytest
import pandas as pd
from datagen import (
    generate_profiles,
    generate_salaries,
    generate_regions,
    generate_cars
)

def test_generate_profiles_default():
    df = generate_profiles(n=10)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 10
    assert "full_name" in df.columns
    assert "phone" in df.columns
    assert "email" in df.columns

def test_generate_profiles_invalid_n():
    with pytest.raises(ValueError):
        generate_profiles(n=0)

def test_generate_salaries_kes():
    df = generate_salaries(n=10, currency="KES")
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 10
    assert df["currency"].iloc[0] == "KES"
    assert "total_compensation" in df.columns

def test_generate_regions_all():
    df = generate_regions(include_all=True)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 6
    assert "region_name" in df.columns

def test_generate_cars():
    df = generate_cars(n=15)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 15
    assert "price_kes" in df.columns