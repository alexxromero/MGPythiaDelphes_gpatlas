"""
gen_events_slurm.py generates events given a MG gridpack. Pythia and Delphes
are used for showering/hadronization and event generation.
"""

import sys
import os
import re
import subprocess as sp
from argparse import ArgumentParser
from textwrap import dedent

def gen_event_script():
    script = dedent(
        """\
        #!/usr/bin/env bash

        echo "------------- running on -------------"
        echo "start: $(date)"
        echo "input arguments:"
        gridpack=$1
        pythia_card=$2
        delphes_card=$3
        nEvents_run=$4
        seed=$5
        event_tag=$6

        echo ${gridpack}
        echo ${pythia_card}
        echo ${delphes_card}
        echo ${nEvents_run}
        echo ${seed}
        echo ${event_tag}

        # setup root
        export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
        source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
        lsetup "root 6.14.04-x86_64-slc6-gcc62-opt"

        echo "Unpacking the gridpack..."
        tar -zxvf $gridpack

        echo "Compiling MG5..."
        cd madevent
        ./bin/compile
        cd ..
        chmod +x run.sh

        echo "Running MG5..."
        ./run.sh $nEvents_run $seed  # generates events.lhe.gz
        gunzip ./events.lhe.gz

        echo "Setting up Pythia8..."
        wget http://home.thep.lu.se/~torbjorn/pythia8/pythia8235.tgz
        tar -xzvf pythia8235.tgz
        cd pythia8235
        ./configure --prefix=$(pwd)
        make install
        export PYTHIA8=$(pwd)  # variable needed if using Delphes
        cd ..

        echo "Setting up Delphes..."
        wget http://cp3.irmp.ucl.ac.be/downloads/Delphes-3.4.2.tar.gz
        tar -xzvf Delphes-3.4.2.tar.gz
        cd Delphes-3.4.2
        export DELPHESDIR=$(pwd)
        make HAS_PYTHIA8=true  # needs PYTHIA8 var
        cd ..

        echo "Running Pythia8+Delphes..."
        ${DELPHESDIR}/DelphesPythia8 $delphes_card $pythia_card delphes.root

        echo "Saving files..."
        output_dir="/DFS-L/DATA/atlas/alexir2/qg_sept2020"
        mkdir $output_dir
        output_dir=${output_dir}/${event_tag}
        mkdir $output_dir
        mkdir ${output_dir}/Events
        mkdir ${output_dir}/Delphes

        mv ./events.lhe ${output_dir}/Events/events_${seed}.lhe
        mv ./delphes.root ${output_dir}/Delphes/delphes_${seed}.root

        echo "done with seed $seed :)"
        """
        )
    return script


def gen_submit_script(event_script, gridpack, pythia_card, delphes_card,
                      nEvents_run, nRuns, seed, event_tag):
    script = dedent(
        """\
        #!/usr/bin/env/bash
        set -euo pipefail
        mkdir -p logs

        """
        )

    for i in range(nRuns):
        script += dedent(
            """\
            FLGS='-t 120 -p atlas -c 2 -o logs/out-%j.txt -e logs/error-%j.txt'
            sbatch ${{FLGS}} {} {} {} {} {} {} {}
            """.format(event_script, gridpack, pythia_card, delphes_card,
                       nEvents_run, seed, event_tag)
            )
        seed += 1
    return script


def submit_jobs(gridpack, pythia_card, delphes_card,
                nEvents_run, nRuns, seed, event_tag, submit_dir):
    event_script = os.path.join(submit_dir, "MG5PythiaDelphes.sh")
    submit_script = os.path.join(submit_dir, "submit_jobs.sh")

    with open(event_script, "w") as f:
        f.write(gen_event_script())

    with open(submit_script, "w") as f:
        f.write(gen_submit_script(event_script,
                                  gridpack,
                                  pythia_card,
                                  delphes_card,
                                  nEvents_run,
                                  nRuns,
                                  seed,
                                  event_tag))

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-g", "--gridpack", type=str, required=True)
    parser.add_argument("--pythia_card", type=str)
    parser.add_argument("--delphes_card", type=str)
    parser.add_argument("-n", "--nEvents_run", type=int, default=10000)
    parser.add_argument("-r", "--nRuns", type=int, default=1)
    parser.add_argument("--seed", type=long, default=123)
    parser.add_argument("--event_tag", type=str, default="event_dummy")
    args = parser.parse_args()

    start_dir = os.getcwd()
    submit_dir = os.path.join(start_dir, args.event_tag)
    sp.call(['mkdir', '-p', submit_dir])
    os.chdir(submit_dir)
    submit_jobs(args.gridpack, args.pythia_card, args.delphes_card,
                args.nEvents_run, args.nRuns, args.seed, args.event_tag,
                submit_dir)
    os.chdir(start_dir)
