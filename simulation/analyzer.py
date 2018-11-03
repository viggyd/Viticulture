""" Analyzes results from viticulture monte carlo simulations

This module is used to analyze the results of simulations. It will generate
plots of interest based on the data provided.

"""

import argparse
import json
import os

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy
from collections import Counter, defaultdict



def parse_results_files(ResultsPath):

    ResultsList = []
    for file in os.listdir(ResultsPath):

        with open(os.path.join(ResultsPath, file), 'r') as f:
            json_results = json.loads(f.read())
            ResultsList.append(json_results)

    return ResultsList


def get_cumulative_probability(raw_data, num_simulation):

    years = [subdct["Years"] for key, subdct in raw_data.items()]
    counts = Counter(years)

    accumulated_data = defaultdict(list)
    accumulator = 0

    for year, count in sorted(counts.items()):

        accumulator += count

        accumulated_data["x"].append(year)
        accumulated_data["y"].append(accumulator / num_simulation)

    return accumulated_data


def get_point_data(parameters, raw_data):

    # small_layout = parameters["0"]["Layout"]
    medium_layout = parameters["Fields"]["1"]["Layout"]
    large_layout = parameters["Fields"]["2"]["Layout"]

    years = [subdct["Years"] for key, subdct in raw_data.items()]
    mean_years = numpy.mean(years)
    median_years = numpy.median(years)
    std_years = numpy.std(years)

    return {
        "x" : medium_layout,
        "y" : large_layout,
        "mean_years" : mean_years,
        "median_years" : median_years,
        "std_years" : std_years
    }



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Analyze simulation results", add_help=True)

    parser.add_argument('-r', dest='ResultsPath', type=str, help="Path to results from sim")

    args = parser.parse_args()


    results = parse_results_files(args.ResultsPath)

    num_sims = 1500

    plt.figure(1)
    plt.xlabel('Years to reach 20 VP')
    plt.ylabel('Probability')
    plt.title('Probability of completion vs. Year Number')
    plt.grid(True)
    for result in results:

        parameters = result["Parameters"]
        fields = parameters["Fields"]
        raw_data = result["Results"]

        test = get_cumulative_probability(raw_data, num_sims)

        plot_label = "M: {0:d}; L: {1:d}".format(fields["1"]["Layout"], fields["2"]["Layout"])
        plt.plot(test["x"], test["y"], label=plot_label)


    plt.figure(2)
    plt.xlabel('Medium Field Layout')
    plt.ylabel('Large Field Layout')
    plt.title('Field Layout Performance')

    param_x = []
    param_y = []
    param_c = []
    param_std = []

    color_array = numpy.zeros(shape=(8, 7))
    std_array = numpy.empty(shape=(8, 7), dtype=object)
    res_array = numpy.empty(shape=(8, 7), dtype=str)

    color_dict = {}

    for result in results:

        parameters = result["Parameters"]
        fields = parameters["Fields"]
        raw_data = result["Results"]

        test = get_point_data(parameters, raw_data)

        param_x.append(test["x"])
        param_y.append(test["y"])
        param_c.append(test["mean_years"])
        param_std.append(test["std_years"])

        color_array[int((test["y"]-7)/-2)][int((test["x"]+6)/2)] = test["mean_years"]
        std_array[int((test["y"] - 7) / -2)][int((test["x"] + 6) / 2)] = \
            "{0:0.2f} +- {1:0.2f}".format(test["mean_years"], test["std_years"])




    # Divide each element by the max
    # We do the 1 -, because we prefer lower years to higher ones
    # param_c = [1 - x / max(param_c) for x in param_c]

    plt.xticks(numpy.arange(min(param_x), max(param_x) + 1, 2.0))
    plt.yticks(numpy.arange(min(param_y), max(param_y) + 1, 2.0))

    sc = plt.scatter(param_x, param_y, c=param_c,  s=500, marker='s', cmap='YlGn_r', edgecolors='black', linewidths=.5)
    plt.colorbar(sc)




    color_array[7][0] = max(param_c)
    color_array[0][6] = max(param_c)
    fig, ax = plt.subplots()
    i = ax.imshow(color_array, cmap='YlGn_r', interpolation='nearest')
    fig.colorbar(i)

    # fig.savefig("heat_map.eps", format="eps", dpi=1000)

    # print(param_x)
    # print(param_y)
    # print(param_c)
    # print(param_std)
    # print()
    # print(color_array)
    # print(std_array)

    print("")

    for row in std_array:
        for col in row:

            # print("{0:20s}".format(col))
            print "{0:20s} ".format(col),

        print("")

    # plt.legend(loc='upper left')
    plt.show()



