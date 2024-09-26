#!/usr/bin/env python
# coding: utf-8

# # HD 58647 (Herbig Ae): continuum GRAVITY,  Br $\gamma$ emmission
# 
# The goal is to model the YSO HD 58647 observed by GRAVITY. In the continuum, the inner star+rim is seen. There is also an emission line in Bracket$_\gamma$ ($\lambda$~2.167$\mu$m) which we can model.
# 
# - AMBER (K-band) paper with Brackett$_\gamma$ fit [Kurosawa et al. (2016)](https://ui.adsabs.harvard.edu/abs/2016MNRAS.457.2236K/abstract)
# - PIONIER (H-band) paper in the continuum [Lazareff et al. (2017)](https://ui.adsabs.harvard.edu/abs/2017A%26A...599A..85L/abstract)
# - GRAVITY (K-band) paper where Brackett$_\gamma$ has been modeled, with better u,v coverage than the AMBER paper [Bouarour et al. (2024)](https://arxiv.org/pdf/2312.08819.pdf)

# In[ ]:


# `widget` requires `pip install ipympl`
get_ipython().run_line_magic('matplotlib', 'widget')
import numpy as np
import matplotlib.pyplot as plt

import pmoired
pmoired.FIG_MAX_WIDTH = 10
pmoired.FIG_MAX_HEIGHT = 10

from pmoired import tellcorr
print(pmoired.__version__, pmoired.__file__)

import solutions


# # Model K-band GRAVITY continuum data
# We use K-band GRAVITY data binned by a factor 100 to reach R=$\lambda/\delta\lambda\sim40$.

# In[ ]:


# -- load data
oi = pmoired.OI('./DATA/GRA*viscalibrated.fits', insname="GRAVITY_SC", binning=100)
oi.show()


# ## Model the star+rim in the K-band continuum
# 
# Read and Follow the `PMOIRED` tutorial on [YSO disks modeling](https://htmlpreview.github.io/?https://github.com/amerand/PMOIRED_examples/blob/main/html/EX2%20chromatic%20YSO%20disk.html) to come up with a good disk model in the continuum. 
# 
# The cell is initialised with a simple model of unresolved `star` and a Gaussian `rim`. Note the way the flux is defined, so the total flux is equal to 1 at $\lambda=2.166\,\mu m$.
# 
# Using the tutorial, you can:
# - spatial dimensions (`ud`, `fwhm`, `diam`, `diamin`, `diamout`, etc) are in mas, angles and in degrees and wavelengths are in microns
# - tilt and rotate with `rim,projang` and `rim,incl` (in degrees)
# - change the `rim` to a ring by replacing `rim,fwhm` by `rim,diamin` and `rim,diamout`
# - play around with the profile of the ring with `'rim,profile':'$R**-2'` or anything you want! `$R` is the radial position in mas 
# - add azimuthal variations to the ring with `rim,az amp1`, `rim,az projang1` (and higher!) to introduce non-0 closure phase
# 
# > 1) *before fitting, you should check your model against the data to get a reasonable first guess. The inital guess below is NOT reasonable! why?*
# 
# > 2) *Pay attention to uncertainties and correlations to decide whether a parameter is fitted or degenerated with other parameters.*
# 
# > 3) *do you think you need a third component, why/why not?*
# 
# > 4) *You can move on the rest of the tutorial when reach a reduced $\chi^2$ of about 5 or better.*

# In[ ]:


m = {'star,ud':0, 'star,spectrum': '(1-$rim,F0)*($WL/2.166)**-3.8',
     'rim,fwhm':8, 'rim,spectrum': '$rim,F0*($WL/2.166)**$rim,SPX', 
     'rim,F0':0.9, 'rim,SPX':1,
    }
doNotFit, prior = ['star,ud'], [('rim,SPX', '>', 0)]

# -- solution
#m, doNotFit, prior = solutions.continuum['m'].copy(), solutions.continuum['doNotFit'], solutions.continuum['prior']

# -- setup fit 
oi.setupFit({'obs':['|V|', 'T3PHI']})

# -- before fitting, you should check your model against the data to get a good first guess
doFit = False
if doFit:
    oi.doFit(m, doNotFit=doNotFit, prior=prior)
    m = oi.bestfit['best']

oi.show(model=m, imFov=21, imMax='99', imPow=0.25, imPlx=3.2831)    


