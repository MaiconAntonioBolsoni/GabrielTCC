def descarga_bateria(pcd, soc, p_net, n_brt, n_cd, sd, soc_min, soc_max, c_bat, p_bat_max):
    fracao_hora = 0.25  # Fração de hora utilizada
    soc_aux = soc
    
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