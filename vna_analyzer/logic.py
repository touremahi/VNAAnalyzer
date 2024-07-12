"""Contains the processing functions for the VNA.
"""
import os
import re
import numpy as np
import skrf as rf
import pandas as pd

def load_network(filename):
    """Import data from a file.
    """
    df = pd.read_csv(filename, sep=r"\s+", decimal=',', header=None)

    name = os.path.dirname(filename).split('/')[-1]
    base_name = os.path.basename(filename).split('.')[0]
    if contains_number(base_name):
        name = base_name

    df.columns = [
        'freq',
        'S11_mag','S11_phase',
        'S12_mag','S12_phase',
        'S21_mag','S21_phase',
        'S22_mag','S22_phase'
        ]

    # Convertir en matrice de paramètres S
    fr = df['freq'].to_numpy()
    s_params = np.zeros((len(fr), 2, 2), dtype=complex)
    s_params[:,0,0] = df['S11_mag'].to_numpy() * np.exp(1j*df['S11_phase'].to_numpy())
    s_params[:,0,1] = df['S12_mag'].to_numpy() * np.exp(1j*df['S12_phase'].to_numpy())
    s_params[:,1,0] = df['S21_mag'].to_numpy() * np.exp(1j*df['S21_phase'].to_numpy())
    s_params[:,1,1] = df['S22_mag'].to_numpy() * np.exp(1j*df['S22_phase'].to_numpy())

    frequency = rf.Frequency.from_f(fr, unit='Mhz')

    return rf.Network(frequency=frequency, s=s_params, name=name)

def contains_number(string):
    """
    Checks if a given string contains a number.
    
    Args:
        string (str): The string to check.
    
    Returns:
        bool: True if the string contains a number, False otherwise.
    """
    return bool(re.search(r'\d', string))
