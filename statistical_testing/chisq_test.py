# Takes binary filled with random bytes generated by the Cherbobyl Dice as input

import sys

import numpy as np
from scipy import stats

from matplotlib import pyplot

if __name__ == "__main__":
    data = np.fromfile(sys.argv[1], dtype=np.uint8)

    num_dict = {}

    for num in data:
        try:
            num_dict[num] += 1
        except KeyError:
            num_dict[num] = 1

    D_SIZE = len(num_dict.keys())
    N_ROLLS = sum(num_dict.values())

    print("Dice size: {}".format(D_SIZE))
    print("Number of rolls: {}".format(N_ROLLS))

    chi_sq = 0

    for val in num_dict.values():
        obs = float(val)
        exp = (1.0/D_SIZE)*N_ROLLS
        chi_sq += ((obs - exp)**2) / exp

    chi_value_string = "Chi sq. (for d.o.f. {}): {}".format(D_SIZE-1, round(chi_sq, 2))
    p_value = 1.0 - stats.chi2.cdf(chi_sq, D_SIZE-1)
    p_value_string = "Prob. of randomly exceeding value: {}".format(round(p_value, 2))

    num_tuples = [(key, value) for key, value in num_dict.items()]
    num_tuples = sorted(num_tuples, key=lambda x: x[0])

    fig, ax = pyplot.subplots(1)

    ax.bar([x[0] for x in num_tuples], [x[1] for x in num_tuples], align='center')
    pyplot.xticks([x[0] for x in num_tuples], [str(x[0]) for x in num_tuples])

    pyplot.title("{} rolls of {}-sided dice".format(N_ROLLS, D_SIZE))
    ax.set_xlabel(chi_value_string + '\n' + p_value_string)
    ax.set_ylabel("Observed rolls")

    pyplot.tight_layout()

    pyplot.savefig('chi_sq_test.png')
