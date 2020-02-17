import os
import collections
import json

# uses pypact to read FISPACT-II printlib5 file
import pypact as pp

filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
    '..', 'reference', 'printlib5_decay_2012.out')

data = collections.defaultdict()

with pp.PrintLib5Reader(filename) as output:
    for entry in output.spectral_data:
        if entry.type == "no spectral data":
            continue

        # remove whitespace
        typename = "_".join(entry.type.split(" "))

        # remove whitespace
        name = "".join(entry.name.split(" "))
        if name not in data:
            data[name] = {
                "zai": entry.zai,
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

with open(outputfile, 'wt') as flines:
    flines.write(json.dumps(data, indent=4, sort_keys=False))