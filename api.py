import requests
from requests.auth import HTTPBasicAuth
import pandas
from census import Census
from us import states
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np

#api key to access data using us census api (acs5)
apikey = "d8fa9f7c0841efecfb91b98bf8cbe056cf654cec"

#url to access
request_url = "http://citysdk.commerce.gov"
c = Census("d8fa9f7c0841efecfb91b98bf8cbe056cf654cec")

years = [2011, 2012, 2013, 2014, 2015]

#function to find no. of households with income >150k in any county in California
def county_income(year, fips):
    # household with income >150K and <200k in a county in California
    income1 = c.acs5.state_county('B19001_016E', states.CA.fips, fips, year=year)
    income150 = sum(int(item['B19001_016E']) for item in income1)
    # household with income >200k in a county in California
    income2 = c.acs5.state_county('B19001_017E', states.CA.fips, fips, year=year)
    income200 = sum(int(item['B19001_017E']) for item in income2)

    total = income150 + income200
    return total

#function to find no. of households with income in any county in California
def county_households(year, fips):
    # households with income in a county in California
    county_hh = c.acs5.state_county('B19051_002E', states.CA.fips, fips, year=year)
    county_households = sum(int(item['B19051_002E']) for item in county_hh)

    return county_households

#function to find no. of households with income >150k in California
def cali_income(year):
    # household with income >150K and <200k in California
    cali1 = c.acs5.state('B19001_016E', states.CA.fips, year=year)
    # household with income >200k in California
    cali2 = c.acs5.state('B19001_017E', states.CA.fips, year=year)
    # share of households with income >150K in California
    cali_tot = sum(int(item['B19001_016E']) for item in cali1) + \
               sum(int(item['B19001_017E']) for item in cali2)
    return cali_tot

#function to find no. of households with income in California
def cali_population(year):
    # households with income California
    cali_pop = c.acs5.state('B19051_002E', states.CA.fips, year=year)
    cali_tot_pop = sum(int(item['B19051_002E']) for item in cali_pop)
    return cali_tot_pop

#function to find no. of households with income >150k in United States
def us_income(year):
    # household with income >150K and <200k in US
    us_tot1 = c.acs5.state('B19001_016E', Census.ALL, year=year)
    # household with income >200k in US
    us_tot2 = c.acs5.state('B19001_017E', Census.ALL, year=year)
    #share of households with income >150K in US
    us_tot= sum(int(item['B19001_016E']) for item in us_tot1) + \
            sum(int(item['B19001_017E']) for item in us_tot2)
    return us_tot

#function to find no. of households with income in United states
def us_population(year):
    # households with income US
    us_pop = c.acs5.state('B19051_002E', Census.ALL, year=year)
    us_tot_pop = sum(int(item['B19051_002E']) for item in us_pop)
    return us_tot_pop

#function to calculate share of households with income >150k
def share(income, population):
    ratio = [round(a/b*100,1) for a,b in zip(income, population)]
    return ratio

#households with income >150k in San Mateo county California
sm = [county_income(year, '081') for year in years]
#households with income >150k in Santa Clara county California
sc = [county_income(year, '085') for year in years]
#households with income >150k in Silicon Valley (San Mateo + Santa Clara) California
income_silicon = [a+b for a,b in zip(sm, sc)]
#households with income >150k in San Fransisco county California
income_sf = [county_income(year, '075') for year in years]
#households with income >150k in California state
income_cali = [cali_income(year) for year in years]
#households with income >150k in United States
income_us = [us_income(year) for year in years]

#households with income in San Mateo county California
smp = [county_households(year, '081') for year in years]
#households with income in Santa Clara county California
scp = [county_households(year, '085') for year in years]
#households with income in Silicon Valley (San Mateo + Santa Clara) California
population_silicon = [a+b for a,b in zip(smp, scp)]
#households with income in San Fransisco county California
population_sf = [county_households(year, '075') for year in years]
#households with income in California state
population_cali = [cali_population(year) for year in years]
#households with income in United States
population_us = [us_population(year) for year in years]

#share of households with income greater than 150k in Silicon valley
ratio_silicon = share(income_silicon, population_silicon)
#share of households with income greater than 150k in San Fransisco
ratio_sf = share(income_sf, population_sf)
#share of households with income greater than 150k in California state
ratio_cali = share(income_cali, population_cali)
#share of households with income greater than 150k in United states
ratio_us = share(income_us, population_us)

#ploting the Income graphs for Silicon valley, San Fransisco, California and United states
trace_silicon = go.Scatter(
    x = years,
    y = ratio_silicon,
    name = 'Silicon valley',
    line = dict(
        color = ('rgb(205, 12, 24)'),
        width = 4)
)

trace_sf = go.Scatter(
    x = years,
    y = ratio_sf,
    name = 'San Fransisco',
    line = dict(
        color = ('rgb(22, 96, 167)'),
        width = 4,
        dash='dash')
)

trace_cali = go.Scatter(
    x = years,
    y = ratio_cali,
    name = 'California',
    line = dict(
        color = ('rgb(205, 12, 24)'),
        width = 4,
        dash='dot')
)

trace_us = go.Scatter(
    x = years,
    y = ratio_us,
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

