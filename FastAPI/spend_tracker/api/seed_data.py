"""
Seed dummy data for May & June 2026 — run once to populate the Compare screen.

Usage (inside the api container):
    docker compose exec api python seed_data.py
"""
import asyncio
import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import select

# Month configs
MONTHS = [
    {
        "month": 5, "year": 2026,
        "salary": 95000.0, "save_pct": 30,
        "allocations": [
            {"instrument": "Liquid MF",   "amount": 11400.0, "rationale": "Easy liquidity buffer"},
            {"instrument": "Index Fund",  "amount": 11400.0, "rationale": "Long-term wealth"},
            {"instrument": "PPF",         "amount": 5700.0,  "rationale": "Tax-free debt component"},
        ],
        "expenses": [
            # category, description, amount, expense_date
            ("EMI",     "home loan emi",       14500, date(2026, 5,  1)),
            ("Saving",  "ppf deposit",          5000, date(2026, 5,  5)),
            ("Grocery", "bigbasket order",      2400, date(2026, 5,  3)),
            ("Food",    "swiggy dinner",         450, date(2026, 5,  5)),
            ("Other",   "electricity bill",     1200, date(2026, 5,  6)),
            ("Travel",  "petrol refill",        1800, date(2026, 5,  8)),
            ("Saving",  "index fund sip",       3000, date(2026, 5, 10)),
            ("Travel",  "metro recharge",        500, date(2026, 5, 10)),
            ("Food",    "zomato order",          680, date(2026, 5, 12)),
            ("Grocery", "zepto vegetables",      780, date(2026, 5, 15)),
            ("Luxury",  "amazon shopping",      1800, date(2026, 5, 16)),
            ("Food",    "cafe coffee",           220, date(2026, 5, 18)),
            ("Travel",  "ola cab",               380, date(2026, 5, 20)),
            ("Family",  "school fees",          8500, date(2026, 5,  2)),
            ("Family",  "doctor visit",          600, date(2026, 5, 22)),
            ("Food",    "restaurant dinner",     950, date(2026, 5, 24)),
            ("Luxury",  "netflix subscription",  499, date(2026, 5,  1)),
        ],
    },
    {
        "month": 6, "year": 2026,
        "salary": 95000.0, "save_pct": 30,
        "allocations": [
            {"instrument": "Liquid MF",  "amount": 11400.0, "rationale": "Emergency buffer"},
            {"instrument": "ELSS SIP",   "amount": 9120.0,  "rationale": "Tax saving + equity growth"},
            {"instrument": "PPF",        "amount": 7980.0,  "rationale": "Safe debt allocation"},
        ],
        "expenses": [
            ("EMI",     "home loan emi",       14500, date(2026, 6,  1)),
            ("Luxury",  "netflix subscription",  499, date(2026, 6,  1)),
            ("Food",    "swiggy order",          520, date(2026, 6,  3)),
            ("Grocery", "bigbasket groceries",  2100, date(2026, 6,  5)),
            ("Saving",  "ppf deposit",          4000, date(2026, 6,  5)),
            ("Other",   "internet bill",         999, date(2026, 6,  5)),
            ("Travel",  "petrol",               2200, date(2026, 6,  7)),
            ("Food",    "zomato biryani",        740, date(2026, 6,  8)),
            ("Family",  "birthday gift",        1500, date(2026, 6, 10)),
            ("EMI",     "credit card bill",     3000, date(2026, 6, 10)),
            ("Saving",  "elss sip",             2000, date(2026, 6, 10)),
            ("Luxury",  "myntra shopping",      2400, date(2026, 6, 12)),
            ("Travel",  "auto rickshaw",         340, date(2026, 6, 14)),
            ("Food",    "lunch out",             380, date(2026, 6, 15)),
            ("Grocery", "blinkit fruits",        650, date(2026, 6, 18)),
            ("Luxury",  "movie tickets",         800, date(2026, 6, 18)),
            ("Travel",  "rapido",                260, date(2026, 6, 20)),
            ("Food",    "dinner restaurant",    1100, date(2026, 6, 22)),
            ("Family",  "medicine",              420, date(2026, 6, 25)),
            ("Food",    "cafe snacks",           180, date(2026, 6, 28)),
        ],
    },
]


async def seed() -> None:
    # Import here so env vars are loaded first
    from app.database import AsyncSessionLocal
    from app.models import Expense, IncomeEvent, SavingsPlan
    from app.services.zone_calculator import recalculate_zone

    async with AsyncSessionLocal() as db:
        for cfg in MONTHS:
            month, year = cfg["month"], cfg["year"]
            salary = cfg["salary"]
            save_pct = cfg["save_pct"]
            total_to_save = round(salary * save_pct / 100, 2)

            # ── Skip if plan already exists ──────────────────────────────
            existing = await db.execute(
                select(SavingsPlan).where(
                    SavingsPlan.month == month,
                    SavingsPlan.year == year,
                )
            )
            if existing.scalar_one_or_none():
                print(f"  [{month}/{year}] SavingsPlan already exists — skipping plan+income insert")
            else:
                # Insert IncomeEvent
                income = IncomeEvent(
                    id=uuid.uuid4(),
                    amount=Decimal(str(salary)),
                    source_name="Software Company",
                    month=month,
                    year=year,
                )
                db.add(income)

                # Insert SavingsPlan
                plan = SavingsPlan(
                    id=uuid.uuid4(),
                    month=month,
                    year=year,
                    salary_amount=Decimal(str(salary)),
                    target_save_pct=save_pct,
                    allocations=cfg["allocations"],
                    total_to_save=Decimal(str(total_to_save)),
                    gemini_narrative=None,
                )
                db.add(plan)
                print(f"  [{month}/{year}] Inserted SavingsPlan  salary=₹{salary:,.0f}  target=₹{total_to_save:,.0f}")

            # ── Insert expenses (skip if already seeded via marker expense) ──
            existing_exp = await db.execute(
                select(Expense).where(
                    Expense.description == "__seed_marker__",
                    Expense.confirmed.is_(True),
                )
            )
            # Use a different check: count expenses for this month
            from sqlalchemy import extract, func
            count_res = await db.execute(
                select(func.count(Expense.id)).where(
                    Expense.confirmed.is_(True),
                    extract("month", Expense.expense_date) == month,
                    extract("year", Expense.expense_date) == year,
                )
            )
            count = count_res.scalar() or 0
            if count >= len(cfg["expenses"]):
                print(f"  [{month}/{year}] Expenses already seeded ({count} rows) — skipping")
            else:
                inserted = 0
                for category, description, amount, exp_date in cfg["expenses"]:
                    exp = Expense(
                        id=uuid.uuid4(),
                        amount=Decimal(str(amount)),
                        description=description,
                        category=category,
                        source="seed",
                        expense_date=exp_date,
                        confirmed=True,
                    )
                    db.add(exp)
                    inserted += 1
                total_expenses = sum(amt for _, _, amt, _ in cfg["expenses"])
                print(f"  [{month}/{year}] Inserted {inserted} expenses  total=₹{total_expenses:,.0f}")

            await db.commit()

            # ── Recalculate zone (no Gemini) ─────────────────────────────
            insight = await recalculate_zone(db, month, year, with_ai=False)
            if insight:
                print(f"  [{month}/{year}] Zone → {insight.zone}  saving={insight.saving_score}  spend={insight.spend_score}")
            else:
                print(f"  [{month}/{year}] Zone recalc failed — check logs")

        print("\nSeed complete. Refresh the Compare page.")


if __name__ == "__main__":
    asyncio.run(seed())
