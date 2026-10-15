# Notebook 代码逐层讲解

对着 `Fuel_Inventory_Analysis.ipynb` 看。顺序和 notebook 一样。每个代码块讲三件事：**做什么、关键行什么意思、为什么这么做**。

先记住贯穿全文的几个"角色"（变量名），后面反复出现：

| 变量 | 是什么 | 一行一条什么 |
|---|---|---|
| `locations` | 8 家店 | 一家店 |
| `tanks` | 23 个油罐 | 一个油罐 |
| `capacity` | 每家店每种油的总容量 | 一个"店 + 油种" |
| `invoices` | 清洗后的发票 | 一张发票 |
| `levels` | 清洗后的油表读数 | 一个油罐的一次读数 |
| `daily_tank` | 每个油罐每天的销量 | 一个油罐的一天 |
| `daily` | 每家店每种油每天的销量 | 一个"店 + 油种"的一天 |
| `consumption` | 日均消耗统计 | 一个"店 + 油种" |
| `policy` / `recommend` | 订货策略表 | 一个"店 + 油种" |

数据流向是：`levels` → `daily_tank` → `daily` → `consumption` → `policy` → `recommend` → 汇总表。发票那条线是：`invoices` → `current`（现状统计）→ 并入 `recommend`。

---

## 0. 准备工作

### 0.1 导入和找文件

```python
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
```

四个工具：`os` 管文件路径，`numpy` 做数学（主要用 `np.where`），`pandas` 处理表格，`matplotlib` 画图。

```python
def find_file(name):
    for path in [os.path.join(DATA_DIR, name), name,
                 os.path.join(DATA_DIR, name.replace(".csv", "-1.csv")), name.replace(".csv", "-1.csv")]:
        if os.path.exists(path):
            return path
    return None
```

给一个文件名，按四个位置依次找：`data/Locations.csv`、`Locations.csv`、`data/Locations-1.csv`、`Locations-1.csv`。找到第一个存在的就返回。为什么要这么麻烦：作业要求相对路径且能在老师电脑上跑，而浏览器下载时可能给文件名加 `-1`，这样两种情况都能读。

```python
missing = [f for f in FILES if find_file(f) is None]
if missing:
    try:
        from google.colab import files
        ...
    except ImportError:
        raise FileNotFoundError(...)
```

列出找不到的文件。如果在 Colab 里（能 import `google.colab`），弹出上传框；不在 Colab 就直接报错提示。

### 0.2 常量

```python
def discount_rate(liters):
    if liters >= 40000:
        return 0.04
    elif liters >= 25000:
        return 0.03
    elif liters >= 15000:
        return 0.02
    else:
        return 0.00
```

这就是课上学的 `def` 加 `if/elif/else`。给一个升数，返回每升折扣。**从大到小判断**是关键：先问是不是 ≥ 40,000，不是再问 ≥ 25,000，这样 30,000 不会被 ≥ 15,000 先截住。`discount_tier` 结构一样，只是返回文字标签，用来画图和统计。

```python
RESERVE_DAYS = 7
NEW_TANK = 60000
NEW_TANK_COST = 250000
YEARS = 5
SPIKE = 2000; GAP_HOURS = 6; DELIVERY = 500; MAX_DROP = 2000; MIN_HOURS = 20
```

所有"拍脑袋定的数"集中在这里。改一处，全文跟着变。前四个是题目给的，后五个是我们清洗油表数据时定的阈值（1.4 节解释）。

---

## 1. 读数据和清洗

### 1.1 Locations

```python
locations = pd.read_csv(find_file("Locations.csv"))
locations = locations.rename(columns={"Gas Station Location": "Station", "Gas Station Name": "Name"})
print(locations.isnull().sum())
```

读进来，把长列名改短（后面 merge 时列名要对得上），数一下每列有几个空值。8 号店坐标在华盛顿这件事只在文字里说明，因为坐标不参与任何计算。

### 1.2 Tanks

```python
tanks["Tank ID"] = tanks["Tank ID"].str.replace(" ", "")
```

`.str` 把整列当文字处理，`.replace(" ", "")` 把空格换成空，`T 12` 变 `T12`。这一步在油表文件里会再做一次，两边一致才能对上。

```python
def fuel_group(tank_type):
    if tank_type == "D":
        return "D"
    else:
        return "G"
tanks["Fuel"] = tanks["Tank Type"].apply(fuel_group)
```

