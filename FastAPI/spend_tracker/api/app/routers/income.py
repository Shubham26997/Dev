import logging
import uuid
from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import IncomeEvent, SavingsPlan
from app.schemas import IncomeCreate, IncomeOut, IncomeResponse, SavingsPlanOut
from app.services import parser
from app.services.advisor import generate_savings_plan
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/income", tags=["income"])

DbDep = Annotated[AsyncSession, Depends(get_db)]


@router.post("", response_model=IncomeResponse)
async def create_income(body: IncomeCreate, db: DbDep) -> IncomeResponse:
    parsed = parser.parse(body.raw_text)
    if parsed is None or parsed.entry_type != "income":
        raise HTTPException(
            status_code=422,
            detail="Could not parse income. Try: 'salary 95000 credited from Software Company'",
        )

    now = datetime.now(tz=timezone.utc)
    income = IncomeEvent(
        id=uuid.uuid4(),
        amount=parsed.amount,
        source_name=parsed.source_name or "salary",
        month=now.month,
        year=now.year,
    )

    try:
        db.add(income)
        await db.commit()
        await db.refresh(income)
    except Exception as exc:
        await db.rollback()
        logger.error("Failed to insert income: %s", exc)
        raise HTTPException(status_code=500, detail="Database error saving income.")

    # Generate savings plan via Gemini
    advice = generate_savings_plan(
        salary=float(parsed.amount),
        target_save_pct=settings.saving_target_pct,
        month=now.month,
        year=now.year,
    )

    total_to_save = parsed.amount * settings.saving_target_pct / 100
    allocations = advice.investment_suggestions or [
        {"instrument": "Liquid MF", "amount": total_to_save * 0.4, "rationale": "Emergency buffer"},
        {"instrument": "Index Fund", "amount": total_to_save * 0.4, "rationale": "Long-term growth"},
        {"instrument": "PPF", "amount": total_to_save * 0.2, "rationale": "Tax saving"},
    ]

    savings_plan = SavingsPlan(
        id=uuid.uuid4(),
        month=now.month,
        year=now.year,
        salary_amount=parsed.amount,
        target_save_pct=settings.saving_target_pct,
        allocations=allocations,
        total_to_save=total_to_save,
        gemini_narrative=advice.narrative,
    )

    try:
        db.add(savings_plan)
        await db.commit()
        await db.refresh(savings_plan)
    except Exception as exc:
        await db.rollback()
        logger.error("Failed to insert savings plan: %s", exc)
        # Non-fatal — income was saved successfully

    # Trigger zone recalculation
    import asyncio
    asyncio.create_task(_recalculate_zone(now.month, now.year))

    return IncomeResponse(
        status="logged",
        income=IncomeOut.model_validate(income),
        savings_plan=SavingsPlanOut.model_validate(savings_plan) if savings_plan.id else None,
    )


@router.get("", response_model=list[IncomeOut])
async def list_income(month: int, year: int, db: DbDep) -> list[IncomeOut]:
    try:
        result = await db.execute(
            select(IncomeEvent)
            .where(IncomeEvent.month == month, IncomeEvent.year == year)
            .order_by(IncomeEvent.credited_at.desc())
        )
        events = result.scalars().all()
    except Exception as exc:
        logger.error("DB error listing income: %s", exc)
        raise HTTPException(status_code=500, detail="Database error.")

    return [IncomeOut.model_validate(e) for e in events]


async def _recalculate_zone(month: int, year: int) -> None:
    from app.database import AsyncSessionLocal
    from app.services.zone_calculator import recalculate_zone
    async with AsyncSessionLocal() as db:
        try:
            await recalculate_zone(db, month, year)
        except Exception as exc:
            logger.error("Zone recalculation failed: %s", exc)
