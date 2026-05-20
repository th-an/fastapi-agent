import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()


async def seed_data():
    client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
    db = client[os.getenv("DATABASE_NAME", "myapp")]

    # Clear existing data
    await db.customers.delete_many({})
    await db.orders.delete_many({})

    # Seed customers
    customers = [
        {
            "customer_id": "CUST-001",
            "name": "John Doe",
            "email": "john@example.com",
            "account_status": "active",
        },
        {
            "customer_id": "CUST-002",
            "name": "Jane Smith",
            "email": "jane@example.com",
            "account_status": "active",
        },
        {
            "customer_id": "CUST-003",
            "name": "Bob Wilson",
            "email": "bob@example.com",
            "account_status": "inactive",
        },
    ]
    await db.customers.insert_many(customers)

    # Seed orders
    orders = [
        {
            "order_id": "ORD-001",
            "status": "shipped",
            "customer_id": "CUST-001",
            "items": [{"name": "Widget", "qty": 2, "price": 24.99}],
            "total": 49.98,
            "created_at": "2026-05-15T10:30:00Z",
        },
        {
            "order_id": "ORD-002",
            "status": "processing",
            "customer_id": "CUST-001",
            "items": [{"name": "Gadget", "qty": 1, "price": 99.99}],
            "total": 99.99,
            "created_at": "2026-05-18T14:20:00Z",
        },
        {
            "order_id": "ORD-003",
            "status": "delivered",
            "customer_id": "CUST-002",
            "items": [{"name": "Thing", "qty": 3, "price": 15.00}],
            "total": 45.00,
            "created_at": "2026-05-10T09:00:00Z",
        },
    ]
    await db.orders.insert_many(orders)

    print(f"Seeded {len(customers)} customers and {len(orders)} orders")

    # Verify
    cust_count = await db.customers.count_documents({})
    ord_count = await db.orders.count_documents({})
    print(f"Verification: {cust_count} customers, {ord_count} orders in database")

    client.close()


if __name__ == "__main__":
    asyncio.run(seed_data())
