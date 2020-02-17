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

    # get half life
    for i, z in enumerate(nd.getdecayzais()):
        if not nd.getdecayisstable(i):
            halflifedata[z] = nd.getdecayhalflife(i)

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

        data[name][typename] = {
            "number": entry.number,
            "mean_energy": entry.mean_energy,
            "mean_energy_unc": entry.mean_energy_unc,
            "mean_normalisation": entry.mean_normalisation,
            "mean_normalisation_unc": entry.mean_normalisation_unc,
            "lines": {
                "energies": entry.lines.energies,
                "energies_unc": entry.lines.energies_unc,
                "intensities": entry.lines.intensities,
                "intensities_unc": entry.lines.intensities_unc,
                "norms": entry.lines.norms,
                "norms_unc": entry.lines.norms_unc
            }
        }

outputfile = os.path.join(os.path.dirname(os.path.abspath(__file__)),
    '..', 'reference', 'lines_decay_2012.json')

print("Creating JSON database...")
with open(outputfile, 'wt') as flines:
    flines.write(json.dumps(data, indent=4, sort_keys=False))