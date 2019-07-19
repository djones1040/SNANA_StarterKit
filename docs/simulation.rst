Running a Simple Simulation
===========================

SNANA is an extremely powerful tool for survey
simulations, and can simulate nearly every aspect
of a survey, at least on the catalogue level (not
pixel level) that I can think of.

From Kessler et al. (2019), here's a basic schematic
of the SNANA simulation framework.

.. image:: _static/SNANA_schematic.png

Building a SNANA simulation requires at minimum,
four principal files: the `KCOR file <kcor.html>`__,
the :code:`SIMLIB` file, which contains the
sequence of observations to simulate, the :code:`SEARCHEFF`
file that gives the efficiency of SN detection, and finally
the sim-input file which is passed to the simulation
program, `snlc_sim.exe`.
	   
Writing a Simple SIMLIB File
----------------------------

The SIMLIB file defines the parameters of the survey
observations.  At minimum, this requires a list of MJDs,
filters, sky noise, and image zeropoints.  Here is a brief
example for the Pan-STARRS medium deep survey::

  TELESCOPE: PS1
  SURVEY: PS1MD    FILTERS: griz

  BEGIN LIBGEN  2016-3-28
  # --------------------------------------------
  LIBID: 1
  RA: 0    DECL: 0 NOBS: 6 MWEBV: 0.024   PIXSIZE: 0.25
  FIELD: 1
  #                           CCD  CCD         PSF1 PSF2 PSF2/1
  #     MJD      IDEXPT  FLT GAIN NOISE SKYSIG (pixels)  RATIO  ZPTAVG ZPTERR  MAG
  S: 55074.600 0 g 1.0 0.0 6.8691 3.7960 0.0000 0.0000 30.2426 0.0034 -99
  S: 55086.600 1 g 1.0 0.0 10.319 4.4315 0.0000 0.0000 30.1481 0.0034 -99
  S: 55089.600 2 g 1.0 0.0 6.8671 2.8140 0.0000 0.0000 30.2175 0.0036 -99
  S: 55095.500 3 g 1.0 0.0 7.2529 3.9464 0.0000 0.0000 30.3894 0.0041 -99
  S: 55098.500 4 g 1.0 0.0 6.8112 3.3349 0.0000 0.0000 30.1146 0.0040 -99
  S: 55101.600 5 g 1.0 0.0 7.4172 3.1407 0.0000 0.0000 30.1131 0.0037 -99
  END_LIBID: 1
  END_OF_SIMLIB: 1 ENTRIES

The basic syntax here is a short header, where the
:code:`TELESCOPE` and :code:`SURVEY` keys shouldn't have
any impact on the simulated outputs and :code:`FILTERS` is
just the list of one-letter filter names (specified in your
`KCOR file <kcor.html>`__).

Next, there are a couple lines that specify different "libraries" with
the :code:`LIBID` key.  In this case, :code:`LIBID` or :code:`FIELD`
can serve to separate the simulation into distinct groups where simulated
supernovae do not overlap.

The keys :code:`RA`, :code:`DEC`, :code:`NOBS`, :code:`MWEBV`, and
:code:`PIXSIZE` are right ascension, declination, number of
observations, Milky Way E(B-V), and the pixel size of the detector.
In particular, the pixel size of the detector is important for
generating simulations with realistic noise properties.

Now, the observation lines::

  #                           CCD  CCD         PSF1 PSF2 PSF2/1
  #     MJD      IDEXPT  FLT GAIN NOISE SKYSIG (pixels)  RATIO  ZPTAVG ZPTERR  MAG
  S: 55074.600 0 g 1.0 0.0 6.8691 3.7960 0.0000 0.0000 30.2426 0.0034 -99

In order, these fields are the observed MJD, an integer label for
the observation number, the filter, the gain, the CCD noise (I think
this is read noise?) and the RMS of the sky measurements.  Next,
three parameters of the PSF, which are spread in X, spread in Y, and the
ratio of the two.  Those second parameters can be set to 0 and
SNANA will assume a spherically symmetric PSF.

:code:`ZPTAVG` is the image zeropoint and the `ZPTERR` will be
propagated to the observational uncertainties.  :code:`MAG` should
be set to -99 or else SNANA will simulate *only* those specific magnitudes on
a given date.

The Search-Efficiency File
--------------------------

The search-efficiency file defines the probability of detecting a source
as a function of magnitude.  This file is a essentially a two-column
list for one or multiple filters that gives a magnitude and a
probability of detection.  Here's an example::

  PHOTFLAG_DETECT: 4096
  FILTER: g
  SNR:  0.500  0.001
  SNR:  1.500  0.004
  SNR:  2.500  0.028
  SNR:  3.500  0.189
  SNR:  4.500  0.428
  SNR:  5.500  0.644
  SNR:  6.500  0.796
  SNR:  7.500  0.841
  SNR:  8.500  0.949
  SNR:  9.500  0.861
  SNR:  10.500  0.936
  SNR:  11.500  0.956
  SNR:  12.500  0.952
  SNR:  13.500  0.920
  SNR:  14.500  1.000
  SNR:  15.500  1.000
  SNR:  16.500  0.857
  SNR:  17.500  0.933
  SNR:  18.500  1.000
  SNR:  19.500  1.000
  FILTER: r
  SNR:  0.500  0.001
  SNR:  1.500  0.004
  SNR:  2.500  0.025
  SNR:  3.500  0.177
  SNR:  4.500  0.423
  SNR:  5.500  0.593
  SNR:  6.500  0.693
  SNR:  7.500  0.769
  SNR:  8.500  0.878
  SNR:  9.500  0.850
  SNR:  10.500  0.900
  SNR:  11.500  0.871
  SNR:  12.500  0.849
  SNR:  13.500  0.915
  SNR:  14.500  0.969
  SNR:  15.500  0.860
  SNR:  16.500  0.889
  SNR:  17.500  0.952
  SNR:  18.500  0.864
  SNR:  19.500  0.955

:code:`PHOTFLAG_DETECT` is just a value that is added to the simulated
data file to indicate whether or not a given epoch was high enough
SNR to be "detected" in the simulation.

The Sim-Input File
------------------

Finally, the input file!

Running the Simulation
----------------------

Examining the Output
--------------------
