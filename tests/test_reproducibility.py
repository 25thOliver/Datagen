from datagen import generate_profiles, generate_salaries, generate_cars

def test_profiles_reproducibility():
    df1 = generate_profiles(n=20, seed=42)
    df2 = generate_profiles(n=20, seed=42)
    assert df1.equals(df2)

def test_salaries_reproducibility():
    df1 = generate_salaries(n=20, seed=123)
    df2 = generate_salaries(n=20, seed=123)
    assert df1.equals(df2)

def test_cars_reproducibility():
    df1 = generate_cars(n=20, seed=999)
    df2 = generate_cars(n=20, seed=999)
    assert df1.equals(df2)