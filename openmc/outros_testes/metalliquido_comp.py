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


########## Tório
print("################################################")
print("################################################")
print("################################################")
print("################################################")
print("################################################")
print("############                         ###########")
print("############        T O R I O        ###########")
print("############                         ###########")
print("################################################")
print("################################################")
print("################################################")
print("################################################")
print("################################################")
print("################################################")
print()
print()
print()


print("################################################")
print("############ Definição dos Materiais ###########")
print("################################################")

#Cria objeto para armazenar os materiais criados
materiais = openmc.Materials()

#Já definir as cores dos materiais para os 'plots'
colors = {}

#Temperatura (°C)	Temperatura (K)	Densidade Aproximada (g/cm³)
#20 	19,1
#100	18,9
#500	18,5
#1000	18,0
#1132 	~17,8 #(ponto de fusão)
#1200	~17,4
#1400	~17,0
#1600	~16,5
#1800	~16,0
#2000	~15,6
#2.000	~15,6
#2.500	~14,8
#3.000	~14,0
#3.500	~13,3
#4.000	~12,6
#4.500	~12,0
#5.000	~11,5
#5.500	~11,0
#6.000	~10,5

combustivel = openmc.Material(name='Uránio metálico líquido')
combustivel.add_nuclide('U233', 20, percent_type='ao')
combustivel.add_nuclide('Th232', 80, percent_type='ao')
combustivel.set_density('g/cm3', 10.5)#12.6)
colors["combustivel"] = "yellow"
materiais.append(combustivel)

ar = openmc.Material(name='Ar')
ar.add_nuclide('N14' , 7.7826E-01 , percent_type='ao')
ar.add_nuclide('N15' , 2.8589E-03 , percent_type='ao')
ar.add_nuclide('O16' , 1.0794E-01 , percent_type='ao')
ar.add_nuclide('O17' , 1.0156E-01 , percent_type='ao')
ar.add_nuclide('O18' , 3.8829E-05 , percent_type='ao')
ar.add_nuclide('Ar36', 2.6789E-03 , percent_type='ao')
ar.add_nuclide('Ar38', 3.4177E-03 , percent_type='ao')
ar.add_nuclide('Ar40', 3.2467E-03 , percent_type='ao')
ar.set_density('g/cm3', 0.001225)
colors["ar"] = "pink"
materiais.append(ar)


SS304 = openmc.Material(name='Aço INOX')
SS304.add_element('C',  4.3000E-04 , percent_type = 'wo')
SS304.add_element('Cr', 1.9560E-01 , percent_type = 'wo')
SS304.add_element('Ni', 9.6600E-02 , percent_type = 'wo')
SS304.add_element('Mo', 8.9000E-03 , percent_type = 'wo')
SS304.add_element('Mn', 5.4000E-04 , percent_type = 'wo')
SS304.add_element('Si', 5.0000E-04 , percent_type = 'wo')
SS304.add_element('Cu', 2.0000E-05 , percent_type = 'wo')
SS304.add_element('Co', 3.0000E-05 , percent_type = 'wo')
SS304.add_element('P',  2.7000E-04 , percent_type = 'wo')
SS304.add_element('S',  1.0000E-04 , percent_type = 'wo')
SS304.add_element('N',  1.4000E-04 , percent_type = 'wo')
SS304.add_element('Fe', 6.9687E-01 , percent_type = 'wo')
SS304.set_density('g/cm3', 7.92)
colors["SS304"] = "gray"
materiais.append(SS304)


#materiais.cross_sections = '/opt/nuclear-data/endfb-viii.0-hdf5/cross_sections.xml' 
materiais.export_to_xml()










print("################################################")
print("############ Definição da Geometria  ###########")
print("################################################")


Altura_Tanque = 500
Tanque_Diametro = 500


plano_fundo_tanque_superior     = openmc.ZPlane(z0=-Altura_Tanque/2,boundary_type='vacuum')
plano_tampa_tanque_inferior     = openmc.ZPlane(z0= Altura_Tanque/2,boundary_type='vacuum')
cilindro_raio_interno_tanque    = openmc.ZCylinder(r=Tanque_Diametro/2,boundary_type='vacuum')#reflective
cilindro_raio_externo_canal_central    = openmc.ZCylinder(r=25,)



celula_tanque                   = openmc.Cell(fill=combustivel,region=
                                                                        +plano_fundo_tanque_superior
                                                                        &-plano_tampa_tanque_inferior
                                                                        &-cilindro_raio_interno_tanque
                                                                        #&+cilindro_raio_externo_canal_central
                                                                        )

