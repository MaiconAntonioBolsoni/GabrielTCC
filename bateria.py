import numpy as np
from carga_bateria import carga_bateria
from carga_bateria_excedente import carga_bateria_excedente
from descarga_bateria_pico import descarga_bateria_pico
from descarga_bateria_ponta import descarga_bateria_ponta
from descarga_bateria import descarga_bateria
def bateria(pop, Pnet, time):
    # Dados da bateria
    Nbrt = 0.98  # eficiência de ida e volta (%)
    Ncd = 0.95   # eficiência de carga e descarga (%)
    Sd = 0.02/96 # taxa de auto descarga (%)
    SOCmin = 0.1 # estado de carga mínimo (%)
    SOCmax = 0.95 # estado de carga máximo (%)
    Cbat = 6000  # capacidade da bateria (kWh)
    Pbatmax = Cbat/3 # potência máxima de carga/descarga
    precoBAT = 0
    Dpeak = 10000 * pop[-7] / 96
    SOCi = 0.5  # Estado de carga inicial

    SOCaux = SOCi

    # Calcula os valores de Pcd para diferentes períodos
    Pcd = [2 * (pop[-6+i] / 96 - 0.5) for i in range(6)]

    # Inicializa arrays para armazenar resultados
    Pt = np.zeros(len(Pnet))
    Pbat = np.zeros(len(Pnet))
    SOC = np.zeros(len(Pnet))

    for i in range(len(Pnet)):
        if Pnet[i] < 0:
            # Carrega a bateria com excedente de energia
            Pt[i], Pbat[i], SOC[i] = carga_bateria_excedente(SOCaux, Pnet[i], Nbrt, Ncd, Sd, SOCmin, SOCmax, Cbat, Pbatmax)
        else:
            if time[i] == 7:
                # Descarrega a bateria no horário de ponta
                Pt[i], Pbat[i], SOC[i] = descarga_bateria_ponta(1, SOCaux, Pnet[i], Nbrt, Ncd, Sd, SOCmin, SOCmax, Cbat, Pbatmax)
            else:
                if Pnet[i] > Dpeak:
                    # Descarrega a bateria para reduzir pico de demanda
                    Pt[i], Pbat[i], SOC[i] = descarga_bateria_pico(Pcd[time[i]-1], SOCaux, Pnet[i], Nbrt, Ncd, Sd, SOCmin, SOCmax, Cbat, Pbatmax, Dpeak)
                else:
                    if Pcd[time[i]-1] > 0:
                        # Descarrega a bateria normalmente
                        Pt[i], Pbat[i], SOC[i] = descarga_bateria(Pcd[time[i]-1], SOCaux, Pnet[i], Nbrt, Ncd, Sd, SOCmin, SOCmax, Cbat, Pbatmax)
                    else:
                        # Carrega a bateria normalmente
                        Pt[i], Pbat[i], SOC[i] = carga_bateria(Pcd[time[i]-1], SOCaux, Pnet[i], Nbrt, Ncd, Sd, SOCmin, SOCmax, Cbat, Pbatmax)
        SOCaux = SOC[i]

    return Pt, Pbat, SOC, precoBAT, Cbat, SOCi

test_cases = [
    ([-500, -600, -700, -800, -900, -1000], "Excesso de geração"),
    ([600, 700, 800, 900, 1000, 1100], "Alto consumo de energia")

]

pop = [10000, 12000, 11000, 10500, 11500, 12500, 13000]
time = [1, 2, 3, 4, 5, 6]

for Pnet, desc in test_cases:
    print(f"\nTeste: {desc}")
    Pt, Pbat, SOC, precoBAT, Cbat, SOCi = bateria(pop, Pnet, time)
    print("Pt:", Pt)
    print("Pbat:", Pbat)
    print("SOC:", np.round(SOC, 4))