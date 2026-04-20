from enum import Enum, IntEnum


class MakerTaker(str, Enum):
    UNKNOWN = "Unknown"
    MAKER = "Maker"
    TAKER = "Taker"


class TimeInForce(IntEnum):
    GTC = 1
    OPG = 2
    IOC = 3
    FOK = 4
    GTX = 5
    GTD = 6


class Side(IntEnum):
    BUY = 0
    SELL = 1
    SHORT = 2
    UNKNOWN = 3


class OrderType(IntEnum):
    MARKET = 1
    LIMIT = 2
    STOP_MARKET = 3
    STOP_LIMIT = 4
    TRAILING_STOP_MARKET = 5
    TRAILING_STOP_LIMIT = 6
    BLOCK_TRADE = 7


class PegPriceType(IntEnum):
    LAST = 1
    BID = 2
    ASK = 3


class InstrumentState(str, Enum):
    BOTH = "Both"
    INACTIVE = "Inactive"


class ReportFrequency(str, Enum):
    ON_DEMAND = "onDemand"
    HOURLY = "Hourly"
    DAILY = "Daily"
    WEEKLY = "Weekly"
    MONTHLY = "Monthly"
    ANNUALLY = "Annually"


class ReportResultStatus(str, Enum):
    NOT_STARTED = "NotStarted"
    NOT_COMPLETE = "NotComplete"
    ERROR_COMPLETE = "ErrorComplete"
    SUCCESS_COMPLETE = "SuccessComplete"
    CANCELLED = "Cancelled"


class ReportRequestStatus(str, Enum):
    SUBMITTED = "Submitted"
    VALIDATING = "Validating"
    SCHEDULED = "Scheduled"
    IN_PROGRESS = "InProgress"
    COMPLETED = "Completed"
    ABORTING = "Aborting"
    ABORTED = "Aborted"
    USER_CANCELLED = "UserCancelled"
    SYS_RETIRED = "SysRetired"
    USER_CANCELLED_PENDING = "UserCancelledPending"


class BankAccountKind(str, Enum):
    CORRIENTE = "corriente"
    VISTA = "vista"
    AHORRO = "ahorro"
    ELECTRONIC_CHECKBOOK = "electronic_checkbook"
    AR_CBU = "ar_cbu"
    AR_CVU = "ar_cvu"
    AR_ALIAS = "ar_alias "
    BR_CORRIENTE_FISICA = "br_corriente_fisica"
    BR_SIMPLE_FISICA = "br_simple_fisica"
    BR_CORRIENTE_JURIDICA = "br_corriente_juridica"
    BR_POUPANCA_FISICA = "br_poupanca_fisica"
    BR_POUPANCA_JURIDICA = "br_poupanca_juridica"
    BR_CAIXA_FACIL = "br_caixa_facil"
    BR_PIX = "br_pix"


class PixType(str, Enum):
    CPF = "CPF"
    CNPJ = "CNPJ"
    EMAIL = "Email"
    PHONE = "Phone"
    OTRO = "Otro"


class UpdateOneStepWithdrawAction(str, Enum):
    ENABLE = "enable"
    DISABLE = "disable"


class DepositPaymentMethod(IntEnum):
    BANK_TRANSFER = 1
    WEB_PAY = 2
    VIRTUAL_WALLET = 3
    QR_CODE = 4
    ASSISTED_BANK_TRANSFER = 5
    CREDIT_OR_DEBIT_CARD = 6
    CASH_OR_CARD = 7


class YieldType(IntEnum):
    VARIABLE = 1


class YieldTypeStr(str, Enum):
    VARIABLE = "variable"


class WithdrawPaymentMethod(IntEnum):
    BANK_TRANSFER = 1
    VIRTUAL_WALLET = 3
    QR_CODE = 4
    ASSISTED_BANK_TRANSFER = 5
    CREDIT_OR_DEBIT_CARD = 6
    CASH_OR_CARD = 7


class QuoteMode(str, Enum):
    DIRECT = "direct"
    INVERSE = "inverse"


class QuoteOperation(IntEnum):
    BUY = 1
    SELL = 2
    CONVERSION = 3


class WalletTransactionType(IntEnum):
    OTHER = 0
    DEPOSIT = 1
    WITHDRAW = 2
    TRANSFER = 3
    TRADE = 4
    PAYMENT = 5
    RECTIFICATION = 6
    FEE = 7
    REVERSE = 8
    HOLD = 9
    MARGIN = 10
    AIRDROP = 11
    DISTRIBUTION = 12
    MIGRATION = 13


class WalletTransactionSubType(IntEnum):
    OTHER = 0
    PAYOUT = 1
    PAYIN = 2
    DEPOSIT = 3
    WITHDRAW = 4
    BANK_TO_EXCHANGE = 5
    EXCHANGE_TO_BANK = 6
    TRADE = 7
    PAYMENT = 8
    SIMPLE = 9
    RECTIFICATION = 10
    TRANSFER = 11
    HOLD = 12
    MARGIN = 13
    AIRDROP = 14
    ORDER = 15
    DISTRIBUTION_ENTRY = 16
    MIGRATION = 17
    MANUAL_ENTRY = 18
