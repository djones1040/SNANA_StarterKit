Installing SNANA
================

Below, I outline the steps to installing SNANA.
While SNANA will run on personal computers, please note
that a lot of SNANA functionality is enabled by using a
cluster environment with batch job submission.

For additional details, please see the SNANA installation
guide: http://snana.uchicago.edu/doc/snana_install.pdf

Installing on a Mac
-------------------
Installing on Linux is very similar, except for the
`preliminaries` stage.

Preliminaries
^^^^^^^^^^^^^
If you haven't already, start by installing command line
tools.  In terminal, type::

  xcode-select --install

Then, install homebrew by following the directions
at https://brew.sh/.  Once Homebrew is installed,
use the following commands to install dependencies
`GSL` and `cfitsio`::

  brew update
  brew install gsl
  brew install cfitsio

SNANA can optionally use ROOT or HBOOK for plotting
and some additional utilities.  From the SNANA
manual: go to http://root.cern.ch/ or pre-compiled libraries at
https://root.cern.ch/content/release-53434.
But, installing those is a bit harder so I won't try to
explain that here.

Setting Environment Variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
SNANA requires the following environment
variables to be set: :code:`CFITSIO_DIR`, :code:`GSL_DIR`,
and :code:`ROOT_DIR` (only if ROOT is installed).
:code:`SNANA_DIR` and :code:`SNDATA_ROOT` must also be defined.

As standard practice I first put the following lines
in my :code:`~/.bash_profile` file with a text editor::

  if [ -f $HOME/.bashrc ]; then
        source $HOME/.bashrc
  fi

Then, I set the environment variables by opening :code:`~/.bashrc`
in a text editor and adding the following lines::

  export SOFTDIR=/my/directory/path
  export GSL_DIR=/usr/local/Cellar/gsl/2.4
  export CFITSIO_DIR=/usr/local/Cellar/cfitsio/3.450_1
  export SNDATA_ROOT=$SOFTDIR/SNDATA_ROOT
  export SNANA_DIR=$SOFTDIR/SNANA
  
The exact path for :code:`GSL_DIR` and :code:`CFITSIO_DIR` will depend
on your system.  Usually Homebrew installs in :code:`/usr/local/Cellar`
and then you'll have to check out the subdirectory to
see where the GSL and CFITSIO files were actually put.
As the example above shows, it will depend which version
gets installed.

Once your :code:`~/.bashrc` file has been saved, run::
  
  source ~/.bashrc

or open up a new tab/window in terminal to set
the environment variables.

Downloading SNANA
^^^^^^^^^^^^^^^^^

SNANA comes in two tarballs - the source code and
the :code:`SNDATA_ROOT` compilation of various data files.
The SNANA source code can be cloned from git::

  mkdir $SNANA_DIR
  cd $SNANA_DIR
  git clone https://github.com/RickKessler/SNANA.git

The :code:`SNDATA_ROOT` tarball can be downloaded from
the SNANA website: http://snana.uchicago.edu/.
Or, at the command line::
  
  mkdir $SNDATA_ROOT
  cd $SNDATA_ROOT
  wget http://snana.uchicago.edu/downloads/SNDATA_ROOT.tar.gz
  tar -xvzf SNDATA_ROOT.tar.gz

  
Installing SNANA
^^^^^^^^^^^^^^^^

Installing SNANA on a Mac requires two small edits to :code:`$SNANA_DIR/src/sntools.h`.  However,
be warned that this could cause some ringing noise in spectral simulations due to a finite number
of randoms.  Unfortunately, I couldn't figure out another workaround here.  The following two
lines should be un-commented (remove the :code:`//` at the beginning of the lines)::

  //#define  ONE_RANDOM_STREAM  // enable this for Mac (D.Jones, July 2020)
  //#define  MACOS              // another MAC OS option, D.Jones, Sep 2020

