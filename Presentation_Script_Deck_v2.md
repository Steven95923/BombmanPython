# Presentation Script – Fuel_Inventory_Slides_v2 (22 slides)

Matches notebook **Fuel_Inventory_Analysis_Final_v1** (regular and premium gasoline treated separately, 17 station–fuel groups). Main talk = slides 1–16, about 9–10 minutes. Slides 17–22 are appendix, only for questions.

Each slide: **Show** (what is on screen) · **Say** (English, read as is) · **中文说明**（这页的数怎么来的、可能被问什么）.

---

## Slide 1 – Title (15 s)
**Say:** "Good afternoon. This is our Fuel Inventory Management project: purchasing and replenishment recommendations for a network of eight fuel stations in Hamilton, Ontario, based on two and a half years of invoices and tank-gauge data."

**中文说明：** 只报题目和范围，不展开。

## Slide 2 – Headline (30 s)
**Show:** CAD 295,112 per year

**Say:** "Our headline is simple. By changing *how* the stations order fuel, not *what* they buy, the network can earn about CAD 295,000 more in quantity discounts every year, with no capital investment. Our recommendation is: fix the ordering policy first, pilot it, and only then revisit the question of bigger tanks."

**中文说明：** 295,112 = 956 天内多拿的折扣 772,950 × 365 ÷ 956。这是"折扣"，不是利润，答辩时如果被问，要说明它没有扣掉多压的库存资金和实施成本。

## Slide 3 – Four decisions (40 s)
**Say:** "The assignment asks four questions, and we treat them as four business decisions. One: how well is inventory managed today? Two: which order quantities are feasible and earn better discounts? Three: is there a dependable cheaper weekday? Four: does a bigger tank pay for itself in five years? Three operating rules sit underneath all four: keep seven days of average demand as a reserve, treat regular, premium and diesel as separate fuels, and, as the brief instructs, assume immediate delivery and fully usable capacity."

**中文说明：** "separate regular, premium and diesel" 是 B 和旧版的核心区别。题目原话 "Keep fuel types separate when calculating purchase discounts, available storage, and ordering policies"，我们按字面执行。

## Slide 4 – Data (60 s)
**Show:** 8 stations, 23 tanks, 17 station–fuel groups; 1,859,660 readings; 2,831 invoices; 29.08 million liters; 956 days

**Say:** "We worked with two kinds of evidence. Tank gauges record inventory every fifteen minutes, about 1.86 million readings across 23 tanks. Invoices record 2,831 purchases, 29 million liters over 956 days. The gauges tell us how fast fuel leaves; the invoices tell us how it was bought and at what price.
The data needed cleaning: tank IDs were spelled inconsistently, the two gauge files used different column names, 42 invoices were blank, and the gauges contain sensor spikes and long gaps, including 44 days in 2018 when every tank stopped reporting. We standardised identifiers, removed duplicates and spikes, and estimated demand only from normal inventory decreases, excluding delivery intervals and gaps.
One important qualification: Station 1's gasoline invoices do not distinguish regular from premium. We allocate them using the gauge-based demand split, which gives premium a 12.9 percent share. That is an assumption, and we flag it wherever it matters."

**中文说明：**
- 17 组 = 8 站 × 2 种油 + 1 号店多出来的高级汽油（T13）。
- 1,859,525 是清洗后保留的读数，删了 135 条（2 条空值、71 条重复、48 条同时间冲突、14 条尖峰）。
- 12.9% 的来源：1 号店高级汽油罐日均 1,620 升，普通 10,957 升，1,620 ÷ (1,620 + 10,957) = 12.88%。发票里没有这个数，是从油表推的。**这是最可能被追问的假设**，答法："invoices are coded G only, so we had to allocate; the allocation only affects how Station 1's current discounts are split between the two grades, the station total is unchanged."

## Slide 5 – Small orders miss discounts (45 s)
**Show:** 88.8% below 15,000 L; below-reserve percentages

**Say:** "Today, 88.8 percent of all deliveries are below 15,000 liters, which is the first discount threshold, so they earn nothing. Not one delivery in the whole period reached the 40,000-liter top tier.
At the same time, Station 1 runs lean. Its premium and regular gasoline inventories sit below the seven-day reserve about 65 and 62 percent of the time, and its diesel 13 percent. Station 5 regular is below reserve 10 percent of the time. These are exposures, not confirmed stockouts, but they tell us where to look first."

