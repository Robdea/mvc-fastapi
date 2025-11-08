import uuid
from fastapi import HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.stripe_schema import PaymentRequest
import stripe
from ..models.history_sold import Transaction, TransactionItem

from ..config import STRIPE_SECRET
from ..models.product import Product
from ..utils import auth

stripe.api_key = STRIPE_SECRET

class PayServices:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def create_payment_intent(self, data: PaymentRequest, request: Request):
        # 1️⃣ Obtener user_id desde el token
        token = request.cookies.get("access_token")
        
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token no encontrado")

        payload = auth.decoe_access_token(token)
        if not payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado")
        
        payload = auth.decoe_access_token(token)
        if not payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado")
        user_id = payload.get("sub")

        # return {"user":user_id, "data":data}

        # 2️⃣ Calcular total y validar productos
        total_amount = 0
        items_data = []

        for item in data.listProducts:
            product = await self.db.get(Product, item.id)
            if not product:
                raise HTTPException(status_code=404, detail=f"Producto {item.id} no encontrado")

            total_amount += product.price * item.quantity
            items_data.append({
                "product_id": product.id,
                "product_name": product.name,
                "product_price": product.price,
                "quantity": item.quantity
            })

        amount_cents = int(float(total_amount) * 100)

        # 3️⃣ Crear PaymentIntent en Stripe
        intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency=data.currency,
            payment_method_types=["card"]
        )

        # 4️⃣ Crear la transacción en la BD
        transaction = Transaction(
            id=str(uuid.uuid4()),
            user_id=user_id,
            total=total_amount
        )
        self.db.add(transaction)

        for item in items_data:
            transaction_item = TransactionItem(
                transaction_id=transaction.id,
                product_id=item["product_id"],
                product_name=item["product_name"],
                product_price=item["product_price"],
                quantity=item["quantity"]
            )
            self.db.add(transaction_item)

        # 5️⃣ Commit y refresh
        await self.db.commit()
        await self.db.refresh(transaction)

        # 6️⃣ Devolver client_secret y transacción
        return {
            "clientSecret": intent.client_secret,
            "transactionId": transaction.id,
            "total": total_amount
        }
