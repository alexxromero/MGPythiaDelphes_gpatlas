#!/usr/bin/env bash

starting_dir=$(pwd)
cards_dir="$(pwd)/cards"
gridpack_dir="${HOME}/gridpacks_qg"
pythia_card="${cards_dir}/configLHE_noHad.cmnd"
#delphes_card="${cards_dir}/delphes_card_ATLAS.tcl"

# ------------------- quarks ------------------------ #
jet_type="quarks"
pT_range=200
gridpack="${gridpack_dir}/${jet_type}_${pT_range}GeV_gridpack.tar.gz"
delphes_card="${cards_dir}/delphes_card_ATLAS_${pT_range}GeV.tcl"
nBatches_100k=45
initial_seed=7000
event_tag="quarks_200_sept242020_noHad"

python ./genEvents_script.py \
  -g $gridpack \
  --pythia_card $pythia_card \
  --delphes_card $delphes_card \
  --nBatches_100k $nBatches_100k \
  --initial_seed $initial_seed \
  --pT_range $pT_range \
  --event_tag $event_tag


# ------------------- quarks ------------------------ #
jet_type="quarks"
pT_range=500
gridpack="${gridpack_dir}/${jet_type}_${pT_range}GeV_gridpack.tar.gz"
delphes_card="${cards_dir}/delphes_card_ATLAS_${pT_range}GeV.tcl"
nBatches_100k=30
initial_seed=8000
event_tag="quarks_500_sept242020_noHad"

python ./genEvents_script.py \
  -g $gridpack \
  --pythia_card $pythia_card \
  --delphes_card $delphes_card \
  --nBatches_100k $nBatches_100k \
  --initial_seed $initial_seed \
  --pT_range $pT_range \
  --event_tag $event_tag


# ------------------- quarks ------------------------ #
jet_type="quarks"
pT_range=1000
gridpack="${gridpack_dir}/${jet_type}_${pT_range}GeV_gridpack.tar.gz"
delphes_card="${cards_dir}/delphes_card_ATLAS_${pT_range}GeV.tcl"
nBatches_100k=25
initial_seed=9000
event_tag="quarks_1000_sept242020_noHad"

python ./genEvents_script.py \
  -g $gridpack \
  --pythia_card $pythia_card \
  --delphes_card $delphes_card \
  --nBatches_100k $nBatches_100k \
  --initial_seed $initial_seed \
  --pT_range $pT_range \
  --event_tag $event_tag
