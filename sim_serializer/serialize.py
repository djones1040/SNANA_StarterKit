#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Alexandre Boucaud <aboucaud@lal.in2p3.fr>
# Modified by D. Jones

import argparse
from pathlib import Path
import os

from .validutils.io import save_compressed
from .validutils.table import parse_model

def main(simname,outfile_root=None,dirpath='$SNDATA_ROOT/SIM',
		 verbose=False):

	if not outfile_root:
		outfile_root = simname
	
	# Use model directory as base name for the output file
	filename = "{}.pkl.gz".format(outfile_root)
	dirpath = os.path.expandvars('%s/%s'%(dirpath,simname))
	
	table = parse_model(dirpath)
	save_compressed(table, filename)

	if verbose:
		print("SN data from {} saved to {}".format(dirpath.name, filename))

	return table
		
if __name__ == '__main__':
	main()
	
