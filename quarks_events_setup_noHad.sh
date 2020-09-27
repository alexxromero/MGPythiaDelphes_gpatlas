#!/usr/bin/env bash

starting_dir=$(pwd)
cards_dir="$(pwd)/cards"
gridpack_dir="/export/home/alexir2/gridpacks_qg"
#pythia_card="${cards_dir}/configLHE.cmnd"
pythia_card="${cards_dir}/configLHE_noHad.cmnd"
#delphes_card="${cards_dir}/delphes_card_ATLAS.tcl"
nEvents_run=100000

# ------------------- quarks ------------------------ #
jet_type="quarks"
pT_range=200
gridpack="${gridpack_dir}/${jet_type}_${pT_range}GeV_gridpack.tar.gz"
delphes_card="${cards_dir}/delphes_card_ATLAS_${pT_range}GeV.tcl"
nRuns=100
seed=123
event_tag="quarks_200_sept242020_noHad"

python ./gen_events_slurm.py \
  -g $gridpack \
  --pythia_card $pythia_card \
  --delphes_card $delphes_card \
  -n $nEvents_run \
  -r $nRuns \
  --seed $seed \
  --pT_range $pT_range \
  --event_tag $event_tag


# ------------------- quarks ------------------------ #
jet_type="quarks"
pT_range=500
gridpack="${gridpack_dir}/${jet_type}_${pT_range}GeV_gridpack.tar.gz"
delphes_card="${cards_dir}/delphes_card_ATLAS_${pT_range}GeV.tcl"
nRuns=120
seed=1234
event_tag="quarks_500_sept242020_noHad"

python ./gen_events_slurm.py \
  -g $gridpack \
  --pythia_card $pythia_card \
  --delphes_card $delphes_card \
  -n $nEvents_run \
  -r $nRuns \
  --seed $seed \
  --pT_range $pT_range \
  --event_tag $event_tag


# ------------------- quarks ------------------------ #
jet_type="quarks"
pT_range=1000
gridpack="${gridpack_dir}/${jet_type}_${pT_range}GeV_gridpack.tar.gz"
delphes_card="${cards_dir}/delphes_card_ATLAS_${pT_range}GeV.tcl"
nRuns=140
seed=12345
event_tag="quarks_1000_sept242020_noHad"

python ./gen_events_slurm.py \
  -g $gridpack \
  --pythia_card $pythia_card \
  --delphes_card $delphes_card \
  -n $nEvents_run \
  -r $nRuns \
  --seed $seed \
  --pT_range $pT_range \
  --event_tag $event_tag
