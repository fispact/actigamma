import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as colors
from matplotlib import cm
import numpy as np
import pypact as pp

import actigamma as ag

COLOURS = ['white', 'blue', 'red', 'green']
cmap = colors.ListedColormap(COLOURS)

def nuclide_mapping(Z, A):
    """
        Return X, Y position where A is on X
        and Z is on Y.
        
        Note different to input!        
    """
    # split chart into four pieces 
    if Z <= 24:
        return int(A+15), int(Z+58)
    elif Z <= 64:
        return int(A-40), int(Z+8)
    elif Z <= 94:
        return int(A-125), int(Z-52)
    else:
        return int(A-178), int(Z-90)


def make_full_nuclide_chart(data_matrix=None, figsize=(12, 8), cmap='Set1'):
    XSIZE = 140
    YSIZE = 90
    # define an empty matrix of size (90,140)
    # X and Y are inverted
    if data_matrix is None:
        data_matrix = np.zeros(shape=(YSIZE, XSIZE))
        
    assert data_matrix.shape == (YSIZE, XSIZE)

    # make a chart of the nuclides
    fig, ax = plt.subplots(figsize=figsize)
    
    # draw Z and N labels with arrows near H1
    X, Y = nuclide_mapping(1, 1)
    plt.text(X-4, Y, r'Z', fontsize=18)
    plt.text(X, Y-4, r'N', fontsize=18)

    # Z arrow
    plt.arrow(X-3, Y+3, 0, 4, fc='k', ec='k', alpha=1.0, width=0.1,
                head_width=1, head_length=None)

    # N arrow
    plt.arrow(X+3, Y-3, 4, 0, fc='k', ec='k', alpha=1.0, width=0.1,
                head_width=1, head_length=None)

    all_isotopes = []
    mZ = -1
    mA = -1
    for d in pp.NUCLIDE_DICTIONARY:
        for i in d['isotopes']:
            mZ = max(mZ, d['Z'])
            mA = max(mA, i)

            X, Y = nuclide_mapping(d['Z'], i)
            all_isotopes.append((X, Y))
            rect = patches.Rectangle((X-0.5, Y-0.5), 1, 1, linewidth=1, edgecolor='k',facecolor='none')
            ax.add_patch(rect)

    # identify key elements
    # Hydrogen
    X, Y = nuclide_mapping(1, 5)
    plt.text(X-0.5+10, Y-0.5, r'Hydrogen', fontsize=10)
    plt.arrow(X-0.5, Y-0.5, 10, 0, fc='k', ec='k', alpha=0.5, width=0.05,
                head_width=0, head_length=0)

    # Chromium
    X, Y = nuclide_mapping(24, 54)
    plt.text(X-0.5+20, Y-0.5, r'Chromium', fontsize=10)
    plt.arrow(X-0.5, Y-0.5, 20, 0, fc='k', ec='k', alpha=0.5, width=0.05,
                head_width=0, head_length=0)

    # Manganese
    X, Y = nuclide_mapping(25, 60)
    plt.text(X-0.5+20, Y-0.5, r'Manganese', fontsize=10)
    plt.arrow(X-0.5, Y-0.5, 20, 0, fc='k', ec='k', alpha=0.5, width=0.05,
                head_width=0, head_length=0)

    # Gadolinium
    X, Y = nuclide_mapping(64, 160)
    plt.text(X-0.5+10, Y-0.5, r'Gadolinium', fontsize=10)
    plt.arrow(X-0.5, Y-0.5, 10, 0, fc='k', ec='k', alpha=0.5, width=0.05,
                head_width=0, head_length=0)

    # Terbium
    X, Y = nuclide_mapping(65, 160)
    plt.text(X-0.5+20, Y-0.5, r'Terbium', fontsize=10)
    plt.arrow(X-0.5, Y-0.5, 20, 0, fc='k', ec='k', alpha=0.5, width=0.05,
                head_width=0, head_length=0)

    # Plutonium
    X, Y = nuclide_mapping(94, 235)
    plt.text(X-0.5+15, Y-0.5, r'Plutonium', fontsize=10)
    plt.arrow(X-0.5, Y-0.5, 15, 0, fc='k', ec='k', alpha=0.5, width=0.05,
                head_width=0, head_length=0)

    # Americium
    X, Y = nuclide_mapping(95, 240)
    plt.text(X-0.5+20, Y-0.5, r'Americium', fontsize=10)
    plt.arrow(X-0.5, Y-0.5, 20, 0, fc='k', ec='k', alpha=0.5, width=0.05,
                head_width=0, head_length=0)

    # Oganesson
    X, Y = nuclide_mapping(118, 294)
    plt.text(X-0.5+5, Y-0.5, r'Oganesson', fontsize=10)
    plt.arrow(X-0.5, Y-0.5, 5, 0, fc='k', ec='k', alpha=0.5, width=0.05,
                head_width=0, head_length=0)
            
    # set everything that is not in the nuclide chart to white
    for x in range(XSIZE):
        for y in range(YSIZE):
            if (x, y) not in all_isotopes:
                data_matrix[y, x] = COLOURS.index('white')
                
    im = plt.imshow(data_matrix, cmap=cmap)
    # ax.invert_yaxis()
    ax.axis('off')
    plt.xlabel("A", fontsize=16)
    plt.ylabel("Z", fontsize=16)
    plt.xlim([0, XSIZE])
    plt.ylim([0, YSIZE])
    plt.subplots_adjust(left=0.01, bottom=0.01, right=0.99, top=0.99, wspace=None, hspace=None)
    # fig.colorbar(im, cax = fig.add_axes([0.91, 0.2, 0.03, 0.6]))
    
    return fig, ax


