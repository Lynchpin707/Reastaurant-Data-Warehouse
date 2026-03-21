import csv
import random
from datetime import datetime, timedelta
from collections import Counter

random.seed(42)

# ─────────────────────────────────────────────
# 0. HELPERS
# ─────────────────────────────────────────────

def maybe_typo(text, prob=0.05):
    if random.random() > prob or len(text) < 3:
        return text
    i = random.randint(0, len(text) - 1)
    typo_type = random.choice(["swap", "double", "drop"])
    if typo_type == "swap" and i < len(text) - 1:
        lst = list(text)
        lst[i], lst[i + 1] = lst[i + 1], lst[i]
        return "".join(lst)
    elif typo_type == "double":
        return text[:i] + text[i] + text[i:]
    else:
        return text[:i] + text[i + 1:]

def maybe_none(val, prob=0.03):
    return "" if random.random() < prob else val

def coin(prob):
    return random.random() < prob

# ─────────────────────────────────────────────
# 1. MOROCCAN MENU
# ─────────────────────────────────────────────

menu_items = [
    (1,  "Msemen",                "breakfast", 4.00),
    (2,  "Beghrir",               "breakfast", 4.50),
    (3,  "Harcha",                "breakfast", 3.50),
    (4,  "Baghrir au Miel",       "breakfast", 5.00),
    (5,  "Atay bi Naanaa",        "breakfast", 2.50),
    (6,  "Zaalouk",               "starter",   5.00),
    (7,  "Taktouka",              "starter",   5.50),
    (8,  "Briouates au Fromage",  "starter",   6.00),
    (9,  "Harira",                "starter",   4.50),
    (10, "Soupe de Lentilles",    "starter",   4.00),
    (11, "Tajine Poulet Citron",  "main",     14.00),
    (12, "Tajine Kefta",          "main",     13.00),
    (13, "Tajine Agneau Pruneaux","main",     16.00),
    (14, "Couscous Royal",        "main",     15.00),
    (15, "Couscous aux Legumes",  "main",     12.00),
    (16, "Pastilla au Poulet",    "main",     14.50),
    (17, "Mechoui",               "main",     18.00),
    (18, "Mrouzia",               "main",     16.50),
    (19, "Rfissa",                "main",     13.50),
    (20, "Tanjia Marrakchia",     "main",     17.00),
    (21, "Pain Marocain",         "side",      2.00),
    (22, "Olives Marinees",       "side",      3.00),
    (23, "Salade Marocaine",      "side",      4.00),
    (24, "Frites",                "side",      3.50),
    (25, "Chebakia",              "dessert",   4.00),
    (26, "Ghoriba",               "dessert",   3.50),
    (27, "Kaab el Ghazal",        "dessert",   5.00),
    (28, "Sellou",                "dessert",   4.50),
    (29, "Jus d Orange Frais",    "drink",     3.50),
    (30, "Lben",                  "drink",     2.50),
    (31, "Citronnade",            "drink",     3.00),
    (32, "Coca-Cola",             "drink",     2.50),
]

menu_errors = {
    14: ("Couscous Royale",         "main",    15.00),
    11: ("Tajine Poulet Citrron",   "main",    14.00),
    27: ("Kaab al Ghazal",          "dessert",  5.00),
    19: ("Rfissa",                  "mian",    13.50),
}

menu_rows = []
for item_id, name, cat, price in menu_items:
    if item_id in menu_errors:
        name, cat, price = menu_errors[item_id]
    menu_rows.append({"item_id": item_id, "name": name, "cat": cat, "price": price})

# ─────────────────────────────────────────────
# 2. MOROCCAN EMPLOYEES
# ─────────────────────────────────────────────

roles_pool = {"waiter": 10, "chef": 3, "manager": 1, "cashier": 2, "busboy": 2}

moroccan_first = [
    "Youssef","Fatima","Mehdi","Khadija","Amine","Zineb","Omar","Meryem",
    "Hamza","Nadia","Rachid","Souad","Ayoub","Houda","Khalid","Salma",
    "Tariq","Imane","Bilal","Loubna","Saad","Rim","Ilyass","Samira",
]
moroccan_last = [
    "El Amrani","Benali","Idrissi","Chraibi","Mansouri","Ouahabi","Tazi",
    "Benkiran","El Fassi","Lahlou","Berrada","Moussaoui","El Alami","Ziani",
    "Bensouda","El Khattabi","Senhaji","Bouazza","El Hajoui","Filali",
]

