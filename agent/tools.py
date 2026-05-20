from pydantic_ai import RunContext
from motor.motor_asyncio import AsyncIOMotorDatabase
from agent.result_types import CustomerInfo, InvoiceValidationResult, OrderStatus
from datetime import datetime


async def get_customer_info(ctx: RunContext[None], customer_id: str) -> CustomerInfo:
    """Fetch customer information from the database.
    
    Args:
        customer_id: The unique customer identifier
    """
    db: AsyncIOMotorDatabase = ctx.deps
    customer = await db.customers.find_one({"customer_id": customer_id})
    
    if not customer:
        return CustomerInfo(
            customer_id=customer_id,
            name="Unknown",
            email="unknown@example.com",
            account_status="not_found"
        )
    
    return CustomerInfo(
        customer_id=str(customer.get("customer_id")),
        name=customer.get("name", "Unknown"),
        email=customer.get("email", "unknown@example.com"),
        account_status=customer.get("account_status", "unknown")
    )


async def validate_invoice(ctx: RunContext[None], invoice_id: str, amount: float) -> InvoiceValidationResult:
    """Validate an invoice against business rules.
    
    Args:
        invoice_id: The invoice identifier
        amount: The invoice amount to validate
    """
    errors = []
    
    if amount <= 0:
        errors.append("Invoice amount must be positive")
    
    if not invoice_id.startswith("INV-"):
        errors.append("Invalid invoice ID format")
    
    return InvoiceValidationResult(
        valid=len(errors) == 0,
        invoice_id=invoice_id,
        errors=errors,
        amount=amount
    )


async def get_order_status(ctx: RunContext[None], order_id: str) -> OrderStatus:
    """Get the status of an order.
    
    Args:
        order_id: The unique order identifier
    """
    db: AsyncIOMotorDatabase = ctx.deps
    order = await db.orders.find_one({"order_id": order_id})
    
    if not order:
        return OrderStatus(
            order_id=order_id,
            status="not_found",
            customer_id="unknown",
            items=[],
            total=0.0,
            created_at=datetime.utcnow()
        )
    
    return OrderStatus(
        order_id=str(order.get("order_id")),
        status=order.get("status", "unknown"),
        customer_id=str(order.get("customer_id")),
        items=order.get("items", []),
        total=order.get("total", 0.0),
        created_at=order.get("created_at", datetime.utcnow())
    )