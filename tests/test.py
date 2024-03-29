from app.utils.Flory_fit import fit_N_Flory, plot_N_Flory
import numpy as np
import pandas as pd

# Import du fichier
file_path = 'tests\GPCIR TOTAL-23-0267.xls'
df_file = pd.read_excel(file_path, sheet_name='Data')
df_data = df_file[['LogM conventional ','Weight fraction / LogM ']]
df_data = df_data.rename(columns={'LogM conventional ':'LogM','Weight fraction / LogM ':'w'})
df_data = df_data.dropna()
df_data = df_data[df_data['LogM'] > 2.2]
df_data['M'] = np.power(10,df_data['LogM'].values)

# Interpolation des valeurs sur 1000 points
logM = np.linspace(np.min(df_data['LogM']),np.max(df_data['LogM']),1000)
w = np.interp(logM, df_data['LogM'].values[::-1], df_data['w'].values[::-1], )

# Lancement du fitting et affichage des résultats
for N in [1,2,3,4,5,6]:
    print(f"Fitting par {N} Flory")
    try:
        params = fit_N_Flory(logM, w, N)
        plot_N_Flory(logM,w,N,params)
    except Exception as e:
        print("Une erreur est survenue lors du fit:",e)