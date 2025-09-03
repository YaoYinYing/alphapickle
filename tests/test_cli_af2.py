import os

from alphapickle.cli import af2


def test_af2_cli(example_data_dir):
    csv_file = example_data_dir / "ranked_1_pLDDT.csv"
    if csv_file.exists():
        os.remove(csv_file)
    af2(["-od", str(example_data_dir), "-ps", "1", "-pi", "50"])
    assert csv_file.exists()
