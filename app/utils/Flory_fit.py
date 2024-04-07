import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Creation des fonctions Flory
def Flory(logM,tau) -> np.ndarray:
    M = np.power(10,logM)
    return 1/np.log10(np.e)*tau**2*np.multiply(np.power(M,2),np.exp(-M*tau))

def fit_N_Flory(logM,w,nb_Flory) -> tuple:
    
    def Flory_multi(logM, *args) -> np.ndarray:
        if len(args) < 1:
            raise ValueError("Number of parameter must be at least 1")    
        elif len(args)%2 == 0:
            raise ValueError("number of parameter should not be a factor of 2")
        nb_Flory = len(args) // 2 + 1
        if nb_Flory == 1:
            return Flory(logM,args[0])
        else :
            Flory_sum = (1-np.sum([args[k] for k in range(0,nb_Flory-1)]))*Flory(logM,args[-1])
            for i in range(0,nb_Flory-1):
                Flory_sum += args[i]*Flory(logM,args[nb_Flory-1+i])
            return Flory_sum
    
    mz = np.ones(nb_Flory-1)*1/nb_Flory
    tau = np.linspace(0.0003, 0.0005, nb_Flory)
    p0 = list(mz) + list(tau)
    bounds = (0,1)
    params, pcov = curve_fit(Flory_multi, logM, w, p0 = p0, bounds=bounds)
    #  Calculate error and add mass for last Flory
    errors = np.sqrt(np.diag(pcov))
    if nb_Flory == 1:
            params = np.append(1.0, params)
            errors = np.append(0.0, errors)
    else:
        m_N = 1 - np.sum([params[0:nb_Flory]])
        std_m_N = np.sum([errors[0:nb_Flory]])
        params = np.insert(params, nb_Flory-1, m_N)
        errors = np.insert(errors, nb_Flory-1, std_m_N)

    return (params, errors) 

def get_model_prediction(logM,nb_Flory,params) -> np.ndarray:
    if nb_Flory == 1 :
        return Flory(logM,params[1]).reshape(1, -1)
    elif nb_Flory>1: 
        w_list = []
        for i in range(0,nb_Flory):
            w = params[i]*Flory(logM, params[nb_Flory+i])
            w_list.append(w)
        w_list.append(np.sum(w_list,axis=0))
        return np.array(w_list)
    return np.empty(1)

def plot_N_Flory(logM,w,nb_Flory,params) -> None:
    fig, ax = plt.subplots()
    if nb_Flory ==1:
        ax.plot(logM, Flory(logM,params[0]), label=f'Flory')
        print(f"Mn = {1/params[0]:.0f}")
    else:
        wlogM_tot = 0
        for i in range(0,nb_Flory-1):
            wlogM = params[i]*Flory(logM,params[nb_Flory-1+i])
            ax.plot(logM, wlogM, label=f'Flory_{i+1}')
            print(f"m_{i+1} = {params[i]:.3f}\nMn_{i+1} = {1/params[nb_Flory-1+i]:.0f}")
            wlogM_tot = np.add(wlogM_tot,wlogM)
        wlogM = (1-np.sum([params[k] for k in range(0,nb_Flory-1)]))*Flory(logM,params[-1])
        ax.plot(logM, wlogM, label=f'Flory_{nb_Flory}')
        print(f"m_{nb_Flory} = {(1-np.sum([params[k] for k in range(0,nb_Flory-1)])):.3f}\nMn_{nb_Flory} = {1/params[-1]:.0f}")
        wlogM_tot = np.add(wlogM_tot,wlogM)
        ax.plot(logM, wlogM_tot, 'r--', label=f'Flory_cumul')
    ax.plot(logM, w, 'k-', label='MMD')
    ax.set_xscale('linear')
    ax.grid()
    ax.legend()
    ax.set_title(f"Fitting par {nb_Flory} Flory")
    plt.show(block = True)

def r_squared(y_true, y_pred) -> float:
    """Calculate R-squared."""
    ss_total = np.sum((y_true - np.mean(y_true))**2)
    ss_residual = np.sum((y_true - y_pred)**2)
    r_squared = 1 - (ss_residual / ss_total)
    return r_squared