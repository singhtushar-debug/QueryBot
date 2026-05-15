from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass


class CartItem(Base):
    __tablename__ = "cart"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]
    product_id: Mapped[int]
    title: Mapped[str]
    price: Mapped[float]
    quantity: Mapped[int]
    image: Mapped[str | None]
