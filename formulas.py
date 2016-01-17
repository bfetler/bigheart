# formulas for outcome prediction
# based on xray, ct / mri data

# would be nice to get actual population data eventually

def getXrayOutcome(gender, ddensity, ob_diam, app_shape):
#   ignore gender for now
#   out = 'Unsure'
    out = 'Normal'
    if (ddensity == 1):
        out = 'Moderate to Severe'
        if (ob_diam > 7.0):
            out = 'Severe'
        if (app_shape > 1):
            out = 'Severe2'
    return out

# possible to set string outcome from percent?

# calc percent using logistic functions of params?
def getXrayOutcomePercent(gender, ddensity, ob_diam, app_shape):
    return 50.0

