"""Core utilities for working with AlphaFold metadata."""
from __future__ import annotations

from pathlib import Path
import json
import pickle

import numpy as np
import pandas as pd
from Bio import PDB
from matplotlib import pyplot as plt, colors


class AlphaFoldMetaData:
    """Base container for AlphaFold metadata."""

    def __init__(self, path: str | Path, fasta: str | None = None, ranking: str | None = None) -> None:
        self.path = Path(path)
        self.fasta = fasta
        self.saving_filename = f"ranked_{ranking}" if ranking else self.path.stem
        self.saving_pathname = str(self.path.parent)
        self.pLDDT: np.ndarray | None = None
        self.PAE: np.ndarray | None = None

    # plotting functions
    def plot_plddt(self, size_in_inches: float = 12, axis_label_increment: int = 100) -> Path:
        """Plot per-residue confidence values."""
        if self.pLDDT is None:
            raise ValueError("pLDDT data not loaded")
        x = np.arange(len(self.pLDDT))
        cmap = colors.LinearSegmentedColormap.from_list("", ["red", "orange", "yellow", "cornflowerblue", "blue"])
        plt.figure(figsize=(size_in_inches, size_in_inches / 2))
        plt.scatter(x, self.pLDDT, c=self.pLDDT, cmap=cmap, s=5)
        plt.clim(0, 100)
        ticks = np.arange(0, len(self.pLDDT), axis_label_increment)
        plt.xticks(ticks, fontname="Helvetica")
        plt.yticks(fontname="Helvetica")
        plt.xlabel("Residue index", size=14, fontweight="bold", fontname="Helvetica")
        plt.ylabel("Predicted LDDT", size=14, fontweight="bold", fontname="Helvetica")
        scale = plt.colorbar(shrink=0.5)
        scale.set_label(label="Predicted LDDT", size=12, fontweight="bold", fontname="Helvetica")
        outfile = Path(self.saving_pathname) / f"{self.saving_filename}_pLDDT.png"
        plt.savefig(outfile, dpi=300)
        plt.close()
        return outfile

    def plot_pae(self, size_in_inches: float = 12, axis_label_increment: int = 100) -> Path:
        """Plot predicted aligned error."""
        if self.PAE is None:
            raise ValueError("PAE data not loaded")
        plt.figure(figsize=(size_in_inches, size_in_inches))
        im = plt.imshow(self.PAE)
        ticks = np.arange(0, self.PAE.shape[0], axis_label_increment)
        plt.xticks(ticks, fontname="Helvetica")
        plt.yticks(ticks, fontname="Helvetica")
        plt.xlabel("Residue index", size=14, fontweight="bold", fontname="Helvetica")
        plt.ylabel("Residue index", size=14, fontweight="bold", fontname="Helvetica")
        scale = plt.colorbar(im, shrink=0.5)
        scale.set_label(label="Predicted error (Å)", size=12, fontweight="bold", fontname="Helvetica")
        outfile = Path(self.saving_pathname) / f"{self.saving_filename}_PAE.png"
        plt.savefig(outfile, dpi=300)
        plt.close()
        pd.DataFrame(self.PAE).to_csv(Path(self.saving_pathname) / f"{self.saving_filename}_PAE.csv")
        return outfile

    def write_plddt_file(self) -> Path:
        """Write pLDDT values to CSV."""
        if self.pLDDT is None:
            raise ValueError("pLDDT data not loaded")
        outfile = Path(self.saving_pathname) / f"{self.saving_filename}_pLDDT.csv"
        pd.DataFrame({"pLDDT": self.pLDDT}).to_csv(outfile, index=False)
        return outfile


class AlphaFoldPickle(AlphaFoldMetaData):
    """Loader for pickled AlphaFold outputs."""

    def __init__(self, path: str | Path, fasta: str | None = None, ranking: str | None = None) -> None:
        super().__init__(path, fasta, ranking)
        with open(self.path, "rb") as fh:
            data: list[dict] = []
            while True:
                try:
                    data.append(pickle.load(fh))
                except EOFError:
                    break
        self.data = data
        self.PAE = np.asarray(data[0].get("predicted_aligned_error")) if data[0].get("predicted_aligned_error") is not None else None
        self.pLDDT = np.asarray(data[0]["plddt"])


class AlphaFoldJson:
    """Utility for reading ranking_debug.json files."""

    def __init__(self, directory: str | Path) -> None:
        directory = Path(directory)
        with open(directory / "ranking_debug.json") as fh:
            raw = json.load(fh)
        self.ranking: list[tuple[int, str]] = list(enumerate(raw["order"], start=1))


class AlphaFoldPDB(AlphaFoldMetaData):
    """Extract pLDDT values from AlphaFold-generated PDB files."""

    def __init__(self, path: str | Path, fasta: str | None = None, ranking: str | None = None) -> None:
        super().__init__(path, fasta, ranking)
        parser = PDB.PDBParser(QUIET=True)
        structure = parser.get_structure("model", str(self.path))
        plddt: list[float] = []
        for residue in structure.get_residues():
            atom = next(residue.get_atoms())
            plddt.append(float(atom.bfactor))
        self.pLDDT = np.asarray(plddt)
        self.data = []
        self.PAE = None


class AlphaFoldPAEJson(AlphaFoldMetaData):
    """Extract PAE values from ColabFold-style JSON files."""

    def __init__(self, path: str | Path, fasta: str | None = None, ranking: str | None = None) -> None:
        super().__init__(path, fasta, ranking)
        self.PAE = self._extract_pae_from_json(path)
        self.pLDDT = None

    @staticmethod
    def _extract_pae_from_json(path: str | Path) -> np.ndarray:
        with open(path) as fh:
            data = json.load(fh)
        if isinstance(data, list):
            data = data[0]
        if "predicted_aligned_error" in data:
            return np.asarray(data["predicted_aligned_error"])
        residue1 = data["residue1"]
        residue2 = data["residue2"]
        pae = data["distance"]
        arr = np.ones((max(residue1), max(residue2)))
        for i, j, val in zip(residue1, residue2, pae):
            arr[int(i - 1), int(j - 1)] = val
        return arr

