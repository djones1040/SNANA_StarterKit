"""
Additional utilities
"""
import pandas
import numpy as np

from .table import LSST_FILTERS


def dict2df(datadict):
    """
    Convert dictionary object to a DataFrame
    """
    for idx in datadict:
        sn = datadict[idx]
        for filt in LSST_FILTERS:
            sn['mjd_%s' % filt] = np.array(sn[filt]['mjd'])
            sn['fluxcal_%s' % filt] = np.array(sn[filt]['fluxcal'])
            sn['fluxcalerr_%s' % filt] = np.array(sn[filt]['fluxcalerr'])
            del sn[filt]
        sn.update(sn['header'])
        del sn['header']

    return pandas.DataFrame.from_dict(datadict, orient='index')