油罐有 U、P、D 三种，发票只有 G、D 两种。这个函数把 U 和 P 都归成 G。`apply` 把函数套到每一行。

```python
capacity = tanks.groupby(["Station", "Fuel"])["Tank Capacity"].sum().reset_index()
```

`groupby` 按"店 + 油种"分组，`sum` 把每组的油罐容量加起来，得到每家店每种油的总容量。`reset_index()` 把分组键从索引变回普通列，方便后面 merge。1 号店 G 有 4 个罐共 160,000，就是这里算出来的。

### 1.3 Invoices

```python
empty = invoices["Cost"].isnull() & invoices["Liters"].isnull() & invoices["Fuel Type"].isnull()
bad_station = ~invoices["Station"].isin(locations["Station"])
```

`isnull()` 返回一列 True/False，`&` 是"并且"，所以 `empty` 标记三个关键列全空的行。`isin` 检查站号是否在 8 家店里，前面的 `~` 是"取反"，所以 `bad_station` 标记站号不存在的行。然后打印一下两者的交集，证明 5 个坏站号全在空行里。

```python
invoices = invoices[~empty].copy()
invoices = invoices.drop_duplicates()
```

用 `~empty` 只保留非空行。`.copy()` 是告诉 pandas 这是一张新表，避免后面赋值时报警告。`drop_duplicates()` 去掉完全相同的行。

```python
invoices["Date"] = pd.to_datetime(invoices["Invoice Date"], format="%m/%d/%Y")
invoices["Weekday"] = invoices["Date"].dt.day_name()
invoices["Rate"] = invoices["Cost"] / invoices["Liters"]
invoices["Discount"] = invoices["Liters"].apply(discount_rate)
invoices["Tier"] = invoices["Liters"].apply(discount_tier)
invoices["Saved"] = invoices["Liters"] * invoices["Discount"]
invoices["Rate_before_discount"] = invoices["Rate"] + invoices["Discount"]
```

逐列派生：

- `Date`：把 `1/2/2017` 这种文字变成真正的日期。`format` 告诉它月/日/年的顺序。
- `Weekday`：从日期取星期几，第三题用。
- `Rate`：老师说的 rate = 总价 ÷ 升数。两列直接相除是整列一起算，不用 apply。
- `Discount`：每张发票拿到的每升折扣，用上面的函数。
- `Saved`：升数 × 折扣，就是题目规定的"折扣节省"算法。
- `Rate_before_discount`：折前价 = 折后价 + 折扣。题目特别提醒：是加回去，不是再减一次。

```python
invoices = invoices.merge(capacity, left_on=["Station", "Fuel Type"], right_on=["Station", "Fuel"], how="left")
print("Deliveries bigger than station capacity:", (invoices["Liters"] > invoices["Capacity"]).sum())
invoices = invoices.drop(columns=["Fuel", "Capacity"])
```

`merge` 把容量表拼到发票上。两张表的列名不同（`Fuel Type` vs `Fuel`），所以用 `left_on` / `right_on` 分别指定。`how="left"` 表示以发票为主，不丢发票。拼上后检查有没有一次送货比整个站容量还大（0 条），检查完把借来的两列删掉。

```python
START, END = invoices["Date"].min(), invoices["Date"].max()
DAYS = (END - START).days + 1
```

观测期首尾日期和天数（956）。后面年化用：年节省 = 期内节省 × 365 / 956。

### 1.4 Fuel levels

```python
levels1.columns = ["Tank ID", "Level", "Time"]
levels2.columns = ["Tank ID", "Level", "Time"]
levels = pd.concat([levels1, levels2], ignore_index=True)
```

两个文件列名不同，直接给它们统一的新列名，然后 `concat` 上下拼起来。`ignore_index=True` 重新编行号，否则两张表的行号会重复。

```python
levels = levels.dropna()
levels = levels.drop_duplicates()
levels = levels.drop_duplicates(subset=["Tank ID", "Time"], keep="last")
```

三步去重：空值行；完全相同的行；同一罐同一时间但读数不同的行（保留最后一条）。

```python
levels = levels.merge(tanks[["Tank ID", "Station", "Fuel", "Tank Capacity"]], on="Tank ID")
```

