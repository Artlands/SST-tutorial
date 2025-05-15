# SST-Tutorial Demos

This folder contains demo materials for the SST tutorial designed for the Southeast University team.

## Folder Structure

- **`GUPS/`**  
  Contains the source code for a simplified version of the GUPS benchmark.

- **`MR/`**  
  Contains the source code for a simplified version of the OSU Micro-Benchmark (message rate test).

## Configuration Files

- **`gups.cfg`** and **`mr.cfg`**  
  SST simulation configuration files for the GUPS and MR demos, respectively.

- **`rev-xbgas-topo.py`**  
  Python script for setting up and running the SST simulation.

## Instructions

### 1. Build the Executables

Navigate to each demo folder (`GUPS/` and `MR/`) and run:

```bash
make
```

### 2. Run the Simulation

Use the following command to launch an SST simulation:
```bash
sst rev-xbgas-topo.py --model-options="-c gups.cfg"
```
Replace gups.cfg with mr.cfg to run the MR benchmark.