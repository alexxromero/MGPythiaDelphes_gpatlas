# MG5+Pythia+Delphes event generation

This repo contains the basics of generating MadGraph events with Pythia8
and Delphes detector simulation in the UCI's GP cluster.

The specifics of the event are setup on the gen_events_setup.sh. This file
creates the files MG5PythiaDelphes.sh with the MG+Pythia+Delphes commands and
submit_jobs.sh to submit the job to SLURM.

Usage:    

      bash gen_events_setup.sh
      bash [event_tag]/submit_jobs.sh

Run specifications:
- gridpack: generated via MadGraph
- pythia_card: pythia card
- delphes_card: delphes card
- nEvents_run: events per run
- nRuns: no. of runs
- seed: gridpack seed. Must be different for each run.
- event_tag: tag for naming the output directory

**Note: ** Delphes and pythia are downloaded and built in each job. To save time and avoid the download, specify the path of the pre-built directories.
