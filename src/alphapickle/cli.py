"""Command line interfaces for AlphaPickle."""
from __future__ import annotations

import argparse
from typing import Sequence
from pathlib import Path

from alphapickle import AlphaPickleRunner

BANNER = r"""
    _       _             ____ ___ ____ _  ___     _____
   __ _| |_ __ | |__   __ _  |  _ \_ _/ ___| |/ / |   | ____|
  / _` | | '_ \| '_ \ / _` | | |_) | | |   | ' /| |   |  _|
 | (_| | | |_) | | | | (_| | |  __/| | |___| . \| |___| |___
  \__,_|_| .__/|_| |_|\__,_| |_|  |___\____|_|\_\_____|_____|
         |_|"""

def af2(argv: Sequence[str] | None = None) -> None:
    """Process an AlphaFold2 output directory.

    Parameters
    ----------
    argv : Sequence[str] | None
        Command line arguments. If ``None`` (default) uses :data:`sys.argv`.
    """
    parser = argparse.ArgumentParser(
        description=(
            "AlphaPickle\n"
            "Process an AlphaFold output directory and generate plots and CSV files."
        )
    )
    parser.add_argument(
        "-od", "--output_directory", required=True, help="Path to AlphaFold output directory"
    )
    parser.add_argument(
        "-ps",
        "--plot_size",
        type=float,
        default=12,
        help="Change size (in inches) of plots (default: 12).",
    )
    parser.add_argument(
        "-pi",
        "--plot_increment",
        type=int,
        default=100,
        help=(
            "Change the increment of plot axis labels using residue numbering (default: 100)."
        ),
    )
    parser.add_argument(
        "-ff",
        "--fasta_file",
        default=None,
        help="Optional: fasta sequence file used for AlphaFold prediction.",
    )
    args = parser.parse_args(argv)

    print(BANNER)

    runner = AlphaPickleRunner(
        fasta_file=args.fasta_file,
        plot_size=args.plot_size,
        axis_label_increment=args.plot_increment,
    )
    runner.process_directory(Path(args.output_directory))
    print("Processing complete!")
    print("Data saved to output directory")
    print(
        "If you use AlphaPickle in your work (during analysis, or for plots that end up in publications), "
        "please cite AlphaPickle as follows: Arnold, M. J. (2021) AlphaPickle doi.org/10.5281/zenodo.5708709"
    )
