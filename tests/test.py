from app.utils.Flory_fit import fit_N_Flory, plot_N_Flory
from app.utils.GPC_data import GPC
import numpy as np
import pandas as pd

# pyinstaller --onefile mon_scripts.py 

# Import du fichier
# file_path = 'tests\GPCIR TOTAL-23-0259.xls'
# file_path = 'tests\GPCIR TOTAL-23-0263.xls'
# file_path = 'tests\GPCIR TOTAL-23-0267.xls'
# data = GPC()
# data.import_file(file_path)

# print(data)


# Lancement du fitting et affichage des résultats
# for N in [1,2,3,4,5,6]:
#     print(f"Fitting par {N} Flory")
#     try:
#         params = fit_N_Flory(logM, w, N)
#         plot_N_Flory(logM,w,N,params)
#     except Exception as e:
#         print("Une erreur est survenue lors du fit:",e)