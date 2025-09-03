import tarfile
from urllib.request import urlretrieve

import pytest

DATA_URL = "https://github.com/YaoYinYing/alphapickle/releases/download/test_data/S4_nosig_AF2_full.tar.bz2"


@pytest.fixture(scope="session")
def example_data_dir(tmp_path_factory):
    """Download and extract the external AlphaFold example dataset."""
    data_root = tmp_path_factory.mktemp("alphafold_data")
    archive = data_root / "S4_nosig_AF2_full.tar.bz2"
    urlretrieve(DATA_URL, archive)
    with tarfile.open(archive, "r:bz2") as tar:
        tar.extractall(path=data_root)
    return data_root / "S4_nosig"


def pytest_configure(config):
    config.addinivalue_line("markers", "serial: mark test as running serially")


def pytest_collection_modifyitems(config, items):
    if config.pluginmanager.hasplugin("xdist"):
        for item in items:
            if "serial" in item.keywords:
                item.add_marker(pytest.mark.xdist_group("serial"))