# ## Use bootstrap to mitigate correlations
# 
# Once you have a model you are satisfied with, run the bootstrapping (data resampling). This takes a lot more time, so do it only once you want to have uncertainties and 
# 
# The number of iterations is an optimum between "not too few" ($\gtrapprox$ number of indepedent data sets) and "not too many" (can take very long). On an average laptop, `Nfits=32` should take a few minutes for a dozen of more parameters
# 
# > *How do the uncertainties and correlations compare to the gradient descent fit?* 

# In[ ]:


oi.bootstrapFit(32)


# In[ ]:


oi.showBootstrap()


# # Br$_\gamma$ emmission in full-resolution GRAVITY data
# 
# load GRAVITY data at full spectral resolution, with correction from tellurics already done (check [this tutorial](https://htmlpreview.github.io/?https://github.com/amerand/PMOIRED_examples/blob/main/html/EX5%20Binary%20with%20spectroscopic%20lines.html) if you are interested how this works).

# In[ ]:


oi2 = pmoired.OI('./DATA/G*viscalibrated.fits', insname="GRAVITY_SC")
oi2.fig = 1000 # offset figure counter so we keep previous figures in the notebook


# In[ ]:


# check the telluric model, zoom around 2.166um to see the Br_gamma line, note the deep tellurics very close!:
tellcorr.showTellurics(oi2.data[12]['filename'], fig=0)


# In[ ]:


# -- isolate fitting region aroung data around Br gamma
oi2.setupFit({'obs':['T3PHI', 'DPHI', 'NFLUX', '|V|'],
             'wl ranges':[(2.1661-0.007, 2.1661+0.007)],
            })
oi2.show()


# ## Add to the continnum model 2 blobs in emission around Brackett $\gamma$
# 
# in `setupFit`,  we can use purely differential quantities: `NFLUX` (flux normalised to continuum), `N|V|` (visibility amplitude normalised to continuum) and `DPHI` (differential phase, with continuum substracted). We use `'wl ranges':[(2.1661-0.007, 2.1661+0.007)]` to limit to the range around Br$_\gamma$. Because uncertainties in data seem optimistic, we set some `min error` and `min relative error`.
# 
# Looking at the double peak line in the spectrum, and the S shape in the differential phase, add 2 components with emission lines (blue- and red-shifted). Based on the visibility amplitude, what should be their sizes compared to the continuum disk? 
# 
# To setup components in emission:
# - `...,ud` or `...,fwhm` to set its morphology and size (in mas)
# - `...,x`, `...,y`: position offest (RA, Dec) in mas
# - `...,line_brg_wl0` central wavelength in um
# - `...,line_brg_gaussian` gaussian line full width at half maximum in nm
# - `...,line_brg_f` amplitude (>0 for emission, <0 for absorption)
# - `...,f` continuum flux: set it to 0 and do not fit it!
# 
# You can use `prior` to add some constraints as a list of tuples. For instance, if you want the component `blob` to be only in a range of sizes:
# 
# `prior = [('blob,fwhm', '>', 1), ('blob,fwhm', '<', 10)]`
# 
# You can also make priors depending on other parameters. For example, if you do not want the `blob` to overlap with the (0,0) position:
# 
# `prior = [('blob,ud', '<', 'np.sqrt(blob,x**2+blob,y**2)/2')]`
# 
# > *in `doFit`, use the `fitOnly` keyword to give a list the parameters to fit: you should only list the ones relative to the components with spectral features (i.e. the one you added), but not the continuum flux!*
#   

# In[ ]:


# -- best continuum model from above
m = {}

# -- add emission line blobs
m.update({})

# -- only fit blobs' parameters (but not their continuum fluxes!)
fitOnly = []
prior = []

# -- solutions ------------
# m, fitOnly, prior = solutions.continuum['m'].copy(), solutions.blobs['fitOnly'], solutions.blobs['prior']
# m.update(solutions.blobs['add'])
# display(m)
# print('fitOnly:', fitOnly)
# print('prior:', prior)
# -------------------------

oi2.setupFit({'obs':['N|V|', # normalised visibility
                     'DPHI',  # differential phase
                     'NFLUX', # normalised flux
                   ],
             'min relative error':{'NFLUX':0.01, 'N|V|':0.01},
             'min error':{'DPHI':1},
             'wl ranges':[(2.1661-0.007, 2.1661+0.007)],
            })

