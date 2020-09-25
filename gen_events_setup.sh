#!/bin/bash

starting_dir=$(pwd)
cards_dir="$(pwd)/cards"
gridpack_dir="/export/home/alexir2/gridpacks_qg"

# ------------------- quarks ------------------------ #
jet_type="quarks"
range=200
gridpack="${gridpack_dir}/${jet_type}_${range}GeV_gridpack.tar.gz"
pythia_card="${cards_dir}/configLHE.cmnd"
delphes_card="${cards_dir}/delphes_card_ATLAS.tcl"
nEvents_run=1000
nRuns=1
seed=123
event_tag="quarks_200_sept242020"

python ./gen_events_slurm.py \
  -g $gridpack \
  --pythia_card $pythia_card \
  --delphes_card $delphes_card \
  -n $nEvents_run \
  -r $nRuns \
  --seed $seed\
  --event_tag $event_tag
