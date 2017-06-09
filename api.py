import requests
from requests.auth import HTTPBasicAuth

apikey = "d8fa9f7c0841efecfb91b98bf8cbe056cf654cec"
request_url = "http://citysdk.commerce.gov"


def main():
    request_obj = {
        'zip': '21401',
        'state': 'MD',
        'level': 'state',
        'sublevel': False,
        'api': 'acs5',
        'year': 2010,
        'variables': ['income', 'population']
    }
    response = requests.post(request_url, auth=HTTPBasicAuth(apikey, None), json=request_obj)

    print(response.json())


if __name__ == "__main__":
    main()