把每条读数属于哪家店、什么油、罐多大拼上来。这是"油表 → 油罐 → 店"的连接。然后检查负数和超容量（都是 0）。

```python
levels = levels.sort_values(["Tank ID", "Time"]).reset_index(drop=True)
```

**非常关键**：按罐、再按时间排序。后面所有"和上一条读数比较"的操作都假设数据是这样排好的。

#### 读数间隔和断档

```python
levels["hours"] = levels.groupby("Tank ID")["Time"].diff().dt.total_seconds() / 3600
```

拆开读：`groupby("Tank ID")` 按罐分组；`["Time"].diff()` 每条减上一条的时间（每个罐的第一条没有上一条，得到空）；`.dt.total_seconds() / 3600` 把时间差换成小时。为什么要分组再 diff：不分组的话，T10 的最后一条会减 T11 的第一条，得到一个没意义的数。

```python
gaps = levels[levels["hours"] > GAP_HOURS].copy()
```

间隔超过 6 小时的就是断档，列出来看最长的几个。

#### 去尖峰

```python
for i in range(3):
    prev_level = levels.groupby("Tank ID")["Level"].shift(1)
    next_level = levels.groupby("Tank ID")["Level"].shift(-1)
    spike = (prev_level - levels["Level"] > SPIKE) & (next_level - levels["Level"] > SPIKE)
    levels = levels[~spike].reset_index(drop=True)
```

`shift(1)` 把整列往下挪一格，得到"上一条读数"；`shift(-1)` 往上挪，得到"下一条"。一个读数如果比上一条低 2,000 以上**并且**比下一条也低 2,000 以上，就是掉下去又弹回来的尖峰，删掉。循环 3 次是防止两个尖峰挨着：删掉一个之后，另一个的"邻居"变了，再查一遍。实际第一遍删了 15 个，后两遍 0 个。

#### 分类每一段变化

```python
levels["hours"] = levels.groupby("Tank ID")["Time"].diff().dt.total_seconds() / 3600
levels["change"] = levels.groupby("Tank ID")["Level"].diff()
```

删了尖峰后行变了，所以重算间隔；再算读数变化量 `change`（这条减上一条，负数是卖油，正数是进货）。

```python
levels["type"] = "normal"
levels.loc[levels["change"].isnull(), "type"] = "first"
levels.loc[levels["hours"] > GAP_HOURS, "type"] = "gap"
levels.loc[(levels["type"] == "normal") & (levels["change"] >= DELIVERY), "type"] = "delivery"
levels.loc[(levels["type"] == "normal") & (levels["change"] < -MAX_DROP * np.maximum(levels["hours"], 1)), "type"] = "anomaly"
```

这是整个清洗的核心，一行一行看：

1. 先把所有行标成 `normal`。
2. `change` 为空的是每个罐的第一条，标 `first`。
3. 间隔超过 6 小时的标 `gap`。
4. 还是 `normal` 且上升 ≥ 500 升的标 `delivery`。
5. 还是 `normal` 且下降超过阈值的标 `anomaly`。阈值是 `2000 × max(小时数, 1)`：15 分钟内掉 2,000 不可能是卖的；但如果间隔 3 小时，掉 6,000 才算异常。

`.loc[条件, "列名"] = 值` 的意思是"把满足条件的那些行的这一列改成这个值"。顺序有讲究：后改的会覆盖先改的，所以 `gap` 排在 `delivery` 前面，一个跨断档的上升不会被当成进货。

```python
levels["sold"] = np.where(levels["type"] == "normal", -levels["change"], 0)
levels["delivered"] = np.where(levels["type"] == "delivery", levels["change"], 0)
levels["hours_ok"] = np.where(levels["type"].isin(["normal", "delivery"]), levels["hours"], 0)
levels["is_anomaly"] = (levels["type"] == "anomaly").astype(int)
levels["Date"] = levels["Time"].dt.normalize()
```

`np.where(条件, A, B)` 是"条件成立取 A，否则取 B"：

- `sold`：正常段的下降量（取负号变成正数），其他段记 0。
- `delivered`：进货段的上升量。
- `hours_ok`：有效覆盖的小时数，只有正常段和进货段算。
- `is_anomaly`：异常段记 1，后面按天数一下。
- `Date`：把时间戳的时分秒抹掉，只剩日期，方便按天分组。

#### 按天汇总

