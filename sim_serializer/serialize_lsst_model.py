#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Alexandre Boucaud <aboucaud@lal.in2p3.fr>

import argparse
from pathlib import Path

from validutils.io import save_compressed
from validutils.table import parse_lsst_model


def parse_args():

	parser = argparse.ArgumentParser("LSST supernovae simulations serializer")
	parser.add_argument('directory', type=str,
						help="Simulation directory (MODEL)")
	parser.add_argument('--destination', type=str, default='.',
						help="Path to the output files")
	parser.add_argument('--timed', action='store_true',
						help="Add a timer")

	return parser.parse_args()


def main():
	args = parse_args()

	if args.timed:
		import time
		start = time.time()

	dirpath = Path(args.directory)

	# Output directory
	outdir = Path(args.destination)
	if not outdir.exists():
		outdir.mkdir()

	# Use model directory as base name for the output file
	filename = "{}.pkl.gz".format(dirpath.name)
	outfile = outdir / filename

	table = parse_lsst_model(dirpath)
	save_compressed(table, outfile)

	print("SN data from {} saved to {}".format(dirpath.name, outfile))

	if args.timed:
		end = time.time()
		secs = end - start
		print("LSST light curves serialized in {:.1f} seconds".format(secs))


if __name__ == '__main__':
	main()
	
