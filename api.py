import requests
from requests.auth import HTTPBasicAuth
import pandas
from census import Census
from us import states
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np

plotly.tools.set_credentials_file(username='manika15', api_key='dogNq5ILvZnKd5BzKOry')

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

def sf_income(year):
    c = Census("d8fa9f7c0841efecfb91b98bf8cbe056cf654cec")

    # household with income >150K and <200k in san fransisco county
    san_fransisco1 = c.acs5.state_county('B19001_016E', states.CA.fips, '075', year=year)
    # household with income >200k in san fransisco county
    san_fransisco2 = c.acs5.state_county('B19001_017E', states.CA.fips, '075', year=year)
    # households with income San Fransisco
    # sf_pop = c.acs5.state_county('B01003_001E', states.CA.fips, '075', year=year)
    sf_pop = c.acs5.state_county('B19051_002E', states.CA.fips, '075', year=year)
    # share of households with income >150K in San Fransisco
    sf_tot = sum(int(item['B19001_016E']) for item in san_fransisco1) + \
             sum(int(item['B19001_017E']) for item in san_fransisco2)
    sf_tot_pop = sum(int(item['B19051_002E']) for item in sf_pop)
    sf_ratio = (sf_tot / sf_tot_pop * 100)
    sf_ratio = round(sf_ratio, 1)

    return sf_ratio

def cali_income(year):
    c = Census("d8fa9f7c0841efecfb91b98bf8cbe056cf654cec")

    # household with income >150K and <200k in California
    cali1 = c.acs5.state('B19001_016E', states.CA.fips, year=year)
    # household with income >200k in California
    cali2 = c.acs5.state('B19001_017E', states.CA.fips, year=year)
    # households with income California
    cali_pop = c.acs5.state('B19051_002E', states.CA.fips, year=year)
    # share of households with income >150K in California
    cali_tot = sum(int(item['B19001_016E']) for item in cali1) + \
               sum(int(item['B19001_017E']) for item in cali2)
    cali_tot_pop = sum(int(item['B19051_002E']) for item in cali_pop)
    cali_ratio = ((cali_tot) / cali_tot_pop * 100)
    cali_ratio = round(cali_ratio, 1)

    return cali_ratio

def us_income(year):
    c = Census("d8fa9f7c0841efecfb91b98bf8cbe056cf654cec")

    # household with income >150K and <200k in US
    us_tot1 = c.acs5.state('B19001_016E', Census.ALL, year=year)
    # household with income >200k in US
    us_tot2 = c.acs5.state('B19001_017E', Census.ALL, year=year)
    #households with income US
    us_pop = c.acs5.state('B19051_002E', Census.ALL, year=year)
    #share of households with income >150K in US
    us_tot= sum(int(item['B19001_016E']) for item in us_tot1) + \
            sum(int(item['B19001_017E']) for item in us_tot2)
    us_tot_pop = sum(int(item['B19051_002E']) for item in us_pop)
    us_ratio = (us_tot / us_tot_pop *100)

    return us_ratio

years = [2011, 2012, 2013, 2014, 2015]

#income for silicon valley from 2011 to 2015
income_silicon = [sm_sc_income(year) for year in years]

#income for San fransisco county from 2011 to 2015
income_sf = [sf_income(year)  for year in years]

#income for California from 2011 to 2015
income_cali = [cali_income(year)  for year in years]

#income for United States from 2011 to 2015
income_us = [us_income(year)  for year in years]

trace_silicon = go.Scatter(
    x = years,
    y = income_silicon,
    name = 'Silicon valley',
    line = dict(
        color = ('rgb(205, 12, 24)'),
        width = 4)
)

trace_sf = go.Scatter(
    x = years,
    y = income_sf,
    name = 'San Fransisco',
    line = dict(
        color = ('rgb(22, 96, 167)'),
        width = 4,
        dash='dash')
)

trace_cali = go.Scatter(
    x = years,
    y = income_cali,
    name = 'California',
    line = dict(
        color = ('rgb(205, 12, 24)'),
        width = 4,
        dash='dot')
)

trace_us = go.Scatter(
    x = years,
    y = income_us,
    name = 'United States',
    line = dict(
        color = ('rgb(22, 96, 167)'),
        width = 4)
)

data = [trace_silicon, trace_sf, trace_cali, trace_us]

layout = dict(title = 'Share of Households with Income >150k',
              xaxis = dict(title = 'year', tickmode= years, nticks=5),
              yaxis = dict(title = 'share of households', ticksuffix= '%'),
              width=1000,
              height=450,

              )

fig = dict(data=data, layout=layout)
py.plot(fig, filename='styled-line')

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

