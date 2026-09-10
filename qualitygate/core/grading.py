#piece of logic. a pure function that converts a null rate(or another metric) into a graded risk.
# this is specifically to cater the soft lane path in the two lane model

# the function to be implementd :
# r(x) = Kx/T if x in [0, T] and r(x) = K + (1 - K)(x - T)/(1 - T) if x in [T, 1]

def grade_soft(value : float, threshold : float, kink : float = 0.2) -> float:
    """
    parameters :
    value : Observed value normalized to [0, 1]
    threshold and kink : self explanatory, both in (0, 1)4 
    """
    if not 0 <  threshold  < 1 :
        raise ValueError(f"threshold must be in (0, 1), got {threshold}")

    if value <= threshold :
        return (kink / threshold) * value
    else :
        return kink + ((1-kink) / (1 - threshold)) * (value - threshold)