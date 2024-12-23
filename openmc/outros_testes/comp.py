#!/usr/bin/python

import os
os.system('clear')
print()
print("####################################################")
print("####################################################")
print("####                                             ###")
print("####   Reator de combustível metalico líquido    ###")
print("####         Liquid metal fuel reactor           ###")
print("####                                             ###")
print("####                                             ###")
print("####        Thalles Oliveira Campagnani          ###")
print("####                                             ###")
print("####                                             ###")
print("####################################################")
print("####################################################")
print()
print()

import openmc
import openmc.data
import numpy as np
import matplotlib.pyplot as plt


Altura_Tanque = 500
Tanque_Diametro = 500
energy = np.logspace(-5, np.log10(11E06), num=151)



print("################################################")
print("########  Trabalhando dados com fonte  #########")
print("################################################")
sp1 = openmc.StatePoint('statepoint.0percent.h5')
sp2 = openmc.StatePoint('statepoint.20percent.h5')

uncertainty = 0.05

flux_espectro_fuel1  = sp1.get_tally(scores=['flux'], name='Fluxo espectro interno comb1')
flux_espectro_fuel2  = sp1.get_tally(scores=['flux'], name='Fluxo espectro interno comb2')

# Espectro
flux_espectro_fuel1_mean    = flux_espectro_fuel1.mean
flux_espectro_fuel1_dev     = flux_espectro_fuel1.std_dev
flux_espectro_fuel2_mean    = flux_espectro_fuel2.mean
flux_espectro_fuel2_dev     = flux_espectro_fuel2.std_dev


### ESPECTRO DO COMBUSTÍVEL ###
print()
print(' Espectro de fluxo:')
print()
flux_spec_fuel1_mean      = []
flux_spec_fuel1_dev       = []
flux_spec_fuel1_energy    = []
V=Altura_Tanque/2 * np.pi * (Tanque_Diametro/4)**2
for i in range(0,len(energy)-1):
    fluxo = flux_espectro_fuel1_mean[i][0][0]/V
    incerteza = flux_espectro_fuel1_dev[i][0][0]/V
    if incerteza/fluxo < uncertainty:
        flux_spec_fuel1_mean.append(fluxo)
        flux_spec_fuel1_dev.append(incerteza)
        flux_spec_fuel1_energy.append(energy[i+1])

flux_spec_fuel2_mean      = []
flux_spec_fuel2_dev       = []
flux_spec_fuel2_energy    = []
#V=Altura_Tanque/2 * np.pi * ((Tanque_Diametro/2)**2-(Tanque_Diametro/4)**2)
for i in range(0,len(energy)-1):
    fluxo = flux_espectro_fuel2_mean[i][0][0]/V*1.7
    incerteza = flux_espectro_fuel2_dev[i][0][0]/V
    if incerteza/fluxo < uncertainty:
        flux_spec_fuel2_mean.append(fluxo)
        flux_spec_fuel2_dev.append(incerteza)
        flux_spec_fuel2_energy.append(energy[i+1])


################################################################################################################################
# ESPECTRO DE ENERGIA

# Criando a figura e o eixo principal
fig, ax1 = plt.subplots()

#Estilo de cores
plt.style.use('seaborn-v0_8-paper')

# Escala logarítimica
plt.xscale('log')
plt.yscale('log')

ax1.plot(flux_spec_fuel1_energy, flux_spec_fuel1_mean, color='xkcd:red', linestyle='-', linewidth=1,marker='^', markersize=5, label='Interno')
plt.plot(flux_spec_fuel2_energy, flux_spec_fuel2_mean, color='xkcd:royal blue', linestyle='-', linewidth=1,marker='.', markersize=7, label='Externo')

# Títulos e legenda
plt.title('Flux Spectrum', fontsize=24)
plt.ylabel('Flux (neutrons.cm⁻².s⁻¹)', fontsize=20)
plt.xlabel('Energy (eV)', fontsize=20)
plt.legend(fontsize=20, loc='upper left')

# Gridlines 
plt.grid(True, which='both', axis='y', linestyle='--', linewidth=0.2, color='gray')
plt.grid(True, which='both', axis='x', linestyle='--', linewidth=0.2, color='gray') # which='major'
plt.tick_params(axis='both', which='major', labelsize=16)



plt.tight_layout()
plt.show()
exit(0)

ax2 = ax1.twinx()
ax2.set_yscale('log')


u235 = openmc.data.IncidentNeutron.from_hdf5("/SSD3/nuclear-data/endfb-viii.0-hdf5/neutron/U235.h5")
energies = u235.energy['294K']
total_xs = u235[18].xs['294K'](energies)
ax2.plot(energies, total_xs, color='xkcd:green', linestyle='-', linewidth=1, label='U235')


u238 = openmc.data.IncidentNeutron.from_hdf5("/SSD3/nuclear-data/endfb-viii.0-hdf5/neutron/U238.h5")
energies = u238.energy['294K']
total_xs = u238[18].xs['294K'](energies)
ax2.plot(energies, total_xs, color='xkcd:green', linestyle='-', linewidth=1, label='U238')


ax2.set_ylabel('Cross section (b)', color='g')
ax2.tick_params(axis='y', labelcolor='g')


plt.show()

