import sncosmo
import os
from astropy.io import fits
import warnings
import numpy as np
import astropy.units as u
ignorelist = ['filtwave','primarywave','snflux','AB','Vega','VEGA','BD17']

def from_kcor(kcorfile):

	bandpassdict = rdkcor(kcorfile)
	
	bandlist = []
	for k in bandpassdict.keys():
		if k not in ignorelist:
			band = sncosmo.Bandpass(
				bandpassdict['filtwave'],
				bandpassdict[k]['filttrans'],
				wave_unit=u.angstrom,name=k)
			sncosmo.register(band, k, force=True)

def rdkcor(kcorfile):

	kcordict = {}
	kcorfile = os.path.expandvars(kcorfile)
	if not os.path.exists(kcorfile):
		raise RuntimeError('kcor file %s does not exist'%kcorfile)	
		
	with warnings.catch_warnings():
		warnings.simplefilter("ignore")
		try:
			hdu = fits.open(kcorfile)
			zpoff = hdu[1].data
			snsed = hdu[2].data
			filtertrans = hdu[5].data
			primarysed = hdu[6].data
			hdu.close()
		except:
			raise RuntimeError('kcor file format is non-standard for kcor file %s'%kcorfile)

	kcordict['filtwave'] = filtertrans['wavelength (A)']
	kcordict['primarywave'] = primarysed['wavelength (A)']
	kcordict['snflux'] = snsed['SN Flux (erg/s/cm^2/A)']
	
	if 'AB' in primarysed.names:
		kcordict['AB'] = primarysed['AB']
	if 'Vega' in primarysed.names:
		kcordict['Vega'] = primarysed['Vega']
	if 'VEGA' in primarysed.names:
		kcordict['Vega'] = primarysed['VEGA']
	if 'BD17' in primarysed.names:
		kcordict['BD17'] = primarysed['BD17']
	for filt in zpoff['Filter Name']:
		kcordict[filt.split('-')[-1].split('/')[-1]] = {}
		kcordict[filt.split('-')[-1].split('/')[-1]]['fullname'] = filt.split('/')[0][1:]
		kcordict[filt.split('-')[-1].split('/')[-1]]['filttrans'] = filtertrans[filt]
		lambdaeff = np.sum(kcordict['filtwave']*filtertrans[filt])/np.sum(filtertrans[filt])
		kcordict[filt.split('-')[-1].split('/')[-1]]['lambdaeff'] = lambdaeff
		kcordict[filt.split('-')[-1].split('/')[-1]]['zpoff'] = \
			zpoff['ZPOff(Primary)'][zpoff['Filter Name'] == filt][0]
		kcordict[filt.split('-')[-1].split('/')[-1]]['magsys'] = \
			zpoff['Primary Name'][zpoff['Filter Name'] == filt][0]
		kcordict[filt.split('-')[-1].split('/')[-1]]['primarymag'] = \
			zpoff['Primary Mag'][zpoff['Filter Name'] == filt][0]

	return kcordict
