import requests
from requests.auth import HTTPBasicAuth
import pandas
from census import Census
from us import states

#api key to access data using us census api (acs5)
apikey = "d8fa9f7c0841efecfb91b98bf8cbe056cf654cec"

#url to access
request_url = "http://citysdk.commerce.gov"

#function to fetch share of households with income >150k in Silicon Valley (San Mateo & santa Clara county
def sm_sc_income(year):
    c = Census("d8fa9f7c0841efecfb91b98bf8cbe056cf654cec")

    # household with income >150K and <200k in san mateo county
    san_mateo1 = c.acs5.state_county('B19001_016E', states.CA.fips, '081', year=year)
    # household with income >200k in san mateo county
    san_mateo2 = c.acs5.state_county('B19001_017E', states.CA.fips, '081', year=year)
    # households with income San Mateo
    san_mateo_pop = c.acs5.state_county('B19051_002E', states.CA.fips, '081', year=year)

    # household with income >150K and <200k in santa clara county
    santa_clara1 = c.acs5.state_county('B19001_016E', states.CA.fips, '085', year=year)
    # household with income >200k in santa clara county
    santa_clara2 = c.acs5.state_county('B19001_017E', states.CA.fips, '085', year=year)
    # households with income Santa clara
    santa_clara_pop = c.acs5.state_county('B19051_002E', states.CA.fips, '085', year=year)
    # share of households with income >150K in San Mateo & Santa clara
    sm_tot = sum(int(item['B19001_016E']) for item in san_mateo1) + \
             sum(int(item['B19001_017E']) for item in san_mateo2)
    sc_tot = sum(int(item['B19001_016E']) for item in santa_clara1) + \
             sum(int(item['B19001_017E']) for item in santa_clara2)
    s_tot_pop = sum(int(item['B19051_002E']) for item in san_mateo_pop) + \
                sum(int(item['B19051_002E']) for item in santa_clara_pop)
    s_ratio = ((sm_tot + sc_tot) / s_tot_pop * 100)
    s_ratio = round(s_ratio, 1)

    return s_ratio

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
    data_gotten = response.json()
    print (data_gotten)
    types = data_gotten['type']
    features = data_gotten['features']
    totals = data_gotten['totals']
    panda_data = pandas.DataFrame(features)

    """
    pandas takes series data meaning a big array of stuffs not dicts so need
    to get array of data then stick into pandas for parsing i guesst 
    """

# if __name__ == "__main__":
#     main()

