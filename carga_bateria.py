def carga_bateria(pcd, soc, pnet, nbrt, ncd, sd, soc_min, soc_max, cbat, pbatmax):
    x = 0.25  # Fração de hora utilizada
    soc_aux = soc

    if ((soc_max - soc_aux) * cbat / (1 * ncd) > abs(pcd) * pbatmax * x):
        soc = soc_aux * (1 - sd) - pcd * pbatmax * x * 1 * ncd / cbat
        pbat = (-1) * pcd * pbatmax
        pgrid = pnet - pcd * pbatmax
    else:
        soc = soc_max * (1 - sd)
        pbat = (soc_max - soc_aux) * cbat / (x * 1 * ncd)
        pgrid = pnet + (soc_max - soc_aux) * cbat / (x * 1 * ncd)

    return round(pgrid, 4), round(pbat, 4), round(soc, 4)
