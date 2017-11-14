""" The MIT License (MIT)

    Copyright (c) 2016 Kyle Hollins Wray, University of Massachusetts

    Permission is hereby granted, free of charge, to any person obtaining a copy of
    this software and associated documentation files (the "Software"), to deal in
    the Software without restriction, including without limitation the rights to
    use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
    the Software, and to permit persons to whom the Software is furnished to do so,
    subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
    FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
    COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
    IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
    CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import os
import sys

thisFilePath = os.path.dirname(os.path.realpath(__file__))

sys.path.append(os.path.join(thisFilePath, "..", "..", "..", "python"))

from nova.pomdp import *
from nova.pomdp_pbvi import *
from nova.pomdp_perseus import*
from nova.pomdp_hsvi2 import*

from pylab import *


numTrials = 1
adrTrials = 100

#algorithms = ['pbvi', 'perseus', 'hsvi2']
#algorithms = ['perseus', 'hsvi2']
algorithms = ['hsvi2']
#algorithms = ['perseus']

files = [
        {'name': "tiger", 'filename': "domains/tiger_95.pomdp", 'filetype': "cassandra", 'numExpandSteps': 4, 'numBeliefsToAdd': 200, 'maxTrials': 100},
        #{'name': "shuttle", 'filename': "domains/shuttle_95.pomdp", 'filetype': "cassandra", 'numExpandSteps': 4, 'numBeliefsToAdd': 300, 'maxTrials': 100},
        #{'name': "paint", 'filename': "domains/paint_95.pomdp", 'filetype': "cassandra", 'numExpandSteps': 4, 'numBeliefsToAdd': 300, 'maxTrials': 100},
        {'name': "grid-4x3", 'filename': "domains/4x3_95.pomdp", 'filetype': "cassandra", 'numExpandSteps': 5, 'numBeliefsToAdd': 500, 'maxTrials': 100},
        {'name': "tiger-grid", 'filename': "domains/tiger_grid.pomdp", 'filetype': "cassandra",'numExpandSteps': 6, 'numBeliefsToAdd': 700, 'maxTrials': 200},
        {'name': "aloha-10", 'filename': "domains/aloha_10.pomdp", 'filetype': "cassandra", 'numExpandSteps': 6, 'numBeliefsToAdd': 700, 'maxTrials': 200},
        {'name': "hallway2", 'filename': "domains/hallway2.pomdp", 'filetype': "cassandra", 'numExpandSteps': 6, 'numBeliefsToAdd': 1000, 'maxTrials': 300},
        #{'name': "aloha-30", 'filename': "domains/aloha_30.pomdp", 'filetype': "cassandra", 'numExpandSteps': 8, 'numBeliefsToAdd': 3000, 'maxTrials': 400},
        {'name': "tag", 'filename': "domains/tag.pomdp", 'filetype': "cassandra", 'numExpandSteps': 10, 'numBeliefsToAdd': 5000, 'maxTrials': 500},
        #{'name': "fourth", 'filename': "domains/fourth.pomdp", 'filetype': "cassandra", 'numExpandSteps': 10, 'numBeliefsToAdd': 5000, 'maxTrials': 500},
        #{'name': "rock-sample (7x8)", 'filename': "domains/rockSample_7_8.pomdp", 'filetype': "cassandra", 'numExpandSteps': 11, 'numBeliefsToAdd': 10000, 'maxTrials': 1000},
        #{'name': "auv-navigation", 'filename': "domains/auvNavigation.pomdp", 'filetype': "cassandra", 'numExpandSteps': 11, 'numBeliefsToAdd': 10000, 'maxTrials': 1000},

        #{'name': "drive_san_francisco", 'filename': "domains/drive_san_francisco.pomdp", 'filetype': "cassandra", 'numExpandSteps': 8, 'numBeliefsToAdd': 30, 'maxTrials': 1000},
        #{'name': "drive_seattle", 'filename': "domains/drive_seattle.pomdp", 'filetype': "cassandra", 'numExpandSteps': 9, 'numBeliefsToAdd': 30, 'maxTrials': 1000},
        #{'name': "drive_new_york_city", 'filename': "domains/drive_new_york_city.pomdp", 'filetype': "cassandra", 'numExpandSteps': 9, 'numBeliefsToAdd': 30, 'maxTrials': 1000},
        #{'name': "drive_boston", 'filename': "domains/drive_boston.pomdp", 'filetype': "cassandra", 'numExpandSteps': 10, 'numBeliefsToAdd': 30, 'maxTrials': 1000},
        ]


for f in files:
    print(f['name'])

    filename = os.path.join(thisFilePath, f['filename'])

    for a in algorithms:
        print(" - %s " % (a), end='')

        fileSuffix = "_".join([f['name'], a])

        with open(os.path.join(thisFilePath, "results", fileSuffix) + ".csv", "w") as out:
            out.write("n,m,z,r,ns,rz,size,time,V(b0),ADR(b0)\n")
            out.flush()

            for j in range(numTrials):
                print(".", end='')
                sys.stdout.flush()

                pomdp = POMDP()
                pomdp.load(filename, filetype=f['filetype'])

                # Store the intial belief from this file.
                b0 = zeros(pomdp.n)
                for k in range(pomdp.rz):
                    s = pomdp.Z[0 * pomdp.rz + k]
                    if s < 0:
                        break
                    b0[s] = pomdp.B[0 * pomdp.rz + k]

                if a == "pbvi":
                    pomdp.expand(method='random_unique', numBeliefsToAdd=f['numBeliefsToAdd'], maxTrials=f['maxTrials'])
                    algorithm = POMDPPBVI(pomdp)
                elif a == "perseus":
                    pomdp.expand(method='random_unique', numBeliefsToAdd=f['numBeliefsToAdd'], maxTrials=f['maxTrials'])
                    algorithm = POMDPPerseus(pomdp)
                elif a == "hsvi2":
                    algorithm = POMDPHSVI2(pomdp)
                    algorithm.trials = 1000
                    algorithm.epsilon = 0.001
                    algorithm.delta = 0.0001
                    algorithm.pruneGrowthThreshold = float(0.1)
                    algorithm.maxAlphaVectors = int(max(pomdp.n, pomdp.m) + algorithm.trials * pomdp.horizon + 1)

                timing = (time.time(), time.clock())
                policy = algorithm.solve()
                timing = (time.time() - timing[0], time.clock() - timing[1])

                print(pomdp)
                print(policy)

                # Point-based vs. FSC solutions have different "sizes" of their solution.
                if a in ["pbvi", "perseus", "hsvi2"]:
                    sizeOfSolution = float(policy.r)
                else:
                    sizeOfSolution = 0

                Vb0, ab0 = policy.value_and_action(b0)
                adrb0 = pomdp.compute_adr(policy, b0, trials=adrTrials)

                # Note: use the time.time() function, which measures wall-clock time.
                out.write("%i,%i,%i,%i,%i,%i,%i,%.5f,%.5f,%.5f\n" % (pomdp.n, pomdp.m, pomdp.z, pomdp.r, pomdp.ns,
                                                                     pomdp.rz, sizeOfSolution, timing[0], Vb0, adrb0))
                out.flush()

        print()

