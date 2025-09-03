import json
import pytest

from alphapickle.cli import main


@pytest.mark.serial
def test_cli_directory_option(example_data_dir):
    csv_file = example_data_dir / "ranked_1_pLDDT.csv"
    if csv_file.exists():
        csv_file.unlink()
    main(["-od", str(example_data_dir), "-ps", "1", "-pi", "50"])
    assert csv_file.exists()


@pytest.mark.serial
def test_cli_pickle_option(example_data_dir):
    csv_file = example_data_dir / "result_model_1_pred_0_pLDDT.csv"
    if csv_file.exists():
        csv_file.unlink()
    main([
        "-pf",
        str(example_data_dir / "result_model_1_pred_0.pkl"),
        "-ps",
        "1",
        "-pi",
        "50",
    ])
    assert csv_file.exists()


@pytest.mark.serial
def test_cli_pdb_option(example_data_dir):
    csv_file = example_data_dir / "ranked_1_pLDDT.csv"
    if csv_file.exists():
        csv_file.unlink()
    main(["-pdb", str(example_data_dir / "ranked_1.pdb"), "-ps", "1", "-pi", "50"])
    assert csv_file.exists()


@pytest.mark.serial
def test_cli_pae_json_option(tmp_path):
    json_file = tmp_path / "pae.json"
    json_file.write_text(json.dumps({"predicted_aligned_error": [[0, 1], [1, 0]]}))
    png_file = tmp_path / "pae_PAE.png"
    if png_file.exists():
        png_file.unlink()
    main(["-json", str(json_file), "-ps", "1", "-pi", "1"])
    assert png_file.exists()

