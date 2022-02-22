### AlphaPickle ###
### Version 1.5.0 ###
### Author: Matt Arnold ###
# AlphaPickle extracts results metadata from pickle (.pkl) files created by DeepMind's AlphaFold (Jumper et al., 2021, doi: 10.1038/s41586-021-03819-2)
# For detailed usage and installation instructions, please consult README.alphapickle
# New in this version: bug fix @ AlphaPickle.py-line163

# Copyright (C) 2021  Matt Arnold

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import src.AlphaPickle as ap
import argparse
import numpy as np
from sys import exit

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="AlphaPickle\n"
    "Version 1.5.0\n"
    "Input an AlphaFold result_model_x.pkl metadata file, or a PDB file generated by AlphaFold (for pLDDT plotting), or \n "
    "a PAE JSON file of the type generated by the DeepMind Colab notebook (for PAE plotting) \n"
    "or a directory containing all output models and a ranking_debug.json file and generate \n"
    "a PAE plot (if pTM models were used), a pLDDT plot and a ChimeraX attribute file \n"
    "containing pLDDT data. Both of these metrics are also exported to \n"
    "csv files. All outputs save to the  directory containing the input files.\n"
    "Copyright (C) 2021  Matt Arnold")
    parser.add_argument("-od","--output_directory", help='Path to AlphaFold output directory', default=None)
    parser.add_argument("-pf","--pickle_file", help='Filename of metadata file for processing.', default=None)
    parser.add_argument("-ff","--fasta_file", help='Optional. Filename of fasta sequence file used for AlphaFold prediction.', default=None)
    parser.add_argument("-pdb","--pdb_file", help='Optional. Provide the absolute file path of an AlphaFold PDB file (v2.0.1 or later) to produce a pLDDT plot fomr the b-factor column', default=None)
    parser.add_argument("-json", "--pae_json_file", help='Optional. Provide a json file containing PAE values, of the type produced by the DeepMind AlphaFold colab notebook', default=None)
    parser.add_argument("-ps","--plot_size", help='Optional (Default = 12). Change size (in inches) of plots. This may be useful for very short or long input sequences', default=12)
    parser.add_argument("-pi","--plot_increment", help='Optional (Default = 100). Change the increment of plot axis labels using residue numbering. This may be useful for very short or long input sequences', default=100)
    args = parser.parse_args()

    print("""
        _       _             ____ ___ ____ _  ___     _____ 
   __ _| |_ __ | |__   __ _  |  _ \_ _/ ___| |/ / |   | ____|
  / _` | | '_ \| '_ \ / _` | | |_) | | |   | ' /| |   |  _|  
 | (_| | | |_) | | | | (_| | |  __/| | |___| . \| |___| |___ 
  \__,_|_| .__/|_| |_|\__,_| |_|  |___\____|_|\_\_____|_____|
         |_|                                                 
                                 
    """)


    if args.pickle_file and not args.output_directory and not args.pdb_file:
        print("Processing 1 metadata file {}".format(args.pickle_file))
        print("\n")
        results = ap.AlphaFoldPickle(args.pickle_file,args.fasta_file)
        results.write_pLDDT_file()
        results.plot_pLDDT(size_in_inches=args.plot_size, axis_label_increment=args.plot_increment)
        if type(results.PAE) == np.ndarray:
            results.plot_PAE(size_in_inches=args.plot_size, axis_label_increment=args.plot_increment)
    
    if args.output_directory and not args.pickle_file and not args.pdb_file:
        rankings = ap.AlphaFoldJson(args.output_directory).RankingDebug
        print("Batch processing {} ranked models, based on {}/ranking_debug.json".format(len(rankings),args.output_directory))
        print("\n")
        for model in rankings:
            print("Processing ranked model {} (result_{}).".format(str(model[0]),model[1]))
            results = ap.AlphaFoldPickle(args.output_directory + "/result_" + model[1] + ".pkl", ranking=str(model[0]))
            results.write_pLDDT_file()
            results.plot_pLDDT(size_in_inches=args.plot_size, axis_label_increment=args.plot_increment)
            if type(results.PAE) == np.ndarray:
                results.plot_PAE(size_in_inches=args.plot_size, axis_label_increment=args.plot_increment)
            print("\n")

    if args.pdb_file and not args.pickle_file and not args.output_directory:
        results = ap.AlphaFoldPDB(args.pdb_file)
        results.plot_pLDDT(size_in_inches=args.plot_size, axis_label_increment=args.plot_increment)
    
    if args.pae_json_file and not args.pickle_file and not args.output_directory:
        results = ap.AlphaFoldPAEJson(args.pae_json_file)
        results.plot_PAE(size_in_inches=args.plot_size, axis_label_increment=args.plot_increment)

    else:
        exit("Incorrect combination of files provided. Please check inputs contain exactly one of pickle_file and output_directory")

    print("Processing complete!")
    print("Data saved to output directory")
    print("If you use AlphaPickle in your work (during analysis, or for plots that end up in publications), please cite AlphaPickle as follows: Arnold, M. J. (2021) AlphaPickle doi.org/10.5281/zenodo.5708709")