doFit = False # -- when you ready, try to fit!
if doFit:
    oi2.doFit(m, fitOnly=fitOnly, prior=prior)
    m = oi2.bestfit['best']

oi2.show(m, imFov=10, imMax='99', imPow=0.25, imWl0=[2.16, 2.1655, 2.16685], imPlx=3.2831, vWl0=2.1662)


# In[ ]:


oi2.showFit()


# ## Add Keplerian disk to the continuum model
# 
# For a full intro to the Keplerian disk, check out [PMOIRED example](https://github.com/amerand/PMOIRED_examples) [#4](https://htmlpreview.github.io/?https://github.com/amerand/PMOIRED_examples/blob/main/html/EX4%20Be%20model%20comparison%20with%20AMHRA.html). This model is a re-implementation of the model described in [Delaa et al. (2011)](https://ui.adsabs.harvard.edu/abs/2011A%26A...529A..87D/abstract) and [Meilland et al. (2012)](https://ui.adsabs.harvard.edu/abs/2012A%26A...538A.110M/abstract), originaly developped to interpret VEGA and AMBER observations of Be stars.
# 
# - `kep,incl`: inclination in degrees
# - `kep,projang`: position angle in degrees
# - `kep,diamin`: inner diameter of the Keplerian disk, in mas 
# - `kep,diamout`:  outer diameter of the Keplerian disk, in mas
# - `kep,Vin`: velocity in km/s at `diamin`, sign defines the rotation direction
# - `kep,line_brg_rpow`:  power law for the radial intensity profile in the line, e.g. -2
# - `kep,line_brg_wl0`: central wavelength in um
# - `kep,line_brg_EW`: equivalent width in nm, (assuming continnum flux is 1 at `kep,line_brg_wl0`)
# 
# you can define as many lines as you want: in the example above `_brg_` identifies the line, you can have `_myline_`, `_0_` or anything you want...
# 
# Optional parameters:
# - `kep,beta`: velocity power law (if not defined, assumed Keplerian, i.e -1/2)
# - `kep,x`, `kep,y`:position of the disk in the field, in mas (default is 0,0)
# 
# > *Note that in the [Bouarour et al. (2024)](https://arxiv.org/pdf/2312.08819.pdf), they find no significant misalignement between the continuum disk and the Keplerian disk. Compare the inclination/PA of your continuum disk with the Keplerian disk seen in Br$_\gamma$ emission.*
#  

# In[ ]:


from importlib import reload
reload(solutions)

# copy your best continuum model, add a keplerian disk
m = {}
fitOnly = []
prior = []

# -- solution -------------
# reload(solutions)
# m, fitOnly, prior = solutions.continuum['m'].copy(), solutions.kep['fitOnly'], solutions.kep['prior']
# m.update(solutions.kep['add'])
# display(m)
# print('fitOnly:', fitOnly)
# print('prior:', prior)
# --------------------------

oi2.setupFit({'obs':['N|V|', 'DPHI', 'NFLUX'],
              'min relative error':{'NFLUX':0.02, 'N|V|':0.01},
              'min error':{'DPHI':1, 'T3PHI':2},
              'wl ranges':[(2.1661-0.007, 2.1661+0.007)],
            })

doFit = False # -- when you ready, try to fit!
if doFit:
    oi2.doFit(m, fitOnly=fitOnly, prior=prior)
    m = oi2.bestfit['best']
    
oi2.show(m, imFov=10, imMax='99', imPow=0.25, imWl0=[2.16, 2.16557, 2.166, 2.1669], imPlx=3.2831, vWl0=2.1662)


# ## Run a bootstrap (if you have a recent laptop with a good processor...)
# 
# Uncertainties turn out to be quite similar to the simple fit!
# 
# > *Why do you think is that?

# In[ ]:


oi2.bootstrapFit(32)


# In[ ]:


oi2.showBootstrap(showChi2=True)


# ## Estimate the Keplerian mass of the star using the velocity of the 
# 
# You can compare your mass to 4.6$M_\odot$ assumed by [Kurosawa et al. (2016)](https://academic.oup.com/mnras/article/457/2/2236/970588) (section 4.2.1 and [table 5](https://academic.oup.com/view-large/16686315))

# In[ ]:


#solutions.starMassFromKeplerianDisk(oi2.bestfit)