**中文说明：** "below reserve" 的分母是油表有数据的观测点。1 号店两种汽油都 60% 以上是因为它几乎每天进货但每次量小。其他 13 组从不跌破安全线，所以没列。

## Slide 6 – Current purchasing by station (45 s)
**Show:** table of six station–fuel groups

**Say:** "Purchasing behaviour differs a lot by station. Station 1 diesel takes about 19 deliveries a month averaging 8,100 liters. Station 1 gasoline is the only group earning a meaningful discount today, about CAD 188,000 over the period. Stations 4 and 5 gasoline earned nothing at all. Station 7 diesel buys very little and very rarely.
The paid price column is volume-weighted and reflects when each station happened to buy, so please don't read it as an efficiency ranking."

**中文说明：** 这页的 G 是发票标签，不是策略里的 U/P。Orders/month = 单数 ÷ (956 ÷ 30.44)。全部 16 组在附录第 20、21 页。

## Slide 7 – The reserve determines feasible quantities (60 s)
**Show:** discount table; Station 4 diesel worked example

**Say:** "Here is the logic of the policy. We trigger an order when inventory falls to seven days of average demand. The order must fit in the space above that reserve. Take Station 4 diesel: 40,000 liters of capacity, minus a reserve of 14,710, leaves 25,290 liters of room. A 15,000-liter order fits and earns two cents. A 25,000-liter order fits and earns three cents. A 40,000-liter order does not fit. Filling the available 25,290 liters stays in the same three-cent tier, so we recommend 25,000 liters: the smallest order that earns the best feasible discount. The point is that capacity alone does not decide the discount; the reserve does."

**中文说明：** 14,710 = 7 × 2,101（4 号店柴油日均）。这页是老师最想看的"compare a few feasible scenarios"。注意 4 号店只比 25,000 门槛多 290 升，是边界情况，第 15 页会回到它。

## Slide 8 – Specific recommendations (60 s)
**Show:** table of six representative groups

**Say:** "Applying that logic to every group gives a specific trigger and order size for each. Station 1 regular has 120,000 liters across three tanks, so it can order 40,000 liters and earn four cents. Station 1 premium, with one 40,000-liter tank, reaches the 25,000-liter tier at three cents. Station 4 and most mid-sized stations land at 25,000 liters. Station 5 diesel reaches 15,000. And three groups cannot reach any discount: Station 5 regular has only 14,142 liters of room above its reserve, 858 short of the first threshold, and Station 7's two 5,000-liter tanks leave under 5,000 liters of space. All 17 groups have positive room above the reserve, so the seven-day rule is feasible everywhere."

**中文说明：** 完整 17 组在附录第 18、19 页。5 号店普通汽油差 858 升（B 的数，旧版是 768，因为 B 的日均略高）。7 号店两种油各 4,880 和 4,119 升可用，装满也不到 15,000。

## Slide 9 – More discounts on the same volume (60 s)
**Show:** 205,979 → 978,929; +772,950; ≈295,112/yr; upper bound 1,163,068

**Say:** "Now the financial comparison, on exactly the same 29 million liters the network actually bought. Historically the discounts came to CAD 205,979. Under our policy, with each group ordering its recommended quantity, they come to CAD 978,929. That is CAD 772,950 more over the 956 days, or about CAD 295,000 a year.
For reference, the unconstrained ceiling, four cents on every liter, would be CAD 1.16 million. Capacity and reserve constraints keep the feasible result below that, and that gap is exactly the storage-limited groups on the previous slide."

**中文说明：**
- 978,929 比"采购量 × 折扣"的简单算法略低，因为 B 按整车算：总量 ÷ 订货量取整数车，最后不足一车的余量按它实际的档位拿折扣。被问到就这么答。
- 年化假设这 956 天有代表性。
- 1 号店 U/P 两行的现有折扣是按 12.9% 拆的，但两行加起来等于发票总数，所以网络总额不受这个假设影响。

## Slide 10 – Observed inventory and replenishment (45 s)
**Show:** Station 1 March 2018 chart