```python
daily_tank = levels.groupby(["Tank ID", "Station", "Fuel", "Date"]).agg(
    sold=("sold", "sum"), delivered=("delivered", "sum"), hours_ok=("hours_ok", "sum"), anomalies=("is_anomaly", "sum")).reset_index()
daily_tank["complete"] = (daily_tank["hours_ok"] >= MIN_HOURS) & (daily_tank["anomalies"] == 0)
```

按"罐 + 天"分组，`agg` 里每一项是 `新列名=("原列", "怎么算")`。得到每个罐每天：卖了多少、进了多少、有效小时数、异常次数。有效小时 ≥ 20 且无异常的天标为 `complete`。

```python
daily = daily_tank.groupby(["Station", "Fuel", "Date"]).agg(
    sold=("sold", "sum"), delivered=("delivered", "sum"), tanks_complete=("complete", "sum"), tanks=("Tank ID", "count")).reset_index()
n_tanks = tanks.groupby(["Station", "Fuel"])["Tank ID"].count().rename("n_tanks").reset_index()
daily = daily.merge(n_tanks, on=["Station", "Fuel"])
daily["complete"] = daily["tanks_complete"] == daily["n_tanks"]
```

再往上一层，按"店 + 油种 + 天"分组，把同站同油种的几个罐加起来。`tanks_complete` 是那天完整的罐数（True 当 1 加）。另外算出每个站油种**应该**有几个罐 `n_tanks`，拼上来比较：只有当天所有罐都完整，这个站油种的这一天才算完整。为什么这么严：如果 1 号店 4 个汽油罐有一个当天缺数据，加出来的销量就少一个罐的量，会拉低平均。

---

## 2. 第一题

### 2.1 每个罐的曲线

```python
daily_level_tank = levels.groupby(["Tank ID", "Date"])["Level"].mean().reset_index()
fig, axes = plt.subplots(6, 4, figsize=(18, 15), sharex=True)
axes = axes.flatten()
for i, tank_id in enumerate(tank_list):
    d = daily_level_tank[daily_level_tank["Tank ID"] == tank_id]
    axes[i].plot(d["Date"], d["Level"], linewidth=0.7)
    axes[i].axhline(t["Tank Capacity"], linestyle="--", color="grey")
```

每罐每天的平均液位（186 万条读数画不动，按天平均后只剩两万条）。`subplots(6, 4)` 开 24 个小格，`flatten()` 把 6×4 的格子摊平成一排 24 个，方便用 `axes[i]` 一个个取。`enumerate` 同时给出序号 i 和罐号。每格画一条线加一条容量虚线。最后一个空格 `axis("off")` 隐藏。

### 2.2 日均消耗

```python
consumption = daily[daily["complete"]].groupby(["Station", "Fuel"])["sold"].agg(
    avg_daily="mean", std_daily="std", p95_daily=lambda x: x.quantile(0.95), max_daily="max", complete_days="count")
```

只取完整天，按店油种分组，对 `sold` 算平均、标准差、95 分位、最大值、天数。`lambda x: x.quantile(0.95)` 是临时定义的小函数，因为 `agg` 没有现成的"95 分位"关键字。`avg_daily` 就是后面一切的基础。

```python
check = daily.groupby(["Station", "Fuel"]).agg(gauge_sold=("sold", "sum"), gauge_delivered=("delivered", "sum"))
invoiced = invoices.groupby(["Station", "Fuel Type"])["Liters"].sum()
invoiced.index.names = ["Station", "Fuel"]
check["invoiced"] = invoiced
check["delivered vs invoiced"] = ((check["gauge_delivered"] / check["invoiced"] - 1) * 100).round(1)
```

三方验证。油表算的总销量、油表测的总进货、发票总量，三个放一起。`invoiced.index.names = [...]` 是把发票那边的索引名改成和 `check` 一样，这样 `check["invoiced"] = invoiced` 才能按店油种自动对齐。除以发票量减 1 乘 100 就是"比发票多百分之几"。这一步发现了柴油发票不全。

季度对比那一块用 `pd.Grouper(key="Date", freq="QS")` 按季度分组，`QS` 是 quarter start。`to_period("Q")` 把日期变成 `2017Q1` 这种标签。

### 2.3 库存位置

