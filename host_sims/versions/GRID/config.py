# configuration parameters for scripts

homedir = '/Users/jaredhand/WFIRST_research/SN_distributions/host_sims/versions/GRID/'  # working directory for scripts
init = 'JSH'  # initials that are tacked on hostlib file names
hostlibsuffix = '1KMS0_WFIRST' # add suffix to hostlib file name
massstep = '0.04'  # Mass step needs to be given as half of actual value.  Must be string.
wgtstep = 0.01  # side of weight map intervals
buff = 2.  # increase zone of excluded host mass values around transition zone
sampletype = 1  # 0: weight map dist, 1: normal dist centered at 10, 2: uniform dist with bounds of 7, 13, 3: mass=8,12
err = True  # If False, noiseerr is used for noise value in hostlib.  If True, noise is determined via errmaker.
noiseerr = 0.0  # Constant noise for observed mass data if err is False.
sample = 1000 # sample size used in combine scipts and hostlib generator.
oksurvs = ['SDSS', 'SNLS', 'PS1', 'LOWZ']  # list of valid survey names.  Must be upper case.
oksmear = ['G10', 'C11']  # list of valid smear models.
