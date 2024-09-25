import math
import pmoired
import numpy as np

continuum = {'m':{'disk,F0':         0.17240, # +/- 0.00096
            'disk,PRO':        0.161, # +/- 0.032
            'disk,SPX':        1.07, # +/- 0.11
            'disk,az amp1':    0.065, # +/- 0.013
            'disk,az projang1':2.5, # +/- 24.8
            'disk,diamout':    27.22, # +/- 0.18
            'rim,F0':          0.5270, # +/- 0.0038
            'rim,SPX':         2.03, # +/- 0.13
            'rim,az amp1':     0.206, # +/- 0.038
            'rim,az amp2':     0.744, # +/- 0.023
            'rim,az amp3':     0.336, # +/- 0.023
            'rim,az projang1': 96.09, # +/- 6.24
            'rim,az projang2': 167.96, # +/- 1.52
            'rim,az projang3': 35.03, # +/- 1.40
            'rim,diamout':     4.765, # +/- 0.031
            'rim,incl':        47.31, # +/- 0.58
            'rim,projang':     21.97, # +/- 0.90
            'disk,diamin':     '$rim,diamout',
            'disk,incl':       '$rim,incl',
            'disk,profile':    '$R**$disk,PRO',
            'disk,projang':    '$rim,projang',
            'disk,spectrum':   '$disk,F0*($WL/2.166)**$disk,SPX',
            'rim,diamin':      0.0,
            'rim,profile':     'doughnut',
            'rim,spectrum':    '$rim,F0*($WL/2.166)**$rim,SPX',
            'star,spectrum':   '(1-$rim,F0-$disk,F0)*($WL/2.166)**-3.8',
            'star,ud':         0,
            },
            'doNotFit':['star,ud', 'rim,diamin'],
            'prior':[('disk,PRO', '<', 0)]}

blobs = {'add':{# -- blob1 size in mas
        'blob1,fwhm': 2,
        # -- continuum flux
        'blob1,f': 0.0, 
        # -- central wavelength, in um
        'blob1,line_0_wl0': '2.166+$blob1,DWL0/1000',
        'blob1,DWL0': -1.2,
        # -- gaussian line, FWHM in nm (not um!)
        'blob1,line_0_gaussian': 0.5,
        # -- line amplitude
        'blob1,line_0_f': 0.2,
        # -- blob position in mas
        'blob1,x': 0,
        'blob1,y': -1,
        # -- same for blob 2:
        'blob2,fwhm': 2,
        'blob2,f': 0.0,
        'blob2,line_0_wl0': '2.166+$blob2,DWL0/1000',
        'blob2,DWL0': 1.2,         
        'blob2,line_0_gaussian': 0.5,
        'blob2,line_0_f': 0.2,
        'blob2,x': 0,
        'blob2,y': 1,
         }}
blobs['fitOnly'] = list(filter(lambda k: k.startswith('blob') and type(blobs['add'][k])!=str and k.split(',')[1]!='f', blobs['add'].keys()))
blobs['prior'] = [('blob1,fwhm', '>', 0.5), ('blob2,fwhm', '>', 0.5)]
blobs['best'] = {'blob1,DWL0':           5.5859, # +/- 0.0033
                'blob1,fwhm':           0.977, # +/- 0.023
                'blob1,line_0_f':       0.2058, # +/- 0.0024
                'blob1,line_0_gaussian':0.8676, # +/- 0.0078
                'blob1,x':              0.1091, # +/- 0.0050
                'blob1,y':              0.4635, # +/- 0.0064
                'blob2,DWL0':           6.8301, # +/- 0.0031
                'blob2,fwhm':           1.034, # +/- 0.021
                'blob2,line_0_f':       0.2251, # +/- 0.0025
                'blob2,line_0_gaussian':0.8525, # +/- 0.0072
                'blob2,x':              -0.1290, # +/- 0.0047
                'blob2,y':              -0.4908, # +/- 0.0059
                'blob1,f':              0.0,
                'blob1,line_0_wl0':     '2.16+$blob1,DWL0/1000',
                'blob2,f':              0.0,
                'blob2,line_0_wl0':     '2.16+$blob2,DWL0/1000',
                'disk,F0':              0.1724,
                'disk,PRO':             0.161,
                'disk,SPX':             1.07,
                'disk,az amp1':         0.065,
                'disk,az projang1':     2.5,
                'disk,diamin':          '$rim,diamout',
                'disk,diamout':         27.22,
                'disk,incl':            '$rim,incl',
                'disk,profile':         '$R**$disk,PRO',
                'disk,projang':         '$rim,projang',
                'disk,spectrum':        '$disk,F0*($WL/2.166)**$disk,SPX',
                'rim,F0':               0.527,
                'rim,SPX':              2.03,
                'rim,az amp1':          0.206,
                'rim,az amp2':          0.744,
                'rim,az amp3':          0.336,
                'rim,az projang1':      96.09,
                'rim,az projang2':      167.96,
                'rim,az projang3':      35.03,
                'rim,diamin':           0.0,
                'rim,diamout':          4.765,
                'rim,incl':             47.31,
                'rim,profile':          'doughnut',
                'rim,projang':          21.97,
                'rim,spectrum':         '$rim,F0*($WL/2.166)**$rim,SPX',
                'star,spectrum':        '(1-$rim,F0-$disk,F0)*($WL/2.166)**-3.8',
                'star,ud':              0,
                }