```python
daily_level = levels.groupby(["Station", "Fuel", "Date"]).agg(level=("Level", "mean"), tanks=("Tank ID", "nunique")).reset_index()
daily_level["level"] = daily_level["level"] * daily_level["tanks"]
daily_level = daily_level.merge(n_tanks, on=["Station", "Fuel"])
daily_level = daily_level[daily_level["tanks"] == daily_level["n_tanks"]]
```

想要每家店每种油每天的总库存。先按店油种天分组算所有读数的平均（这是"平均每罐"），再乘当天有读数的罐数得到总量。`nunique` 数不重复的罐号。最后只留所有罐都有数据的天。

```python
for (station, fuel), r in position.iterrows():
    d = daily_level[(daily_level["Station"] == station) & (daily_level["Fuel"] == fuel)]
    rows.append({"days below reserve %": round((d["level"] < r["reserve_7d"]).mean() * 100, 1), ...})
```

`iterrows()` 一行一行遍历策略表，每行是一个店油种。取出它的每日库存 `d`，`d["level"] < 安全线` 得到一列 True/False，对它求 `mean()` 就是 True 的比例（True 当 1），乘 100 变百分比。这就是"库存低于安全线的天数占比"。其他几列同理：最低库存、换算成几天用量。

### 2.4 现在的采购表现

```python
current = invoices.groupby(["Station", "Fuel Type"]).agg(
    orders=("Invoice ID", "count"), total_liters=("Liters", "sum"), avg_order=("Liters", "mean"),
    max_order=("Liters", "max"), total_cost=("Cost", "sum"), saved=("Saved", "sum"))
current["orders_per_month"] = (current["orders"] / months).round(1)
current["avg_rate"] = (current["total_cost"] / current["total_liters"]).round(3)
```

按店油种汇总发票：几单、多少升、平均每单、总价、总折扣。每月单数 = 单数 ÷ 月数。平均每升价 = 总价 ÷ 总升数（这是加权平均，比对每张发票的 Rate 取平均更准，因为大单权重应该更大）。

```python
tier_share = pd.crosstab([invoices["Station"], invoices["Fuel Type"]], invoices["Tier"], normalize="index")
```

`crosstab` 是交叉表：行是店油种，列是折扣档，格子里是数量。`normalize="index"` 把每行换算成占比。这就是"各站有百分之几的订单在哪一档"。

---

## 3. 第二题

### 3.1 策略表

```python
def best_order(available):
    if available >= 40000:
        return 40000
    elif available >= 25000:
        return 25000
    elif available >= 15000:
        return 15000
    else:
        return 0
```

给可用空间，返回能够到的最高门槛。和 `discount_rate` 一样的结构，只是返回的是门槛升数而不是折扣。

```python
policy = capacity.set_index(["Station", "Fuel"]).copy()
policy["avg_daily"] = consumption["avg_daily"]
policy["reserve_7d"] = (RESERVE_DAYS * policy["avg_daily"]).round(0)
policy["available"] = policy["Capacity"] - policy["reserve_7d"]
policy["best_order"] = policy["available"].apply(best_order)
policy["best_discount"] = policy["best_order"].apply(discount_rate)
```

`set_index(["Station", "Fuel"])` 把店油种设成索引，这样 `policy["avg_daily"] = consumption["avg_daily"]` 能按索引自动对齐（两张表的索引都是店油种）。然后就是题目的公式：安全库存 = 7 × 日均；可用空间 = 容量 − 安全库存；最佳订货量 = 可用空间够到的最高门槛；折扣 = 那个门槛对应的折扣。

### 3.2 方案对比

```python
for (station, fuel), r in policy.iterrows():
    liters_bought = current.loc[(station, fuel), "total_liters"]
    for name, q in [("15,000 L", 15000), ("25,000 L", 25000), ("40,000 L", 40000), ("fill up", r["available"])]:
        feasible = (q <= r["available"]) and (q > 0)
        rows.append({... "Savings on bought liters": round(liters_bought * discount_rate(q)) if feasible else None})
```

双重循环：外层遍历 16 个店油种，内层遍历 4 种订货量。每种判断可不可行（放得下且大于 0），可行就算折扣、间隔天数（订货量 ÷ 日均）、以及按实际采购量能省多少。`x if 条件 else None` 是单行的 if，不可行的格子留空。最后 `pivot` 把长表转成"行是店油种、列是方案"的宽表。

### 3.3 推荐策略和节省

