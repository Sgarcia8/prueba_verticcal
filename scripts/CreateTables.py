import asyncio
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

# Importar desde el mismo directorio de scripts
from .DataBaseConfig import engine
from .Model import Base

async def create_db_tables(engine: AsyncEngine):
    """
    Crea todas las tablas de la base de datos si no existen.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tablas de la base de datos creadas exitosamente.")

async def main():
    """
    Función principal para crear tablas e insertar datos.
    """
    await create_db_tables(engine)

    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    
    async with async_session() as session:
        await session.commit()
    
    print("\nProceso de inserción completado.")

if __name__ == "__main__":
    asyncio.run(main())