from sqlalchemy import DateTime, ForeignKey, Integer, func, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class Cart(Base):

    __tablename__ = "carts"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    created_at: Mapped[DateTime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )

    user = relationship("User", back_populates="cart")
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")

    @property
    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.items if item.product.is_active)


class CartItem(Base):
    __tablename__ = "cart_items"

    cart_id: Mapped[int] = mapped_column(Integer, ForeignKey("carts.id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False, server_default="1")

    cart = relationship("Cart", back_populates="items")
    product = relationship("Product", back_populates="cart_items")