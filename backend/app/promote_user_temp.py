import asyncio
import sys
import uuid
from sqlalchemy import select, update
from app.database import get_db
from app.models.user import User

async def promote_user(email: str):
    async for db in get_db():
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        
        if not user:
            print(f"Error: User with email '{email}' not found.")
            return

        await db.execute(
            update(User)
            .where(User.id == user.id)
            .values(is_superuser=True)
        )
        await db.commit()
        print(f"Success: User {email} ({user.id}) has been promoted to superuser.")
        return

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python promote_user.py <email>")
        sys.exit(1)
    
    email_to_promote = sys.argv[1]
    asyncio.run(promote_user(email_to_promote))
