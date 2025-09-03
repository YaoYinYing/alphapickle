import pytest

from alphapickle import AlphaPickleRunner, AlphaFoldJson


@pytest.mark.serial
def test_process_directory_real(example_data_dir):
    runner = AlphaPickleRunner(n_jobs=1, plot_size=1)
    outputs = runner.process_directory(example_data_dir)
    expected = len(AlphaFoldJson(example_data_dir).ranking)
    assert len(outputs) == expected
    assert (example_data_dir / "ranked_1_pLDDT.csv").exists()
