import os
import collections
import json

# uses pypact to read FISPACT-II printlib5 file
import pypact as pp

filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
    '..', 'reference', 'printlib5_decay_2012.out')

# full dataset 
data = collections.defaultdict()

# get halflives 
halflifedata = collections.defaultdict()

# use FISPACT-II API instead if available
try:
    import sys
    import pyfispact as pf

    nd_path = os.getenv('NUCLEAR_DATA')

    log = pf.Monitor()
    pf.initialise(log)

    # we only care about errors
    log.setlevel(pf.severity.error)

    ndr = pf.io.NuclearDataReader(log)
    nd = pf.NuclearData(log)

    # just load decay data
    ndr.setpath(pf.io.ND_IND_NUC_KEY(), os.path.join(nd_path, 'decay', 'decay_2012_index_2012'))
    ndr.setpath(pf.io.ND_DK_ENDF_KEY(), os.path.join(nd_path, 'decay', 'decay_2012'))

    # callback for nuclear data loader
    def loadfunc(k, p, index, total):
        print(" [{}/{}]  Reading {}: {}".format(index, total, k, p), end="\r")
        sys.stdout.write("\033[K")

    # load data
    ndr.load(nd, op=loadfunc)

    # check for error
    if log.hasfatal():
        print(log)
        sys.exit(1)

    DECAYTYPES = {
        pf.SPECTRUM_TYPE_ALPHA(): "alpha",
        pf.SPECTRUM_TYPE_BETA(): "beta",
        pf.SPECTRUM_TYPE_EC(): "ec",
        pf.SPECTRUM_TYPE_ELECTRON(): "electron",
        pf.SPECTRUM_TYPE_GAMMA(): "gamma",
        pf.SPECTRUM_TYPE_NEUTRON(): "neutron",
        pf.SPECTRUM_TYPE_PROTON(): "proton",
        pf.SPECTRUM_TYPE_SF(): "SF",
        pf.SPECTRUM_TYPE_UNKNOWN(): "unknown",
        pf.SPECTRUM_TYPE_X_RAY(): "x-ray"
    }

    # get half life
    for i, zai in enumerate(nd.getdecayzais()):
        halflife = -1
        if not nd.getdecayisstable(i):
            halflife = nd.getdecayhalflife(i)

        name = pf.util.nuclide_from_zai(log, zai)
        nroftypes = nd.getdecaynrofspectrumtypes(i)
        for mode in range(nroftypes):
            typeid = nd.getdecayspectrumtype(i, mode)
            typename = DECAYTYPES[typeid]

            if name not in data:
                data[name] = {
                    "zai": zai,
                    "halflife": halflife,
                    typename: {}
                }
            nroflines = nd.getdecayspectrumnroflines(i, mode)

            # ignore empty data
            if nroflines == 0:
                continue

            norm = nd.getdecayspectrumnorm(i, mode)
            norm_unc = nd.getdecayspectrumnormunc(i, mode)

            # get the line data
            energies = []
            energies_unc = []
            intensities = []
            intensities_unc = []
            norms = []
            norms_unc = []
            for l in range(nroflines):
                line = nd.getdecayspectrumline(i, mode, l)
                energies.append(line.energy[0])
                energies_unc.append(line.energy[1])
                intensities.append(line.intensity[0])
                intensities_unc.append(line.intensity[1])
                norms.append(norm)
                norms_unc.append(norm_unc)

            data[name][typename] = {
                "number": nroflines,
                "mean_energy": nd.getdecayspectrummeanenergy(i, mode),
                "mean_energy_unc": nd.getdecayspectrummeanenergyuncert(i, mode),
                "mean_normalisation": norm,
                "mean_normalisation_unc": norm_unc,
                "lines": {
                    "energies": energies,
                    "energies_unc": energies_unc,
                    "intensities": intensities,
                    "intensities_unc": intensities_unc,
                    "norms": norms,
                    "norms_unc": norms_unc,
                }
            }
except:
    print("WARNING: Without the API this does not get the half-lives!")

    # TODO: if have pyfispact then do it the correct way
    # printlib5 does not have halflives - we need this too!
    with pp.PrintLib5Reader(filename) as output:
        for entry in output.spectral_data:
            if entry.type == "no spectral data":
                continue

            # check if the halflife has been set
            halflife = -1
            if entry.zai in halflifedata:
                halflife = halflifedata[entry.zai]

            # remove whitespace
            typename = "_".join(entry.type.split(" "))

            # remove whitespace
            name = "".join(entry.name.split(" "))
            if name not in data:
                data[name] = {
                    "zai": entry.zai,
                    "halflife": halflife,
                    typename: {}
                }

            # ignore empty data
            if entry.lines == 0:
                continue

            # get the line data
            energies = []
            energies_unc = []
            intensities = []
            intensities_unc = []
            norms = []
            norms_unc = []
            for l in entry.lines:
                energies.append(l[0])
                energies_unc.append(l[1])
                intensities.append(l[2])
                intensities_unc.append(l[3])
                norms.append(l[4])
                norms_unc.append(l[5])

            data[name][typename] = {
                "number": entry.number,
                "mean_energy": entry.mean_energy,
                "mean_energy_unc": entry.mean_energy_unc,
                "mean_normalisation": entry.mean_normalisation,
                "mean_normalisation_unc": entry.mean_normalisation_unc,
                "lines": {
                    "energies": energies,#entry.lines.energies,
                    "energies_unc": energies_unc,#entry.lines.energies_unc,
                    "intensities": intensities,#entry.lines.intensities,
                    "intensities_unc": intensities_unc,#entry.lines.intensities_unc,
                    "norms": norms,#entry.lines.norms,
                    "norms_unc": norms_unc,#entry.lines.norms_unc
                }
            }


outputfile = os.path.join(os.path.dirname(os.path.abspath(__file__)),
    '..', 'reference', 'lines_decay_2012.json')

print("Creating JSON database...")
with open(outputfile, 'wt') as flines:
    flines.write(json.dumps(data, indent=4, sort_keys=False))