emp_rows   = []
emp_id     = 1
waiter_ids = []

for role, count in roles_pool.items():
    for _ in range(count):
        fname = random.choice(moroccan_first)
        lname = random.choice(moroccan_last)
        full  = f"{fname} {lname}"
        base  = {"waiter": 12, "chef": 18, "manager": 22, "cashier": 14, "busboy": 10}[role]
        rate  = round(base + random.uniform(-1, 2), 2)
        row   = {
            "emp_id":      emp_id,
            "name":        maybe_typo(full, prob=0.07),
            "role":        maybe_typo(role, prob=0.04),
            "hourly_rate": maybe_none(rate, prob=0.02),
        }
        if role == "waiter":
            waiter_ids.append(emp_id)
        emp_rows.append(row)
        emp_id += 1

# ─────────────────────────────────────────────
# 3. WEATHER  — CLEAN, NO ERRORS AT ALL
# ─────────────────────────────────────────────

CONDITIONS = ["sunny", "cloudy", "rainy", "windy", "partly cloudy", "stormy", "foggy"]

START = datetime(2025, 8, 1)
END   = datetime(2026, 1, 31, 23, 59)

weather_rows = []
weather_id   = 1
hour_weather = {}

current = START.replace(minute=0, second=0, microsecond=0)
while current <= END:
    condition = random.choices(
        CONDITIONS,
        weights=[30, 20, 18, 10, 12, 5, 5],
        k=1
    )[0]
    month = current.month
    if month in [8, 9]:
        base_temp = 30
    elif month in [10, 11]:
        base_temp = 18
    else:
        base_temp = 12
    if condition in ["rainy", "stormy"]:
        base_temp -= 4
    temp = round(base_temp + random.uniform(-2, 2), 1)

    weather_rows.append({
        "weather_id": weather_id,
        "timestamp":  current.strftime("%Y-%m-%d %H:%M:%S"),
        "temp":       temp,
        "condition":  condition,
    })
    hour_weather[current] = (weather_id, condition)
    weather_id += 1
    current += timedelta(hours=1)

# ─────────────────────────────────────────────
# 4. WAITER PERFORMANCE PROFILES
# ─────────────────────────────────────────────

waiter_weights = {}
for wid in waiter_ids:
    w = random.choices([1, 2, 4, 7, 10], weights=[10, 20, 30, 25, 15])[0]
    waiter_weights[wid] = w

# ─────────────────────────────────────────────
# 5. ORDER TYPES
# ─────────────────────────────────────────────

ORDER_TYPES_NORMAL = ["on site", "on site", "on site", "to go", "delivery"]
ORDER_TYPES_RAINY  = ["delivery", "delivery", "delivery", "to go", "on site"]

ORDER_TYPE_VARIANTS = {
    "on site":  ["on site", "on-site", "onsite", "On Site"],
    "to go":    ["to go",   "to-go",   "To Go"],
    "delivery": ["delivery", "Delivery", "delivrey"],
}

def pick_order_type(is_rainy):
    pool = ORDER_TYPES_RAINY if is_rainy else ORDER_TYPES_NORMAL
    base = random.choice(pool)
    return random.choice(ORDER_TYPE_VARIANTS[base]) if coin(0.12) else base

# ─────────────────────────────────────────────
# 6. GENERATE ORDERS + DETAILS
# ─────────────────────────────────────────────

MEAL_WINDOWS = [(7, 10), (12, 15), (19, 22)]

def is_meal_hour(h):
    return any(s <= h < e for s, e in MEAL_WINDOWS)

order_rows  = []
detail_rows = []
order_id    = 1
detail_id   = 1

current_day = START.date()
end_day     = END.date()

while current_day <= end_day:
    weekend = current_day.weekday() >= 5
    for hour in range(24):
        dt       = datetime(current_day.year, current_day.month, current_day.day, hour)
        hour_key = dt.replace(minute=0, second=0, microsecond=0)
        wid, condition = hour_weather.get(hour_key, (1, "sunny"))
        is_rainy = condition in ["rainy", "stormy"]
        meal     = is_meal_hour(hour)

        if meal:
            n_orders = random.randint(18, 30) if weekend else random.randint(16, 25)
        else:
            n_orders = random.randint(3, 8)   if weekend else random.randint(2, 6)

        for _ in range(n_orders):
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            ts     = dt.replace(minute=minute, second=second)
            server = random.choices(waiter_ids, weights=[waiter_weights[w] for w in waiter_ids], k=1)[0]
            o_type = pick_order_type(is_rainy)

            order_rows.append({
                "order_id":   order_id,
                "server_id":  maybe_none(server, prob=0.01),
                "order_type": o_type,
                "timestamp":  maybe_none(ts.strftime("%Y-%m-%d %H:%M:%S"), prob=0.005),
                "weather_id": wid,
            })

            n_items = random.randint(1, 4)
            chosen  = random.sample(menu_items, k=min(n_items, len(menu_items)))
            for (iid, *_) in chosen:
                qty = random.choices([1, 2, 3], weights=[60, 30, 10])[0]
                detail_rows.append({
                    "detail_id": detail_id,
                    "order_id":  order_id,
                    "item_id":   iid,
                    "qty":       maybe_none(qty, prob=0.02),
                })
                detail_id += 1
            order_id += 1

    current_day += timedelta(days=1)

