from sqlalchemy import String, Integer, Boolean, func, TIMESTAMP, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class Product(Base):

    __tablename__ = "products"

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    cart_items = relationship("CartItem", back_populates="product")
