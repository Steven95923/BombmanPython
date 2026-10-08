# Cross-check prompt for ChatGPT (or any other AI)

Paste everything below the line into ChatGPT, together with the two small files `data/Tanks.csv` and `data/Invoices.csv` (the fuel-level files are too big to upload; the consumption numbers are given in the prompt). Ask it to check our logic and our numbers independently. Compare its answers with section 3.3 and section 5.1 of the notebook.

---

I am checking a group project about fuel inventory for 8 gas stations. Please recompute the following independently from the attached `Tanks.csv` and `Invoices.csv` and tell me if you get the same numbers. Do not assume my numbers are right.

**Rules from the assignment**
- Quantity discount per delivery, applied to every liter in that delivery: less than 15,000 L = 0; 15,000 to <25,000 L = CAD 0.02/L; 25,000 to <40,000 L = CAD 0.03/L; 40,000 L or more = CAD 0.04/L.
- Discounts are per station and per fuel type. Tank types U and P are both gasoline (invoice fuel type G); D is diesel.
- Minimum reserve = 7 x average daily consumption. Orders arrive immediately. Available space at the reserve = total capacity of that fuel at the station minus the reserve. The best attainable discount is the largest threshold that fits in the available space.
- Invoices.csv contains 42 blank rows (drop them) and some rows with station IDs that don't exist (they are among the blank rows).

**Average daily consumption we estimated from tank gauges (liters per day)**
Station 1: G 12,484, D 7,080. Station 2: G 3,146, D 4,098. Station 3: G 512, D 450. Station 4: G 1,897, D 2,087. Station 5: G 1,538, D 1,043. Station 6: G 434, D 67. Station 7: G 124, D 16. Station 8: G 243, D 74.

**Please check**
1. Number of valid invoices after dropping blank rows and duplicates, the date range, and the total liters and total cost.
2. Total discount savings actually earned (sum over invoices of liters x applicable discount). We get CAD 205,979.
3. Share of invoices below 15,000 L. We get 89%. Largest delivery: we get 33,827 L.
4. For each station and fuel type: total capacity, reserve, available space, best attainable discount, and the savings if every liter actually bought got that discount. Our totals: policy savings CAD 996,007, upper bound (4 cents on everything) CAD 1,163,069.
5. Tank replacement: replacing one tank per station with a 60,000 L tank at CAD 250,000. Extra annual savings = annual liters x (new discount - policy discount), annual liters = total liters x 365 / 956. Which station has the best 5-year net benefit (5 x annual savings - 250,000)? We get station 5 (replace T25, 25,000 L gasoline) at about -CAD 147,000 and station 1 (replace a 40,000 L diesel tank) at about -CAD 157,000, i.e. nothing pays back in 5 years.
6. Is there anything in our logic that contradicts the assignment rules above?

Please show your calculations as a table so I can compare line by line.