celula_canal_central                   = openmc.Cell(fill=ar,region=
                                                                        +plano_fundo_tanque_superior
                                                                        &-plano_tampa_tanque_inferior
                                                                        &-cilindro_raio_externo_canal_central
                                                                        )

############ Exportar Geometrias
geometria = openmc.Geometry([celula_tanque])#,celula_canal_central])
geometria.export_to_xml()








print("################################################")
print("########### Definição da Simulação  ############")
print("################################################")

settings = openmc.Settings()
settings.particles = 50000
settings.batches = 200
settings.inactive = 40
settings.source = openmc.IndependentSource(space=openmc.stats.Point((0, 0, 0)))
settings.output = {'tallies': False}
settings.export_to_xml()
    



print("################################################")
print("###########  Definição de Tallies   ############")
print("################################################")

energy = np.logspace(-5, np.log10(11E06), num=151)
#energy = [1.0000E-05, 1.0, 5.0E+03, 20.0E+06]
energy_filter = openmc.EnergyFilter(energy)

# ESPECTRO COMUM MÉDIO INTERNO AO COMBUSTÍVEL
tally_spectrum_fuel1 = openmc.Tally(name='Fluxo espectro interno comb1') # F34
tally_spectrum_fuel1.scores.append('flux')
tally_spectrum_fuel1.filters.append(energy_filter)
tally_spectrum_fuel1.filters.append(
    openmc.MeshFilter(
        openmc.CylindricalMesh(
            r_grid=(0, Tanque_Diametro/4), #De 0 ao raio interno do combustivel
            z_grid=(-Altura_Tanque/4,Altura_Tanque/4,), #No nivel da fonte
            origin=(0,0,0)
            )
        )
    )

tally_spectrum_fuel2 = openmc.Tally(name='Fluxo espectro interno comb2') # F34
tally_spectrum_fuel2.scores.append('flux')
tally_spectrum_fuel2.filters.append(energy_filter)
tally_spectrum_fuel2.filters.append(
    openmc.MeshFilter(
        openmc.CylindricalMesh(
            r_grid=(Tanque_Diametro/4, Tanque_Diametro/2), #De 0 ao raio interno do combustivel
            z_grid=(-Altura_Tanque/4,Altura_Tanque/4,), #No nivel da fonte
            origin=(0,0,0)
            )
        )
    )

############# Coleção de tallies ##############
vetor_tallies = []
vetor_tallies.append(tally_spectrum_fuel1)
vetor_tallies.append(tally_spectrum_fuel2)
tallies = openmc.Tallies(vetor_tallies)
tallies.export_to_xml()



print("################################################")
print("###########        Executando       ############")
print("################################################")
openmc.run()




########## Tório
print("################################################")
print("################################################")
print("################################################")
print("################################################")
print("################################################")
print("############                         ###########")
print("############       U R A N I O       ###########")
print("############                         ###########")
print("################################################")
print("################################################")
print("################################################")
print("################################################")
print("################################################")
print("################################################")
print()
print()
print()











print("################################################")
print("############ Definição dos Materiais ###########")
print("################################################")

#Cria objeto para armazenar os materiais criados
materiais2 = openmc.Materials()

#Já definir as cores dos materiais para os 'plots'
colors2 = {}

#Temperatura (°C)	Temperatura (K)	Densidade Aproximada (g/cm³)
#20 	19,1
#100	18,9
#500	18,5
#1000	18,0
#1132 	~17,8 #(ponto de fusão)
#1200	~17,4
#1400	~17,0
#1600	~16,5
#1800	~16,0
#2000	~15,6
#2.000	~15,6
#2.500	~14,8
#3.000	~14,0
#3.500	~13,3
#4.000	~12,6
#4.500	~12,0
#5.000	~11,5
#5.500	~11,0
#6.000	~10,5

combustivel2 = openmc.Material(name='Uránio metálico líquido')
combustivel2.add_nuclide('Pu239', 20, percent_type='ao')
#combustivel2.add_nuclide('U235', 20, percent_type='ao')
combustivel2.add_nuclide('U238', 80, percent_type='ao')
combustivel2.set_density('g/cm3', 10.5)#12.6)
colors2["combustivel"] = "yellow"
materiais2.append(combustivel2)