```python
recommend["order_size"] = np.where(recommend["best_order"] > 0, recommend["best_order"], recommend["available"])
```

有门槛够得着就订那个门槛的量，够不着（best_order 是 0）就订满可用空间。

```python
recommend["policy_savings"] = recommend["liters_bought"] * recommend["discount"]
recommend["upper_bound"] = recommend["liters_bought"] * 0.04
recommend["extra_savings"] = recommend["policy_savings"] - recommend["current_savings"]
recommend["extra_per_year"] = (recommend["extra_savings"] * 365 / DAYS).round(0)
```

三个数都乘的是**同一个** `liters_bought`（实际买过的升数），这是题目要求的"用同样的总量比较"。上限直接乘 0.04。额外节省 = 策略 − 现状。年化 = 乘 365 除以 956。注意这里不提前取整，只在显示时 `.round(0)`，否则 16 行各差几毛钱，加起来差 1 块。

### 3.4 逐日模拟

```python
def simulate(station, fuel, keep_path=False):
    r = recommend.loc[(station, fuel)]
    d = daily[(daily["Station"] == station) & (daily["Fuel"] == fuel)].set_index("Date")
    demand = d["sold"].where(d["complete"], r["avg_daily"])
```

取出这个店油种的每日销量。`.where(条件, 替代值)` 的意思是"条件成立保留原值，否则换成替代值"，所以不完整的天用平均值顶上。

```python
    level = capacity_
    for date, sold in demand.items():
        level_at_order = None
        if level - sold < reserve and q > 0:
            amount = min(q, capacity_ - level)
            level_at_order = level
            level = level + amount
            orders += 1; ordered += amount; savings += amount * discount_rate(amount)
        level = level - sold
        if level < 0:
            stockouts += 1; level = 0
        lowest = min(lowest, level)
```

从满罐开始，一天一天走。每天先问：今天卖完会不会跌破安全线？会就立刻订货，订货量是推荐量但不能超过剩余空间（`min`），记下下单时的库存、累加单数和折扣。然后减掉当天销量。如果减成负数就是断油，计一次并归零。全程记录最低点。这个循环就是"把策略放回真实需求里回放"，结果零断油。`keep_path` 为真时额外返回每天的库存，画图用。

### 3.5 送货时间

```python
lead["available_1day_early"] = lead["available"] - lead["p95_daily"]
lead["discount_1day_early"] = lead["available_1day_early"].apply(best_order).apply(discount_rate)
lead["loses a level"] = lead["discount_1day_early"] < lead["discount"]
```

如果提前一天下单（触发点抬高一个 95 分位日销量），可用空间就少这么多。两次 `apply` 连起来：先算够到哪个门槛，再算那个门槛的折扣。和原折扣比，变小了就是掉档。

---

## 4. 第三题

### 4.1 箱线图

```python
by_day = invoices[invoices["Weekday"].isin(weekdays)].groupby("Weekday").agg(...).loc[weekdays]
```

只留周一到周五，按星期分组统计。最后的 `.loc[weekdays]` 是按周一到周五的顺序排，不然 pandas 会按字母排。

```python
data = [d[d["Weekday"] == day]["Rate"] for day in weekdays]
ax.boxplot(data)
ax.set_xticklabels([f"{day[:3]}\n(n={len(x)})" for day, x in zip(weekdays, data)])
```

列表推导式：对五个星期各取出那天所有发票的 Rate，得到五个序列，`boxplot` 一次画五个箱子。横轴标签拼上样本数（题目要求报每天的观测数）。三张图分别是全部、汽油、柴油。

### 4.2 排除其他解释

```python
monthly = invoices.groupby(["Fuel Type", pd.Grouper(key="Date", freq="MS")])["Rate_before_discount"].median().unstack("Fuel Type")
```

按油种和月份分组取折前价中位数，`unstack` 把油种从行转到列，得到一张"行是月份、列是 G 和 D"的表，画出油价随时间的走势（2019 年翻倍）。

```python
same_day = invoices.groupby(["Date", "Fuel Type"])["Rate_before_discount"].std()
```

同一天同一油种所有发票的价格标准差。中位数是 0，证明全网同一天一个价。

```python
month_median = invoices.groupby(["Fuel Type", "Month"])["Rate_before_discount"].transform("median")
invoices["vs_month_median_cents"] = (invoices["Rate_before_discount"] - month_median) * 100
```

