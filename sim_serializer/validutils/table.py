"""
Parsers for astro tables
"""
from collections import defaultdict

from astropy.table import Table
import glob

def parse_phot_table(table, rows, filters=None):
	"""
	Retrieve filter information from the photometric file

	Parameters
	----------
	path : str
		path to LSST light curve file
	rows : slice
		range of rows for this SN

	Returns
	-------
	dict
		dictionary of filter data for the light curve

	"""
	fitstable = table[rows]

	data = {}

	for filt in filters:
		data[filt] = defaultdict(list)

	for row in fitstable:
		filt = row['FLT'].strip()
		if filt not in filters:
			continue
		data[filt]['mjd'].append(row['MJD'])
		data[filt]['fluxcal'].append(row['FLUXCAL'])
		data[filt]['fluxcalerr'].append(row['FLUXCALERR'])
#		data[filt]['snrmag20'].append(row['SIM_SNRMAG20'])
		
	return data


def parse_header_table(table, index=0, filters=None):
	"""
	Retrieve metadata from header file

	Parameters
	----------
	path : str
		Pointer to the header FITS file
	index : int, optional
		Row number in the header table (default is 0)
		Corresponds to the SN id in this exposure.

	Returns
	-------
	header : dict
		stripped version of the header
	rows : slice
		range of rows in the corresponding PHOT file
	istarget : bool
		boolean flag to distinguish between train/test sample

	"""
	head = table[index]

	header = {}
	# SN ID
#	import pdb; pdb.set_trace()
	header['snid'] = int(head['SNID'])
	# Redshift
	header['z'] = head['SIM_REDSHIFT_HOST']
	# Type
	header['type'] = head['SIM_TYPE_INDEX']
	# Peak MJD
	header['pkmjd'] = head['SIM_PEAKMJD']
	# Peak magnitudes
	for filt in filters:
		header['pkmag_%s' % filt] = head['SIM_PEAKMAG_%s' % filt]

	# Add all the SIM_ info for validation purposes
	simkeys = [colname
			   for colname in head.colnames
			   if colname.startswith("SIM_")]
	for key in simkeys:
		header[key] = head[key]

	# Corresponding rows in the photometric file
	rows = slice(head['PTROBS_MIN'] - 1, head['PTROBS_MAX'] - 1)

	return header, rows


def parse_model(dirpath):
	"""
	Parse all files in the provided directory and save relevant
	information in a dictionary saved back to disk (and compressed)

	Parameters
	----------
	dirpath : Path
		path to a LSST simulated FITS directory
	destination : str
		path to save the output files
	save : bool, optional
		save the result into a compressed pickle file (default is False)

	Returns
	-------
	dataframe or tuple of dataframes

	"""
	# get the filters
	README_FILE = glob.glob('%s/*README'%dirpath)
	if not len(README_FILE):
		raise RuntimeError('README file doesn\'t exist in %s'%dirpath)
	README_FILE = README_FILE[0]
	
	with open(README_FILE) as fin:
		for line in fin:
			if 'Generation FILTERS:' in line:
				filters = line.split()[-1]
				break

	# List all header files in the given directory
	header_files = glob.glob('%s/*HEAD.FITS*'%dirpath)

	datadict = {}
	for hfile in header_files:
		#as_posix()
		pfile = hfile.replace('HEAD', 'PHOT')
		htable = Table.read(hfile, format='fits')
		ptable = Table.read(pfile, format='fits')
		for idx in range(len(htable)):
			header, rows = parse_header_table(htable, idx, filters=filters)
			data = parse_phot_table(ptable, rows, filters=filters)
			# Add the header info to the light curve data
			data['header'] = header
			# Use the SN id to index the dictionary
			datadict[header['snid']] = data

	return datadict
