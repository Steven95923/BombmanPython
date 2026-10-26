# Recording Script – Speaker A, Slides 1–8

Deck: Fuel_Inventory_Slides_FINAL_V11. Your part runs about 4 minutes. Square brackets are cues, not words. Say rounded numbers; the slides show the precise ones.

---

## Before you record (your slides only)

- Slide 1: remove "V11 Verified Final" from the title if it is still there.
- Slides 6 and 8: remove footnote phrases "shown to V11's two-decimal precision" and "match V11".
- Full-screen the deck (press F). Record screen plus voice. When a cue says [point], move the mouse there so it shows in the video.
- Do one dry run with a timer. Target 3:45–4:15.

---

## Slide 1 — Title (15 s)

Hello, everyone.

Today we will present our fuel inventory project for eight gas stations.

We looked at how much fuel they order, when they order it, and whether they need larger tanks.

Our goal is to lower buying costs while keeping enough fuel in storage.

> **中文：** 只报题目和范围。"lower buying costs while keeping enough fuel" 就是整个项目的矛盾：多买有折扣，但不能断油。

## Slide 2 — Headline (25 s)

Our main finding is simple.

The stations should improve their ordering first, before buying new tanks.

Our model shows about **two hundred and ninety-five thousand dollars** in extra discounts per year.

This is an estimate. Extra storage and financing costs would affect the final profit.

We will explain where this benefit comes from.

> **中文：** 295,111.50 = 956 天多拿的折扣 772,949.59 × 365 ÷ 956。它是"折扣"不是"利润"，所以第二句一定要说。

## Slide 3 — Four decisions (35 s)

We asked four questions.

How well do the stations manage fuel today?

How can they improve their orders?

Is there a better weekday to buy fuel?

And are larger tanks worth the cost?

We follow the project rules. Each station must keep seven days of average demand as a reserve.

We calculate each fuel type separately. We also assume that deliveries arrive immediately and all tank capacity is usable.

> **中文：** 三条规则来自作业：7 天安全库存；普通汽油、高级汽油、柴油分开算（这是 B 版的特点）；立即到货、容量全可用是题目给的简化假设，不是我们的发明。

## Slide 4 — Data (60 s)

We used two main types of records: tank readings and purchase invoices.

The data covers eight stations and twenty-three tanks.

It includes almost **two million readings** and about **twenty-eight hundred invoices**, over roughly **two and a half years**.

We checked for missing data, duplicates, and unusual readings. For example, every tank stopped reporting for forty-four days in May and June of 2018, so those days are excluded from our demand estimates.

We then used changes in fuel levels to estimate daily demand.

One issue is important. Station One's gasoline invoices do not separate regular and premium.

We estimated that split from demand. Premium accounts for about **thirteen percent**. The financial results depend on this estimate.

> **中文：**
> - 1,859,660 条原始读数，清洗后 1,859,525 条；2,831 张有效发票（原 2,873 减 42 行空白）；956 天。
> - "changes in fuel levels to estimate daily demand"：油表每 15 分钟一条，相邻读数的下降就是卖掉的油，上升是进货，排除掉进货段、断档和异常后按天加总。
> - 13% 的来源：1 号店高级汽油罐 T13 日均约 1,620 升，普通罐 T10/T11/T14 合计约 10,957 升，1,620 ÷ 12,577 = 12.88%。发票只写 G，没有这个数，所以是假设。**这是你这部分最可能被追问的点**，所以台词里主动说了 "depend on this estimate"。

## Slide 5 — Small orders miss discounts (40 s)

We found two main problems.

First, almost **ninety percent** of invoices are below the first discount level. So most deliveries earn no quantity discount.

Second, some fuel groups often fall below the seven-day reserve.

[Point to the two longest bars.]

At Station One, this happens in about **sixty-five percent** of valid readings for premium and **sixty-two percent** for regular gasoline.

This means less fuel protection. It does not mean the station actually ran out of fuel.

Missing readings also limit what we can say.

