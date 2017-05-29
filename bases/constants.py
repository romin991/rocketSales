class ContactConstant(object):

    OFFLINE_ADS = 'OFA'
    ONLINE_ADS = 'ONA'
    COLD_CALL = 'CC'
    INTERNAL_REFERRAL = 'IR'
    EXTERNAL_REFERRAL = 'ER'
    PARTNER = 'P'
    SALES = 'S'
    TRADE_SHOW = 'TS'
    SEMINAR = 'SR'

    LEAD_SOURCE = (
        (OFFLINE_ADS, 'OfflineAds'),
        (ONLINE_ADS, 'OnlineAds'),
        (INTERNAL_REFERRAL, 'InternalReferral'),
        (EXTERNAL_REFERRAL, 'ExternalReferral'),
        (PARTNER, 'Partner'),
        (SALES, 'Sales'),
        (TRADE_SHOW, 'TradeShow'),
        (SEMINAR, 'Seminar'),
    )