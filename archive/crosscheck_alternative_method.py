"""Independent re-computation of the key numbers with a different method, for cross-checking the notebook."""
import pandas as pd, numpy as np
D = "data/"
tanks = pd.read_csv(D + "Tanks.csv"); tanks["Tank ID"] = tanks["Tank ID"].str.replace(" ", "")
tanks["Fuel"] = np.where(tanks["Tank Type"] == "D", "D", "G")
cap = tanks.groupby(["Tank Location", "Fuel"])["Tank Capacity"].sum()

inv = pd.read_csv(D + "Invoices.csv").dropna(subset=["Amount Purchased", "Gross Purchase Cost", "Fuel Type"]).drop_duplicates()
inv["d"] = pd.to_datetime(inv["Invoice Date"], format="%m/%d/%Y")
days = (inv["d"].max() - inv["d"].min()).days + 1
# discount via pd.cut (different implementation from the if/elif function)
rate = pd.cut(inv["Amount Purchased"], bins=[0, 15000, 25000, 40000, np.inf], right=False, labels=[0, .02, .03, .04]).astype(float)
inv["saved"] = inv["Amount Purchased"] * rate
cur = inv.groupby(["Invoice Gas Station Location", "Fuel Type"]).agg(liters=("Amount Purchased", "sum"), saved=("saved", "sum"))
cur.index.names = ["Station", "Fuel"]
print("invoices:", len(inv), "days:", days, "| current savings:", round(cur["saved"].sum()))

# --- consumption by a different method: start-of-day minus end-of-day level + upward jumps (>300 L) within the day ---
f = pd.concat([pd.read_csv(D + "Fuel_Level_Part_1.csv").set_axis(["Tank ID", "Level", "Time"], axis=1),
               pd.read_csv(D + "Fuel_Level_Part_2.csv").set_axis(["Tank ID", "Level", "Time"], axis=1)])
f["Tank ID"] = f["Tank ID"].str.replace(" ", ""); f["Time"] = pd.to_datetime(f["Time"], format="%m/%d/%Y %H:%M")
f = f.dropna().drop_duplicates(subset=["Tank ID", "Time"], keep="first").sort_values(["Tank ID", "Time"])
# rolling-median smoothing (window 5) instead of spike rule
f["Level_s"] = f.groupby("Tank ID")["Level"].transform(lambda s: s.rolling(5, center=True, min_periods=1).median())
f["date"] = f["Time"].dt.normalize()
f["jump"] = f.groupby(["Tank ID", "date"])["Level_s"].diff().clip(lower=0)
f.loc[f["jump"] < 300, "jump"] = 0
g = f.groupby(["Tank ID", "date"]).agg(first=("Level_s", "first"), last=("Level_s", "last"), jumps=("jump", "sum"), n=("Level", "count"))
g["sold"] = g["first"] - g["last"] + g["jumps"]
g = g[g["n"] >= 88].reset_index()                       # at least 88 readings ~ 22 h of 15-min data
g = g.merge(tanks[["Tank ID", "Tank Location", "Fuel"]], on="Tank ID")
ntank = tanks.groupby(["Tank Location", "Fuel"])["Tank ID"].count()
sf = g.groupby(["Tank Location", "Fuel", "date"]).agg(sold=("sold", "sum"), k=("Tank ID", "count")).reset_index()
sf = sf.merge(ntank.rename("n").reset_index(), on=["Tank Location", "Fuel"])
sf = sf[sf["k"] == sf["n"]]
# drop implausible days (> 5x median) as a crude anomaly filter
med = sf.groupby(["Tank Location", "Fuel"])["sold"].transform("median")
sf = sf[(sf["sold"] >= 0) & (sf["sold"] <= 5 * med + 500)]
avg = sf.groupby(["Tank Location", "Fuel"])["sold"].mean(); avg.index.names = ["Station", "Fuel"]

pol = pd.DataFrame({"cap": cap.values, "avg": avg.reindex(cap.index).values}, index=avg.index)
pol["reserve"] = 7 * pol["avg"]; pol["avail"] = pol["cap"] - pol["reserve"]
pol["tier_q"] = pd.cut(pol["avail"], bins=[-np.inf, 15000, 25000, 40000, np.inf], right=False, labels=[0, 15000, 25000, 40000]).astype(float)
pol["rate"] = pd.cut(pol["tier_q"], bins=[-1, 14999, 24999, 39999, np.inf], labels=[0, .02, .03, .04]).astype(float)
pol["liters"] = cur["liters"]; pol["cur_saved"] = cur["saved"]; pol["pol_saved"] = pol["liters"] * pol["rate"]
pol["liters_yr"] = pol["liters"] * 365 / days
print(pol.round(0).to_string())
print("policy savings:", round(pol["pol_saved"].sum()), "| extra:", round((pol["pol_saved"] - pol["cur_saved"]).sum()),
      "| per year:", round((pol["pol_saved"] - pol["cur_saved"]).sum() * 365 / days), "| upper bound:", round(pol["liters"].sum() * .04))

# --- Q4 brute force ---
rows = []
for _, t in tanks.iterrows():
    key = (t["Tank Location"], t["Fuel"]); r = pol.loc[key]; extra = 60000 - t["Tank Capacity"]
    if extra <= 0: continue
    av2 = r["avail"] + extra
    rate2 = .04 if av2 >= 40000 else .03 if av2 >= 25000 else .02 if av2 >= 15000 else 0
    inc = r["liters_yr"] * (rate2 - r["rate"])
    rows.append((t["Tank Location"], t["Tank ID"], t["Fuel"], round(inc), round(5 * inc - 250000), round(250000 / inc, 1) if inc > 0 else None))
q4 = pd.DataFrame(rows, columns=["Station", "Tank", "Fuel", "inc_per_year", "net5", "payback"]).sort_values(["Station", "inc_per_year"], ascending=[True, False]).groupby("Station").head(1)
print(q4.to_string(index=False))
