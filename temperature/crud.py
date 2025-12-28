from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from temperature import models, schemas
from cities import crud


async def create_temperature(db: AsyncSession, temp: schemas.TemperatureCreate):
    db_temp = models.DBTemperature(
        city_id=temp.city_id,
        temperature=temp.temperature,
        date_time=temp.date_time
    )
    db.add(db_temp)
    await db.commit()
    await db.refresh(db_temp)
    return db_temp


async def get_all_temperatures(db: AsyncSession):
    result = await db.execute(select(models.DBTemperature))
    return result.scalars().all()


async def get_temperatures_by_city(db: AsyncSession, city_id: int):
    stmt = select(models.DBTemperature).where(models.DBTemperature.city_id == city_id)
    result = await db.execute(stmt)
    return result.scalars().all()


async def update_all_temperatures(db: AsyncSession):
    from temperature.utils import fetch_temperature
    from cities.crud import get_all_cities
    cities = await get_all_cities(db)
    temps = []
    for city in cities:
        temp_value = await fetch_temperature(city.name)
        temp = schemas.TemperatureCreate(city_id=city.id, temperature=temp_value)
        temps.append(await create_temperature(db, temp))
    return temps
