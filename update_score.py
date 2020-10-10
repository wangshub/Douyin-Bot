from bs4 import BeautifulSoup
import requests
import time
import random

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Origin': 'http://g.17koko.com',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Referer': 'http://g.17koko.com/54mb6fe',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.5;q=0.4',
    'Cookie': '17koko_debug=eYNNfc0Kcw%2F1L8r2lTw97pmjlo43GXjoBe5drWDj7GXg7QHkAZf6qaf7oE2I72523BNJM8iFUj32MHN5EsMRnA%3D%3D; ci_session=97a2a5deecaaeedfc9634536978b6f04a46eff12; 17koko_player_token=Q5MK6k3s2U5ZdWYcqRyu7rLfuXcJjUEXO8ylSAuJcsFNIR16xS8lP9rM728xJZaYsg1kI5rK8cWCMnkLI1eMumpnnU83enVrAAJ0yX38ZDjaXPM434bhy01I9Ow05Wt3xPBpQaUvRzHy5SzPl8drjXLv6Svk8cpwjHb82biChhLq77It%2F6BvcSgqMQalT3JqDBjhbOfPT44atg6Jr8rxnc97hfcobNZZORQcjfDUnxhFOLTltZLHGMGl8dhF28pZ3YoEG80qiJ%2BikAwnoT%2Bwub%2FflWmO7ZmVC4Gir7tBGEkvOx847bbJ5hzUnMnBGx7lg%2BwP3tlKColH5rS9RYrujBOlsvSXugWwg58t9nM%2F7SDUYfycp8Am0tjZHXhL0%2BQ6yDrfz0NgQY6%2FHkDE1cxOZBImOc7RIA36zzgLV5Qz%2BP3rHmkq1fzfY4IKKnQITAwQZj9huvffMeu2VvqmQU90%2F0xHqVubMXnH1ieBD2z29Wn72Stdaf6%2BpxuIWU0lebmmHhnybjLoheWRlbErL%2Bnnx6BHa990Lexk6aaZx2ygFpaqhFjqbeCvK9cWZDvnhrtYX91YW0oDdt47TUbKHCwsZw%3D%3D; Hm_lvt_fac83900736474fa47a41cb70f23de3a=1601187033; Hm_lpvt_fac83900736474fa47a41cb70f23de3a=1601190979'
}

# cookies = {
#     'Cookie': '17koko_debug=eYNNfc0Kcw%2F1L8r2lTw97pmjlo43GXjoBe5drWDj7GXg7QHkAZf6qaf7oE2I72523BNJM8iFUj32MHN5EsMRnA%3D%3D; ci_session=948c41c4de38fba1ba7ff235061d296c09fbe0a8; 17koko_player_token=bL%2B%2FkVDJdpmNKKXxG%2Ful%2BdAiIvOZ0HvikpJPHUAP4URCaApCX5bNxzVdHsDsbEi7gDW3Ldu06yJDFxDxJW4tNTDo7Y7qdMctqpOrDCMZRt5Hkq19vJshIVt3sgl%2FbbjYGDrXZFoqF82oKYOoiG9es%2B39fBbcLGBTtH%2FiVbjvA1DRggk7Vqj%2BMezBNJNIqckHtpQZaQYwHAx%2FQn7fdKcynvOT37jeqbZmOQCg9ukC2I%2FM%2B8%2BLUHVCSon5saWiPXOBvizxj03oUufOdwDdt5NPDuEJOGhoL5zqjYjiU%2BIhsRfKKOFeNG4GKPPA%2FOMplGv3hG%2B9pBOFopFVeKvzMAuY4fLMugAXD8EeZpWRT0BHn8ugb9xyiMZui3dluEdleMfApiUk6P6RkU5mLlbbicwxnvexmHI%2FTCKUA6wMNQpCIaSfL9tA2BnKH1KjZ%2BQ6mBCbnBmn1yfavh0N6YhumYKyzPQC3BJkLTrt%2BIguZaQHQkznb3KMd4%2FzwhD90KUDifg79E22S05WJNKcLorL17rbjsydr3%2BA6No0Qp%2BgQA6qzdc1vnQ5SQdZ7GWm3RHDi3Ag6B7bXJ1cLBXgOmtYADZS6A%3D%3D; Hm_lvt_fac83900736474fa47a41cb70f23de3a=1601187033; Hm_lpvt_fac83900736474fa47a41cb70f23de3a=1601190073'
# }

update_score_url = 'http://g.17koko.com/game/update_score'
analytics_url = 'http://g.17koko.com/game/analytics?s=426fb28466b5708c0a9f25d56b69fcc1&token=60052ecd8a15231ccd1ecf04b88b58a6&q=68gr6N%3D%3D'
coupon_url = 'http://g.17koko.com/game/get_coupon_url'

s = requests.Session()

try:
    score_payload = {
        'token': '60052ecd8a15231ccd1ecf04b88b58a6',
        'id': 1438107,
        'score': 6000
    }

    analytics_payload = {
        's': '426fb28466b5708c0a9f25d56b69fcc1',
        'token': '60052ecd8a15231ccd1ecf04b88b58a6',
        'q': '68126N=='
    }

    coupon_payload = {
        'current_score': 6000,
        'game_id': 46846
    }

    # 提交数据：
    score_response = s.post(update_score_url, data=score_payload, headers=headers)
    print(score_response.text)

    analytics_response = s.get(analytics_url, data=analytics_payload, headers=headers)
    print(analytics_response.text)

    coupon_response = s.post(coupon_url, data=coupon_payload, headers=headers)
    print(coupon_response.text)
except Exception as e:
    print(e)