> **中文：** 88.8% 的发票低于 15,000 升，没有一单到 40,000 升。1 号店两种汽油 60% 以上时间低于安全线，因为它几乎天天进货但每次量小；1 号店柴油 13.5%，5 号店普通汽油 10.4%；其他 13 组从不跌破。"valid readings" 指油表有数据的时点，覆盖率约 91% 到 95%。

## Slide 6 — Current purchasing varies by station (35 s)

This table shows that stations have different buying patterns.

For example, Station One orders diesel about **nineteen times a month**. Each order averages about **eight thousand liters**.

Station Four and Station Five earned no gasoline quantity discounts during the period.

Station Seven's diesel orders are much smaller and less frequent.

So one order size will not suit every station.

The prices also reflect different fuels and purchase dates. A lower price alone does not prove better management.

> **中文：** 这页的 G 是发票标签，不是策略里的 U/P。每月单数 = 单数 ÷ (956 ÷ 30.44)。1 号店汽油是唯一常拿折扣的组，956 天拿了 188,240。全部 16 组在附录第 20、21 页，视频里不用翻。

## Slide 7 — The reserve determines feasible quantities (55 s)

Our policy has two parts: when to order, and how much to order.

We order when fuel reaches the seven-day reserve.

The delivery must fit in the space above that reserve.

[Point to the Station Four example.]

Station Four's diesel capacity is **forty thousand liters**. Its reserve is about **fifteen thousand liters**.

That leaves just over **twenty-five thousand liters** of space.

An order of twenty-five thousand liters fits and earns **three cents per liter**.

An order of forty thousand does not fit.

Filling the remaining space gives the same discount rate. We therefore recommend twenty-five thousand liters.

> **中文：** 安全库存 14,709.55 = 7 × 2,101.36（4 号店柴油日均）。可用空间 40,000 − 14,710 = 25,290，只比 25,000 门槛多 290 升，所以是边界情况（Speaker B 第 15 页会讲需求涨 5% 它就掉档）。"装满也是 3 分，所以订 25,000"：同档折扣一样，少订少压钱。这页是老师要求的"比较几个可行方案"。

## Slide 8 — Specific recommendations (45 s) — hand over after this slide

The same rule gives different results at different stations.

Station One can order **forty thousand liters** of regular gasoline, earning **four cents per liter**.

For premium, it can order **twenty-five thousand liters**, earning **three cents**.

But Station Five's regular gasoline has space for only about **fourteen thousand liters** above reserve. That is below the first discount level.

So tank capacity matters, but we must also leave enough fuel in reserve.

I will now hand over to my teammate to explain the benefits and the other decisions.

> **中文：** 1 号店普通汽油三个罐 120,000 升，安全库存 76,702，可用 43,298 ≥ 40,000 → 4 分；高级一个罐 40,000，安全库存 11,340，可用 28,660 → 25,000 升 3 分。5 号店普通汽油可用 14,141.68，差 858 升够不到 15,000。7 号店两种油各不到 5,000 升可用，也拿不到折扣。17 组全部可用空间为正，所以 7 天规则处处可行。

---

## If you record a short "questions you may have" segment

Speaker B will cover this at the end, but if the team decides you should answer the Station One question yourself, here is the 25-second version:

"You may wonder where the thirteen percent premium share comes from. It comes from the tank readings: at Station One, premium demand is about sixteen hundred liters a day and regular about eleven thousand. Invoices only say 'gasoline', so we had to split them. The split only affects how Station One's historical discount is divided between the two grades; the station total is unchanged."

## Practice cues

| Slide | Say this if you lose your place |
|---|---|
| 1 | Eight stations. Better orders. Enough fuel. |
| 2 | Improve orders first. About $295,000 a year. Estimate, not profit. |
| 3 | Four questions. Seven-day reserve. Separate fuels. Immediate delivery. |
| 4 | Readings and invoices. 44-day gap excluded. Station One split is estimated, 13%. |
| 5 | Almost 90% miss discounts. Station One below reserve 65% / 62%. Not stockouts. |
| 6 | Different stations, different patterns. Station One diesel: 19 orders a month. |
| 7 | Order at reserve. Delivery must fit. Station Four: 25,000 L at 3 cents. |
| 8 | Station One: 40,000 regular, 25,000 premium. Station Five: no discount. Hand over. |
