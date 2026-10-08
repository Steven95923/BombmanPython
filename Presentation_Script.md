# Presentation Script – Fuel Inventory Management Project
Target length: 6–8 minutes. Each section lists: what to show on screen, what to say (English), and a Chinese note on what the section is really about.

---

## 1. Opening (30 s)
**Show:** notebook title + executive summary cell

**Say:**
"Hi, this is our Fuel Inventory Management project. We analysed two and a half years of purchasing and tank-gauge data for a network of eight gas stations in Hamilton, Ontario. The business question is simple: the stations buy fuel in bulk and get a bigger discount per litre when they order more at once, but tanks are limited and they can't run dry. We wanted to know whether the network is ordering well today, and how it should order instead."

**中文说明：** 一句话讲清矛盾：多买有折扣，但油罐有限、不能断油。

---

## 2. The data and what was wrong with it (60 s)
**Show:** cleaning log table (section 1, "Cleaning log")

**Say:**
"We worked with four datasets: station locations, 23 tanks with their capacities, 2,873 invoices, and about 1.9 million tank-gauge readings taken every 15 minutes.
The data was realistic, which means it was messy. Tank IDs were written inconsistently, the two gauge files used different column names, 42 invoices were blank, and five of them pointed to stations that don't exist. In the gauge data we found sensor spikes, where a reading drops by thousands of litres and jumps straight back 15 minutes later, and a network-wide outage: every tank stopped reporting for 44 days in May and June 2018.
We documented every cleaning decision in a log, so anyone can see what we removed and why."

**中文说明：** 老师明确要求"说清楚你怎么处理脏数据"，这一段就是展示你做到了。重点词：log（日志）。

---

## 3. How we measured demand (60 s)
**Show:** the "interval classification" table in section 1.4, then the validation table (gauge vs invoices)

**Say:**
"The gauges don't tell us sales directly, so we inferred them. Between two consecutive readings, a small drop is fuel sold, a big rise is a delivery, and a very large drop that never recovers is a sensor anomaly we exclude. Summing the drops gives daily consumption per tank, and summing tanks gives it per station and fuel type.
To check that this works, we compared three numbers that should agree: fuel delivered according to the gauges, fuel consumed according to the gauges, and fuel invoiced. For gasoline they agree within a few percent. For diesel the invoices are consistently 8 to 27 percent short, and from spring 2019 both fuels are under-invoiced. So the invoice file is incomplete, and our savings estimates based on invoices are conservative."

**中文说明：** 这是全项目最"技术"的一段，也是最能体现你理解方法的一段。关键逻辑：三个数互相验证，汽油对得上说明方法没问题，柴油对不上说明发票缺了。

---

## 4. Question 1 – How are they doing today? (75 s)
**Show:** the delivery-size histogram with discount thresholds, then the station/fuel inventory grid (16 panels)

**Say:**
"The short answer: they buy small and often. 89 percent of all deliveries are below 15,000 litres, which earns no discount at all. Not a single delivery in two and a half years reached the 40,000-litre top tier. In total the network earned about 206,000 dollars in discounts, which is less than one cent per litre.
Station 1, EastMount, is the interesting one. It is by far the busiest, taking a delivery almost every day, but it runs lean: its gasoline inventory sat below a seven-day reserve more than half the time, and it typically reorders with about six days of fuel left. That's the one station with real stockout exposure. Most other stations are the opposite: they hold two to four weeks of fuel and never come close to running out, but they still order in quantities too small to earn a discount."

**中文说明：** 两个发现：全网几乎不拿折扣；1 号店是唯一真有断油风险的。图上红色区域是 7 天安全线以下，1 号店的曲线一半时间在红区里。

---

## 5. Question 2 – The recommended policy (90 s)
**Show:** the recommended policy table (section 3.3), then the bar chart "current vs proposed vs upper bound", then the simulation table

**Say:**
"Our policy follows the rule in the brief: keep a minimum reserve of seven days of average demand. Available storage is tank capacity minus that reserve, and the attainable discount is the highest tier that fits in that space. Then we order when inventory reaches the reserve, and we order the smallest quantity that earns the best available discount, because ordering more within the same tier only ties up cash.
That gives 40,000-litre orders at station 1 gasoline, station 2 and station 6 gasoline, 25,000 litres at most other stations, and no discount at station 7, whose tanks only hold 5,000 litres.
On exactly the same volume the network actually bought, discounts rise from 206,000 to 996,000 dollars. That is an extra 790,000 over the period, or roughly 300,000 dollars a year, with no capital spending. The theoretical ceiling, four cents on every litre, would be 1.16 million, so the policy captures most of what is physically possible.
We also replayed the policy day by day against actual demand. It never ran out of fuel and never dropped below seven days of cover."

