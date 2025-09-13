from growwapi import GrowwAPI

SEGMENT = {
    'cash': GrowwAPI.SEGMENT_CASH,
    'commodity': GrowwAPI.SEGMENT_COMMODITY,
    'currency': GrowwAPI.SEGMENT_CURRENCY,
    'fno': GrowwAPI.SEGMENT_FNO,
}
VALIDITY = {
    'day', GrowwAPI.VALIDITY_DAY,
    'eos', GrowwAPI.VALIDITY_EOS,
    'gtc', GrowwAPI.VALIDITY_GTC,
    'gtd', GrowwAPI.VALIDITY_GTD,
    'ioc', GrowwAPI.VALIDITY_IOC,
}
EXCHANGE = {
    'nse': GrowwAPI.EXCHANGE_NSE,
    'ncdex': GrowwAPI.EXCHANGE_NCDEX,
    'bse': GrowwAPI.EXCHANGE_BSE,
    'mcx': GrowwAPI.EXCHANGE_MCX,
    'mcxsx': GrowwAPI.EXCHANGE_MCXSX,
    'us': GrowwAPI.EXCHANGE_US,
}
PRODUCT = {
    'arbitrage': GrowwAPI.PRODUCT_ARBITRAGE,
    'bo': GrowwAPI.PRODUCT_BO,
    'cnc': GrowwAPI.PRODUCT_CNC,
    'co': GrowwAPI.PRODUCT_CO,
    'mis': GrowwAPI.PRODUCT_MIS,
    'mtf': GrowwAPI.PRODUCT_MTF,
    'nrml': GrowwAPI.PRODUCT_NRML,
}
ORDER = {
    'limit', GrowwAPI.ORDER_TYPE_LIMIT,
    'market', GrowwAPI.ORDER_TYPE_MARKET,
    'stop_loss', GrowwAPI.ORDER_TYPE_STOP_LOSS,
    'stop_loss_market', GrowwAPI.ORDER_TYPE_STOP_LOSS_MARKET,
}
TRANSACTION = {
    'buy', GrowwAPI.TRANSACTION_TYPE_BUY,
    'sell', GrowwAPI.TRANSACTION_TYPE_SELL,
}