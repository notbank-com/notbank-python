from enum import Enum


class Endpoints(str, Enum):

    # account
    GET_ACCOUNT_TRANSACTIONS = "GetAccountTransactions"
    GET_ACCOUNT_POSITIONS = "GetAccountPositions"
    GET_ACCOUNT_INSTRUMENT_STATISTICS = "GetAccountInstrumentStatistics"
    GET_ACCOUNT_INFO = "GetAccountInfo"

    # authentication
    AUTHENTICATE_USER = "AuthenticateUser"
    WEB_AUTHENTICATE_USER = "WebAuthenticateUser"
    LOGOUT = "LogOut"

    # # fee
    GET_WITHDRAW_FEE = "GetWithdrawFee"
    GET_DEPOSIT_FEE = "GetDepositFee"
    GET_OMS_DEPOSIT_FEES = "GetOMSDepositFees"
    GET_OMS_WITHDRAW_FEES = "GetOMSWithdrawFees"
    GET_ACCOUNT_FEES = "GetAccountFees"
    GET_ORDER_FEE = "GetOrderFee"

    # instrument
    GET_INSTRUMENT = "GetInstrument"
    GET_INSTRUMENTS = "GetInstruments"
    GET_INSTRUMENT_VERIFICATION_LEVEL_CONFIG = "GetInstrumentVerificationLevelConfig"

    # product
    GET_PRODUCT = "GetProduct"
    GET_PRODUCTS = "GetProducts"
    GET_VERIFICATION_LEVEL_CONFIG = "GetVerificationLevelConfig"

    # reports
    GENERATE_TRADE_ACTIVITY_REPORT = "GenerateTradeActivityReport"
    GENERATE_TRANSACTION_ACTIVITY_REPORT = "GenerateTransactionActivityReport"
    GENERATE_PRODUCT_DELTA_ACTIVITY_REPORT = "GenerateProductDeltaActivityReport"
    GENERATE_PNL_ACTIVITY_REPORT = "GeneratePnLActivityReport"
    SCHEDULE_TRADE_ACTIVITY_REPORT = "ScheduleTradeActivityReport"
    SCHEDULE_TRANSACTION_ACTIVITY_REPORT = "ScheduleTransactionActivityReport"
    SCHEDULE_PRODUCT_DELTA_ACTIVITY_REPORT = "ScheduleProductDeltaActivityReport"
    SCHEDULE_PROFIT_AND_LOSS_ACTIVITY_REPORT = "ScheduleProfitAndLossActivityReport"
    CANCEL_USER_REPORT = "CancelUserReport"
    GET_USER_REPORT_WRITER_RESULT_RECORDS = "GetUserReportWriterResultRecords"
    GET_USER_REPORT_TICKETS = "GetUserReportTickets"
    REMOVE_USER_REPORT_TICKET = "RemoveUserReportTicket"
    GET_USER_REPORT_TICKETS_BY_STATUS = "GetUserReportTicketsByStatus"
    DOWNLOAD_DOCUMENT = "DownloadDocument"
    DOWNLOAD_DOCUMENT_SLICE = "DownloadDocumentSlice"

    # ping
    PING = "Ping"
    HEALTH_CHECK = "HealthCheck"

    # trading
    SEND_ORDER_LIST = "SendOrderList"
    SEND_CANCEL_LIST = "SendCancelList"
    SEND_CANCEL_REPLACE_LIST = "SendCancelReplaceList"
    MODIFY_ORDER = "ModifyOrder"
    CANCEL_ALL_ORDERS = "CancelAllOrders"
    GET_ORDER_STATUS = "GetOrderStatus"
    GET_ORDERS_HISTORY = "GetOrdersHistory"
    GET_TRADES_HISTORY = "GetTradesHistory"
    GET_ORDER_HISTORY_BY_ORDER_ID = "GetOrderHistoryByOrderId"
    GET_TICKER_HISTORY = "GetTickerHistory"
    GET_LAST_TRADES = "GetLastTrades"
    GET_LEVEL1_SUMMARY = "GetLevel1Summary"
    GET_LEVEL1_SUMMARY_MIN = "GetLevel1SummaryMin"
    GET_OPEN_TRADE_REPORTS = "GetOpenTradeReports"
    GET_ORDERS = "GetOrders"
    GET_ORDER_HISTORY = "GetOrderHistory"
    SEND_ORDER = "SendOrder"
    CANCEL_REPLACE_ORDER = "CancelReplaceOrder"
    CANCEL_ORDER = "CancelOrder"
    GET_OPEN_ORDERS = "GetOpenOrders"
    GET_ACCOUNT_TRADES = "GetAccountTrades"
    SUMMARY = "Summary"
    TICKER = "Ticker"
    ORDER_BOOK = "OrderBook"
    TRADES = "Trades"
    GET_L2_SNAPSHOT = "GetL2Snapshot"
    GET_LEVEL1 = "GetLevel1"
    GET_ENUMS = "GetEnums"

    # user
    GET_USER_ACCOUNTS = "GetUserAccounts"
    GET_USER_DEVICES = "GetUserDevices"
    GET_USER_INFO = "GetUserInfo"
    GET_USER_PERMISSIONS = "GetUserPermissions"

    # wallet
    BANKS = "banks"
    BANK_ACCOUNTS = "bank-accounts"
    GET_NETWORK_TEMPLATES = "wallet/crypto/withdrawal/templates"
    GET_DEPOSIT_ADDRESSES = "wallet/crypto"
    CREATE_DEPOSIT_ADDRESS = "wallet/crypto"
    WHITELISTED_ADDRESSES = "wallet/crypto/whitelist-addresses"
    UPDATE_ONE_STEP_WITHDRAW = "wallet/crypto/whitelist-addresses/one-step/status"
    CREATE_CRIPTO_WITHDRAW = "wallet/crypto/withdrawal"
    FIAT_DEPOSIT = "wallet/fiat/deposit"
    GET_OWNERS_FIAT_WITHDRAW = "wallet/fiat/withdrawal/owners"
    FIAT_WITHDRAW = "wallet/fiat/withdrawal"
    TRANSFER_FUNDS = "wallet/transfer-funds"
    GET_TRANSACTIONS = "wallet/transactions"

    # subaccount
    SUBACCOUNT = "subaccounts"

    # quote
    QUOTES = "quotes"
    QUOTES_DIRECT = "quotes/direct"
    QUOTES_INVERSE = "quotes/inverse"