kep = {'add':{'kep,DWL0':        0., 
        'kep,Vin':         -200, 
        'kep,diamin':      0.5, 
        'kep,incl':        50, 
        'kep,line_brg_EW':   0.3, 
        'kep,line_brg_rpow': -2, 
        'kep,projang':     22, 
        'kep,diamout':     3.5,
        'kep,line_brg_wl0':  '2.166+$kep,DWL0/1000',
         },
       'prior':[],
      }
kep['fitOnly'] = list(filter(lambda x: x.startswith('kep,') and type(kep['add'][x])!=str and not x.endswith('_rpow') , kep['add'].keys()))
kep['best'] = {'kep,DWL0':         0.2052, # +/- 0.0024
    'kep,Vin':          -196.33, # +/- 2.66
    'kep,diamin':       0.75271, # +/- 0.00010
    'kep,diamout':      3.911, # +/- 0.086
    'kep,incl':         54.83, # +/- 1.18
    'kep,line_brg_EW':  0.3876, # +/- 0.0025
    'kep,line_brg_rpow':-2, 
    'kep,projang':      13.66, # +/- 0.39
    'kep,x':            -0.0072, # +/- 0.0028
    'kep,y':            -0.0173, # +/- 0.0032
    'disk,F0':          0.1724,
    'disk,PRO':         0.161,
    'disk,SPX':         1.07,
    'disk,az amp1':     0.065,
    'disk,az projang1': 2.5,
    'disk,diamin':      '$rim,diamout',
    'disk,diamout':     27.22,
    'disk,incl':        '$rim,incl',
    'disk,profile':     '$R**$disk,PRO',
    'disk,projang':     '$rim,projang',
    'disk,spectrum':    '$disk,F0*($WL/2.166)**$disk,SPX',
    'kep,line_brg_wl0': '2.166+$kep,DWL0/1000',
    'rim,F0':           0.527,
    'rim,SPX':          2.03,
    'rim,az amp1':      0.206,
    'rim,az amp2':      0.744,
    'rim,az amp3':      0.336,
    'rim,az projang1':  96.09,
    'rim,az projang2':  167.96,
    'rim,az projang3':  35.03,
    'rim,diamin':       0.0,
    'rim,diamout':      4.765,
    'rim,incl':         47.31,
    'rim,profile':      'doughnut',
    'rim,projang':      21.97,
    'rim,spectrum':     '$rim,F0*($WL/2.166)**$rim,SPX',
    'star,spectrum':    '(1-$rim,F0-$disk,F0)*($WL/2.166)**-3.8',
    'star,ud':          0,
    }

def starMassFromKeplerianDisk(m):
    formula = """
# with m is your "bestfit" dictionnary (e.g. `oi.bestfit`)
tmp = pmoired.dpfit.randomParam(m, N=100, x=None)
plx = 3.2831
a_au = np.array([t['kep,diamin'] for t in tmp['r_param']])/2/plx
P_yr = 2*np.pi*a_au*150e6/np.array([np.abs(t['kep,Vin']) for t in tmp['r_param']])/3600/24/365.25
M_msun = a_au**3/P_yr**2
print("star's mass = %.1f ± %.1f Msun"%(np.mean(M_msun), np.std(M_msun)))
    """
    print(formula)
    # -- randomise parameters according to the covariance
    tmp = pmoired.dpfit.randomParam(m, N=100, x=None)
    plx = 3.2831
    a_au = np.array([t['kep,diamin'] for t in tmp['r_param']])/2/plx
    P_yr = 2*np.pi*a_au*150e6/np.array([np.abs(t['kep,Vin']) for t in tmp['r_param']])/3600/24/365.25
    M_msun = a_au**3/P_yr**2
    print("star's mass = %.1f ± %.1f Msun"%(np.mean(M_msun), np.std(M_msun)))
    