# ─────────────────────────────────────────────
# 7. INJECT DUPLICATES (not in weather)
# ─────────────────────────────────────────────

def inject_duplicates(rows, n=6):
    sample = random.sample(rows, k=min(n, len(rows)))
    rows.extend(sample)
    return rows

order_rows  = inject_duplicates(order_rows,  n=5)
detail_rows = inject_duplicates(detail_rows, n=8)
menu_rows   = inject_duplicates(menu_rows,   n=2)
emp_rows    = inject_duplicates(emp_rows,    n=2)

random.shuffle(order_rows)
random.shuffle(detail_rows)

# ─────────────────────────────────────────────
# 8. WRITE CSVs
# ─────────────────────────────────────────────

def write_csv(filename, fieldnames, rows):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  checkmark  {filename:35s}  ({len(rows):>6,} rows)")

print("\nGenerating Moroccan restaurant CSV files ...\n")
write_csv("employees_raw.csv",  ["emp_id","name","role","hourly_rate"], emp_rows)
write_csv("menu_raw.csv",       ["item_id","name","cat","price"],       menu_rows)
write_csv("weather_raw.csv",    ["weather_id","timestamp","temp","condition"], weather_rows)
write_csv("orders_raw.csv",     ["order_id","server_id","order_type","timestamp","weather_id"], order_rows)
write_csv("details_raw.csv",    ["detail_id","order_id","item_id","qty"], detail_rows)
print("\nAll files generated successfully!")

# ─────────────────────────────────────────────
# 9. SANITY SUMMARY
# ─────────────────────────────────────────────

print("\nQuick data summary")
print(f"  Period          : Aug 2025 to Jan 2026")
print(f"  Total orders    : {len(order_rows):,}")
print(f"  Total details   : {len(detail_rows):,}")
print(f"  Menu items      : {len(menu_rows)}")
print(f"  Employees       : {len(emp_rows)}")
print(f"  Waiters         : {len(waiter_ids)}")
print(f"  Weather records : {len(weather_rows):,}  (clean, no errors)")

rainy_wids    = {r["weather_id"] for r in weather_rows if r["condition"] in ["rainy","stormy"]}
rainy_orders  = [r for r in order_rows if r["weather_id"] in rainy_wids]
normal_orders = [r for r in order_rows if r["weather_id"] not in rainy_wids]

def type_pct(orders, label):
    c = Counter(str(r["order_type"]).lower().replace("-","").replace(" ","") for r in orders if r["order_type"])
    total = sum(c.values()) or 1
    delivery = c.get("delivery",0) + c.get("delivrey",0)
    onsite   = c.get("onsite",0)
    togo     = c.get("togo",0)
    print(f"  {label}  delivery={delivery/total*100:.1f}%  on-site={onsite/total*100:.1f}%  to-go={togo/total*100:.1f}%")

print("\nOrder type distribution:")
type_pct(rainy_orders,  "Rainy/Stormy ->")
type_pct(normal_orders, "Normal       ->")

server_counter = Counter(r["server_id"] for r in order_rows if r["server_id"] != "")
sorted_waiters = sorted(server_counter.items(), key=lambda x: -x[1])
print("\nWaiter performance (best to worst):")
for wid, cnt in sorted_waiters:
    print(f"  emp_id={wid:>2}  {cnt:>5,} orders")

weekend_orders = sum(
    1 for r in order_rows
    if r["timestamp"] and datetime.strptime(r["timestamp"], "%Y-%m-%d %H:%M:%S").weekday() >= 5
)
print(f"\nWeekend orders : {weekend_orders:,}")
print(f"Weekday orders : {len(order_rows) - weekend_orders:,}")