class WebSocketEndpoint(str, Enum):
    SUBSCRIBE_LEVEL2 = "SubscribeLevel2"
    UNSUBSCRIBE_LEVEL2 = "UnsubscribeLevel2"
    SUBSCRIBE_LEVEL1 = "SubscribeLevel1"
    UNSUBSCRIBE_LEVEL1 = "UnsubscribeLevel1"
    SUBSCRIBE_TRADES = "SubscribeTrades"
    UPDATE_TRADES = "TradeDataUpdateEvent"
    UNSUBSCRIBE_TRADES = "UnsubscribeTrades"
    SUBSCRIBE_TICKER = "SubscribeTicker"
    UNSUBSCRIBE_TICKER = "UnsubscribeTicker"
    SUBSCRIBE_ACCOUNT_EVENTS = "SubscribeAccountEvents"
    UNSUBSCRIBE_ACCOUNT_EVENTS = "UnSubscribeAccountEvents"
    SUBSCRIBE_ORDER_STATE_EVENTS = "SubscribeOrderStateEvents"
    UNSUBSCRIBE_ORDER_STATE_EVENTS = "UnSubscribeOrderStateEvents"

    WEB_AUTHENTICATE_USER = "WebAuthenticateUser"
    ACCOUNT_EVENT_TRANSACTION = "TransactionEvent"
    ACCOUNT_EVENT_WITHDRAW_TICKET_UPDATE = "WithdrawTicketUpdateEvent"
    ACCOUNT_EVENT_ACCOUNT_POSITION = "AccountPositionEvent"
    ACCOUNT_EVENT_ORDER_TRADE = "OrderTradeEvent"
    ACCOUNT_EVENT_ORDER_STATE = "OrderStateEvent"
    ACCOUNT_EVENT_DEPOSIT_TICKET_UPDATE = "DepositTicketUpdateEvent"
    ACCOUNT_EVENT_ACCOUNT_INFO_UPDATE = "AccountInfoUpdateEvent"
    ACCOUNT_EVENT_CANCEL_ORDER_REJECT = "CancelOrderRejectEvent"
    ACCOUNT_EVENT_DEPOSIT = "DepositEvent"
    UPDATE_TICKER = "TickerDataUpdateEvent"
    SUBSCRIBE_LEVEL_1 = "SubscribeLevel1"
    UPDATE_LEVEL_1 = "Level1UpdateEvent"
    SUBSCRIBE_LEVEL_2 = "SubscribeLevel2"
    UPDATE_LEVEL_2 = "Level2UpdateEvent"
