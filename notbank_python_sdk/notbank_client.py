from decimal import Decimal
from typing import Any, Callable, List, Optional, Type, TypeVar, Dict
from uuid import UUID
import simplejson as json
from notbank_python_sdk.client_connection import ClientConnection, RequestType
from notbank_python_sdk.core.endpoint_category import EndpointCategory
from notbank_python_sdk.core.endpoints import Endpoints, WebSocketEndpoint
from notbank_python_sdk.core.converter import from_json_str, to_dict, from_dict, to_nb_dict
from notbank_python_sdk.error import ErrorCode, NotbankException
from notbank_python_sdk.models.cbu_owner import CbuOwner
from notbank_python_sdk.models.account_fee import AccountFee
from notbank_python_sdk.models.authenticate_response import AuthenticateResponse
from notbank_python_sdk.models.bank import Banks
from notbank_python_sdk.models.address import Address
from notbank_python_sdk.models.bank_account import BankAccount, BankAccounts
from notbank_python_sdk.models.cancel_order_reject_event import CancelOrderRejectEvent
from notbank_python_sdk.models.cancel_replace_order_request import CancelReplaceOrderResponse
from notbank_python_sdk.models.deposit_event import DepositEvent
from notbank_python_sdk.models.oms_fee import OmsFee
from notbank_python_sdk.models.id_response import IdResponse
from notbank_python_sdk.models.document import Document
from notbank_python_sdk.models.document_slice import DocumentSlice
from notbank_python_sdk.models.enums import EnumsResponse
from notbank_python_sdk.models.activity_report import ActivityReport
from notbank_python_sdk.models.account_trade import AccountTrade
from notbank_python_sdk.models.quote import Quote
from notbank_python_sdk.models.transaction import Transactions
from notbank_python_sdk.models.url_response import UrlResponse
from notbank_python_sdk.models.uuid_response import UuidResponse
from notbank_python_sdk.models.withdraw_tickets import WithdrawTicket
from notbank_python_sdk.models.deposit_ticket import DepositTicket
from notbank_python_sdk.models.instrument import Instrument
from notbank_python_sdk.models.level2_ticker_snapshot import Level2TickerSnapshot
from notbank_python_sdk.models.public_trade import PublicTrade, public_trade_list_from_json_str
from notbank_python_sdk.models.level1_ticker_summary import Level1TickerSummary
from notbank_python_sdk.models.level1_ticker_summary_min import Level1TickerSummaryMin, level1_ticker_summary_min_list_from_json_list_str
from notbank_python_sdk.models.order_fee import OrderFee
from notbank_python_sdk.models.ticker import Ticker, ticker_list_from_json_str
from notbank_python_sdk.models.user_info import UserInfo
from notbank_python_sdk.models.user_report_tickets import UserReportTicket
from notbank_python_sdk.models.report_writer_result_records import ReportWriterResultRecords
from notbank_python_sdk.models.order import Order
from notbank_python_sdk.models.ticker import Ticker
from notbank_python_sdk.models.fee import Fee
from notbank_python_sdk.models.level1_ticker import Level1
from notbank_python_sdk.models.level2_ticker_feed import Level2Feed, level_2_ticker_feed_list_from_json_str
from notbank_python_sdk.models.order_book import OrderBook, OrderBookRaw, order_book_from_raw
from notbank_python_sdk.models.pong import Pong
from notbank_python_sdk.models.send_order import SendOrderResponse
from notbank_python_sdk.models.currency_network_templates import CurrencyNetworkTemplates
from notbank_python_sdk.models.instrument_summary import InstrumentSummary
from notbank_python_sdk.models.ticker_summary import TickerSummary
from notbank_python_sdk.models.trade_summary import TradeSummary
from notbank_python_sdk.models.user_devices import UserDevice
from notbank_python_sdk.models.verification_level_config import InstrumentVerificationLevelConfig, ProductVerificationLevelConfig
from notbank_python_sdk.models.web_authenticate_user import WebAuthenticateUser
from notbank_python_sdk.models.account_transaction import AccountTransaction
from notbank_python_sdk.models.account_positions import AccountPosition
from notbank_python_sdk.models.instrument_statistic import InstrumentStatistic
from notbank_python_sdk.models.account_info import AccountInfo
from notbank_python_sdk.models.subaccount import Subaccount, Subaccounts
from notbank_python_sdk.models.product import Product
from notbank_python_sdk.models.withdrawal_id_response import WithdrawalIdResponse
from notbank_python_sdk.parsing import build_subscription_handler, parse_response_fn, parse_response_list_fn, parse_report_response_fn
from notbank_python_sdk.requests_models.add_whitelisted_address_request import AddWhitelistedAddressRequest
from notbank_python_sdk.requests_models.authenticate_request import AuthenticateRequest
from notbank_python_sdk.requests_models.cancel_all_orders import CancelAllOrdersRequest
from notbank_python_sdk.requests_models.cancel_order import CancelOrder
from notbank_python_sdk.requests_models.cancel_order_request import CancelOrderRequest
from notbank_python_sdk.requests_models.cancel_replace_order_request import CancelReplaceOrderRequest
from notbank_python_sdk.requests_models.cancel_user_report import CancelUserReportRequest
from notbank_python_sdk.requests_models.confirm_fiat_withdraw_request import ConfirmFiatWithdrawRequest, ConfirmFiatWithdrawRequestInternal
from notbank_python_sdk.requests_models.confirm_whitelisted_address_request import ConfirmWhiteListedAddressRequest, ConfirmWhiteListedAddressRequestInternal
from notbank_python_sdk.requests_models.create_subaccount_request import CreateSubaccountRequest
from notbank_python_sdk.requests_models.create_direct_quote_request import CreateDirectQuoteRequest
from notbank_python_sdk.requests_models.create_fiat_deposit_request import CreateFiatDepositRequest
from notbank_python_sdk.requests_models.create_fiat_withdraw_request import CreateFiatWithdrawRequest
from notbank_python_sdk.requests_models.create_inverse_quote_request import CreateInverseQuoteRequest
from notbank_python_sdk.requests_models.delete_whitelisted_address_request import DeleteWhiteListedAddressRequest, DeleteWhiteListedAddressRequestInternal
from notbank_python_sdk.requests_models.delete_client_bank_account_request import DeleteClientBankAccountRequest
from notbank_python_sdk.requests_models.download_document import DownloadDocumentRequest
from notbank_python_sdk.requests_models.download_document_slice import DownloadDocumentSliceRequest
from notbank_python_sdk.requests_models.execute_quote_request import ExecuteQuoteRequest
from notbank_python_sdk.requests_models.generate_pnl_activity_report import GeneratePnlActivityReportRequest
from notbank_python_sdk.requests_models.generate_product_delta_activity_report import GenerateProductDeltaActivityReportRequest
from notbank_python_sdk.requests_models.generate_trade_activity_report import GenerateTradeActivityReportRequest
from notbank_python_sdk.requests_models.generate_transaction_activity_report import GenerateTransactionActivityReportRequest
from notbank_python_sdk.requests_models.get_account_trades import GetAccountTradesRequest
from notbank_python_sdk.requests_models.fee_request import FeeRequest
from notbank_python_sdk.requests_models.add_client_bank_account_request import AddClientBankAccountRequest
from notbank_python_sdk.requests_models.get_client_bank_account_request import GetClientBankAccountRequest
from notbank_python_sdk.requests_models.get_client_bank_accounts_request import GetClientBankAccountsRequest
from notbank_python_sdk.requests_models.get_banks_request import GetBanksRequest
from notbank_python_sdk.requests_models.deposit_address_request import DepositAddressRequest
from notbank_python_sdk.requests_models.get_instrument_request import GetInstrumentRequest
from notbank_python_sdk.requests_models.get_network_templates_request import GetNetworksTemplatesRequest
from notbank_python_sdk.requests_models.get_owners_fiat_withdraw import GetOwnersFiatWithdrawRequest
from notbank_python_sdk.requests_models.get_quote_request import GetQuoteRequest
from notbank_python_sdk.requests_models.get_quotes_request import GetQuotesRequest
from notbank_python_sdk.requests_models.get_transactions_request import GetTransactionsRequest
from notbank_python_sdk.requests_models.resend_verification_code_whitelisted_address_request import ResendVerificationCodeWhitelistedAddressRequest, ResendVerificationCodeWhitelistedAddressInternal
from notbank_python_sdk.requests_models.transfer_funds_request import TransferFundsRequest
from notbank_python_sdk.requests_models.update_one_step_withdraw_request import UpdateOneStepWithdrawRequest
from notbank_python_sdk.requests_models.verification_level_config_request import VerificationLevelConfigRequest
from notbank_python_sdk.requests_models.get_instruments_request import GetInstrumentsRequest
from notbank_python_sdk.requests_models.get_l2_snapshot import GetL2SnapshotRequest
from notbank_python_sdk.requests_models.get_last_trades import GetLastTradesRequest
from notbank_python_sdk.requests_models.get_level1_summary import GetLevel1SummaryRequest
from notbank_python_sdk.requests_models.get_level1_summary_min import GetLevel1SummaryMinRequest, GetLevel1SummaryMinRequestInternal
from notbank_python_sdk.requests_models.get_open_orders import GetOpenOrdersRequest
from notbank_python_sdk.requests_models.get_open_trade_reports import GetOpenTradeReportsRequest
from notbank_python_sdk.requests_models.get_order_fee_request import GetOrderFeeRequest
from notbank_python_sdk.requests_models.get_order_history import GetOrderHistoryRequest
from notbank_python_sdk.requests_models.get_order_history_by_order_id import GetOrderHistoryByOrderIdRequest
from notbank_python_sdk.requests_models.get_order_status import GetOrderStatusRequest
from notbank_python_sdk.requests_models.get_orders import GetOrdersRequest
from notbank_python_sdk.requests_models.get_subaccounts_request import GetSubaccountsRequest
from notbank_python_sdk.requests_models.get_orders_history import GetOrdersHistoryRequest
from notbank_python_sdk.requests_models.get_ticker_history import GetTickerHistoryRequest
from notbank_python_sdk.requests_models.get_trades_history import GetTradesHistoryRequest
from notbank_python_sdk.requests_models.create_crypto_withdraw_request import CreateCryptoWithdrawRequest
from notbank_python_sdk.requests_models.get_user_info import GetUserInfoRequest
from notbank_python_sdk.requests_models.get_user_permissions import GetUserPermissionsRequest
from notbank_python_sdk.requests_models.get_user_report_tickets import GetUserReportTicketsRequest
from notbank_python_sdk.requests_models.get_user_report_tickets_by_status import GetUserReportTicketsByStatusRequest, convert_to_get_user_report_tickets_by_status_request_internal
from notbank_python_sdk.requests_models.get_user_report_writer_result_records import GetUserReportWriterResultRecordsRequest
from notbank_python_sdk.requests_models.level1 import GetLevel1Request
from notbank_python_sdk.requests_models.modify_order import ModifyOrderRequest
from notbank_python_sdk.requests_models.order_book import OrderBookRequest
from notbank_python_sdk.requests_models.get_whitelisted_addresses_request import GetWhitelistedAddressesRequest
from notbank_python_sdk.requests_models.remove_user_report_ticket import RemoveUserReportTicketRequest
from notbank_python_sdk.requests_models.schedule_product_delta_activity_report import ScheduleProductDeltaActivityReportRequest
from notbank_python_sdk.requests_models.schedule_profit_and_loss_activity_report import ScheduleProfitAndLossActivityReportRequest
from notbank_python_sdk.requests_models.schedule_trade_activity_report import ScheduleTradeActivityReportRequest
from notbank_python_sdk.requests_models.schedule_transaction_activity_report import ScheduleTransactionActivityReportRequest
from notbank_python_sdk.requests_models.subscribe_account_events_request import SubscribeAccountEventsRequest
from notbank_python_sdk.requests_models.subscribe_level1_request import SubscribeLevel1Request
from notbank_python_sdk.requests_models.subscribe_level2_request import SubscribeLevel2Request
from notbank_python_sdk.requests_models.subscribe_order_state_events_request import SubscribeOrderStateEventsRequest
from notbank_python_sdk.requests_models.subscribe_ticker_request import SubscribeTickerRequest
from notbank_python_sdk.requests_models.subscribe_trades_request import SubscribeTradesRequest
from notbank_python_sdk.requests_models.unsubscribe_account_events_request import UnsubscribeAccountEventsRequest
from notbank_python_sdk.requests_models.unsubscribe_level1_request import UnsubscribeLevel1Request
from notbank_python_sdk.requests_models.unsubscribe_level2_request import UnsubscribeLevel2Request
from notbank_python_sdk.requests_models.unsubscribe_order_state_events_request import UnsubscribeOrderStateEventsRequest
from notbank_python_sdk.requests_models.unsubscribe_ticker_request import UnsubscribeTickerRequest
from notbank_python_sdk.requests_models.unsubscribe_trades_request import UnsubscribeTradesRequest
from notbank_python_sdk.requests_models.send_order import SendOrderRequest, SendOrderRequestInternal
from notbank_python_sdk.requests_models.trades import TradesRequest
from notbank_python_sdk.requests_models.user_accounts import GetUserAccountsRequest
from notbank_python_sdk.requests_models.user_devices import GetUserDevicesRequest
from notbank_python_sdk.requests_models.account_fees_request import AccountFeesRequest
from notbank_python_sdk.requests_models.oms_fees_request import OmsFeesRequest
from notbank_python_sdk.requests_models.web_authenticate_user_request import WebAuthenticateUserRequest
from notbank_python_sdk.requests_models.get_account_transactions_request import GetAccountTransactionsRequest
from notbank_python_sdk.requests_models.get_account_positions_request import GetAccountPositionsRequest
from notbank_python_sdk.requests_models.get_account_instrument_statistics_request import GetAccountInstrumentStatisticsRequest
from notbank_python_sdk.requests_models.get_account_info_request import GetAccountInfoRequest
from notbank_python_sdk.requests_models.get_product_request import GetProductRequest
from notbank_python_sdk.requests_models.get_products_request import GetProductsRequest
from notbank_python_sdk.notbank_client_cache import NotbankClientCache
from notbank_python_sdk.websocket.callback_identifier import CallbackIdentifier
from notbank_python_sdk.websocket.subscription import Subscription, Unsubscription
from notbank_python_sdk.websocket.subscription_handler import Callback


