def carga_bateria_excedente(soc, p_net, n_brt, n_cd, sd, soc_min, soc_max, c_bat, p_bat_max):
    """
    Função para calcular o carregamento da bateria com excedente de energia.

    Parâmetros:
    soc (float): Estado de carga atual da bateria
    p_net (float): Potência líquida da rede (negativa para excedente)
    n_brt (float): Eficiência de ida e volta
    n_cd (float): Eficiência de carga e descarga
    sd (float): Taxa de auto-descarga
    soc_min (float): Estado de carga mínimo
    soc_max (float): Estado de carga máximo
    c_bat (float): Capacidade da bateria
    p_bat_max (float): Potência máxima da bateria

    Retorna:
    tuple: (p_grid, p_bat, soc)
    """

    fracao_hora = 0.25  # Fração de hora utilizada
    soc_aux = soc

    if (soc_max - soc_aux) * c_bat / (1 * n_cd) > abs(p_net) * fracao_hora:
        # Tem espaço para armazenar toda energia
        if p_bat_max > abs(p_net):
            # Consegue absorver toda potência
            soc = soc_aux * (1 - sd) - p_net * fracao_hora * 1 * n_cd / c_bat
            p_bat = (-1) * p_net
            p_grid = 0
        else:
            # Só consegue armazenar p_bat_max
            soc = soc_aux * (1 - sd) + p_bat_max * fracao_hora * 1 * n_cd / c_bat
            p_bat = p_bat_max
            p_grid = p_net + p_bat_max
    else:
        if p_bat_max > abs(p_net):
            soc = soc_max * (1 - sd)
            p_bat = (soc_max - soc_aux) * c_bat / (fracao_hora * 1 * n_cd)
            p_grid = p_net + (soc_max - soc_aux) * c_bat / (fracao_hora * 1 * n_cd)
        else:
            if (soc_max - soc_aux) * c_bat / (1 * n_cd) > p_bat_max * fracao_hora:
                soc = soc_aux * (1 - sd) + p_bat_max * fracao_hora * 1 * n_cd / c_bat
                p_bat = p_bat_max
                p_grid = p_net + p_bat_max
            else:
                soc = soc_max * (1 - sd)
                p_bat = (soc_max - soc_aux) * c_bat / (fracao_hora * 1 * n_cd)
                p_grid = p_net + (soc_max - soc_aux) * c_bat / (fracao_hora * 1 * n_cd)

    return p_grid, p_bat, soc
