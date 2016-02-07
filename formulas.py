# formulas for outcome prediction
# based on xray, ct / mri data

# would be nice to get actual population data eventually

import numpy as np

#   Normal, Mild, Moderate, Severe
def getXrayOutcomeV1(gender, ddensity, ob_diam, app_shape):
#   ignore gender for now
    out = 'Normal'
    if (ddensity > 1):
        out = 'Moderate'
        if (ob_diam > 7.0):
            out = 'Severe'
        if (app_shape > 1):
            out = 'Severe'
    return out

# set string outcome from percent
# Normal < 0.5 < Moderate < 0.69 < Severe
def getXrayOutcome(gender, ddensity, ob_diam, app_shape):
    p = getXrayOutcomePercent(gender, ddensity, ob_diam, app_shape)
    if (p > 0.69):
        out = 'Severe'
    elif (p > 0.5):
        out = 'Moderate'
    else:
        out = 'Normal'
    return out

# heuristic parameters
xray_direct_params = { 'double_density':   1.0,
                       'oblique_diameter': 0.1,
                       'appendage_shape':  0.2,
                       'intercept':        0.0 }

# calc percent using logistic functions of params
def getXrayOutcomePercent(gender, ddensity, ob_diam, app_shape):
    a1 = -xray_direct_params['double_density']
    a2 = -xray_direct_params['oblique_diameter']
    a3 = -xray_direct_params['appendage_shape']
    b  = -xray_direct_params['intercept']
    p  = 1 / (1 + np.exp( b + a1 * (ddensity - 1.0) + \
           a2 * (ob_diam - 7.0) + a3 * (app_shape - 1.0) ))
#   print '  a1 %g, a2 %g, a3 %g, b %g' % (a1, a2, a3, b)
#   print '  ddensity %g, ob_diam %g, app_shape %g => percent %g' % (ddensity, ob_diam, app_shape, p)
    return p


