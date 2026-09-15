import logging
import uuid
from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, extract, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Bank, Expense, IncomeEvent, SavingsPlan, SpendInsight
from app.schemas import BankCreate, BankOut, MonthSettings, MonthSettingsOut

logger = logging.getLogger(__name__)
router = APIRouter(tags=["settings"])
DbDep = Annotated[AsyncSession, Depends(get_db)]


@router.get("/settings", response_model=MonthSettingsOut)
async def get_settings(month: int, year: int, db: DbDep) -> MonthSettingsOut:
    """Get current month settings. locked=True means salary is set and cannot change."""
    try:
        result = await db.execute(
            select(SavingsPlan)
            .where(SavingsPlan.month == month, SavingsPlan.year == year)
            .order_by(SavingsPlan.created_at.desc())
            .limit(1)
        )
        plan = result.scalar_one_or_none()
    except Exception as exc:
        logger.error("DB error fetching settings: %s", exc)
        raise HTTPException(status_code=500, detail="Database error.")

    if plan:
        return MonthSettingsOut(
            salary=float(plan.salary_amount),
            save_pct=plan.target_save_pct,
            month=month,
            year=year,
            locked=True,
        )
    return MonthSettingsOut(month=month, year=year, locked=False)


@router.post("/settings", response_model=MonthSettingsOut)
async def save_settings(body: MonthSettings, db: DbDep) -> MonthSettingsOut:
    """Lock salary + save % for a month. Cannot be changed afterwards (use restart to reset)."""
    try:
        result = await db.execute(
            select(SavingsPlan)
            .where(SavingsPlan.month == body.month, SavingsPlan.year == body.year)
            .limit(1)
        )
        existing = result.scalar_one_or_none()
    except Exception as exc:
        logger.error("DB error checking settings lock: %s", exc)
        raise HTTPException(status_code=500, detail="Database error.")

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Settings are already locked for this month. Restart the month to change.",
        )

    # Create income event for the salary
    income = IncomeEvent(
        id=uuid.uuid4(),
        amount=body.salary,
        source_name="salary",
        month=body.month,
        year=body.year,
    )
    db.add(income)

    # Create savings plan with default allocations
    total_to_save = body.salary * body.save_pct / 100
    allocs = [
        {"instrument": "Liquid MF", "amount": round(total_to_save * 0.4, 2), "rationale": "Emergency buffer"},
        {"instrument": "Index Fund", "amount": round(total_to_save * 0.4, 2), "rationale": "Long-term growth"},
        {"instrument": "PPF", "amount": round(total_to_save * 0.2, 2), "rationale": "Tax saving"},
    ]
    plan = SavingsPlan(
        id=uuid.uuid4(),
        month=body.month,
        year=body.year,
        salary_amount=body.salary,
        target_save_pct=body.save_pct,
        allocations=allocs,
        total_to_save=total_to_save,
    )
    db.add(plan)

    try:
        await db.commit()
    except Exception as exc:
        await db.rollback()
        logger.error("Failed to save settings: %s", exc)
        raise HTTPException(status_code=500, detail="Database error saving settings.")

    import asyncio
    asyncio.create_task(_recalculate_zone(body.month, body.year))

    return MonthSettingsOut(
        salary=body.salary,
        save_pct=body.save_pct,
        month=body.month,
        year=body.year,
        locked=True,
    )


@router.patch("/settings", response_model=MonthSettingsOut)
async def update_settings(body: MonthSettings, db: DbDep) -> MonthSettingsOut:
    """Update salary + save % for a month. Updates the SavingsPlan and the salary IncomeEvent."""
    try:
        result = await db.execute(
            select(SavingsPlan)
            .where(SavingsPlan.month == body.month, SavingsPlan.year == body.year)
            .limit(1)
        )
        plan = result.scalar_one_or_none()
    except Exception as exc:
        logger.error("DB error checking settings: %s", exc)
        raise HTTPException(status_code=500, detail="Database error.")

    if not plan:
        raise HTTPException(
            status_code=404,
            detail="Settings not initialized for this month yet. Save first.",
        )

    try:
        result_income = await db.execute(
            select(IncomeEvent)
            .where(
                IncomeEvent.month == body.month,
                IncomeEvent.year == body.year,
                IncomeEvent.source_name == "salary",
            )
            .limit(1)
        )
        income = result_income.scalar_one_or_none()
    except Exception as exc:
        logger.error("DB error fetching salary income: %s", exc)
        raise HTTPException(status_code=500, detail="Database error.")

    if income:
        income.amount = body.salary
    else:
        income = IncomeEvent(
            id=uuid.uuid4(),
            amount=body.salary,
            source_name="salary",
            month=body.month,
            year=body.year,
        )
        db.add(income)

    total_to_save = body.salary * body.save_pct / 100
    allocs = [
        {"instrument": "Liquid MF", "amount": round(total_to_save * 0.4, 2), "rationale": "Emergency buffer"},
        {"instrument": "Index Fund", "amount": round(total_to_save * 0.4, 2), "rationale": "Long-term growth"},
        {"instrument": "PPF", "amount": round(total_to_save * 0.2, 2), "rationale": "Tax saving"},
    ]
    plan.salary_amount = body.salary
    plan.target_save_pct = body.save_pct
    plan.allocations = allocs
    plan.total_to_save = total_to_save

    try:
        await db.commit()
    except Exception as exc:
        await db.rollback()
        logger.error("Failed to update settings: %s", exc)
        raise HTTPException(status_code=500, detail="Database error updating settings.")

    import asyncio
    asyncio.create_task(_recalculate_zone(body.month, body.year))

    return MonthSettingsOut(
        salary=body.salary,
        save_pct=body.save_pct,
        month=body.month,
        year=body.year,
        locked=True,
    )