ar2 = openmc.Material(name='Ar')
ar2.add_nuclide('N14' , 7.7826E-01 , percent_type='ao')
ar2.add_nuclide('N15' , 2.8589E-03 , percent_type='ao')
ar2.add_nuclide('O16' , 1.0794E-01 , percent_type='ao')
ar2.add_nuclide('O17' , 1.0156E-01 , percent_type='ao')
ar2.add_nuclide('O18' , 3.8829E-05 , percent_type='ao')
ar2.add_nuclide('Ar36', 2.6789E-03 , percent_type='ao')
ar2.add_nuclide('Ar38', 3.4177E-03 , percent_type='ao')
ar2.add_nuclide('Ar40', 3.2467E-03 , percent_type='ao')
ar2.set_density('g/cm3', 0.001225)
colors2["ar"] = "pink"
materiais2.append(ar2)


SS3042 = openmc.Material(name='Aço INOX')
SS3042.add_element('C',  4.3000E-04 , percent_type = 'wo')
SS3042.add_element('Cr', 1.9560E-01 , percent_type = 'wo')
SS3042.add_element('Ni', 9.6600E-02 , percent_type = 'wo')
SS3042.add_element('Mo', 8.9000E-03 , percent_type = 'wo')
SS3042.add_element('Mn', 5.4000E-04 , percent_type = 'wo')
SS3042.add_element('Si', 5.0000E-04 , percent_type = 'wo')
SS3042.add_element('Cu', 2.0000E-05 , percent_type = 'wo')
SS3042.add_element('Co', 3.0000E-05 , percent_type = 'wo')
SS3042.add_element('P',  2.7000E-04 , percent_type = 'wo')
SS3042.add_element('S',  1.0000E-04 , percent_type = 'wo')
SS3042.add_element('N',  1.4000E-04 , percent_type = 'wo')
SS3042.add_element('Fe', 6.9687E-01 , percent_type = 'wo')
SS3042.set_density('g/cm3', 7.92)
colors2["SS304"] = "gray"
materiais2.append(SS3042)


#materiais.cross_sections = '/opt/nuclear-data/endfb-viii.0-hdf5/cross_sections.xml' 
materiais2.export_to_xml()

print("################################################")
print("############ Definição da Geometria  ###########")
print("################################################")


Altura_Tanque = 500
Tanque_Diametro = 500


plano_fundo_tanque_superior     = openmc.ZPlane(z0=-Altura_Tanque/2,boundary_type='vacuum')
plano_tampa_tanque_inferior     = openmc.ZPlane(z0= Altura_Tanque/2,boundary_type='vacuum')
cilindro_raio_interno_tanque    = openmc.ZCylinder(r=Tanque_Diametro/2,boundary_type='vacuum')#reflective
cilindro_raio_externo_canal_central    = openmc.ZCylinder(r=25,)



celula_tanque                   = openmc.Cell(fill=combustivel2,region=
                                                                        +plano_fundo_tanque_superior
                                                                        &-plano_tampa_tanque_inferior
                                                                        &-cilindro_raio_interno_tanque
                                                                        #&+cilindro_raio_externo_canal_central
                                                                        )

celula_canal_central                   = openmc.Cell(fill=ar2,region=
                                                                        +plano_fundo_tanque_superior
                                                                        &-plano_tampa_tanque_inferior
                                                                        &-cilindro_raio_externo_canal_central
                                                                        )

############ Exportar Geometrias
geometria = openmc.Geometry([celula_tanque])#,celula_canal_central])
geometria.export_to_xml()

print("################################################")
print("###########  Definição de Tallies   ############")
print("################################################")

energy = np.logspace(-5, np.log10(11E06), num=151)
#energy = [1.0000E-05, 1.0, 5.0E+03, 20.0E+06]
energy_filter = openmc.EnergyFilter(energy)

# ESPECTRO COMUM MÉDIO INTERNO AO COMBUSTÍVEL
tally_spectrum_fuel1 = openmc.Tally(name='Fluxo espectro interno comb1') # F34
tally_spectrum_fuel1.scores.append('flux')
tally_spectrum_fuel1.filters.append(energy_filter)
tally_spectrum_fuel1.filters.append(
    openmc.MeshFilter(
        openmc.CylindricalMesh(
            r_grid=(0, Tanque_Diametro/4), #De 0 ao raio interno do combustivel
            z_grid=(-Altura_Tanque/4,Altura_Tanque/4,), #No nivel da fonte
            origin=(0,0,0)
            )
        )
    )

