import numpy as np
import os
import scipy.interpolate as interp
import sys
from config import *

# set random seed:
np.random.seed(seed=12345)

# G10 high-z values
cp0 = [-0.054, 0.101, 0.043]  # cbar, csigpos, csigneg
x1p0 = [0.973, 0.222, 1.472]  # x1bar, x1sigpos, s1signeg

# G10 SDSS values
cp1 = [-0.038, 0.079, 0.048]
x1p1 = [1.141, 0.100, 1.653]

# G10 PS1 values:
cp2 = [-0.077, 0.121, 0.029]
x1p2 = [0.514, 0.37, 0.963

# G10 SNLS values:
cp3 = [-0.077, 0.121, 0.029]
x1p3 = [0.964, 0.282, 1.232]

# important things?
C = 1 / (2 * np.pi)

class SurvError(Exception):
    # exception raised if survey id given as sys argv[1] is not in oksurvs
    def __init__(self, message):
        self.message = message


class IterError(Exception):
    # exception raised if specified iteration step is not 0. 1, 2, or 3
    def __init__(self, message):
        self.message = message

class SmearError(Exception):
    # exception raised if smear model is not C11 or G10
    def __init__(self, message):
        self.message = message


surv = sys.argv[1]
smeararg = sys.argv[3]
# check smear model and survey name
if surv not in oksurvs:
    raise SurvError('Survey ID not valid.')
if smeararg not in oksmear:
    raise SmearError('Smear model not valid.')
cidlist = [1, 4, 15, 999]  # cids for sdss, snls, ps1.  999 is for lowz cids
ciddict = dict(zip(oksurvs, cidlist))
os.chdir(homedir + '/fitres/{}'.format(surv))

# sim1 results
columns = tuple(list(range(1, 4)) + list(range(5, 39)))
fitres = '{}_WFIRST_{}1.fitres'.format(init, surv)
try:
    with open(fitres, 'r') as f:
        for line in f:
            if 'VARNAME' in line:
                var = line
                break
    with open(fitres, 'r') as f:
        for line in f:
            if 'NVAR' in line:
                varscount = int(line.split(' ')[1]) - 2
                break
    var = var.split()
    var.remove('VARNAMES:')
    var.remove('FIELD')
    datasim1 = np.loadtxt(fitres, dtype=float, skiprows=12, usecols=columns)
    for i in range(varscount):
        if var[i] == 'HOST_LOGMASS':
            sim1mass = np.copy(datasim1[:, i])
        elif var[i] == 'x1':
            sim1x1 = np.copy(datasim1[:, i])
        elif var[i] == 'c':
            sim1c = np.copy(datasim1[:, i])
except ValueError:
    print('ValueError raised.')
    print('Warning: Fitres iteration 1 not imported.  Directory given: ' + os.getcwd() + '.  File given: ' + fitres + '.')
    pass
except FileNotFoundError:
    print('FileNotFoundError raised.')
    print('Warning: Fitres iteration 1 not imported.  Directory given: ' + os.getcwd() + '.  File given: ' + fitres + '.')
    pass
except:
    raise

# sim2 results
fitres = '{}_WFIRST_{}2.fitres'.format(init, surv)
try:
    with open(fitres, 'r') as f:
        for line in f:
            if 'VARNAME' in line:
                var = line
                break
    with open(fitres, 'r') as f:
        for line in f:
            if 'NVAR' in line:
                varscount = int(line.split(' ')[1]) - 2
                break
    var = var.split()
    var.remove('VARNAMES:')
    var.remove('FIELD')
    datasim2 = np.loadtxt(fitres, dtype=float, skiprows=12, usecols=columns)
    for i in range(varscount):
        if var[i] == 'HOST_LOGMASS':
            sim2mass = np.copy(datasim2[:, i])
        elif var[i] == 'x1':
            sim2x1 = np.copy(datasim2[:, i])
        elif var[i] == 'c':
            sim2c = np.copy(datasim2[:, i])
except ValueError:
    print('ValueError raised.')
    print('Warning: Fitres iteration 2 not imported.  Directory given: ' + os.getcwd() + '.  File given: ' + fitres + '.')
    pass
except FileNotFoundError:
    print('FileNotFoundError raised.')
    print('Warning: Fitres iteration 2 not imported.  Directory given: ' + os.getcwd() + '.  File given: ' + fitres + '.')
    pass
except:
    raise

# sim3 results
fitres = '{}_WFIRST_{}3.fitres'.format(init, surv)
try:
    with open(fitres, 'r') as f:
        for line in f:
            if 'VARNAME' in line:
                var = line
                break
    with open(fitres, 'r') as f:
        for line in f:
            if 'NVAR' in line:
                varscount = int(line.split(' ')[1]) - 2
                break
    var = var.split()
    var.remove('VARNAMES:')
    var.remove('FIELD')
    datasim3 = np.loadtxt(fitres, dtype=float, skiprows=12, usecols=columns)
    for i in range(varscount):
        if var[i] == 'HOST_LOGMASS':
            sim3mass = np.copy(datasim3[:, i])
        elif var[i] == 'x1':
            sim3x1 = np.copy(datasim3[:, i])
        elif var[i] == 'c':
            sim3c = np.copy(datasim3[:, i])
except ValueError:
    print('ValueError raised.')
    print('Warning: Fitres iteration 3 not imported.  Directory given: ' + os.getcwd() + '.  File given: ' + fitres + '.')
    pass
except FileNotFoundError:
    print('FileNotFoundError raised.')
    print('Warning: Fitres iteration 3 not imported.  Directory given: ' + os.getcwd() + '.  File given: ' + fitres + '.')
    pass
except:
    raise

# Dragan data
datafitres = 'dragan2.fitres'
os.chdir(homedir + '/dragan')
with open(datafitres, 'r') as f:
    for line in f:
        if 'VARNAME' in line:
            datavars = line
            break
with open(datafitres, 'r') as f:
    for line in f:
        if 'NVAR' in line:
            datavarscount = int(line.split(' ')[1]) - 3
            break
datavars = datavars.split()
datavars.remove('VARNAMES:')
datavars.remove('FIELD')
datavars.remove('CID')
columns = tuple(list(range(2, 5)) + list(range(6, 42)))
dragan = np.loadtxt(datafitres, dtype=float, skiprows=18, usecols=columns)
for i in range(datavarscount):
    if datavars[i] == 'IDSURVEY':
        datacidint = np.copy(dragan[:, i])
    elif datavars[i] == 'zCMB':
        datazcmb = np.copy(dragan[:, i])
    elif datavars[i] == 'HOST_LOGMASS':
        datahostmass = np.copy(dragan[:, i])
    elif datavars[i] == 'c':
        datac = np.copy(dragan[:, i])
    elif datavars[i] == 'x1':
        datax1 = np.copy(dragan[:, i])

# supercal data for error data
errfitres = 'supercal_vH0.fitres'
with open(errfitres, 'r') as f:
    for line in f:
        if 'VARNAME' in line:
            errvars = line
            break
with open(errfitres, 'r') as f:
    for line in f:
        if 'NVAR' in line:
            errvarscount = int(line.split(' ')[1]) - 3
            break
errvars = errvars.split()
errvars.remove('VARNAMES:')
errvars.remove('FIELD')
errvars.remove('CID')
columns = tuple(list(range(2, 5)) + list(range(6, 42)))
errdata = np.loadtxt(errfitres, dtype=float, skiprows=18, usecols=columns)
for i in range(errvarscount):
    if errvars[i] == 'IDSURVEY':
        errcidint = np.copy(errdata[:, i])
    elif errvars[i] == 'zCMB':
        errzcmb = np.copy(errdata[:, i])
    elif errvars[i] == 'z':
        errzcmb = np.copy(errdata[:, i])
    elif errvars[i] == 'HOST_LOGMASS_ERR':
        errhostmasserr = np.copy(errdata[:, i])
    elif errvars[i] == 'MURES':
        errmures = np.copy(errdata[:, i])
    elif errvars[i] == 'HOST_LOGMASS':
        errhostmass = np.copy(errdata[:, i])

os.chdir(homedir + '/fitres/{}'.format(surv))

# only use correct CID
if ciddict[surv] == 999:
    bad_z = np.asarray([x <= 0.1 for x in datazcmb])
    bad_cidint = np.asarray([(x == 1 or x == 4 or x == 15) for x in datacidint])
    bad_zandcid = np.logical_or(bad_z, bad_cidint)
    datahostmass = datahostmass[bad_zandcid]
    datazcmb = datazcmb[bad_zandcid]
    datax1 = datax1[bad_zandcid]
    datac = datac[bad_zandcid]
else:
    bad_cidint = np.asarray([x == ciddict[surv] for x in datacidint])
    datahostmass = datahostmass[bad_cidint]
    datazcmb = datazcmb[bad_cidint]
    datax1 = datax1[bad_cidint]
    datac = datac[bad_cidint]

# remove host_logmass < 7 from dragan data.
bad_logmass = np.asarray([x >= 7. for x in datahostmass])
datahostmass = datahostmass[bad_logmass]
datazcmb = datazcmb[bad_logmass]
datax1 = datax1[bad_logmass]
datac = datac[bad_logmass]
data_arr = np.vstack((datahostmass, datazcmb, datax1, datac)).T

# use correct cid
if ciddict[surv] == 999:
    bad_z = np.asarray([x <= 0.1 for x in errzcmb])
    bad_cidint = np.asarray([(x == 1 or x == 4 or x == 15) for x in errcidint])
    bad_zandcid = np.logical_or(bad_z, bad_cidint)
    errhostmasserr = errhostmasserr[bad_zandcid]
    errzcmb = errzcmb[bad_zandcid]
    errmures = errmures[bad_zandcid]
    errhostmass = errhostmass[bad_zandcid]
else:
    bad_cidint = np.asarray([x == ciddict[surv] for x in errcidint])
    errhostmasserr = errhostmasserr[bad_cidint]
    errzcmb = errzcmb[bad_cidint]
    errmures = errmures[bad_cidint]
    errhostmass = errhostmass[bad_cidint]

# only use hostmass > 7
bad_logmass = np.asarray([x > 7 for x in errhostmass])
errhostmasserr = errhostmasserr[bad_logmass]
errzcmb = errzcmb[bad_logmass]
errmures = errmures[bad_logmass]
errhostmass = errhostmass[bad_logmass]

# remove mures > abs(10)
bad_mures = np.asarray([x < 10 for x in np.abs(errmures)])
errhostmasserr = errhostmasserr[bad_mures]
errzcmb = errzcmb[bad_mures]

# remove bad errors
bad_masserr = np.asarray([0.0001 < x < 15 for x in errhostmasserr])
errhostmasserr = errhostmasserr[bad_masserr]
errzcmb = errzcmb[bad_masserr]


def asymgauss1d(p):
    """
    Asymmetric gaussian function.
    :param p: array-like value with p[0]=mu, p[1]=sigpos, p[2]=signeg
    :return: piecewise function of one parameter that must be a numpy array.
    """
    dist = lambda v: np.piecewise(v, [v < p[0], v == p[0], v > p[0]],
                                     [lambda x: C * np.exp(-(x - p[0])**2 / (2 * p[2]**2)),
                                      lambda x: C,
                                      lambda x: C * np.exp(-(x - p[0])**2 / (2 * p[1]**2))])
    return dist


def sample_gen(dist, res, nmin, nmax):
    """
    generates random samples for asym dists
    :param dist: this needs to be a lambda function returned from asymgauss1d
    :param res: number of bins used to create perfect histogram
    :param nmin: starting bin
    :param nmax: stopping bin
    :return: pseudorandom sample based on distribution and bounds given.
    """
    bins = np.linspace(nmin, nmax, res)
    step = bins[1] - bins[0]
    binweights = dist(bins) / np.sum(dist(bins))
    newsample = []
    for i in range(res - 1):
        count = 0
        start = bins[i]
        stop = bins[i] + step
        while count < int(sample * 10 * binweights[i]):
            choice = abs(start - stop) * np.random.random() + start
            newsample.append(choice)
            count += 1
    return np.random.choice(newsample, size=sample)


def digitize3D(arr1, arr2, arr3, bounds, step1=1., step2=1., step3=1., norm=False):
    """
    Finds weights of arr1 vs arr2 vs arr3 in 3D plot
    :param arr1: x-axis arr
    :param arr2: y-axis arr
    :param arr3: z-axis arr
    :param bounds: specify bounds as list of length 6.
    :param step1: x-axis resolution.  Default is 1.
    :param step2: y-axis resolution.  Default is 1.
    :param step3: z-axis resolution.  Default is 1.
    :param norm: If true, returned array is normalized.  Default is False
    :return:
    """
    if len(bounds) == 6:
        min1, max1 = bounds[0], bounds[1]
        min2, max2 = bounds[2], bounds[3]
        min3, max3 = bounds[4], bounds[5]
    else:
        return False
    bins1 = np.arange(min1, max1, step1)
    bins2 = np.arange(min2, max2, step2)
    bins3 = np.arange(min3, max3, step3)
    cells = np.zeros((len(bins2), len(bins1), len(bins3)), dtype=float)
    superarr = np.vstack((arr1, arr2, arr3)).T
    # print(superarr)
    for i in range(len(bins2)):
        for j in range(len(bins1)):
            for k in range(len(bins3)):
                for l in superarr:
                    if bins2[i] <= l[1] < bins2[i] + step2 and bins1[j] <= l[0] < bins1[j] + step1 and bins3[k] <= l[2] < bins3[k] + step3:
                        cells[i, j, k] += 1.
    if norm:
        return cells / np.sum(cells)
    else:
        return cells


def weightmaker3D(arr2, arr3, bounds, datamap, simmap, wmap0=False, step1=1., step2=1., step3=1.):
    """
    Generate 3D weight map for generate host mass sample based on digitized count cells
    :param arr2:
    :param arr3:
    :param bounds:
    :param datamap:
    :param simmap:
    :param step1:
    :param step2:
    :param step3:
    :return:
    """
    min1, max1 = bounds[0], bounds[1]
    min2, max2 = bounds[2], bounds[3]
    min3, max3 = bounds[4], bounds[5]
    bins1 = np.arange(min1, max1, step1)  # mass
    bins2 = np.arange(min2, max2, step2)  # stretch
    bins3 = np.arange(min3, max3, step3)  # color
    if type(wmap0) == bool:
        wmap = np.true_divide(datamap, simmap)  # color, mass, color
    else:
        wmap = np.multiply(np.true_divide(datamap, simmap), wmap0)
    wmap[wmap == np.inf] = 0.
    wmap = np.nan_to_num(wmap)
    h = len(wmap[:, 0, 0])  # height of wmap -> stretch
    w = len(wmap[0, :, 0])  # width of wmap -> mass
    d = len(wmap[0, 0, :])  # depth of wmap -> color
    massarr = np.zeros(sample)
    for i in range(h):  # i = stretch cell
        for j in range(d):  # j = color cell
            if np.sum(wmap[i, :, j]) != 0.:
                massprobs = wmap[i, :, j] / np.sum(wmap[i, :, j])
                wpinterp = interp.interp1d(range(w), massprobs, fill_value=0.)
                neww = np.linspace(0, w - 1, w * 10)
                newmassprobs = wpinterp(neww)
                newmassprobs[newmassprobs < 0.] = 0.
                newmassprobs = newmassprobs / np.sum(newmassprobs)
                for k in range(sample):
                    if bins2[i] <= arr2[k] < bins2[i] + step2 and bins3[j] <= arr3[k] < bins3[j] + step3 and massarr[k] == 0:
                        choice = np.random.choice(neww, p=newmassprobs) * step1  # choose mass value location in 3D grid
                        rand = np.random.random()
                        mass = step1 * rand + min1 + choice
                        while 10. + buff * wgtstep >= mass >= 10. - buff * wgtstep:
                            # choose new mass value outside transition zone
                            choice = np.random.choice(neww, p=newmassprobs) * step1
                            mass = step1 * rand + min1 + choice
                        massarr[k] = mass
    badcount = 0
    for l in range(sample):
        if massarr[l] == 0.:
            mass = 2. / 3. * np.random.randn() + np.nanmean(datahostmass)
            # while loop prevents extreme host mass values
            while mass < 7. or mass > 13. or 10 + buff * wgtstep >= mass >= 10 - buff * wgtstep:
                mass = 2. / 3. * np.random.randn() + np.nanmean(datahostmass)
            massarr[l] = mass
            badcount += 1
    return massarr, wmap


def z_mod(massarr, zarr, res=6):
    """
    Adds small mass offset to take into consideration dynamic host mass value with respect to redshift.
    !!!!!!CURRENTLY NOT USED!!!!!!
    :param massarr: input mass sample
    :param zarr: input z sample
    :param res: number of z bins used to interpolate average offsets
    :return: Modified host mass array.
    """
    massarr_copy = np.copy(massarr)
    zbins = np.linspace(min(datazcmb), max(datazcmb), res)
    zstep = zbins[1] - zbins[0]
    datazbin0 = np.asarray([zbins[0] <= x < zbins[1] for x in datazcmb])
    datazbin1 = np.asarray([zbins[1] <= x < zbins[2] for x in datazcmb])
    datazbin2 = np.asarray([zbins[2] <= x < zbins[3] for x in datazcmb])
    datazbin3 = np.asarray([zbins[3] <= x < zbins[4] for x in datazcmb])
    datazbin4 = np.asarray([zbins[4] <= x < zbins[5] for x in datazcmb])
    datazbin5 = np.asarray([zbins[5] <= x < zbins[5] + zstep for x in datazcmb])
    datazbins = [datazbin0, datazbin1, datazbin2, datazbin3, datazbin4, datazbin5]
    zbins_massavg = []
    for z in datazbins:
        meanoffset = np.mean(datahostmass[z]) - np.mean(datahostmass)
        zbins_massavg.append(meanoffset)
    zmassinterp = interp.interp1d(zbins, zbins_massavg, fill_value='extrapolate')
    # print(zmassinterp([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, max(zsample)]))
    for i in range(sample):
        massmod = zmassinterp(zarr[i])
        massarr_copy[i] = massarr[i] + massmod
    return massarr_copy


def errmaker(zarr, errdata, zdata):
    """
    Finds linear fit of z data and error data from sdss and snls.  Fit is used to give accurate host mass error value
    for a given z value
    :param zarr: randomly generated z sample
    :param errdata: mass error data
    :param zdata: corresponding redshift data
    :return: random host mass error sample as numpy array
    """
    errsample = []
    m, b = np.polyfit(zdata, errdata, 1)
    for z in zarr:
        errval = m * z + b
        errsample.append(errval)
    return np.asarray(errsample)

# asym gauss dists for mass, c and x1, respectively
casymgauss = asymgauss1d(cp3)
x1asymgauss = asymgauss1d(x1p3)

# independent variable samples drawn from respective distributions
csample = sample_gen(casymgauss, 1000, -1, 1)
x1sample = sample_gen(x1asymgauss, 1000, -4, 3)
zsample = (max(datazcmb) + 0.2) * np.random.random(size=sample) + 0.009
masssample = 6. * np.random.random(size=sample) + 7.
masserrsample = errmaker(zsample, errhostmasserr, errzcmb)
# map cell things for iterative weighting mass thingy
massx1cbounds = [7., 13., -4., 3., -0.3, 0.3]
# step bounds
s = [0.5, 1., 0.1]

# second input argument determines weight map iteration step
argv2 = int(sys.argv[2])  # cast second argv as int for comparison
if sampletype == 0:
    if argv2 == 0:
        masssamplefinal = masssample
    elif argv2 == 1:
        sim1massx1cmap = digitize3D(sim1mass, sim1x1, sim1c, massx1cbounds, step1=s[0], step2=s[1], step3=s[2], norm=True)
        datamassx1cmap = digitize3D(datahostmass, datax1, datac, massx1cbounds, step1=s[0], step2=s[1], step3=s[2],
                                    norm=True)
        # weighted mass sample
        megamasssample1, wmap1 = weightmaker3D(x1sample, csample, massx1cbounds, datamassx1cmap, sim1massx1cmap,
                                               step1=s[0], step2=s[1], step3=s[2])
        masssamplefinal = megamasssample1
    elif argv2 == 2:
        sim1massx1cmap = digitize3D(sim1mass, sim1x1, sim1c, massx1cbounds, step1=s[0], step2=s[1], step3=s[2], norm=True)
        sim2massx1cmap = digitize3D(sim2mass, sim2x1, sim2c, massx1cbounds, step1=s[0], step2=s[1], step3=s[2], norm=True)
        datamassx1cmap = digitize3D(datahostmass, datax1, datac, massx1cbounds, step1=s[0], step2=s[1], step3=s[2],
                                    norm=True)
        # weighted mass samples
        megamasssample1, wmap1 = weightmaker3D(x1sample, csample, massx1cbounds, datamassx1cmap, sim1massx1cmap,
                                               step1=s[0], step2=s[1], step3=s[2])
        megamasssample2, wmap2 = weightmaker3D(x1sample, csample, massx1cbounds, datamassx1cmap, sim2massx1cmap,
                                               wmap0=wmap1,
                                               step1=s[0], step2=s[1], step3=s[2])
        masssamplefinal = megamasssample2
    elif argv2 == 3:
        sim1massx1cmap = digitize3D(sim1mass, sim1x1, sim1c, massx1cbounds, step1=s[0], step2=s[1], step3=s[2], norm=True)
        sim2massx1cmap = digitize3D(sim2mass, sim2x1, sim2c, massx1cbounds, step1=s[0], step2=s[1], step3=s[2], norm=True)
        sim3massx1cmap = digitize3D(sim3mass, sim3x1, sim3c, massx1cbounds, step1=s[0], step2=s[1], step3=s[2], norm=True)
        datamassx1cmap = digitize3D(datahostmass, datax1, datac, massx1cbounds, step1=s[0], step2=s[1], step3=s[2], norm=True)

        # weighted mass samples
        megamasssample1, wmap1 = weightmaker3D(x1sample, csample, massx1cbounds, datamassx1cmap, sim1massx1cmap,
                                               step1=s[0], step2=s[1], step3=s[2])
        megamasssample2, wmap2 = weightmaker3D(x1sample, csample, massx1cbounds, datamassx1cmap, sim2massx1cmap,
                                               wmap0=wmap1, step1=s[0], step2=s[1], step3=s[2])
        megamasssample3, wmap3 = weightmaker3D(x1sample, csample, massx1cbounds, datamassx1cmap, sim3massx1cmap,
                                               wmap0=wmap2, step1=s[0], step2=s[1], step3=s[2])

        masssamplefinal = megamasssample3
        # print(np.mean(masssamplefinal), np.min(masssamplefinal), np.max(masssamplefinal))
    else:
        # raise error is iteration number is not valid.
        raise IterError('Must choose iteration number of 0, 1, 2, or 3.')
elif sampletype == 1:
    masssamplefinal = 2 / 3 * np.random.randn(sample) + 10.
    for m in masssamplefinal:
        while 10 + buff * wgtstep >= m >= 10 - buff * wgtstep:
            m = 2 / 3 * np.random.randn() + 10.
elif sampletype == 2:
    masssamplefinal = 6. * np.random.random(sample) + 7.
elif sampletype == 3:
    masssamplefinal = np.empty([sample])
    for m in masssamplefinal:
        m = np.random.choice([8., 12.])
# create HOSTLIB file
os.chdir(homedir + '/hostlib/{}'.format(surv))
hostlib = open('{}_{}_{}_{}.HOSTLIB'.format(init, hostlibsuffix,  surv, smeararg), mode='w')
hostlib.write('NVAR: 7\n'
                'VARNAMES: GALID ZTRUE c x1 LOGMASS_TRUE LOGMASS_OBS LOGMASS_ERR\n\n')

# write weights to file.
if massstep == '0.00':
    hostlib.write('NVAR_WGTMAP: 1\nVARNAMES_WGTMAP:  LOGMASS_TRUE\n')
    for i in np.arange(int(min(masssamplefinal)) - 2, 10., 0.5):
        hostlib.write('WGT:   ' + str(i) + '   1    0.00\n')
    for i in np.arange(10., int(max(masssamplefinal)) + 3, 0.5):
        hostlib.write('WGT:   ' + str(i) + '   1   0.00\n')
else:
    hostlib.write('NVAR_WGTMAP: 1\nVARNAMES_WGTMAP:  LOGMASS_TRUE\n')
    for i in np.arange(int(min(masssamplefinal)) - 2 + wgtstep / 2, 10., wgtstep):
        hostlib.write('WGT:   ' + str(i) + '   1    {}\n'.format(massstep))
    for i in np.arange(10. + wgtstep / 2, int(max(masssamplefinal)) + 3, wgtstep):
        hostlib.write('WGT:   ' + str(i) + '   1   -{}\n'.format(massstep))

hostlib.write('\n') # add a space between wgt map and host list

# use constant noise error
if not err:
    for i in range(sample):
        ztrue = zsample[i]
        c = csample[i]
        x1 = x1sample[i]
        """
        if sampletype == 0:
            logmass_true = masssamplefinal[i]
        elif sampletype == 1:
            logmass_true = 2 / 3 * np.random.randn() + 10.
            while 10 + buff * wgtstep >= logmass_true >= 10 - buff * wgtstep:
                logmass_true = 2 / 3 * np.random.randn() + 10.
        elif sampletype == 3:
            logmass_true = 6. * np.random.random() + 7.
        elif sampletype == 2:
            logmass_true = np.random.choice([8., 12.])
        """
        logmass_true = masssamplefinal[i]
        noise = noiseerr * np.random.randn()
        galid = str(i)
        logmass_obs = str(logmass_true + noise)
        logmass_err = str(noiseerr)
        hostlib.write('GAL: ' + galid + '   ' + str(ztrue) + '   ' + str(c) + '   ' + str(x1) + '   ' +
                      str(logmass_true) + '   ' + logmass_obs + '   ' + logmass_err + '\n')
# use errmaker sample
else:
    for i in range(sample):
        ztrue = zsample[i]
        c = csample[i]
        x1 = x1sample[i]
        """
        if sampletype == 0:
            logmass_true = masssamplefinal[i]
        elif sampletype == 1:
            logmass_true = 2 / 3 * np.random.randn() + 10.
            while 10 + buff * wgtstep >= logmass_true >= 10 - buff * wgtstep:
                logmass_true = 2 / 3 * np.random.randn() + 10.
        elif sampletype == 3:
            logmass_true = 6. * np.random.random() + 7.
        elif sampletype == 2:
            logmass_true = np.random.choice([8., 12.])
        """
        logmass_true = masssamplefinal[i]
        noise = masserrsample[i] * np.random.randn()
        galid = str(i)
        logmass_obs = str(logmass_true + noise)
        logmass_err = str(masserrsample[i])
        hostlib.write('GAL: ' + galid + '   ' + str(ztrue) + '   ' + str(c) + '   ' + str(x1) + '   ' +
                      str(logmass_true) + '   ' + logmass_obs + '   ' + logmass_err + '\n')
hostlib.close()