T1 = TypeVar('T1')
T2 = TypeVar('T2')


class NotbankClient:
    _client_connection: ClientConnection
    _notbank_client_cache: NotbankClientCache

    def __init__(self, client_connection: ClientConnection):
        self._client_connection = client_connection
        self._notbank_client_cache = NotbankClientCache()

    def _get_ap_data_list(self, endpoint: str, request_data: Any, response_cls: Type[T2], no_pascal_case: List[str] = [], overrides: Dict[str, str] = {}) -> List[T2]:
        request_data_dict = to_dict(request_data)
        return self._client_connection.request(
            endpoint,
            EndpointCategory.AP,
            request_data_dict,
            parse_response_list_fn(response_cls, no_pascal_case, overrides=overrides))

    def _get_nb_data_list(self, endpoint: str, request_data: Any, response_cls: Type[T2], no_pascal_case: List[str] = []) -> List[T2]:
        request_data_dict = to_nb_dict(request_data)
        return self._client_connection.request(
            endpoint,
            EndpointCategory.NB,
            request_data_dict,
            parse_response_list_fn(response_cls, no_pascal_case, from_pascal_case=False))

    def _get_data(self, endpoint: str, request_data: Any, response_cls: Type[T2], no_pascal_case: List[str] = [], response_conversion_overrides: Dict[str, str] = {}, endpoint_category: EndpointCategory = EndpointCategory.AP) -> T2:
        request_data_dict = to_dict(request_data)
        return self._client_connection.request(
            endpoint, endpoint_category, request_data_dict, parse_response_fn(response_cls, no_pascal_case, overrides=response_conversion_overrides))

    def _get_report_data(self, endpoint: str, request_data: Any, response_cls: Type[T2], no_pascal_case: List[str] = [], response_conversion_overrides: Dict[str, str] = {}, endpoint_category: EndpointCategory = EndpointCategory.AP) -> T2:
        request_data_dict = to_dict(request_data)
        return self._client_connection.request(
            endpoint, endpoint_category, request_data_dict, parse_report_response_fn(response_cls, no_pascal_case, overrides=response_conversion_overrides))

    def _get_nb_data(self, endpoint: str, request_data: Any, response_cls: Type[T2], no_pascal_case: List[str] = [], endpoint_category: EndpointCategory = EndpointCategory.NB) -> T2:
        request_data_dict = to_nb_dict(request_data)
        return self._client_connection.request(
            endpoint, endpoint_category, request_data_dict, parse_response_fn(response_cls, no_pascal_case, from_pascal_case=False))

    def _do_request(self, endpoint: str, request_data: Any, endpoint_category: EndpointCategory = EndpointCategory.AP) -> None:
        request_data_dict = to_dict(request_data)
        return self._client_connection.request(endpoint, endpoint_category, request_data_dict, lambda x: None)

    def _subscribe(self, endpoint: str, request_data: Any, callbacks: List[Callback], parse_response_fn: Callable[[Any], T2]) -> T2:
        request_data_dict = to_dict(request_data)
        return self._client_connection.subscribe(Subscription(endpoint, request_data_dict, callbacks, parse_response_fn))

    def _unsubscribe(self, endpoint: str, request_data: Any, callbacks_ids: List[str], parse_response_fn: Callable[[Any], T2]) -> T2:
        request_data_dict = to_dict(request_data)
        return self._client_connection.unsubscribe(Unsubscription(endpoint, request_data_dict, callbacks_ids, parse_response_fn))

    def close(self):
        return self._client_connection.close()

    def authenticate(self, authenticate_request: AuthenticateRequest) -> AuthenticateResponse:
        """https://apidoc.notbank.exchange/#authenticate"""
        return self._client_connection.authenticate(authenticate_request)

    def get_oms_deposit_fees(self, deposit_fees_request: OmsFeesRequest) -> List[OmsFee]:
        """
        https://apidoc.notbank.exchange/#getomsdepositfees
        """
        return self._get_ap_data_list(Endpoints.GET_OMS_DEPOSIT_FEES, deposit_fees_request, OmsFee)

    def get_oms_withdraw_fees(self, request: OmsFeesRequest) -> List[OmsFee]:
        """
        https://apidoc.notbank.exchange/#getomswithdrawfees
        """
        return self._get_ap_data_list(
            Endpoints.GET_OMS_WITHDRAW_FEES,
            request,
            OmsFee
        )

    def get_account_fees(self, account_fees_request: AccountFeesRequest) -> List[AccountFee]:
        """
        https://apidoc.notbank.exchange/#getaccountfees
        """
        return self._get_ap_data_list(Endpoints.GET_ACCOUNT_FEES, account_fees_request, AccountFee)

    def web_authenticate_user(self, web_authenticate_user_request: WebAuthenticateUserRequest) -> WebAuthenticateUser:
        """
        https://apidoc.notbank.exchange/#webauthenticateuser
        """
        return self._get_data(Endpoints.WEB_AUTHENTICATE_USER, web_authenticate_user_request, WebAuthenticateUser)

    def get_account_transactions(
        self, request: GetAccountTransactionsRequest
    ) -> List[AccountTransaction]:
        """
        https://apidoc.notbank.exchange/#getaccounttransactions
        """
        return self._get_ap_data_list(Endpoints.GET_ACCOUNT_TRANSACTIONS, request, AccountTransaction)

    def get_account_positions(self, request: GetAccountPositionsRequest) -> List[AccountPosition]:
        """
        https://apidoc.notbank.exchange/#getaccountpositions
        """
        return self._get_ap_data_list(
            Endpoints.GET_ACCOUNT_POSITIONS,
            request,
            AccountPosition
        )

    def get_account_instrument_statistics(
        self,
        request: GetAccountInstrumentStatisticsRequest
    ) -> List[InstrumentStatistic]:
        """
        https://apidoc.notbank.exchange/#getaccountinstrumentstatistics
        """
        return self._get_ap_data_list(
            Endpoints.GET_ACCOUNT_INSTRUMENT_STATISTICS,
            request,
            InstrumentStatistic
        )

    def get_account_info(self, request: GetAccountInfoRequest) -> AccountInfo:
        """
        https://apidoc.notbank.exchange/#getaccountinfo
        """
        return self._get_data(
            Endpoints.GET_ACCOUNT_INFO,
            request,
            AccountInfo,
            response_conversion_overrides={"oms_id": "OMSID"}
        )

    def logout(self) -> None:
        """
        https://apidoc.notbank.exchange/#logout
        """
        return self._do_request(
            Endpoints.LOGOUT,
            None,  # No se requiere payload en la solicitud.
        )

    def get_withdraw_fee(
        self,
        request: FeeRequest,
    ) -> Fee:
        """
        https://apidoc.notbank.exchange/#getwithdrawfee
        """
        return self._get_data(
            Endpoints.GET_WITHDRAW_FEE,
            request,
            Fee,
        )

    def get_deposit_fee(
        self,
        request: FeeRequest,
    ) -> Fee:
        """
        https://apidoc.notbank.exchange/#getdepositfee
        """
        return self._get_data(
            Endpoints.GET_DEPOSIT_FEE,
            request,
            Fee,
        )

    def get_product(
        self,
        request: GetProductRequest,
    ) -> Product:
        """
        https://apidoc.notbank.exchange/#product
        """
        return self._get_data(
            Endpoints.GET_PRODUCT,
            request,
            Product,
        )

    def get_products(
        self,
        request: GetProductsRequest = GetProductsRequest(),
    ) -> List[Product]:
        """
        https://apidoc.notbank.exchange/#getproducts
        """
        return self._get_ap_data_list(
            Endpoints.GET_PRODUCTS,
            request,
            Product,
        )

    def get_product_by_symbol(self, symbol: str) -> Product:
        product = self._notbank_client_cache.get_product(symbol)
        if product is not None:
            return product
        products = self.get_products()
        self._notbank_client_cache.update_products(products)
        product = self._notbank_client_cache.get_product(symbol)
        if product is not None:
            return product
        raise NotbankException(
            ErrorCode.RESOURCE_NOT_FOUND,
            "no instrument found for symbol: {}".format(symbol))

    def get_product_id_by_symbol(self, symbol: str) -> int:
        return self.get_product_by_symbol(symbol).product_id

    def get_verification_level_config(
        self,
        request: VerificationLevelConfigRequest,
    ) -> ProductVerificationLevelConfig:
        """
        https://apidoc.notbank.exchange/#getverificationlevelconfig
        """
        return self._get_data(
            Endpoints.GET_VERIFICATION_LEVEL_CONFIG,
            request,
            ProductVerificationLevelConfig,
        )

    def get_instrument(
        self,
        request: GetInstrumentRequest,
    ) -> Instrument:
        """
        https://apidoc.notbank.exchange/#getinstrument
        """
        return self._get_data(
            Endpoints.GET_INSTRUMENT,
            request,
            Instrument,
        )

    def get_instruments(
        self,
        request: GetInstrumentsRequest,
    ) -> List[Instrument]:
        """
        https://apidoc.notbank.exchange/#getinstruments
        """
        return self._get_ap_data_list(
            Endpoints.GET_INSTRUMENTS,
            request,
            Instrument,
        )

    def get_instrument_by_symbol(self, symbol: str) -> Instrument:
        instrument = self._notbank_client_cache.get_instrument(symbol)
        if instrument is not None:
            return instrument
        instruments = self.get_instruments(GetInstrumentsRequest())
        self._notbank_client_cache.update_instruments(instruments)
        instrument = self._notbank_client_cache.get_instrument(symbol)
        if instrument is not None:
            return instrument
        raise NotbankException(
            ErrorCode.RESOURCE_NOT_FOUND,
            "no instrument found for symbol: {}".format(symbol))

    def get_instrument_id_by_symbol(
        self,
        symbol: str
    ) -> int:
        return self.get_instrument_by_symbol(symbol).instrument_id

    def get_instrument_verification_level_config(
        self,
        request: VerificationLevelConfigRequest,
    ) -> InstrumentVerificationLevelConfig:
        """
        https://apidoc.notbank.exchange/#getinstrumentverificationlevelconfig
        """
        return self._get_data(
            Endpoints.GET_INSTRUMENT_VERIFICATION_LEVEL_CONFIG,
            request,
            InstrumentVerificationLevelConfig,
        )

    def get_order_fee(
        self,
        request: GetOrderFeeRequest,
    ) -> OrderFee:
        """
        https://apidoc.notbank.exchange/#getorderfee
        """
        return self._get_data(
            Endpoints.GET_ORDER_FEE,
            request,
            OrderFee,
        )

    def ping(self) -> Pong:
        """
        https://apidoc.notbank.exchange/#ping
        """
        return self._get_data(Endpoints.PING, None, Pong, no_pascal_case=["msg"])

    def health_check(self) -> None:
        """
        https://apidoc.notbank.exchange/#healthcheck
        """
        return self._do_request(Endpoints.HEALTH_CHECK, None)

    def send_order_list(
        self,
        request: List[SendOrderRequest],
    ) -> None:
        """
        https://apidoc.notbank.exchange/#sendorderlist
        """
        internal_request = list(
            map(SendOrderRequestInternal.from_send_order_request, request)
        )
        return self._do_request(
            Endpoints.SEND_ORDER_LIST,
            internal_request
        )

    def send_cancel_list(self, request: List[CancelOrder]) -> None:
        """
        https://apidoc.notbank.exchange/#sendcancellist
        """
        return self._do_request(Endpoints.SEND_CANCEL_LIST, request)

    def send_cancel_replace_list(self, request: List[CancelReplaceOrderRequest]) -> None:
        """
        https://apidoc.notbank.exchange/#sendcancelreplacelist
        """
        return self._do_request(Endpoints.SEND_CANCEL_REPLACE_LIST, request)

    def modify_order(self, request: ModifyOrderRequest) -> None:
        """
        https://apidoc.notbank.exchange/#modifyorder
        """
        return self._do_request(Endpoints.MODIFY_ORDER, request)

    def cancel_all_orders(self, request: CancelAllOrdersRequest) -> None:
        """
        https://apidoc.notbank.exchange/#cancelallorders
        """
        return self._do_request(Endpoints.CANCEL_ALL_ORDERS, request)

    def get_order_status(self, request: GetOrderStatusRequest) -> Order:
        """
        https://apidoc.notbank.exchange/#getorderstatus
        """
        return self._get_data(Endpoints.GET_ORDER_STATUS, request, Order)

    def get_orders_history(self, request: GetOrdersHistoryRequest) -> List[Order]:
        """
        https://apidoc.notbank.exchange/#getordershistory
        """
        return self._get_ap_data_list(Endpoints.GET_ORDERS_HISTORY, request, Order)

    def get_trades_history(
        self,
        request: GetTradesHistoryRequest,
    ) -> List[TradeSummary]:
        """
        https://apidoc.notbank.exchange/#gettradeshistory
        """
        return self._get_ap_data_list(
            Endpoints.GET_TRADES_HISTORY,
            request,
            TradeSummary,
        )

    def get_order_history_by_order_id(
        self,
        request: GetOrderHistoryByOrderIdRequest,
    ) -> List[Order]:
        """
        https://apidoc.notbank.exchange/#getorderhistorybyorderid
        """
        return self._get_ap_data_list(
            Endpoints.GET_ORDER_HISTORY_BY_ORDER_ID,
            request,
            Order,
        )

    def get_ticker_history(
        self,
        request: GetTickerHistoryRequest,
    ) -> List[Ticker]:
        """
        https://apidoc.notbank.exchange/#gettickerhistory
        """
        def parse_ticker_list(data: Any) -> List[Ticker]:
            return [Ticker(
                end_date_time=ticker_raw[0],
                high=Decimal(str(ticker_raw[1])),
                low=Decimal(str(ticker_raw[2])),
                open=Decimal(str(ticker_raw[3])),
                close=Decimal(str(ticker_raw[4])),
                volume=Decimal(str(ticker_raw[5])),
                bid=Decimal(str(ticker_raw[6])),
                ask=Decimal(str(ticker_raw[7])),
                instrument_id=ticker_raw[8],
                begin_date_time=ticker_raw[9]
            ) for ticker_raw in data]

        return self._client_connection.request(
            Endpoints.GET_TICKER_HISTORY,
            EndpointCategory.AP,
            to_dict(request),
            parse_ticker_list
        )

    def get_last_trades(
        self,
        request: GetLastTradesRequest,
    ) -> List[PublicTrade]:
        """
        https://apidoc.notbank.exchange/#getlasttrades
        """
        def parse_trade_list(data: Any) -> List[PublicTrade]:
            return [PublicTrade(
                trade_id=elem[0],
                instrument_id=elem[1],
                quantity=elem[2],
                price=elem[3],
                order1=elem[4],
                order2=elem[5],
                trade_time=elem[6],
                direction=elem[7],
                taker_side=elem[8],
                block_trade=elem[9],
                order_client_id=elem[10]
            ) for elem in data]
        return self._client_connection.request(
            Endpoints.GET_LAST_TRADES,
            EndpointCategory.AP,
            to_dict(request),
            parse_trade_list,
        )

    def get_level1_summary(
        self,
    ) -> List[Level1TickerSummary]:
        """
        https://apidoc.notbank.exchange/#getlevel1summary
        """
        result: List[str] = self._client_connection.request(
            Endpoints.GET_LEVEL1_SUMMARY,
            EndpointCategory.AP,
            to_dict(GetLevel1SummaryRequest()),
            parse_response_fn=lambda data: data,
        )
        return list(map(lambda data: from_dict(Level1TickerSummary, json.loads(data, use_decimal=True)), result))

    def get_level1_summary_min(
        self,
        request: GetLevel1SummaryMinRequest,
    ) -> List[Level1TickerSummaryMin]:
        """
        https://apidoc.notbank.exchange/#getlevel1summarymin
        """
        internal_request = GetLevel1SummaryMinRequestInternal(
            json.dumps(request.instrument_ids)
            if request.instrument_ids is not None
            else None)
        return self._client_connection.request(
            Endpoints.GET_LEVEL1_SUMMARY_MIN,
            EndpointCategory.AP,
            to_dict(internal_request),
            parse_response_fn=level1_ticker_summary_min_list_from_json_list_str,
        )

    def get_open_trade_reports(
        self,
        request: GetOpenTradeReportsRequest,
    ) -> List[Order]:
        """
        https://apidoc.notbank.exchange/#getopentradereports
        """
        return self._get_ap_data_list(
            Endpoints.GET_OPEN_TRADE_REPORTS,
            request,
            Order,
        )

    def get_orders(
        self,
        request: GetOrdersRequest,
    ) -> List[Order]:
        """
        https://apidoc.notbank.exchange/#getorders
        """
        return self._get_ap_data_list(
            Endpoints.GET_ORDERS,
            request,
            Order,
        )

    def get_order_history(
        self,
        request: GetOrderHistoryRequest,
    ) -> List[Order]:
        """
        https://apidoc.notbank.exchange/#getorderhistory
        """
        return self._get_ap_data_list(
            Endpoints.GET_ORDER_HISTORY,
            request,
            Order,
        )

    def send_order(
        self,
        request: SendOrderRequest,
    ) -> SendOrderResponse:
        """
        https://apidoc.notbank.exchange/#sendorder
        """
        internal_request = SendOrderRequestInternal.from_send_order_request(
            request
        )
        return self._get_data(
            endpoint=Endpoints.SEND_ORDER,
            request_data=internal_request,
            response_cls=SendOrderResponse,
            no_pascal_case=["status"]
        )

    def cancel_replace_order(
        self,
        request: CancelReplaceOrderRequest,
    ) -> CancelReplaceOrderResponse:
        """
        https://apidoc.notbank.exchange/#cancelreplaceorder
        """
        return self._get_data(
            Endpoints.CANCEL_REPLACE_ORDER,
            request,
            CancelReplaceOrderResponse,
        )

    def cancel_order(
        self,
        request: CancelOrderRequest,
    ) -> None:
        """
        https://apidoc.notbank.exchange/#cancelorder
        """
        return self._do_request(
            Endpoints.CANCEL_ORDER,
            request
        )

    def get_open_orders(self, request: GetOpenOrdersRequest) -> List[Order]:
        """
        https://apidoc.notbank.exchange/#getopenorders
        """
        return self._get_ap_data_list(Endpoints.GET_OPEN_ORDERS, request, Order)

    def get_account_trades(self, request: GetAccountTradesRequest) -> List[AccountTrade]:
        """
        https://apidoc.notbank.exchange/#getaccounttrades
        """
        return self._get_ap_data_list(Endpoints.GET_ACCOUNT_TRADES, request, AccountTrade)

    def get_summary(self) -> List[InstrumentSummary]:
        """
        https://apidoc.notbank.exchange/#summary
        """
        return self._get_ap_data_list(Endpoints.SUMMARY, None, InstrumentSummary)

    def get_ticker(self) -> Dict[str, TickerSummary]:
        """
        https://apidoc.notbank.exchange/#ticker
        """
        def response_fn(data): return {key: TickerSummary(
            **value) for key, value in data.items()}
        return self._client_connection.request(
            endpoint=Endpoints.TICKER,
            endpoint_category=EndpointCategory.AP,
            request_data=None,
            parse_response_fn=response_fn
        )

    def get_orderbook(self, request: OrderBookRequest) -> OrderBook:
        """
        https://apidoc.notbank.exchange/#orderbook
        """
        raw_orderbook = self._get_data(
            Endpoints.ORDER_BOOK, request, OrderBookRaw, no_pascal_case=["timestamp", "bids", "asks"])
        return order_book_from_raw(raw_orderbook)

    def get_order_book(self, request: OrderBookRequest) -> OrderBook:
        return self.get_orderbook(request)

    def get_trades(self, request: TradesRequest) -> List[TradeSummary]:
        """
        https://apidoc.notbank.exchange/#trades
        """
        return self._get_ap_data_list(Endpoints.TRADES, request, TradeSummary)

    def get_l2_snapshot(self, request: GetL2SnapshotRequest) -> List[Level2TickerSnapshot]:
        """
        https://apidoc.notbank.exchange/#getl2snapshot
        """
        def response_fn(data): return [Level2TickerSnapshot(
            md_update_id=item[0],
            number_of_unique_accounts=item[1],
            action_date_time=item[2],
            action_type=item[3],
            last_trade_price=item[4],
            number_of_orders=item[5],
            price=item[6],
            product_pair_code=item[7],
            quantity=item[8],
            side=item[9]
        ) for item in data]
        return self._client_connection.request(
            endpoint=Endpoints.GET_L2_SNAPSHOT,
            endpoint_category=EndpointCategory.AP,
            request_data=to_dict(request),
            parse_response_fn=response_fn
        )

    def get_level1(
        self,
        request: GetLevel1Request,
    ) -> Level1:
        """
        https://apidoc.notbank.exchange/#getlevel1
        """
        return self._get_data(
            Endpoints.GET_LEVEL1,
            request,
            Level1
        )

    def subscribe_level_1(
            self,
            request: SubscribeLevel1Request,
            snapshot_handler: Callable[[Level1], None],
            update_handler: Callable[[Level1], None]):
        """
        https://apidoc.notbank.exchange/#subscribelevel1
        """
        self._subscribe(
            WebSocketEndpoint.SUBSCRIBE_LEVEL1,
            request,
            [Callback(
                CallbackIdentifier.get(
                    WebSocketEndpoint.SUBSCRIBE_LEVEL1, request.instrument_id),
                build_subscription_handler(snapshot_handler, lambda json_str:from_json_str(Level1, json_str))),
             Callback(
                CallbackIdentifier.get(
                    WebSocketEndpoint.UPDATE_LEVEL_1, request.instrument_id),
                build_subscription_handler(update_handler, lambda json_str:from_json_str(Level1, json_str)))],
            lambda x: None)

    def subscribe_level_2(
        self,
        request: SubscribeLevel2Request,
            snapshot_handler: Callable[[List[Level2Feed]], None],
            update_handler: Callable[[List[Level2Feed]], None]):
        """
        https://apidoc.notbank.exchange/#subscribelevel2
        """
        instrument_id = None
        if request.instrument_id is not None:
            instrument_id = request.instrument_id
        if request.symbol is not None:
            instrument_id = self.get_instrument_id_by_symbol(request.symbol)
        self._subscribe(
            WebSocketEndpoint.SUBSCRIBE_LEVEL2,
            request,
            [Callback(
                CallbackIdentifier.get(
                    WebSocketEndpoint.SUBSCRIBE_LEVEL2, instrument_id),
                build_subscription_handler(snapshot_handler, lambda json_str:level_2_ticker_feed_list_from_json_str(json_str))),
             Callback(
                CallbackIdentifier.get(
                    WebSocketEndpoint.UPDATE_LEVEL_2, instrument_id),
                build_subscription_handler(update_handler, lambda json_str:level_2_ticker_feed_list_from_json_str(json_str)))],
            lambda x: None)

    def get_enums(self) -> List[EnumsResponse]:
        """
        https://apidoc.notbank.exchange/#getenums
        """
        return self._get_ap_data_list(
            Endpoints.GET_ENUMS,
            None,
            EnumsResponse
        )

    def get_user_accounts(self, request: GetUserAccountsRequest) -> List[int]:
        """
        https://apidoc.notbank.exchange/#getuseraccounts
        """
        def parse_response(data):
            return list(map(lambda account_id: int(account_id), data))

        return self._client_connection.request(
            Endpoints.GET_USER_ACCOUNTS,
            EndpointCategory.AP,
            to_dict(request),
            parse_response_fn=parse_response
        )

    def subscribe_ticker(
        self,
        request: SubscribeTickerRequest,
        snapshot_handler: Callable[[List[Ticker]], None],
        update_handler: Callable[[List[Ticker]], None]
    ):
        """
        https://apidoc.notbank.exchange/#subscribeticker
        """
        self._subscribe(
            WebSocketEndpoint.SUBSCRIBE_TICKER,
            request,
            [Callback(
                CallbackIdentifier.get(
                    WebSocketEndpoint.SUBSCRIBE_TICKER, request.instrument_id),
                build_subscription_handler(snapshot_handler, lambda json_str: ticker_list_from_json_str(json_str))),
             Callback(
                CallbackIdentifier.get(
                    WebSocketEndpoint.UPDATE_TICKER, request.instrument_id),
                build_subscription_handler(update_handler, lambda json_str: ticker_list_from_json_str(json_str)))],
            lambda x: None)

    def subscribe_trades(
            self,
            request: SubscribeTradesRequest,
            snapshot_handler: Callable[[List[PublicTrade]], None],
            update_handler: Callable[[List[PublicTrade]], None]):
        """
        https://apidoc.notbank.exchange/#subscribetrades
        """
        self._subscribe(
            WebSocketEndpoint.SUBSCRIBE_TRADES,
            request,
            [Callback(
                CallbackIdentifier.get(
                    WebSocketEndpoint.SUBSCRIBE_TRADES, request.instrument_id),
                build_subscription_handler(snapshot_handler, lambda json_str: public_trade_list_from_json_str(json_str))),
             Callback(
                CallbackIdentifier.get(
                    WebSocketEndpoint.UPDATE_TRADES, request.instrument_id),
                build_subscription_handler(update_handler, lambda json_str: public_trade_list_from_json_str(json_str)))],
            lambda x: None)

    def subscribe_order_state_events(
        self,
        request: SubscribeOrderStateEventsRequest,
        handler: Callable[[Order], None]
    ):
        """
        https://apidoc.notbank.exchange/#subscribeorderstateevents
        """
        if request.instrument_id is None:
            callback_id = CallbackIdentifier.get(
                WebSocketEndpoint.ACCOUNT_EVENT_ORDER_STATE, request.account_id)
        else:
            callback_id = CallbackIdentifier.get(
                WebSocketEndpoint.ACCOUNT_EVENT_ORDER_STATE, request.account_id, request.instrument_id)
        self._subscribe(
            WebSocketEndpoint.SUBSCRIBE_ORDER_STATE_EVENTS,
            request,
            [Callback(
                callback_id,
                build_subscription_handler(handler, lambda json_str: from_json_str(Order, json_str)))],
            lambda x: None)

    def subscribe_account_events(
            self,
            request: SubscribeAccountEventsRequest,
            withdraw_ticket_handler: Optional[Callable[[
                WithdrawTicket], None]] = None,
            transaction_handler: Optional[Callable[[
                AccountTransaction], None]] = None,
            trade_handler: Optional[Callable[[TradeSummary], None]] = None,
            order_handler: Optional[Callable[[Order], None]] = None,
            deposit_ticket_handler: Optional[Callable[[
                DepositTicket], None]] = None,
            account_handler: Optional[Callable[[AccountInfo], None]] = None,
            deposit_handler: Optional[Callable[[DepositEvent], None]] = None,
            cancel_order_reject_event_handler: Optional[Callable[[
                CancelOrderRejectEvent], None]] = None,
            account_position_handler: Optional[Callable[[
                AccountPosition], None]] = None,
    ):
        """
        https://apidoc.notbank.exchange/#subscribeaccountevents
        """
        callbacks: List[Callback] = []
        if withdraw_ticket_handler is not None:
            callback = Callback(
                CallbackIdentifier.get(
                    WebSocketEndpoint.ACCOUNT_EVENT_WITHDRAW_TICKET_UPDATE, request.account_id),
                build_subscription_handler(withdraw_ticket_handler, lambda json_str: from_json_str(WithdrawTicket, json_str)))
            callbacks.append(callback)
        if transaction_handler is not None:
            callback = Callback(
                CallbackIdentifier.get(
                    WebSocketEndpoint.ACCOUNT_EVENT_TRANSACTION, request.account_id),
                build_subscription_handler(transaction_handler, lambda json_str: from_json_str(AccountTransaction, json_str)))
            callbacks.append(callback)
        if trade_handler is not None:
            callback = Callback(
                CallbackIdentifier.get(
                    WebSocketEndpoint.ACCOUNT_EVENT_ORDER_TRADE, request.account_id),
                build_subscription_handler(trade_handler, lambda json_str: from_json_str(TradeSummary, json_str)))
            callbacks.append(callback)
        if order_handler is not None:
            callback = Callback(
                CallbackIdentifier.get(
                    WebSocketEndpoint.ACCOUNT_EVENT_ORDER_STATE, request.account_id),
                build_subscription_handler(order_handler, lambda json_str: from_json_str(Order, json_str)))
            callbacks.append(callback)
        if deposit_ticket_handler is not None:
            callback = Callback(
                CallbackIdentifier.get(
                    WebSocketEndpoint.ACCOUNT_EVENT_DEPOSIT_TICKET_UPDATE, request.account_id),
                build_subscription_handler(deposit_ticket_handler, lambda json_str: from_json_str(DepositTicket, json_str)))
            callbacks.append(callback)
        if account_handler is not None:
            callback = Callback(
                CallbackIdentifier.get(
                    WebSocketEndpoint.ACCOUNT_EVENT_ACCOUNT_INFO_UPDATE, request.account_id),
                build_subscription_handler(account_handler, lambda json_str: from_json_str(AccountInfo, json_str)))
            callbacks.append(callback)
        if deposit_handler is not None:
            callback = Callback(
                CallbackIdentifier.get(
                    WebSocketEndpoint.ACCOUNT_EVENT_DEPOSIT, request.account_id),
                build_subscription_handler(deposit_handler, lambda json_str: from_json_str(DepositEvent, json_str)))
            callbacks.append(callback)
        if cancel_order_reject_event_handler is not None:
            callback = Callback(
                CallbackIdentifier.get(
                    WebSocketEndpoint.ACCOUNT_EVENT_CANCEL_ORDER_REJECT, request.account_id),
                build_subscription_handler(cancel_order_reject_event_handler, lambda json_str: from_json_str(CancelOrderRejectEvent, json_str)))
            callbacks.append(callback)
        if account_position_handler is not None:
            callback = Callback(
                CallbackIdentifier.get(
                    WebSocketEndpoint.ACCOUNT_EVENT_ACCOUNT_POSITION, request.account_id),
                build_subscription_handler(account_position_handler, lambda json_str: from_json_str(AccountPosition, json_str)))
            callbacks.append(callback)
        self._subscribe(
            WebSocketEndpoint.SUBSCRIBE_ACCOUNT_EVENTS,
            request,
            callbacks,
            lambda x: None)

    def unsubscribe_level_1(self, request: UnsubscribeLevel1Request) -> None:
        """
        https://apidoc.notbank.exchange/#unsubscribelevel1
        """
        self._unsubscribe(WebSocketEndpoint.UNSUBSCRIBE_LEVEL1, request, [
            CallbackIdentifier.get(
                WebSocketEndpoint.SUBSCRIBE_LEVEL1, request.instrument_id),
            CallbackIdentifier.get(
                WebSocketEndpoint.UPDATE_LEVEL_1, request.instrument_id)
        ],
            lambda x: None)

    def unsubscribe_level_2(self, request: UnsubscribeLevel2Request) -> None:
        """
        https://apidoc.notbank.exchange/#unsubscribelevel2
        """
        self._unsubscribe(WebSocketEndpoint.UNSUBSCRIBE_LEVEL2, request, [
            CallbackIdentifier.get(
                WebSocketEndpoint.SUBSCRIBE_LEVEL2, request.instrument_id),
            CallbackIdentifier.get(
                WebSocketEndpoint.UPDATE_LEVEL_2, request.instrument_id)
        ],
            lambda x: None)

    def unsubscribe_ticker(self, request: UnsubscribeTickerRequest) -> None:
        """
        https://apidoc.notbank.exchange/#unsubscribeticker
        """
        self._unsubscribe(WebSocketEndpoint.UNSUBSCRIBE_TICKER, request, [
            CallbackIdentifier.get(
                WebSocketEndpoint.SUBSCRIBE_TICKER, request.instrument_id),
            CallbackIdentifier.get(
                WebSocketEndpoint.UPDATE_TICKER, request.instrument_id)
        ],
            lambda x: None)

    def unsubscribe_trades(self, request: UnsubscribeTradesRequest) -> None:
        """
        https://apidoc.notbank.exchange/#unsubscribetrades
        """
        self._unsubscribe(WebSocketEndpoint.UNSUBSCRIBE_TRADES, request, [
            CallbackIdentifier.get(
                WebSocketEndpoint.SUBSCRIBE_TRADES, request.instrument_id),
            CallbackIdentifier.get(
                WebSocketEndpoint.UPDATE_TRADES, request.instrument_id),
        ],
            lambda x: None)

    def unsubscribe_order_state_events(self, request: UnsubscribeOrderStateEventsRequest):
        """
        https://apidoc.notbank.exchange/#unsubscribeorderstateevents
        """
        if request.instrument_id is None:
            callback_id = CallbackIdentifier.get(
                WebSocketEndpoint.ACCOUNT_EVENT_ORDER_STATE, request.account_id)
        else:
            callback_id = CallbackIdentifier.get(
                WebSocketEndpoint.ACCOUNT_EVENT_ORDER_STATE, request.account_id, request.instrument_id)
        self._unsubscribe(
            WebSocketEndpoint.UNSUBSCRIBE_TICKER,
            request,
            [callback_id],
            lambda x: None)

    def unsubscribe_account_events(self, request: UnsubscribeAccountEventsRequest):
        """
        https://apidoc.notbank.exchange/#unsubscribeaccountevents
        """
        callback_ids: List[str] = [
            CallbackIdentifier.get(
                WebSocketEndpoint.ACCOUNT_EVENT_WITHDRAW_TICKET_UPDATE, request.account_id),
            CallbackIdentifier.get(
                WebSocketEndpoint.ACCOUNT_EVENT_TRANSACTION, request.account_id),
            CallbackIdentifier.get(
                WebSocketEndpoint.ACCOUNT_EVENT_ORDER_TRADE, request.account_id),
            CallbackIdentifier.get(
                WebSocketEndpoint.ACCOUNT_EVENT_ORDER_STATE, request.account_id),
            CallbackIdentifier.get(
                WebSocketEndpoint.ACCOUNT_EVENT_DEPOSIT_TICKET_UPDATE, request.account_id),
            CallbackIdentifier.get(
                WebSocketEndpoint.ACCOUNT_EVENT_ACCOUNT_INFO_UPDATE, request.account_id),
            CallbackIdentifier.get(
                WebSocketEndpoint.ACCOUNT_EVENT_DEPOSIT, request.account_id),
            CallbackIdentifier.get(
                WebSocketEndpoint.ACCOUNT_EVENT_CANCEL_ORDER_REJECT, request.account_id),
        ]
        self._unsubscribe(
            WebSocketEndpoint.UNSUBSCRIBE_ACCOUNT_EVENTS,
            request,
            callback_ids,
            lambda x: None)

    def get_user_devices(self, request: GetUserDevicesRequest) -> List[UserDevice]:
        """
        https://apidoc.notbank.exchange/#getuserdevices
        """
        return self._get_ap_data_list(
            Endpoints.GET_USER_DEVICES,
            request,
            UserDevice
        )

    def get_user_info(self, request: GetUserInfoRequest) -> UserInfo:
        """
        https://apidoc.notbank.exchange/#getuserinfo
        """
        return self._get_data(
            Endpoints.GET_USER_INFO,
            request,
            UserInfo
        )

    def generate_trade_activity_report(
        self, request: GenerateTradeActivityReportRequest
    ) -> ActivityReport:
        """
        https://apidoc.notbank.exchange/#generatetradeactivityreport
        """
        return self._get_report_data(
            Endpoints.GENERATE_TRADE_ACTIVITY_REPORT,
            request,
            ActivityReport,
            response_conversion_overrides={
                "report_flavor": "reportFlavor",
                "create_time": "createTime",
                "initial_run_time": "initialRunTime",
                "interval_start_time": "intervalStartTime",
                "interval_end_time": "intervalEndTime",
                "interval_duration": "intervalDuration",
                "last_instance_id": "lastInstanceId",
                "account_ids": "accountIds",
            }
        )

    def generate_transaction_activity_report(
        self, request: GenerateTransactionActivityReportRequest
    ) -> ActivityReport:
        """
        https://apidoc.notbank.exchange/#generatetransactionactivityreport
        """
        return self._get_report_data(
            Endpoints.GENERATE_TRANSACTION_ACTIVITY_REPORT,
            request,
            ActivityReport
        )

    def generate_product_delta_activity_report(
        self, request: GenerateProductDeltaActivityReportRequest
    ) -> ActivityReport:
        """
        https://apidoc.notbank.exchange/#generateproductdeltaactivityreport
        """
        return self._get_report_data(
            Endpoints.GENERATE_PRODUCT_DELTA_ACTIVITY_REPORT,
            request,
            ActivityReport
        )

    def generate_pnl_activity_report(
        self, request: GeneratePnlActivityReportRequest
    ) -> ActivityReport:
        """
        https://apidoc.notbank.exchange/#generatepnlactivityreport
        """
        return self._get_report_data(
            Endpoints.GENERATE_PNL_ACTIVITY_REPORT,
            request,
            ActivityReport,
        )

    def schedule_trade_activity_report(
        self, request: ScheduleTradeActivityReportRequest
    ) -> ActivityReport:
        """
        https://apidoc.notbank.exchange/#healthcheck
        """
        return self._get_report_data(
            Endpoints.SCHEDULE_TRADE_ACTIVITY_REPORT,
            request,
            ActivityReport
        )

    def schedule_transaction_activity_report(
        self, request: ScheduleTransactionActivityReportRequest
    ) -> ActivityReport:
        """
        http://apidoc.notbank.exchange/#scheduletransactionactivityreport
        """
        return self._get_report_data(
            Endpoints.SCHEDULE_TRANSACTION_ACTIVITY_REPORT,
            request,
            ActivityReport
        )

    def schedule_product_delta_activity_report(
        self, request: ScheduleProductDeltaActivityReportRequest
    ) -> ActivityReport:
        """
        https://apidoc.notbank.exchange/#scheduleproductdeltaactivityreport
        """
        return self._get_report_data(
            Endpoints.SCHEDULE_PRODUCT_DELTA_ACTIVITY_REPORT,
            request,
            ActivityReport
        )

    def schedule_profit_and_loss_activity_report(
        self, request: ScheduleProfitAndLossActivityReportRequest
    ) -> ActivityReport:
        """
        https://apidoc.notbank.exchange/#scheduleprofitandlossactivityreport
        """
        return self._get_report_data(
            Endpoints.SCHEDULE_PROFIT_AND_LOSS_ACTIVITY_REPORT,
            request,
            ActivityReport
        )

    def cancel_user_report(self, request: CancelUserReportRequest) -> None:
        """
        https://apidoc.notbank.exchange/#canceluserreport
        """
        return self._do_request(
            Endpoints.CANCEL_USER_REPORT,
            request,
        )

    def get_user_report_writer_result_records(
        self, request: GetUserReportWriterResultRecordsRequest
    ) -> List[ReportWriterResultRecords]:
        """
        https://apidoc.notbank.exchange/#getuserreportwriterresultrecords
        """
        return self._get_ap_data_list(
            Endpoints.GET_USER_REPORT_WRITER_RESULT_RECORDS,
            request,
            ReportWriterResultRecords,
            overrides={
                "urt_ticket_id": "urtTicketId",
                "descriptor_id": "descriptorId",
                "result_status": "resultStatus",
                "report_execution_start_time": "reportExecutionStartTime",
                "report_execution_complete_time": "reportExecutionCompleteTime",
                "report_output_file_pathname": "reportOutputFilePathname",
                "report_descriptive_header": "reportDescriptiveHeader",
            }
        )

    def get_user_report_tickets(self, request: GetUserReportTicketsRequest) -> List[UserReportTicket]:
        """
        https://apidoc.notbank.exchange/#getuserreporttickets
        """
        return self._get_ap_data_list(
            Endpoints.GET_USER_REPORT_TICKETS,
            request,
            UserReportTicket
        )

    def remove_user_report_ticket(self, request: RemoveUserReportTicketRequest) -> None:
        """
        https://apidoc.notbank.exchange/#removeuserreportticket
        """
        payload = "{" + request.user_report_ticket_id + "}"
        return self._client_connection.request(Endpoints.REMOVE_USER_REPORT_TICKET, EndpointCategory.AP, payload, lambda x: None)

    def get_user_report_tickets_by_status(self, request: GetUserReportTicketsByStatusRequest) -> List[UserReportTicket]:
        """
        https://apidoc.notbank.exchange/#getuserreportticketsbystatus
        """
        request_data = convert_to_get_user_report_tickets_by_status_request_internal(
            request)
        return self._client_connection.request(
            Endpoints.GET_USER_REPORT_TICKETS_BY_STATUS,
            EndpointCategory.AP,
            request_data,
            parse_response_list_fn(UserReportTicket))

    def download_document(self, request: DownloadDocumentRequest) -> Document:
        """
        https://apidoc.notbank.exchange/#downloaddocument
        """
        return self._get_report_data(
            Endpoints.DOWNLOAD_DOCUMENT,
            request,
            Document
        )

    def download_document_slice(self, request: DownloadDocumentSliceRequest) -> DocumentSlice:
        """
        https://apidoc.notbank.exchange/#downloaddocumentslice
        """
        return self._get_report_data(
            Endpoints.DOWNLOAD_DOCUMENT_SLICE,
            request,
            DocumentSlice
        )

    def get_user_permissions(self, request: GetUserPermissionsRequest) -> List[str]:
        """
        https://apidoc.notbank.exchange/#getuserpermissions
        """
        return self._client_connection.request(
            Endpoints.GET_USER_PERMISSIONS,
            EndpointCategory.AP,
            to_dict(request),
            parse_response_fn=lambda x: x
        )

    # wallet

    def get_banks(self, request: GetBanksRequest) -> Banks:
        """
        https://apidoc.notbank.exchange/?http#getbanks
        """
        return self._client_connection.request(
            endpoint=Endpoints.BANKS,
            endpoint_category=EndpointCategory.NB_PAGE,
            request_data=to_nb_dict(request),
            parse_response_fn=parse_response_fn(Banks, from_pascal_case=False),
            request_type=RequestType.GET
        )

    def add_client_bank_account(self, request: AddClientBankAccountRequest) -> BankAccount:
        """
        https://apidoc.notbank.exchange/#addclientbankaccount
        """
        return self._get_nb_data(
            Endpoints.BANK_ACCOUNTS,
            request,
            BankAccount,
            endpoint_category=EndpointCategory.NB,
        )

    def get_client_bank_account(self, request: GetClientBankAccountRequest) -> BankAccount:
        """
        https://apidoc.notbank.exchange/#getclientbankaccount
        """
        return self._client_connection.request(
            endpoint=Endpoints.BANK_ACCOUNTS +
            "/" + str(request.bank_account_id),
            endpoint_category=EndpointCategory.NB,
            request_data=None,
            parse_response_fn=parse_response_fn(
                BankAccount, from_pascal_case=False),
            request_type=RequestType.GET

        )

    def get_client_bank_accounts(self, request: GetClientBankAccountsRequest= GetClientBankAccountsRequest()) -> BankAccounts:
        """
        https://apidoc.notbank.exchange/#getclientbankaccounts
        """
        return self._client_connection.request(
            endpoint=Endpoints.BANK_ACCOUNTS,
            endpoint_category=EndpointCategory.NB_PAGE,
            request_data=to_nb_dict(request),
            parse_response_fn=parse_response_fn(
                BankAccounts, from_pascal_case=False),
            request_type=RequestType.GET
        )

    def delete_client_bank_account(self, request: DeleteClientBankAccountRequest) -> None:
        """
        https://apidoc.notbank.exchange/#deleteclientbankaccount
        """
        return self._client_connection.request(
            endpoint=Endpoints.BANK_ACCOUNTS +
            "/" + str(request.bank_account_id),
            endpoint_category=EndpointCategory.NB,
            request_data=None,
            parse_response_fn=lambda x: None,
            request_type=RequestType.DELETE
        )

    def get_networks_templates(self, request: GetNetworksTemplatesRequest) -> List[CurrencyNetworkTemplates]:
        """
        https://apidoc.notbank.exchange/?http#getnetworkstemplates
        """
        return self._client_connection.request(
            endpoint=Endpoints.GET_NETWORK_TEMPLATES,
            endpoint_category=EndpointCategory.NB,
            request_data=to_nb_dict(request),
            parse_response_fn=parse_response_list_fn(
                CurrencyNetworkTemplates, from_pascal_case=False),
            request_type=RequestType.GET
        )

    def get_deposit_addresses(self, request: DepositAddressRequest) -> List[str]:
        """
        https://apidoc.notbank.exchange/?http#getdepositaddresses
        """
        return self._client_connection.request(
            endpoint=Endpoints.GET_DEPOSIT_ADDRESSES,
            endpoint_category=EndpointCategory.NB,
            request_data=to_nb_dict(request),
            parse_response_fn=lambda x: x,
            request_type=RequestType.GET
        )

    def create_deposit_address(self, request: DepositAddressRequest) -> str:
        """
        https://apidoc.notbank.exchange/?http#createdepositaddress
        """
        return self._client_connection.request(
            endpoint=Endpoints.CREATE_DEPOSIT_ADDRESS,
            endpoint_category=EndpointCategory.NB,
            request_data=to_nb_dict(request),
            parse_response_fn=lambda x: x
        )

    def get_whitelisted_addresses(self, request: GetWhitelistedAddressesRequest) -> List[Address]:
        """
        https://apidoc.notbank.exchange/?http#getwhitelistedaddresses
        """
        return self._client_connection.request(
            endpoint=Endpoints.WHITELISTED_ADDRESSES,
            endpoint_category=EndpointCategory.NB,
            request_data=to_nb_dict(request),
            parse_response_fn=parse_response_list_fn(
                Address, from_pascal_case=False),
            request_type=RequestType.GET
        )

    def add_whitelisted_addresses(self, request: AddWhitelistedAddressRequest) -> UUID:
        """
        https://apidoc.notbank.exchange/?http#addwhitelistedaddress
        """
        return self._get_nb_data(
            Endpoints.WHITELISTED_ADDRESSES,
            request,
            IdResponse
        ).id

    def confirm_whitelisted_address(self, request: ConfirmWhiteListedAddressRequest) -> None:
        """
        https://apidoc.notbank.exchange/?http#confirmwhitelistedaddress
        """
        return self._client_connection.request(
            endpoint=Endpoints.WHITELISTED_ADDRESSES +
            "/" + str(request.whitelisted_address_id) + "/verification",
            endpoint_category=EndpointCategory.NB,
            request_data=to_nb_dict(ConfirmWhiteListedAddressRequestInternal(
                request.account_id, request.sms_code)),
            parse_response_fn=lambda x: None,
            request_type=RequestType.POST
        )

    def resend_verification_code_whitelisted_address(self, request: ResendVerificationCodeWhitelistedAddressRequest) -> None:
        """
        https://apidoc.notbank.exchange/#resendverificationcodewhitelistedaddress
        """
        return self._client_connection.request(
            endpoint=Endpoints.WHITELISTED_ADDRESSES +
            "/" + str(request.whitelisted_address_id) + "/verification",
            endpoint_category=EndpointCategory.NB,
            request_data=to_nb_dict(
                ResendVerificationCodeWhitelistedAddressInternal(request.account_id)),
            parse_response_fn=lambda x: None,
            request_type=RequestType.GET
        )

    def delete_whitelisted_address(self, request: DeleteWhiteListedAddressRequest) -> None:
        """
        https://apidoc.notbank.exchange/?http#deletewhitelistedaddress
        """
        return self._client_connection.request(
            endpoint=Endpoints.WHITELISTED_ADDRESSES +
            "/" + str(request.whitelisted_address_id),
            endpoint_category=EndpointCategory.NB,
            request_data=to_nb_dict(DeleteWhiteListedAddressRequestInternal(
                account_id=request.account_id, otp=request.otp)),
            parse_response_fn=lambda x: None,
            request_type=RequestType.DELETE
        )

    def update_one_step_withdraw(self, request: UpdateOneStepWithdrawRequest) -> None:
        """
        https://apidoc.notbank.exchange/?http#updateonestepwithdraw
        """
        return self._client_connection.request(
            endpoint=Endpoints.UPDATE_ONE_STEP_WITHDRAW,
            endpoint_category=EndpointCategory.NB,
            request_data=to_nb_dict(request),
            parse_response_fn=lambda x: None,
            request_type=RequestType.POST
        )

    def create_crypto_withdraw(self, request: CreateCryptoWithdrawRequest) -> UUID:
        """
        https://apidoc.notbank.exchange/?http#createcriptowithdraw
        """
        return self._client_connection.request(
            endpoint=Endpoints.CREATE_CRIPTO_WITHDRAW,
            endpoint_category=EndpointCategory.NB,
            request_data=to_nb_dict(request),
            parse_response_fn=lambda x: UUID(x),
            request_type=RequestType.POST
        )

    def create_fiat_deposit(self, request: CreateFiatDepositRequest) -> Optional[str]:
        """
        https://apidoc.notbank.exchange/#createfiatdeposit
        """
        return self._client_connection.request(
            endpoint=Endpoints.FIAT_DEPOSIT,
            endpoint_category=EndpointCategory.NB,
            request_data=to_nb_dict(request),
            parse_response_fn=parse_response_fn(
                UrlResponse, from_pascal_case=False),
            request_type=RequestType.POST
        ).url

    def get_owners_fiat_withdraw(self, request: GetOwnersFiatWithdrawRequest) -> List[CbuOwner]:
        """
        https://apidoc.notbank.exchange/#getownersfiatwithdraw
        """
        return self._client_connection.request(
            endpoint=Endpoints.GET_OWNERS_FIAT_WITHDRAW,
            endpoint_category=EndpointCategory.NB,
            request_data=to_nb_dict(request),
            parse_response_fn=parse_response_list_fn(
                CbuOwner, from_pascal_case=False),
            request_type=RequestType.GET
        )

    def create_fiat_withdraw(self, request: CreateFiatWithdrawRequest) -> Optional[str]:
        """
        https://apidoc.notbank.exchange/#getownersfiatwithdraw
        """
        return self._client_connection.request(
            endpoint=Endpoints.FIAT_WITHDRAW,
            endpoint_category=EndpointCategory.NB,
            request_data=to_nb_dict(request),
            parse_response_fn=parse_response_fn(
                WithdrawalIdResponse, from_pascal_case=False),
            request_type=RequestType.POST
        ).withdrawal_id

    def confirm_fiat_withdraw(self, request: ConfirmFiatWithdrawRequest) -> None:
        """
        https://apidoc.notbank.exchange/#confirmfiatwithdraw
        """
        return self._client_connection.request(
            endpoint=Endpoints.FIAT_WITHDRAW+"/"+str(request.withdrawal_id),
            endpoint_category=EndpointCategory.NB,
            request_data=to_nb_dict(
                ConfirmFiatWithdrawRequestInternal(request.attempt_code)),
            parse_response_fn=lambda x: None,
            request_type=RequestType.POST
        )

    def transfer_funds(self, request: TransferFundsRequest) -> UUID:
        """
        https://apidoc.notbank.exchange/#transferfunds
        """
        return self._client_connection.request(
            endpoint=Endpoints.TRANSFER_FUNDS,
            endpoint_category=EndpointCategory.NB,
            request_data=to_nb_dict(request),
            parse_response_fn=lambda x: UUID(x),
            request_type=RequestType.POST
        )

    def get_transactions(self, request: GetTransactionsRequest) -> Transactions:
        """
        https://apidoc.notbank.exchange/#gettransactions
        """
        return self._client_connection.request(
            endpoint=Endpoints.GET_TRANSACTIONS,
            endpoint_category=EndpointCategory.NB_PAGE,
            request_data=to_nb_dict(request),
            parse_response_fn=parse_response_fn(
                Transactions, from_pascal_case=False),
            request_type=RequestType.GET
        )

    def get_quotes(self, request: GetQuotesRequest) -> List[Quote]:
        """
        https://apidoc.notbank.exchange/#getquotes
        """
        return self._client_connection.request(
            endpoint=Endpoints.QUOTES,
            endpoint_category=EndpointCategory.NB,
            request_data=to_nb_dict(request),
            parse_response_fn=parse_response_list_fn(
                Quote, from_pascal_case=False),
            request_type=RequestType.GET
        )

    def create_direct_quote(self, request: CreateDirectQuoteRequest) -> UUID:
        """
        https://apidoc.notbank.exchange/#createdirectquote
        """
        return self._client_connection.request(
            endpoint=Endpoints.QUOTES_DIRECT,
            endpoint_category=EndpointCategory.NB,
            request_data=to_nb_dict(request),
            parse_response_fn=parse_response_fn(
                UuidResponse, from_pascal_case=False),
            request_type=RequestType.POST
        ).id

    def create_inverse_quote(self, request: CreateInverseQuoteRequest) -> UUID:
        """
        https://apidoc.notbank.exchange/#createinversequote
        """
        return self._client_connection.request(
            endpoint=Endpoints.QUOTES_INVERSE,
            endpoint_category=EndpointCategory.NB,
            request_data=to_nb_dict(request),
            parse_response_fn=parse_response_fn(
                UuidResponse, from_pascal_case=False),
            request_type=RequestType.POST
        ).id

    def get_quote(self, request: GetQuoteRequest) -> Quote:
        """
        https://apidoc.notbank.exchange/#getquote
        """
        return self._client_connection.request(
            endpoint=Endpoints.QUOTES+"/"+str(request.quote_id),
            endpoint_category=EndpointCategory.NB,
            request_data=None,
            parse_response_fn=parse_response_fn(
                Quote, from_pascal_case=False),
            request_type=RequestType.GET
        )

    def execute_quote(self, request: ExecuteQuoteRequest) -> Quote:
        """
        https://apidoc.notbank.exchange/#executequote
        """
        return self._client_connection.request(
            endpoint=Endpoints.QUOTES+"/"+str(request.quote_id),
            endpoint_category=EndpointCategory.NB,
            request_data=None,
            parse_response_fn=parse_response_fn(
                Quote, from_pascal_case=False),
            request_type=RequestType.POST
        )

    # subaccount

    def create_subaccount(self, request: CreateSubaccountRequest) -> None:
        """
        https://apidoc.notbank.exchange/#createsubaccount
        """
        return self._client_connection.request(
            endpoint=Endpoints.SUBACCOUNT,
            endpoint_category=EndpointCategory.NB,
            request_data=to_nb_dict(request),
            parse_response_fn=lambda x: None,
            request_type=RequestType.POST
        )

    def get_subaccounts(self, request: GetSubaccountsRequest = GetSubaccountsRequest()) -> Subaccounts:
        """
        https://apidoc.notbank.exchange/#getsubaccounts
        """
        return self._client_connection.request(
            endpoint=Endpoints.SUBACCOUNT,
            endpoint_category=EndpointCategory.NB,
            request_data=to_nb_dict(request),
            parse_response_fn=parse_response_fn(
                Subaccounts, from_pascal_case=False),
            request_type=RequestType.GET
        )