tally_spectrum_fuel2 = openmc.Tally(name='Fluxo espectro interno comb2') # F34
tally_spectrum_fuel2.scores.append('flux')
tally_spectrum_fuel2.filters.append(energy_filter)
tally_spectrum_fuel2.filters.append(
    openmc.MeshFilter(
        openmc.CylindricalMesh(
            r_grid=(Tanque_Diametro/4, Tanque_Diametro/2), #De 0 ao raio interno do combustivel
            z_grid=(-Altura_Tanque/4,Altura_Tanque/4,), #No nivel da fonte
            origin=(0,0,0)
            )
        )
    )

############# Coleção de tallies ##############
vetor_tallies = []
vetor_tallies.append(tally_spectrum_fuel1)
vetor_tallies.append(tally_spectrum_fuel2)
tallies = openmc.Tallies(vetor_tallies)
tallies.export_to_xml()


print("################################################")
print("########### Definição da Simulação  ############")
print("################################################")

settings2 = openmc.Settings()
settings2.particles = 50000
settings2.batches = 201
settings2.inactive = 40
settings2.source = openmc.IndependentSource(space=openmc.stats.Point((0, 0, 0)))
settings2.output = {'tallies': False}
settings2.export_to_xml()
    
print("################################################")
print("###########        Executando       ############")
print("################################################")
openmc.run()




























print("################################################")
print("########  Trabalhando dados com fonte  #########")
print("################################################")
sp = openmc.StatePoint('statepoint.'+str(settings.batches)+'.h5')
sp2 = openmc.StatePoint('statepoint.'+str(settings2.batches)+'.h5')

uncertainty = 0.05

flux_espectro_fuel1  = sp.get_tally(scores=['flux'], name='Fluxo espectro interno comb1')
flux_espectro_fuel2  = sp.get_tally(scores=['flux'], name='Fluxo espectro interno comb2')
flux_espectro_fuel3  = sp2.get_tally(scores=['flux'], name='Fluxo espectro interno comb1')
flux_espectro_fuel4  = sp2.get_tally(scores=['flux'], name='Fluxo espectro interno comb2')

# Espectro
flux_espectro_fuel1_mean    = flux_espectro_fuel1.mean
flux_espectro_fuel1_dev     = flux_espectro_fuel1.std_dev
flux_espectro_fuel2_mean    = flux_espectro_fuel2.mean
flux_espectro_fuel2_dev     = flux_espectro_fuel2.std_dev
flux_espectro_fuel3_mean    = flux_espectro_fuel3.mean
flux_espectro_fuel3_dev     = flux_espectro_fuel3.std_dev
flux_espectro_fuel4_mean    = flux_espectro_fuel4.mean
flux_espectro_fuel4_dev     = flux_espectro_fuel4.std_dev

### ESPECTRO DO COMBUSTÍVEL ###
print()
print(' Espectro de fluxo:')
print()
flux_spec_fuel1_mean      = []
flux_spec_fuel1_dev       = []
flux_spec_fuel1_energy    = []
V=Altura_Tanque/2 * np.pi * (Tanque_Diametro/4)**2
for i in range(0,len(energy)-1):
    fluxo = flux_espectro_fuel1_mean[i][0][0]
    incerteza = flux_espectro_fuel1_dev[i][0][0]
    if incerteza/fluxo < uncertainty:
        flux_spec_fuel1_mean.append(fluxo)
        flux_spec_fuel1_dev.append(incerteza)
        flux_spec_fuel1_energy.append(energy[i+1])

flux_spec_fuel2_mean      = []
flux_spec_fuel2_dev       = []
flux_spec_fuel2_energy    = []
V=Altura_Tanque/2 * np.pi * ((Tanque_Diametro/2)**2-(Tanque_Diametro/4)**2)
for i in range(0,len(energy)-1):
    fluxo = flux_espectro_fuel2_mean[i][0][0]
    incerteza = flux_espectro_fuel2_dev[i][0][0]
    if incerteza/fluxo < uncertainty:
        flux_spec_fuel2_mean.append(fluxo)
        flux_spec_fuel2_dev.append(incerteza)
        flux_spec_fuel2_energy.append(energy[i+1])


flux_spec_fuel3_mean      = []
flux_spec_fuel3_dev       = []
flux_spec_fuel3_energy    = []
V=Altura_Tanque/2 * np.pi * (Tanque_Diametro/4)**2
for i in range(0,len(energy)-1):
    fluxo = flux_espectro_fuel3_mean[i][0][0]
    incerteza = flux_espectro_fuel3_dev[i][0][0]
    if incerteza/fluxo < uncertainty:
        flux_spec_fuel3_mean.append(fluxo)
        flux_spec_fuel3_dev.append(incerteza)
        flux_spec_fuel3_energy.append(energy[i+1])

