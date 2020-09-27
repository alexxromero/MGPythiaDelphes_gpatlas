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
    pT_range=$6
    event_tag=$7

    echo ${gridpack}
    echo ${pythia_card}
    echo ${delphes_card}
    echo ${nEvents_run}
    echo ${seed}
    echo ${pT_range}
    echo ${event_tag}

    # setup root
    export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
    source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
    lsetup "root 6.14.04-x86_64-slc6-gcc62-opt"

    home_dir=$(pwd)  # SLURM starts off at the home directory
    temp_dir="/DFS-L/DATA/atlas/${USER}/${event_tag}_${seed}"
    mkdir -p $temp_dir
    cd $temp_dir

    # setup Pythia8
    echo "Setting up Pythia8..."
    if [ ! -d "${home_dir}/pythia8235" ]
    then
        wget http://home.thep.lu.se/~torbjorn/pythia8/pythia8235.tgz
        tar -xzvf pythia8235.tgz
    else
        cp "${home_dir}/pythia8235.tgz" $temp_dir
        tar -xzvf pythia8235.tgz
    fi
    cd pythia8235
    ./configure --prefix=$(pwd)
    make install
    export PYTHIA8=$(pwd)  # variable needed if using Delphes
    cd ..

    # setup Delphes
    echo "Setting up Delphes..."
    if [ ! -d "${home_dir}/Delphes-3.4.2" ]
    then
        wget http://cp3.irmp.ucl.ac.be/downloads/Delphes-3.4.2.tar.gz
        tar -xzvf Delphes-3.4.2.tar.gz
    else
        cp "${home_dir}/Delphes-3.4.2.tar.gz" $temp_dir
        tar -xzvf Delphes-3.4.2.tar.gz
    fi
    cd Delphes-3.4.2
    export DELPHESDIR=$(pwd)
    make HAS_PYTHIA8=true  # needs PYTHIA8 var
    cd ..

    echo "Unpacking the gridpack..."
    temp_gridpack="${temp_dir}/gridpack_${event_tag}_${seed}.tar.gz"
    cp $gridpack $temp_gridpack
    tar -zxvf $temp_gridpack

    echo "Compiling MG5..."
    cd madevent
    ./bin/compile
    cd ..
    chmod +x run.sh

    echo "Running MG5..."
    ./run.sh $nEvents_run $seed  # generates events.lhe.gz
    gunzip ./events.lhe.gz

    echo " "
    echo " "
    echo " "
    echo "current working dir"
    echo $(pwd)
    echo "temp dir"
    echo $temp_dir
    echo "delphes dir"
    echo $DELPHESDIR
    echo " "
    echo " "
    echo " "

    echo "Running Pythia8+Delphes..."
    ${DELPHESDIR}/DelphesPythia8 $delphes_card $pythia_card delphes.root

    output_dir="/DFS-L/DATA/atlas/alexir2/qg_sept2020/${event_tag}"
    echo "Saving files to ${output_dir}..."
    mkdir -p $output_dir
    mkdir -p ${output_dir}/Events
    mkdir -p ${output_dir}/Delphes

    mv ./events.lhe ${output_dir}/Events/events_${seed}.lhe
    mv ./delphes.root ${output_dir}/Delphes/delphes_${seed}.root

    echo "done with seed $seed :)"
    rm -rf $temp_dir
    """
        )
    return script


def gen_submit_script(event_script, gridpack, pythia_card, delphes_card,
                      nEvents_run, nRuns, seed, pT_range, event_tag):
    script = dedent(
        """\
        #!/usr/bin/env bash
        set -euo pipefail
        mkdir -p logs

        """
        )

    for i in range(nRuns):
        script += dedent(
            """\

            FLGS='-t 120 -p atlas -c 2 -o logs/out-%j.txt -e logs/error-%j.txt'
            sbatch ${{FLGS}} {} {} {} {} {} {} {} {}
            """.format(event_script, gridpack, pythia_card, delphes_card,
                       nEvents_run, seed, pT_range, event_tag)
            )
        seed += 1
    return script


def submit_jobs(gridpack, pythia_card, delphes_card, nEvents_run, nRuns,
                seed, pT_range, event_tag, submit_dir):
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
                                  pT_range,
                                  event_tag))

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-g", "--gridpack", type=str, required=True)
    parser.add_argument("--pythia_card", type=str)
    parser.add_argument("--delphes_card", type=str)
    parser.add_argument("-n", "--nEvents_run", type=int, default=10000)
    parser.add_argument("-r", "--nRuns", type=int, default=1)
    parser.add_argument("--seed", type=int, default=123)
    parser.add_argument("--pT_range", type=int)
    parser.add_argument("--event_tag", type=str, default="event_dummy")
    args = parser.parse_args()

    start_dir = os.getcwd()
    submit_dir = os.path.join(start_dir, args.event_tag)
    sp.call(['mkdir', '-p', submit_dir])
    os.chdir(submit_dir)
    submit_jobs(args.gridpack,
                args.pythia_card,
                args.delphes_card,
                args.nEvents_run,
                args.nRuns,
                args.seed,
                args.pT_range,
                args.event_tag,
                submit_dir)
    os.chdir(start_dir)