"""
    Main script 
"""
SPECTYPE = "gamma"
# setup the DB
db = ag.Decay2012Database()
allradionuclides = db.allnuclidesoftype(spectype=SPECTYPE)

# for 1 == blue - all nuclides that are either stable or no data in database
value = COLOURS.index('blue')
allCount = pp.NUMBER_OF_ISOTOPES
allnuclideArtist = plt.Line2D((0,1),(0,0), color=COLOURS[value], marker='o', linestyle='')
data_matrix = np.zeros(shape=(140, 90))
data_matrix[:, :] = value

# show all radioisotopes
# for 2 == red - all nuclides that are unstable and exist in database
value = COLOURS.index('red')
unstablenuclideArtist = plt.Line2D((0,1),(0,0), color=COLOURS[value], marker='o', linestyle='')
for nuc in db.allnuclides:
    z, a, _ = ag.get_zai_props(db, nuc)
    x, y = nuclide_mapping(z, a)
    data_matrix[x, y] = value
    
# show all radioisotopes for that spectype
# for 3 == green - all nuclides that are unstable and have gamma lines in database
value = COLOURS.index('green')
allGammaCount = len(allradionuclides)
allUnstableCount = len(db.allnuclides) - allGammaCount
gammanuclideArtist = plt.Line2D((0,1),(0,0), color=COLOURS[value], marker='o', linestyle='')
for nuc in allradionuclides:
    z, a, _ = ag.get_zai_props(db, nuc)
    x, y = nuclide_mapping(z, a)
    data_matrix[x, y] = value

fig1, ax1 = make_full_nuclide_chart(data_matrix=data_matrix.transpose(), cmap=cmap)
ax1.legend([ allnuclideArtist, unstablenuclideArtist, gammanuclideArtist],
           [ 'Either stable or not in database = {}'.format(allCount), 
           'Unstable (no {} lines) = {}'.format(SPECTYPE, allUnstableCount), 
           'Unstable (has {} lines) = {}'.format(SPECTYPE, allGammaCount)])
plt.show()