**Say:** "This is two weeks at Station 1. Each line is a tank; the vertical jumps marked in red are deliveries, the slopes between them are sales. This is where our demand estimates come from. You can also see one tank, T10, sitting flat at about 8,000 liters: Station 1 keeps one regular tank idle at a time and rotates it, which is why its effective gasoline capacity is a bit below the nominal figure.
We also replayed the policy day by day against actual demand for all 17 groups, holding purchase volume constant and starting and ending at the reserve. It never breached the reserve or the capacity."

**中文说明：** 模拟的三个设定要记住：需求按发票量缩放、起止库存都是安全线、立即到货。被问"模拟为什么可信"，答这三点加"same volume as history"。T10 那条平线如果不解释老师一定会问。

## Slide 11 – Weekday price distributions (45 s)
**Show:** four box plots

**Say:** "For the weekday question we followed the lecture method: box plots of price per liter, Monday to Friday, with the number of invoices under each. Gasoline on the left, diesel on the right; the top row is the paid price, the bottom row adds the quantity discount back so that order size cannot masquerade as a weekday effect.
Gasoline Tuesdays show a slightly higher median. Diesel shows nothing comparable. In every panel the boxes overlap substantially."

**中文说明：** 老师的判断标准：箱子整体更低才算证据，只是中位数略偏就是"偶尔"。这里五个箱子都重叠，所以结论是没有可靠的便宜日。样本数周一到周五：汽油 268/331/292/170/445，柴油 254/218/314/168/358。周六 13 张、周日 0 张，所以只比工作日。

## Slide 12 – No dependable preferred weekday (45 s)
**Show:** gasoline +3.82¢ Tuesday, diesel ≈0; CAD 0 extra savings

**Say:** "We then compared like with like: same station, same fuel, same month. In that matched comparison gasoline Tuesdays are about 3.8 cents dearer than the station-month median; diesel shows no difference. But the pattern is historical, it does not appear in diesel, and the comparable sample is under half of the observations. By the box-plot test it is 'sometimes', not 'most of the time'. So we recommend no compulsory ordering day, and we credit zero additional weekday savings. Where inventory allows flexibility, the station should simply use the actual quote on the day."

**中文说明：** 可比样本 996 / 2,195 个日观测，来自 1、2、4、5 四个站（其他站同月同油种订单太少没法配对）。这页是"证据不足就是谣言"的结论，和老师的口径一致。

## Slide 13 – No station recovers replacement cost (60 s)
**Show:** per-station table; strongest case Station 5 T25, payback 12.2 years

**Say:** "Question four: replacing one tank per station with a 60,000-liter tank at CAD 250,000. We measure the gain against our improved ordering policy, not against today's inefficient ordering, otherwise we would credit the tank with savings that the policy already delivers.
No station pays back within five years. The strongest case is Station 5, replacing its 25,000-liter regular tank: the station would move from no discount to four cents, worth about CAD 20,500 a year, but that is still a twelve-year payback and a five-year net of minus CAD 148,000. Station 1 diesel is similar. Station 2 gains nothing because it already reaches the top tier and its big tanks are already larger than 60,000 liters."

**中文说明：** 年增量 = 年采购量 × (新折扣 − 策略折扣)。五年净 = 5 × 年增量 − 250,000。回本 = 250,000 ÷ 年增量。假设额外运营成本为零、不折现。附录第 22 页有每个罐的明细。

## Slide 14 – Only one tested case is positive (40 s)
**Show:** sensitivity table for Stations 1 and 5

**Say:** "We stress-tested this with three replacement costs and three demand levels, 72 combinations in all. Only one is positive: Station 1 at CAD 150,000 and demand 20 percent above baseline, worth about CAD 67,000 over five years. Everything else is negative. So this is a scenario, not a forecast, and the practical reading is: don't replace tanks now; revisit only if a quote comes in well under 150,000 and demand has clearly grown."

**中文说明：** 需求变了两件事跟着变：安全库存变大（可用空间变小、可能掉档）和年采购量变大。正值那一格是 T10，不是基准情况下最好的 T12，因为需求涨了以后最佳罐会变。

## Slide 15 – Demand changes can reduce the discount (40 s)
**Show:** Station 1 regular 4→3 cents, Station 4 diesel 3→2 cents at +5% demand

