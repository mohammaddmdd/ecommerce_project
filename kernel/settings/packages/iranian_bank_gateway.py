from decouple import config

AZ_IRANIAN_BANK_GATEWAYS = {
    'GATEWAYS': {
        'IDPAY': {
            'MERCHANT_CODE': config('ID_PAY_MERCHANT_CODE', cast=str),
            'METHOD': 'POST',  # GET or POST
            'X_SANDBOX': 1,  # 0 disable, 1 active
        },
    },
    'IS_SAMPLE_FORM_ENABLE': True,  # optional
    'DEFAULT': 'IDPAY',
    'CURRENCY': 'IRR',  # optional
    'TRACKING_CODE_QUERY_PARAM': 'tn',  # optional
    'TRACKING_CODE_LENGTH': 16,  # optional
    'SETTING_VALUE_READER_CLASS': 'azbankgateways.readers.DefaultReader',  # optional
    'BANK_PRIORITIES': [],
}
