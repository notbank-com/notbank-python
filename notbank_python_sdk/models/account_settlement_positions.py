from decimal import Decimal
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class AccountSettlementPosition:
    oms_id: int
    account_id: int
    product_id: int
    product_symbol: str
    product_type: str
    position: Decimal
    base_product_id: int
    base_product_symbol: Optional[str]
    base_product_notional_amount: Decimal
    credit_limit: Decimal
    credit_utilization: Decimal
    credit_remaining: Decimal
    current_notional_rate: Decimal
    current_base_product_notional_amount: Decimal


@dataclass
class AccountSettlementPositions:
    oms_id: int
    account_id: int
    account_name: str
    credit_tier: int
    trading_halted: bool
    base_product_id: int
    base_product_amount_fiat: Decimal
    base_product_amount_crypto: Decimal
    base_product_net_owed_amount: Decimal
    base_product_net_owed_limit: Decimal
    base_product_net_owed_remaining: Decimal
    base_product_net_owed_amount_fiat: Decimal
    base_product_net_owed_amount_crypto: Decimal
    account_settlement_positions: List[AccountSettlementPosition]
    base_product_symbol: Optional[str] = None
