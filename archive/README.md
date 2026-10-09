# Archive

Not part of the submission. Kept for reference.

* `Fuel_Inventory_Analysis_full_version.ipynb` – the earlier, more technical version of the notebook (Styler tables, 15-minute inventory grid, Kruskal-Wallis test, lead-time and weekday-flexibility analysis, sensitivity heat-map). Same data, same method, same conclusions as the submitted notebook; it was simplified to course level for the submission. Git history: commit 8eafc69.
* `crosscheck_alternative_method.py` – a short script that recomputes the key numbers with a different approach (rolling-median smoothing, first-reading-minus-last-reading daily consumption, `pd.cut` discount tiers). Run it from the repo root with `python3 archive/crosscheck_alternative_method.py`; it prints the comparison tables. Together with `../Codex_crosscheck_report.md` this is the cross-check evidence.
