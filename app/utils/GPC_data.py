# GPC_data.py
import pandas as pd
import numpy as np


# File to import .xls file and treat GPC data to use it

class GPC():
    def __init__(self):
        self.logM = None
        self.w = None
        self.dict_info = {}

    def __repr__(self) -> str:
        return "\n".join(
            ['{:<13}'.format(key) + " : " + val for key,val in self.dict_info.items()])

    def import_file(self, file_path: str):
        # Lecture des données
        df_file = pd.read_excel(file_path, sheet_name='Data')
        # Récupération des colonnes LogM et Proba
        df_data = df_file[['LogM conventional ','Weight fraction / LogM ']]
        df_data = df_data.rename(columns={'LogM conventional ':'LogM','Weight fraction / LogM ':'w'})
        df_data = df_data.dropna()
        df_data = df_data[df_data['LogM'] > 2.2]
        # Interpolation
        self.logM = np.linspace(np.min(df_data['LogM']),np.max(df_data['LogM']),1000)
        self.w = np.interp(self.logM, df_data['LogM'].values[::-1], df_data['w'].values[::-1], )
        # Lecture des informations
        df_file = pd.read_excel(file_path, sheet_name='Results')
        df_file = df_file.iloc[:,1:3]
        df_file.set_index(df_file.columns[0], drop=True, inplace=True)
        self.dict_info['Project'] = df_file.loc['Project #',df_file.columns[0]]
        self.dict_info['Sample'] = df_file.loc['Name',df_file.columns[0]]
        self.dict_info['Description'] = df_file.loc['Description',df_file.columns[0]]