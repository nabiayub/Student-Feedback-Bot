#!/usr/bin/env python3
"""
Test Neon + asyncpg connection WITHOUT tables.
Just verifies async driver + Neon connectivity.
"""

import asyncio
import os

from sqlalchemy import text

from src.config.settings import settings
from sqlalchemy.ext.asyncio import create_async_engine

print(settings.DATABASE_URL)


async def test_neon_async():
    """Pure async connection test"""
    print("🧪 Testing Neon + asyncpg connection...")

    # Create engine from your settings
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=True,  # Shows SQL queries
        pool_pre_ping=True
    )

    try:
        # Test 1: Ping database
        async with engine.connect() as conn:
            print("🔗 Connection opened...")

            # Simple SELECT (no tables needed)
            result = await conn.execute(text("SELECT 1 as ping"))
            print(f"✅ Ping: {result.scalar()}")

            # Test 2: Database info
            result = await conn.execute(text("SELECT current_database() as db"))
            print(f"📊 Database: {result.scalar()}")

            # Test 3: Postgres version
            result = await conn.execute(text("SELECT version()"))
            print(f"🐘 Postgres: {result.scalar()[:80]}...")

            # Test 4: Connection pool (open 2nd connection)
            async with engine.connect() as conn2:
                result2 = await conn2.execute   (text("SELECT pg_backend_pid() as pid"))
                print(f"🔄 Pool works (PID): {result2.scalar()}")

    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

    finally:
        await engine.dispose()
        print("🔌 Engine disposed")


if __name__ == "__main__":
    asyncio.run(test_neon_async())
