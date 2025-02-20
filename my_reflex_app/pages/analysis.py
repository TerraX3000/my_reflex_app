import reflex as rx 
from typing import List 
from my_reflex_app.components.navbar import navbar
from my_reflex_app.models.models import Account, Transaction, Category, Split, TransactionType, SplitType
import pandas as pd


class AnalysisState(rx.State):
    transactions: List[TransactionType] = []
    analysis_data: List | None = None
    columns: List[str] = []
    analysis_data_loaded: bool
    @rx.event
    def load_transactions(self):
        with rx.session() as session:
            transactions: List[Transaction] = session.exec(
                Transaction.select()
            ).all()
            self.transactions = [transaction.to_dataclass() for transaction in transactions]

    @rx.event
    def initialize_state(self):
        self.load_transactions()
        self.load_analysis_data()

    @rx.event
    def load_analysis_data(self):
        df = pd.DataFrame(self.transactions)
        df = df.explode('splits')
        # if a transaction has no splits, the 'splits' column will be None
        # so we need to handle this case
        df['splits'] = df['splits'].apply(lambda x: x if isinstance(x, dict) else {})
    
        # now we can create separate columns for the split category and amount
        df['split_category'] = df['splits'].apply(lambda x: x.get('category_name'))
        df["split_sub_category"] = df['splits'].apply(lambda x: x.get('sub_category_name'))
        df['split_amount'] = df['splits'].apply(lambda x: x.get('amount'))
        
        # drop the original 'splits' column
        df = df.drop('splits', axis=1)
        
        df = df[["date", "description", "amount", "category_name", "sub_category_name", "split_category", "split_sub_category", "split_amount"]]
        df['category_name'] = df['split_category'].combine_first(df['category_name'])
        df['sub_category_name'] = df['split_sub_category'].combine_first(df['sub_category_name'])
        df['amount'] = df['split_amount'].combine_first(df['amount'])

        # drop split columns
        df = df.drop(['split_category', 'split_sub_category', 'split_amount'], axis=1)

        self.analysis_data = df.values.tolist()
        self.columns = list(df.columns)
        self.analysis_data_loaded = True
        

@rx.page(route="/analysis", on_load=AnalysisState.initialize_state)
def analysis():
    return rx.container(
        rx.vstack(
            navbar(),
        ),
        rx.heading("Analysis"),
        rx.button("Load Analysis Data", on_click=AnalysisState.load_analysis_data),
        rx.text(f"Analysis data loaded: {AnalysisState.analysis_data_loaded}"),
        rx.cond(
            AnalysisState.analysis_data_loaded,
            rx.data_table(
            data=AnalysisState.analysis_data,
            columns=AnalysisState.columns,
            pagination=True,
            search=True,
            sort=True,
            ),
            rx.text("no analysis data")
        ),

    )
