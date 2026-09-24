from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.driver import Driver
from app.schemas.driver import DriverCreate, DriverRead

router = APIRouter(prefix="/drivers", tags=["drivers"])


@router.post("/", response_model=DriverRead, status_code=201)
async def create_driver(payload: DriverCreate, db: AsyncSession = Depends(get_db)):
    driver = Driver(**payload.model_dump())
    db.add(driver)
    await db.commit()
    await db.refresh(driver)
    return driver


@router.get("/", response_model=list[DriverRead])
async def list_drivers(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Driver))
    return result.scalars().all()


@router.get("/{driver_id}", response_model=DriverRead)
async def get_driver(driver_id: int, db: AsyncSession = Depends(get_db)):
    driver = await db.get(Driver, driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver


@router.delete("/{driver_id}", status_code=204)
async def delete_driver(driver_id: int, db: AsyncSession = Depends(get_db)):
    driver = await db.get(Driver, driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    await db.delete(driver)
    await db.commit()
