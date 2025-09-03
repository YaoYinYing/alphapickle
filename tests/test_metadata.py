import json
import pickle

import numpy as np
import pytest

from alphapickle import AlphaFoldPAEJson, AlphaFoldPDB, AlphaFoldPickle, AlphaPickleRunner


@pytest.mark.parametrize("plot_increment", [1, 2])
def test_pickle_processing(tmp_path, plot_increment):
    data = {"plddt": [80.0, 90.0], "predicted_aligned_error": [[0.0, 1.0], [1.0, 0.0]]}
    pickle_file = tmp_path / "result_model_1.pkl"
    with open(pickle_file, "wb") as fh:
        pickle.dump(data, fh)
    obj = AlphaFoldPickle(pickle_file)
    obj.write_plddt_file()
    obj.plot_plddt(size_in_inches=1, axis_label_increment=plot_increment)
    obj.plot_pae(size_in_inches=1, axis_label_increment=plot_increment)
    assert (tmp_path / "result_model_1_pLDDT.csv").exists()


def test_pae_json(tmp_path):
    json_file = tmp_path / "sample_pae.json"
    with open(json_file, "w") as fh:
        json.dump({"predicted_aligned_error": [[0, 0], [0, 0]]}, fh)
    obj = AlphaFoldPAEJson(json_file)
    assert obj.PAE.shape == (2, 2)


def test_pdb_processing(tmp_path):
    pdb_content = (
        "ATOM      1  CA  ALA A   1       0.000   0.000   0.000  1.00 10.00           C\n"
        "ATOM      2  CA  ALA A   2       1.000   1.000   1.000  1.00 20.00           C\n"
        "TER\nEND\n"
    )
    pdb_path = tmp_path / "model.pdb"
    pdb_path.write_text(pdb_content)
    obj = AlphaFoldPDB(pdb_path)
    obj.write_plddt_file()
    assert (tmp_path / "model_pLDDT.csv").exists()


def test_runner_directory(tmp_path):
    with open(tmp_path / "ranking_debug.json", "w") as fh:
        json.dump({"order": ["model_1"]}, fh)
    with open(tmp_path / "result_model_1.pkl", "wb") as fh:
        pickle.dump({"plddt": [10, 20]}, fh)
    runner = AlphaPickleRunner(n_jobs=1)
    runner.process_directory(tmp_path)
    assert (tmp_path / "ranked_1_pLDDT.csv").exists()