**中文说明：** 这是全片的高潮。三个数要记牢：现在 20.6 万，建议 99.6 万，上限 116 万。模拟回放是证明"建议能落地"。

---

## 6. Question 3 – Day of the week (45 s)
**Show:** monthly price trend chart, then the day-level weekday residual table

**Say:**
"At first glance prices look different by weekday, but that's misleading: every station pays the same supplier price on a given day, and that price moves with the market, doubling in spring 2019. Once we remove the time trend and the quantity discounts and treat each purchase day as one observation, most of the weekday difference disappears.
One pattern survives: price increases cluster on Tuesdays, so Tuesday purchases are about 1.6 cents per litre dearer than other days. Avoiding Tuesday where the discount tier allows it is worth roughly 40,000 dollars a year. That's a useful tie-breaker, not a strategy, and it is on top of the discount savings, not instead of them."

**中文说明：** 老师在这题最想看的是"你有没有被表面差异骗到"。先说差异是假的，再说剥掉干扰后还剩一个小规律，并且把它的分量压低。

---

## 7. Question 4 – Replacing tanks (45 s)
**Show:** best replacement per station table, then the sensitivity heat-map

**Say:**
"We evaluated replacing one tank per station with a 60,000-litre tank at 250,000 dollars each, measuring the gain against our improved policy, not against today.
No replacement pays back within five years. The two best cases are a diesel tank at station 1 and the gasoline tank at station 5, each saving around 19 to 21 thousand dollars a year, which is a 12 to 13 year payback. Station 2 gains nothing because it already reaches the top tier. The sensitivity analysis shows station 1 only turns positive if the tank costs 150,000 and demand grows by 20 percent. So our recommendation is: don't replace tanks on financial grounds."

**中文说明：** 结论是"不值"，这在商业分析里很正常。关键是讲清在什么条件下会翻转。

---

## 8. Limitations and close (30 s)
**Show:** summary table by station and fuel, then limitations section

**Say:**
"Main limitations: demand is inferred from gauges, not metered; there are data gaps; the invoice file is incomplete; and the brief assumes immediate delivery and fully usable tanks, which real operations won't match exactly.
To summarise: adopt the reserve-based ordering policy for about 300,000 dollars a year, avoid Tuesday when the schedule allows, and don't replace tanks. Thank you."

---

## Numbers to memorise

| Item | Number |
|---|---|
| Observation period | 2 Jan 2017 – 15 Aug 2019, 956 days |
| Valid invoices / gauge readings | 2,831 / ~1.86 million |
| Deliveries below 15,000 L | 89 % (73 % of volume) |
| Largest single delivery | 33,827 L (never reached 40k tier) |
| Current discount savings | CAD 205,979 (0.71 c/L) |
| Proposed policy savings | CAD 996,006 |
| Theoretical upper bound | CAD 1,163,068 |
| Incremental | CAD 790,027 total ≈ CAD 302,000 / year |
| Station 1 gasoline below reserve | 53 % of the time |
| Tuesday premium | ≈ 1.6 c/L, ≈ CAD 40,000 / year if avoided |
| Best tank replacement | Station 1 diesel / station 5 gasoline, ~CAD 19–21k/yr, payback 12–13 yrs |

## Likely questions and short answers

- **Why 7 days?** It is the rule given in the brief; we also show what a one-day delivery lead time would do to it.
- **Why order the minimum for the tier instead of filling up?** Same discount per litre, less cash tied up; fill-up is shown as an alternative scenario.
- **How did you handle the 44-day outage?** Those days are excluded from the averages; consumption is only averaged over "complete" days with at least 20 hours of readings.
- **Is the Tuesday effect real?** It holds in 2017 and 2018 and survives several robustness checks, but it disappears in the volatile 2019 period, so we treat it as weak evidence.
- **Why is station 5 gasoline getting no discount?** With the 7-day reserve its available storage is 14,232 L, 768 L short of the 15,000 L tier. Relaxing to 6.5 days would unlock 2 cents.
- **What about fuel ageing at low-volume stations?** We flag it: three diesel sites would go 10–12 months between orders under the pure discount rule, and we recommend capping at ~90 days.