flux_spec_fuel4_mean      = []
flux_spec_fuel4_dev       = []
flux_spec_fuel4_energy    = []
V=Altura_Tanque/2 * np.pi * ((Tanque_Diametro/2)**2-(Tanque_Diametro/4)**2)
for i in range(0,len(energy)-1):
    fluxo = flux_espectro_fuel4_mean[i][0][0]
    incerteza = flux_espectro_fuel4_dev[i][0][0]
    if incerteza/fluxo < uncertainty:
        flux_spec_fuel4_mean.append(fluxo)
        flux_spec_fuel4_dev.append(incerteza)
        flux_spec_fuel4_energy.append(energy[i+1])
################################################################################################################################
# ESPECTRO DE ENERGIA

# Criando a figura e o eixo principal
fig, ax1 = plt.subplots()

#Estilo de cores
plt.style.use('seaborn-v0_8-paper')

# Escala logarítimica
plt.xscale('log')
plt.yscale('log')

ax1.plot(flux_spec_fuel1_energy, flux_spec_fuel1_mean, color='xkcd:red', linestyle='-', linewidth=1,marker='^', markersize=5, label='Torio')
ax1.plot(flux_spec_fuel3_energy, flux_spec_fuel3_mean, color='xkcd:blue', linestyle='-', linewidth=1,marker='^', markersize=5, label='Uranio')

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
#plt.show()
#exit(0)


ax2 = ax1.twinx()
ax2.set_yscale('log')

th232 = openmc.data.IncidentNeutron.from_hdf5("/SSD3/nuclear-data/endfb-viii.0-hdf5/neutron/Th232.h5")
energies = th232.energy['294K']
total_xs = th232[18].xs['294K'](energies)
ax2.plot(energies, total_xs, color='xkcd:black', linestyle='-', linewidth=1, label='Th232')

u233 = openmc.data.IncidentNeutron.from_hdf5("/SSD3/nuclear-data/endfb-viii.0-hdf5/neutron/U233.h5")
energies = u233.energy['294K']
total_xs = u233[18].xs['294K'](energies)
ax2.plot(energies, total_xs, color='xkcd:blue', linestyle='-', linewidth=1, label='U233')


u235 = openmc.data.IncidentNeutron.from_hdf5("/SSD3/nuclear-data/endfb-viii.0-hdf5/neutron/U235.h5")
energies = u235.energy['294K']
total_xs = u235[18].xs['294K'](energies)
ax2.plot(energies, total_xs, color='xkcd:green', linestyle='-', linewidth=1, label='U235')


u238 = openmc.data.IncidentNeutron.from_hdf5("/SSD3/nuclear-data/endfb-viii.0-hdf5/neutron/U238.h5")
energies = u238.energy['294K']
total_xs = u238[18].xs['294K'](energies)
ax2.plot(energies, total_xs, color='xkcd:pink', linestyle='-', linewidth=1, label='U238')


pu239 = openmc.data.IncidentNeutron.from_hdf5("/SSD3/nuclear-data/endfb-viii.0-hdf5/neutron/Pu239.h5")
energies = pu239.energy['294K']
total_xs = pu239[18].xs['294K'](energies)
ax2.plot(energies, total_xs, color='xkcd:red', linestyle='-', linewidth=1, label='Pu239')




ax2.set_ylabel('Cross section (b)', color='g')
ax2.tick_params(axis='y', labelcolor='g')


# Limitar os eixos
ax1.set_xlim(4e3, 1e7)
ax2.set_xlim(4e3, 1e7)
ax2.set_ylim(10e-8, 10e0)
plt.show()



#print(list(u235.reactions.values())[:10])
#<Reaction: MT=2 (n,elastic)>
#<Reaction: MT=4 (n,level)>
#<Reaction: MT=5 (n,misc)>
#<Reaction: MT=16 (n,2n)>
#<Reaction: MT=17 (n,3n)>
#<Reaction: MT=18 (n,fission)>
#<Reaction: MT=51 (n,n1)>
#<Reaction: MT=52 (n,n2)>
#<Reaction: MT=53 (n,n3)>
#<Reaction: MT=54 (n,n4)>]
