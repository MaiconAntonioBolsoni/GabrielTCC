def carga_bateria(pcd, soc, pnet, nbrt, ncd, sd, soc_min, soc_max, cbat, pbatmax):
    """
    Função para calcular o carregamento da bateria.

    Parâmetros:
    pcd (float): Percentual de carga/descarga
    soc (float): Estado de carga atual da bateria
    pnet (float): Potência líquida da rede
    nbrt (float): Eficiência de ida e volta
    ncd (float): Eficiência de carga e descarga
    sd (float): Taxa de auto-descarga
    soc_min (float): Estado de carga mínimo
    soc_max (float): Estado de carga máximo
    cbat (float): Capacidade da bateria
    pbatmax (float): Potência máxima da bateria

    Retorna:
    tuple: (pgrid, pbat, soc)
    """

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
