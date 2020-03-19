import math
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.animation as animation
import numpy as np

import actigamma as ag


SPECTYPE = "gamma"

# in MeV
MIN_ENERGY = 0.0
MAX_ENERGY = 4.0

# halflife limits in seconds
MIN_HALFLIFE = 1e-6
MAX_HALFLIFE = 1e20

db = ag.Decay2012Database()
allnuclides = db.allnuclidesoftype(spectype=SPECTYPE)


def getdata(min_intensity=0.0):
    x, y = [], []
    for nuc in allnuclides:
        energies = db.getenergies(nuc, spectype=SPECTYPE)*1e-6
        intensites = db.getintensities(nuc, spectype=SPECTYPE)

        filteredenergies = [ e for i, e in enumerate(energies) if intensites[i] > min_intensity ]

        x.extend(list(filteredenergies))
        y.extend([db.gethalflife(nuc)]*len(filteredenergies))
    return x, y 


# get the data without any intensity threshold
X, Y = getdata(min_intensity=0.0)

# full range
fig = plt.figure(figsize=(12, 7))
# plt.scatter(X, Y, c='k')
plt.hist2d(X, Y, bins=[
    np.linspace(MIN_ENERGY, MAX_ENERGY, 100), 
    np.logspace(math.log10(MIN_HALFLIFE), math.log10(MAX_HALFLIFE), 100)], 
    norm=mcolors.LogNorm(),
    cmap='gnuplot')
plt.yscale('log')
plt.xlim([MIN_ENERGY, MAX_ENERGY])
plt.ylim([MIN_HALFLIFE, MAX_HALFLIFE])
plt.xlabel("Energy (MeV)", fontsize=18)
plt.ylabel("Halflife (sec)", fontsize=18)
plt.colorbar()

# zoomed in linear
fig = plt.figure(figsize=(12, 7))
plt.hist2d(X, Y, bins=[
    np.linspace(MIN_ENERGY, MAX_ENERGY, 100), 
    np.linspace(0, 1e4, 200)], 
    norm=mcolors.LogNorm(),
    cmap='gnuplot')
plt.xlim([MIN_ENERGY, MAX_ENERGY])
plt.xlabel("Energy (MeV)", fontsize=18)
plt.ylabel("Halflife (sec)", fontsize=18)
plt.colorbar()

# animation
fig, ax = plt.subplots(figsize=(12, 7))
data, x, y, _ = plt.hist2d(X, Y, bins=[
    np.linspace(MIN_ENERGY, MAX_ENERGY, 100), 
    np.logspace(math.log10(MIN_HALFLIFE), math.log10(MAX_HALFLIFE), 100)], 
    norm=mcolors.LogNorm(),
    cmap='gnuplot')

plt.yscale('log')
plt.xlim([MIN_ENERGY, MAX_ENERGY])
plt.ylim([MIN_HALFLIFE, MAX_HALFLIFE])
plt.xlabel("Energy (MeV)", fontsize=18)
plt.ylabel("Halflife (sec)", fontsize=18)
plt.colorbar()

def animate(threshold):
    ax.cla()
    X, Y = getdata(min_intensity=threshold)
    data, x, y, _ = plt.hist2d(X, Y, bins=[
        np.linspace(MIN_ENERGY, MAX_ENERGY, 100), 
        np.logspace(math.log10(MIN_HALFLIFE), math.log10(MAX_HALFLIFE), 100)], 
        norm=mcolors.LogNorm(),
        cmap='gnuplot')
    plt.yscale('log')
    plt.xlim([MIN_ENERGY, MAX_ENERGY])
    plt.ylim([MIN_HALFLIFE, MAX_HALFLIFE])
    plt.xlabel("Energy (MeV)", fontsize=18)
    plt.ylabel("Halflife (sec)", fontsize=18)
    intensity_text = ax.text(MIN_ENERGY, MAX_HALFLIFE*0.98, 
        "line intensity threshold = {:.7f} %".format(threshold*100.), fontsize=18)
    # intensity_text.set_text("intensity threshold = {:.3e} ".format(
    #     threshold))
    return [ax, intensity_text]

ani = animation.FuncAnimation(fig, animate, list(reversed(np.logspace(-7, 0, 500))),
                            interval=50, blit=False, repeat=True)

# ani.save('./halflifelines.gif', writer='imagemagick', fps=10)

plt.show()