`transform("median")` 和 `agg` 不同：它算出每组的中位数后**广播回每一行**，所以 `month_median` 和原表一样长，每张发票对应它那个月那种油的中位价。用折前价减它，得到"比当月中位贵/便宜几分"。这一步把油价趋势和折扣两个干扰一起剥掉了。然后按星期看这个差值的平均和中位数：中位数全是 0。

---

## 5. 第四题

### 5.1 候选表

```python
for _, t in tanks.iterrows():
    r = recommend.loc[(t["Station"], t["Fuel"])]
    extra = NEW_TANK - t["Tank Capacity"]
    if extra <= 0:
        row.update({... "extra_savings_per_year": 0, "note": "60,000 L is not bigger - no increase"})
    else:
        available_after = r["available"] + extra
        discount_after = discount_rate(best_order(available_after))
        row.update({... "extra_savings_per_year": round(r["liters_per_year"] * (discount_after - r["discount"]))})
```

遍历 23 个罐。每个罐找到它所属店油种的策略行 `r`。净增容量 = 60,000 − 原容量；不增加的（70,000 升的罐）直接标注。增加的：新可用空间 = 原可用空间 + 净增，再算新折扣档，年增量节省 = 年采购量 × (新折扣 − 策略折扣)。**这里减的是策略折扣，不是现状折扣**，因为题目要求相对于改进后的策略算。

```python
candidates["five_year_net"] = np.where(candidates["extra_space"] > 0, YEARS * candidates["extra_savings_per_year"] - NEW_TANK_COST, 0)
candidates["payback_years"] = np.where(candidates["extra_savings_per_year"] > 0, NEW_TANK_COST / ..., np.nan).round(1)
```

五年净收益 = 5 × 年节省 − 25 万。回本期 = 25 万 ÷ 年节省，年节省为 0 时用 `np.nan` 表示"不适用"，避免除以零。

```python
best = candidates[candidates["extra_space"] > 0].sort_values(["Station", "extra_savings_per_year"], ascending=[True, False]).groupby("Station").head(1)
```

先按店升序、节省降序排，再每个店取第一行，就是每店最划算的那个罐。

### 5.2 敏感性

```python
def best_net_benefit(station, demand_factor, cost):
    for _, t in tanks[tanks["Station"] == station].iterrows():
        reserve = r["reserve_7d"] * demand_factor
        liters = r["liters_per_year"] * demand_factor
        available_before = r["Capacity"] - reserve
        available_after = available_before + extra
        ...
        net = YEARS * liters * (d_after - d_before) - cost
```

把 5.1 的逻辑包成函数，多两个参数：需求倍数和换罐成本。需求变了，安全库存和年采购量都要乘这个倍数，可用空间和折扣档要重算。外面两层循环跑 3 个成本 × 3 个需求 = 9 种组合，每种对 8 个店各算一个最佳值，填成一张表。

---

## 6. 汇总表

```python
summary = pd.DataFrame({
    "Station name": [names[s] for s, f in recommend.index],
    "Capacity (L)": recommend["Capacity"],
    ...
}, index=recommend.index)
```

用字典建表，每个键是列名，值是一整列（大多直接从 `recommend` 和 `current` 拿）。`index=recommend.index` 让它和策略表的店油种索引一致。

```python
summary.loc[("All", ""), :] = totals
for col in [...]:
    summary.loc[("All", ""), col] = np.nan
```

加一行"All"放合计，但容量、日均、触发点这些加起来没意义的列设为空。`to_csv` 导出一份。

---

## 几个反复出现的模式

学会这五个，整本 notebook 就没有看不懂的地方：

1. **`groupby(...).agg(...)`**：按什么分组、每组算什么。全文出现十几次。
2. **`merge`**：把另一张表的列按共同键拼过来。油表拼油罐、发票拼容量、天表拼罐数。
3. **`.loc[条件, 列] = 值`** 和 **`np.where(条件, A, B)`**：按条件改值。分类读数变化全靠它们。
4. **`def` 函数 + `apply`**：折扣档、油种归类、最佳订货量，三个函数一个结构。
5. **`for ... in ...iterrows()`**：一行一行处理，逻辑复杂、表不大时用。方案对比、库存位置、换罐、模拟都是。

你看 notebook 时如果卡在某一行，先判断它属于上面哪一种，基本就能顺下来。