Recently, there's one more hack needed in the Makefile.  If your Mac has GCC version 10.x, SNANA will read the version incorrectly.  That means you'll have to search for these lines::
  
  ifeq ($(GCCVERSION10),0)
    EXTRA_FLAGS_FORTRAN  = $(EXTRA_FLAGS)
    EXTRA_FLAGS_C        = $(EXTRA_FLAGS)
  else 
    # for gcc v10, allow argument-mismatch errors (9.2020)
    EXTRA_FLAGS_FORTRAN = $(EXTRA_FLAGS) -fallow-argument-mismatch -fcommon
    EXTRA_FLAGS_C       = $(EXTRA_FLAGS) -fcommon
  endif

and add the extra fortran flags to the first :code:`EXTRA_FLAGS` line, like so::

  ifeq ($(GCCVERSION10),0)
    EXTRA_FLAGS_FORTRAN  = $(EXTRA_FLAGS) -fallow-argument-mismatch -fcommon
    EXTRA_FLAGS_C        = $(EXTRA_FLAGS) -fcommon
  else 
    # for gcc v10, allow argument-mismatch errors (9.2020)
    EXTRA_FLAGS_FORTRAN = $(EXTRA_FLAGS) -fallow-argument-mismatch -fcommon
    EXTRA_FLAGS_C       = $(EXTRA_FLAGS) -fcommon
  endif
  
After that, installing should be as easy as::
  
  cd $SNANA_DIR/src
  make

Once it finishes, open your :code:`~/.bashrc` file again
and add the following line at the bottom::

  export PATH=$SNANA_DIR/bin:$PATH

and remember to type :code:`source ~/.bashrc` afterwards.
For the other exercises in this guide, check that :code:`kcor.exe`,
:code:`snlc_sim.exe` and :code:`snlc_fit.exe` have compiled correctly.
Hopefully you can reproduce the following lines.

For :code:`kcor.exe`::
  
  > kcor.exe
  SNANA_DIR   = /usr/local/SNANA
  SNDATA_ROOT = /usr/local/SNDATA_ROOT

  FATAL[rd_input]:
	 Cannot open input file :
	  'kcor.input'



   `|```````|`
   <| o\ /o |>
    | ' ; ' |
    |  ___  |     ABORT program on Fatal Error.
    | |' '| |
    | `---' |
    \_______/

For :code:`snlc_sim.exe`::
  
  > snlc_sim.exe

  ******************************************************************
   Begin execution of snlc_sim.exe
   Full command:

  SNDATA_ROOT = /usr/local/SNDATA_ROOT
  SNANA_DIR   = /usr/local/SNANA

  ########################################################
     INIT_SNVAR: Init variables.
  ########################################################

   HOST MACHINE =    ()
   SNDATA_ROOT = /usr/local/SNDATA_ROOT
   SNANA_DIR = /usr/local/SNANA    (v10_73j)
   Allocate 12.50 MB for CIDMASK array (to check duplicates)
   sizeof(INPUTS) =   1.001 MB
   sizeof(GENLC)  =   7.880 MB

  FATAL[read_input]:
	 Cannot open input file :
	  'snlc_sim.input'



   `|```````|`
   <| o\ /o |>
    | ' ; ' |
    |  ___  |     ABORT program on Fatal Error.
    | |' '| |
    | `---' |
    \_______/

And finally, for :code:`snlc_fit.exe`::

  > snlc_fit.exe

  ########################################################
     INIT_SNVAR: Init variables.
  ########################################################

   HOST MACHINE =    ()
   SNDATA_ROOT = /usr/local/SNDATA_ROOT
   SNANA_DIR = /usr/local/SNANA    (v10_73j)
   Allocate 12.50 MB for CIDMASK array (to check duplicates)

  ########################################################
     READ SNLCINP NAMELIST.
  ########################################################

    Enter namelist filename (CR=snlc_fit.nml) ==>
  
You're done!  Please report any issues with this
guide using the `SNANA_StarterKit GitHub page
<https://github.com/djones1040/SNANA_StarterKit/issues>`_.
