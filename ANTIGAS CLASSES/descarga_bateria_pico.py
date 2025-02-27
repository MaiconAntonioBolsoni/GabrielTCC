def descarga_bateria_pico(pcd, soc, p_net, n_brt, n_cd, sd, soc_min, soc_max, c_bat, p_bat_max, d_peak):
    """
    Parâmetros:
    pcd (float): Percentual de carga/descarga
    soc (float): Estado de carga atual da bateria
    p_net (float): Potência líquida da rede
    n_brt (float): Eficiência de ida e volta
    n_cd (float): Eficiência de carga e descarga
    sd (float): Taxa de auto-descarga
    soc_min (float): Estado de carga mínimo
    soc_max (float): Estado de carga máximo
    c_bat (float): Capacidade da bateria
    p_bat_max (float): Potência máxima da bateria
    d_peak (float): Demanda de pico

    Retorna:
    tuple: (p_grid, p_bat, soc)
    Função para calcular a descarga da bateria durante picos de demanda.
    """
    fracao_hora = 0.25  # Fração de hora utilizada
    soc_aux = soc
    
    if (p_net - d_peak) > pcd * p_bat_max:
        if p_bat_max > (p_net - d_peak):
            if ((soc_aux - soc_min) * c_bat * n_brt * n_cd > (p_net - d_peak) * fracao_hora):
                soc = soc_aux * (1 - sd) - (p_net - d_peak) * fracao_hora / (c_bat * n_brt * n_cd)
                p_bat = - (p_net - d_peak)
                p_grid = d_peak
            else:
                soc = soc_min * (1 - sd)
                p_bat = - (soc_aux - soc_min) * c_bat * n_brt * n_cd / fracao_hora
                p_grid = p_net - (soc_aux - soc_min) * c_bat * n_brt * n_cd / fracao_hora
        else:
            if ((soc_aux - soc_min) * c_bat * n_brt * n_cd > p_bat_max * fracao_hora):
                soc = soc_aux * (1 - sd) - p_bat_max * fracao_hora / (c_bat * n_brt * n_cd)
                p_bat = -p_bat_max
                p_grid = p_net - p_bat_max
            else:
                soc = soc_min * (1 - sd)
                p_bat = - (soc_aux - soc_min) * c_bat * n_brt * n_cd / fracao_hora
                p_grid = p_net - (soc_aux - soc_min) * c_bat * n_brt * n_cd / fracao_hora
    else:
        if pcd * p_bat_max > p_net:
            if ((soc_aux - soc_min) * c_bat * n_brt * n_cd > p_net * fracao_hora):
                soc = soc_aux * (1 - sd) - p_net * fracao_hora / (c_bat * n_brt * n_cd)
                p_bat = -p_net
                p_grid = 0
            else:
                soc = soc_min * (1 - sd)
                p_bat = - (soc_aux - soc_min) * c_bat * n_brt * n_cd / fracao_hora
                p_grid = p_net - (soc_aux - soc_min) * c_bat * n_brt * n_cd / fracao_hora
        else:
            if ((soc_aux - soc_min) * c_bat * n_brt * n_cd > pcd * p_bat_max * fracao_hora):
                soc = soc_aux * (1 - sd) - pcd * p_bat_max * fracao_hora / (c_bat * n_brt * n_cd)
                p_bat = -pcd * p_bat_max
                p_grid = p_net - pcd * p_bat_max
            else:
                soc = soc_min * (1 - sd)
                p_bat = - (soc_aux - soc_min) * c_bat * n_brt * n_cd / fracao_hora
                p_grid = p_net - (soc_aux - soc_min) * c_bat * n_brt * n_cd / fracao_hora
    
    return p_grid, p_bat, soc