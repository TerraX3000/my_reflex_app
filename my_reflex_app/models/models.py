import reflex as rx
from datetime import date
from enum import Enum as PyEnum
from typing import List, Optional
from sqlmodel import Field, Relationship
from sqlalchemy import Enum
import dataclasses


@dataclasses.dataclass
class SplitType:
    id: int
    transaction_id: int
    category_id: int
    description: str
    amount: float
    is_expense_category: bool
    category_name: str = ""
    sub_category_name: str = ""

@dataclasses.dataclass
class TransactionType:
    id: int
    date: str
    description: str
    original_description: str
    bank_category: str
    amount: float
    bank_status: str
    bank_type: str
    memo: str
    category_id: int
    account_id: int
    splits: List[SplitType]
    category_name: str = ""
    sub_category_name: str = ""


# ✅ TimePeriod Enum
class TimePeriod(PyEnum):
    DAILY = "Daily"
    WEEKLY = "Weekly"
    MONTHLY = "Monthly"
    QUARTERLY = "Quarterly"
    SEMIANNUALLY = "Semiannually"
    ANNUALLY = "Annually"

@dataclasses.dataclass
class BudgetType:
    id: int
    category_id: int
    time_period: str
    amount: float
    category_name: str = ""
    sub_category_name: str = ""

@dataclasses.dataclass
class CategoryType:
    id: int
    name: str
    description: str
    is_expense_category: bool
    parent_id: int
    parent_name: str = ""

# ✅ Category Model
class Category(rx.Model, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    description: Optional[str] = None
    is_expense_category: bool = Field(default=True)
    parent_id: Optional[int] = Field(default=None, foreign_key="category.id")

    # Relationships
    parent: Optional["Category"] = Relationship(
        back_populates="children",
        sa_relationship_kwargs={
            "remote_side": "Category.id",
            "lazy": "joined"
            },
    )
    children: List["Category"] = Relationship(
        back_populates="parent",
        cascade_delete=True,
    )
    transactions: List["Transaction"] = Relationship(back_populates="category")
    splits: List["Split"] = Relationship(back_populates="category")
    budgets: List["Budget"] = Relationship(
        back_populates="category",
        cascade_delete=True,
    )

    def to_dataclass(self) -> CategoryType:
        return CategoryType(
            id=self.id,
            name=self.name,
            description=self.description,
            is_expense_category=self.is_expense_category,
            parent_id=self.parent_id,
            parent_name=self.parent.name if self.parent else "",
        )


# ✅ Budget Model
class Budget(rx.Model, table=True):
    id: int | None = Field(default=None, primary_key=True)
    category_id: int = Field(foreign_key="category.id", nullable=False)
    time_period: str = Field(nullable=False)
    amount: float

    # Relationships
    category: "Category" = Relationship(back_populates="budgets")

    def to_dataclass(self) -> BudgetType:
        return BudgetType(
            id=self.id,
            category_id=self.category_id,
            time_period=self.time_period,
            amount=self.amount,
            category_name=self.category.parent.name if self.category.parent else self.category.name,
            sub_category_name=self.category.name if self.category.parent else "",
        )


# ✅ Account Model
class Account(rx.Model, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, unique=True)
    date_field: str = Field(default="")
    date_format: str = Field(default="%Y-%m-%d")
    amount_field: str = Field(default="")
    description_field: str = Field(default="")
    original_description_field: str = Field(default="")
    bank_category_field: str = Field(default="")
    type_field: str = Field(default="")
    status_field: str = Field(default="") 
    is_reverse_negative_values: bool = Field(default=False)
    include_pending_status: bool = Field(default=False)


    # Relationships
    transactions: List["Transaction"] = Relationship(
        back_populates="account",
        cascade_delete=True,
    )


# ✅ Transaction Model
class Transaction(rx.Model, table=True):
    id: int | None = Field(default=None, primary_key=True)
    date: str
    description: str
    original_description: str
    bank_category: str
    bank_status: str
    bank_type: str
    memo: str = Field(default="")
    category_id: int = Field(foreign_key="category.id", nullable=True)
    account_id: int = Field(foreign_key="account.id", nullable=False)
    amount: float  # Net amount (after splits)

    # Relationships
    category: "Category" = Relationship(
        back_populates="transactions",
        sa_relationship_kwargs={
            "lazy": "joined"
            },
        )
    account: "Account" = Relationship(back_populates="transactions")
    splits: List["Split"] = Relationship(
        back_populates="transaction",
        cascade_delete=True,
        sa_relationship_kwargs={"lazy": "selectin"}, 
    )

    def to_dataclass(self) -> TransactionType:
        if self.category:
            if self.category.parent:
                category_name = self.category.parent.name
                sub_category_name = self.category.name
                is_expense_category = self.category.is_expense_category
            else:
                category_name = self.category.name
                sub_category_name = ""
                is_expense_category = self.category.is_expense_category
        else:
            is_expense_category = True
            category_name = ""
            sub_category_name = ""

        return TransactionType(
            id=self.id,
            date=self.date,
            description=self.description,
            original_description=self.original_description,
            bank_category=self.bank_category,
            amount=self.amount,
            bank_status=self.bank_status,
            bank_type=self.bank_type,
            memo=self.memo,
            category_id=self.category_id,
            account_id=self.account_id,
            is_expense_category=is_expense_category,
            category_name=category_name,
            sub_category_name=sub_category_name,
            splits=[split.to_dataclass() for split in self.splits],
        )


# ✅ Split Model
class Split(rx.Model, table=True):
    id: int | None = Field(default=None, primary_key=True)
    transaction_id: int = Field(foreign_key="transaction.id", nullable=False)
    category_id: int | None = Field(default=None, foreign_key="category.id")
    description: str | None = None
    amount: float

    # Relationships
    transaction: "Transaction" = Relationship(back_populates="splits")
    category: Optional["Category"] = Relationship()

    def to_dataclass(self) -> SplitType:
        if self.category:
            if self.category.parent:
                category_name = self.category.parent.name
                sub_category_name = self.category.name
                is_expense_category = self.category.is_expense_category
            else:
                category_name = self.category.name
                sub_category_name = ""
                is_expense_category = self.category.is_expense_category
        else:
            category_name = ""
            sub_category_name = ""
            is_expense_category = True

        return SplitType(
            id=self.id,
            transaction_id=self.transaction_id,
            category_id=self.category_id,
            description=self.description,
            amount=self.amount,
            category_name=category_name,
            sub_category_name=sub_category_name,
            is_expense_category=is_expense_category
        )