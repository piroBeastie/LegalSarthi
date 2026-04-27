"""
LegalSarthi - Database Connection
Async MongoDB connection using Motor driver.
"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import settings

client: AsyncIOMotorClient = None
db: AsyncIOMotorDatabase = None


async def connect_db():
    """Initialize MongoDB connection and create indexes."""
    global client, db
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.MONGODB_DB_NAME]

    # ── Create indexes ──
    await db.users.create_index("email", unique=True)
    await db.conversations.create_index("user_id")
    await db.conversations.create_index("created_at")
    await db.messages.create_index("conversation_id")
    await db.messages.create_index("created_at")

    print(f"✅ Connected to MongoDB: {settings.MONGODB_DB_NAME}")


async def close_db():
    """Close MongoDB connection."""
    global client
    if client:
        client.close()
        print("🔌 MongoDB connection closed.")


def get_db() -> AsyncIOMotorDatabase:
    """Get database instance."""
    return db
