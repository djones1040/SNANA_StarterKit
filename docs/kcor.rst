Using Filter Functions to Make a KCOR file
==========================================

One of the slightly peculiar things about SNANA
is the so-called :code:`KCOR` file.  In spite
of the name, this file usually does *not* contain
k-corrections!  Instead, it takes filter throughputs,
combines them with user-defined filter shifts and zeropoint offsets,
and creates an output FITS file that is used by
the SNANA fitting and simulations programs.

The KCOR input file
-------------------
For creating a new KCOR file, you need
to create an INPUT file.  I'll use the Pan-STARRS
filter set to create a kcor file for fitting or
simulating Pan-STARRS observations.  Let's name
this file :code:`kcor_PS1.input`::

  MAGSYSTEM:  AB
  FILTSYSTEM: COUNT
  FILTPATH: $SNDATA_ROOT/filters/PS1/Pantheon/PS1
  FILTER: PS1-g   g_filt_tonry.txt   0.0
  FILTER: PS1-r   r_filt_tonry.txt   0.0
  FILTER: PS1-i   i_filt_tonry.txt   0.0
  FILTER: PS1-z   z_filt_tonry.txt   0.0
  FILTER: PS1-y   y_filt_tonry.txt   0.0

  OUTFILE:  kcor_PS1.fits

The input file can get *a lot* more complicated,
but this gives the basics.  First, :code:`magsystem`
is set to :code:`AB`, :code:`VEGA`, or :code:`BD17`,
for example.  For multiple magsystems, one simply
has to split the filters into multiple blocks like
so::

  MAGSYSTEM:  AB
  FILTSYSTEM: COUNT
  FILTPATH: $SNDATA_ROOT/filters/PS1/Pantheon/PS1
  FILTER: PS1-g   g_filt_tonry.txt   0.0
  FILTER: PS1-r   r_filt_tonry.txt   0.0

  MAGSYSTEM:  BD17
  FILTSYSTEM: COUNT
  FILTPATH: $SNDATA_ROOT/filters/PS1/Pantheon/CFA3_native
  FILTER:  CFA41-U/k            cfa4_U_p1.dat  9.724
  FILTER:  CFA41-B/l            cfa4_B_p1.dat  9.88605-0.024
  FILTER:  CFA41-V/m            cfa4_V_p1.dat  9.47432-0.0012
  
The final column here defines a zeropoint offset
(these lines are specifically from the `Pantheon sample
<http://adsabs.harvard.edu/abs/2018ApJ...859..101S>`_,
and the final term is the "Supercal" offset and is subtracted from
the nominal zeropoint).  Specifically, this number is
the magnitude of BD17 in the Vega system, so these are
effectively Vega magnitudes.

The :code:`FILTER` lines give first a longer filter name
and then after the :code:`/`, a one-letter abbreviation
for the filter.  These have to be unique (unfortunately)
so you might end up with counterintuitive names for your
filters if you have a survey with many different filters.
The next column is just the name of the filter file.

The last thing is the output file, which is
fairly self-explanatory::

  OUTFILE:  kcor_PS1.fits

Using :code:`kcor.exe` to create the KCOR file
----------------------------------------------

Finally, to create the file::
  
  > kcor.exe kcor_PS1.input

After running this, you should see the output FITS file.
This file will be referenced in your simulation and LC fitting
input files.