@router.delete("/settings/restart")
async def restart_month(month: int, year: int, db: DbDep) -> dict:
    """Delete ALL data for a month (expenses, income, plan, insights). Irreversible."""
    try:
        await db.execute(
            delete(Expense).where(
                extract("month", Expense.expense_date) == month,
                extract("year", Expense.expense_date) == year,
            )
        )
        await db.execute(
            delete(IncomeEvent).where(IncomeEvent.month == month, IncomeEvent.year == year)
        )
        await db.execute(
            delete(SavingsPlan).where(SavingsPlan.month == month, SavingsPlan.year == year)
        )
        await db.execute(
            delete(SpendInsight).where(SpendInsight.month == month, SpendInsight.year == year)
        )
        await db.commit()
    except Exception as exc:
        await db.rollback()
        logger.error("Failed to restart month: %s", exc)
        raise HTTPException(status_code=500, detail="Database error during restart.")

    return {"status": "restarted", "month": month, "year": year}


@router.get("/settings/banks", response_model=list[BankOut])
async def list_banks(db: DbDep) -> list[BankOut]:
    try:
        result = await db.execute(select(Bank).order_by(Bank.name))
        banks = result.scalars().all()
    except Exception as exc:
        logger.error("DB error listing banks: %s", exc)
        raise HTTPException(status_code=500, detail="Database error.")
    return [BankOut.model_validate(b) for b in banks]


@router.post("/settings/banks", response_model=BankOut, status_code=201)
async def create_bank(body: BankCreate, db: DbDep) -> BankOut:
    name = body.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Bank name cannot be empty.")

    try:
        result = await db.execute(select(Bank).where(func.lower(Bank.name) == name.lower()))
        existing = result.scalar_one_or_none()
    except Exception as exc:
        logger.error("DB error checking bank uniqueness: %s", exc)
        raise HTTPException(status_code=500, detail="Database error.")

    if existing:
        raise HTTPException(status_code=409, detail="Bank already exists.")

    bank = Bank(id=uuid.uuid4(), name=name)
    db.add(bank)
    try:
        await db.commit()
        await db.refresh(bank)
    except Exception as exc:
        await db.rollback()
        logger.error("Failed to save bank: %s", exc)
        raise HTTPException(status_code=500, detail="Database error saving bank.")

    return BankOut.model_validate(bank)


@router.delete("/settings/banks/{bank_id}")
async def delete_bank(bank_id: uuid.UUID, db: DbDep) -> dict:
    try:
        result = await db.execute(select(Bank).where(Bank.id == bank_id))
        bank = result.scalar_one_or_none()
    except Exception as exc:
        logger.error("DB error fetching bank: %s", exc)
        raise HTTPException(status_code=500, detail="Database error.")

    if bank is None:
        raise HTTPException(status_code=404, detail="Bank not found.")

    try:
        await db.delete(bank)
        await db.commit()
    except Exception as exc:
        await db.rollback()
        logger.error("Failed to delete bank: %s", exc)
        raise HTTPException(status_code=500, detail="Database error deleting bank.")

    return {"status": "deleted", "bank_id": str(bank_id)}


async def _recalculate_zone(month: int, year: int) -> None:
    from app.database import AsyncSessionLocal
    from app.services.zone_calculator import recalculate_zone
    async with AsyncSessionLocal() as db:
        try:
            await recalculate_zone(db, month, year, with_ai=False)
        except Exception as exc:
            logger.error("Zone recalculation failed: %s", exc)