**Say:** "One more sensitivity that matters for implementation. Because the reserve scales with demand, a five percent rise in demand shrinks the available space enough to drop Station 1 regular from four cents to three, and Station 4 diesel from three to two. These are the two groups sitting right at a threshold. So before the pilot, verify the grade-level records and the demand estimates; during the pilot, monitor reserve exposure, realised discounts and cash tied up in inventory."

**中文说明：** 这就是 4 号店"只多 290 升"的后果。被问"你们的估计有多可靠"，答：我们用第二种方法重算过日消耗，差异在 3% 以内，但 4 号店离门槛只有 1 到 3%，所以要用新数据复核。

## Slide 16 – Recommended next step (30 s)
**Say:** "To close: validate the grade-specific records, pilot the ordering policy and measure what it actually earns, use real quotes rather than a fixed weekday, and defer tank replacement. The prize is roughly CAD 295,000 a year under the model's assumptions. The decision we are asking for is support for data validation and a controlled pilot. Thank you, happy to take questions."

---

## Appendix slides 17–22 (only if asked)

| Slide | Use when asked about | Key point |
|---|---|---|
| 17 | Full sensitivity for all 8 stations | All negative except Station 1 at 150k & +20% |
| 18–19 | Trigger / order / savings for any specific group | Station 1 U: 76,702 / 40,000 / 4c; Station 1 P: 11,340 / 25,000 / 3c; Station 5 U: 10,858 / 14,142 / 0c |
| 20–21 | Current purchasing for any station | Station 1 G: 762 invoices, 14,260 L avg, 24.3/month |
| 22 | Which tank, how much extra capacity, payback | T25 at Station 5: +35,000 L, 12.2 yr; T12 at Station 1: +20,000 L, 13.5 yr |

## Numbers to memorise (B version)

| Item | Number |
|---|---|
| Period | 2 Jan 2017 – 15 Aug 2019, 956 days |
| Raw / retained readings | 1,859,660 / 1,859,525 |
| Valid invoices / liters | 2,831 / 29.08 million |
| Below 15,000 L | 88.8% of invoices; none ≥ 40,000 L |
| Current discounts | CAD 205,979 |
| Policy discounts | CAD 978,929 |
| Extra | CAD 772,950 over period ≈ CAD 295,112 / year |
| Upper bound | CAD 1,163,068 |
| Station 1 premium share | 12.9% (assumption) |
| Below reserve | S1 P 65.1%, S1 U 61.5%, S1 D 13.5%, S5 U 10.4% |
| Groups with no discount reachable | Station 5 regular, Station 7 both fuels |
| Tuesday gasoline premium (matched) | +3.82 c/L; diesel 0; credited savings CAD 0 |
| Best replacement | Station 5 T25: +CAD 20,480/yr, 5-yr net −147,600, payback 12.2 yr |
| Only positive scenario | Station 1 T10 at CAD 150k and +20% demand: +66,950 |

## Likely questions and short answers

- **Why separate regular and premium?** The brief says to keep fuel types separate for discounts, storage and ordering; they are physically different products in different tanks.
- **Where does 12.9% come from?** From gauge-based demand: premium 1,620 L/day vs regular 10,957 L/day at Station 1. Invoices only say "G", so an allocation was unavoidable; it only affects how Station 1's historical discount is split, not the network total.
- **How did you estimate demand?** From gauge decreases between consecutive readings, excluding deliveries, gaps and anomalies; scaled to 24 hours; averaged over days with at least 20 hours of coverage. A second method gave results within about 3%.
- **Why is the policy total not simply volume × discount?** Because we count whole deliveries; the final partial delivery of each group earns only the discount for its actual size.
- **Is the replay a guarantee against stockouts?** No. It assumes immediate delivery and continuous monitoring. It shows the policy is internally consistent, not that the real world will behave.
- **Why no weekday recommendation when Tuesday is dearer?** Boxes overlap; the effect is gasoline-only, historical, and based on under half the observations. By the lecture's test that is not enough evidence.
- **What about delivery lead time?** With a real lead time the trigger must rise by the demand during the lead time, which shrinks available space; at threshold groups like Station 1 regular and Station 4 diesel that costs one discount tier. The data cannot tell us the actual lead time.
- **What did you leave out?** Holding and financing cost of larger orders, fuel ageing at low-volume stations, truck compartment sizes, site constraints for bigger tanks, and the gauge-vs-invoice volume gap (gauges show more diesel moving than was invoiced).
