# Fuel Inventory Management Project

Python notebook answering the four business questions of the Fuel Inventory Management group project
(gas-station network, Hamilton ON, Jan 2017 – Aug 2019).

## Contents

| Path | What it is |
|---|---|
| `Fuel_Inventory_Analysis.ipynb` | The full analysis: data cleaning, Q1–Q4, summary table, limitations, references (already executed, outputs included) |
| `data/Locations.csv`, `Tanks.csv`, `Invoices.csv`, `Fuel_Level_Part_1.csv`, `Fuel_Level_Part_2.csv` | The supplied datasets (unchanged, renamed from the `-1` download copies) |
| `summary_by_station_fuel.csv` | The station × fuel summary table written by the notebook |

## How to run

**Google Colab**
1. Upload `Fuel_Inventory_Analysis.ipynb` to Colab (File ▸ Upload notebook).
2. Run the first code cell – it asks you to upload the five CSV files (select all five at once). They are stored in a `data/` folder inside the Colab session.
   Alternatively mount Google Drive and put the notebook and a `data/` folder in the same Drive directory.
3. Runtime ▸ Run all. Takes about 2–4 minutes.

**Local Jupyter / VS Code**
Keep the notebook and the `data/` folder together and run all cells. Requirements: Python 3.9+, pandas, numpy, matplotlib (scipy optional, used for one statistical test).

All file paths are relative. The loader also accepts the original download names (`Locations-1.csv` etc.).

## Collaborating on this repo

* `Fuel_Inventory_Analysis.ipynb` is the single source of truth. Before editing, pull the latest version; after editing, **Runtime ▸ Restart and run all** so the outputs match the code, then commit.
* Notebook diffs are hard to read on GitHub. Keep commits small and say in the message which section (Q1–Q4, summary, limitations) you changed.
* Do not rename or edit the files in `data/`; the notebook loads them by name.
* `Presentation_Script.md` is the script for the recorded presentation; `simulation_policy_vs_actual.png` and `summary_by_station_fuel.csv` are exported by the notebook and will be regenerated on every full run.
