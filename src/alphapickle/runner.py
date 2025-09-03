"""High level runner for AlphaPickle workflows."""
from __future__ import annotations

from pathlib import Path

import numpy as np
from joblib import Parallel, delayed

from alphapickle.metadata import (
    AlphaFoldJson,
    AlphaFoldPAEJson,
    AlphaFoldPDB,
    AlphaFoldPickle,
)


class AlphaPickleRunner:
    """Convenience interface for processing AlphaFold outputs."""

    def __init__(
        self,
        fasta_file: str | None = None,
        plot_size: float = 12,
        axis_label_increment: int = 100,
        n_jobs: int = 1,
    ) -> None:
        """Configure default plotting options and threading behavior."""
        self.fasta_file = fasta_file
        self.plot_size = plot_size
        self.axis_label_increment = axis_label_increment
        self.n_jobs = n_jobs

    def process_pickle(self, pickle_file: str | Path, ranking: int | None = None) -> AlphaFoldPickle:
        """Process a single AlphaFold pickle output file."""
        obj = AlphaFoldPickle(pickle_file, self.fasta_file, ranking=str(ranking) if ranking else None)
        obj.write_plddt_file()
        obj.plot_plddt(self.plot_size, self.axis_label_increment)
        if isinstance(obj.PAE, np.ndarray):
            obj.plot_pae(self.plot_size, self.axis_label_increment)
        return obj

    def process_directory(self, directory: str | Path) -> list[AlphaFoldPickle]:
        """Batch process all ranking results in a directory."""
        directory = Path(directory)
        rankings = AlphaFoldJson(directory).ranking
        return Parallel(n_jobs=self.n_jobs)(
            delayed(self.process_pickle)(
                directory / f"result_{model_name}.pkl", ranking=rank
            )
            for rank, model_name in rankings
        )

    def process_pdb(self, pdb_file: str | Path) -> AlphaFoldPDB:
        """Extract and plot pLDDT values from a PDB file."""
        obj = AlphaFoldPDB(pdb_file, self.fasta_file)
        obj.write_plddt_file()
        obj.plot_plddt(self.plot_size, self.axis_label_increment)
        return obj

    def process_pae_json(self, json_file: str | Path) -> AlphaFoldPAEJson:
        """Plot PAE values from a ColabFold-style JSON file."""
        obj = AlphaFoldPAEJson(json_file)
        obj.plot_pae(self.plot_size, self.axis_label_increment)
        return obj

