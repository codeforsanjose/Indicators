import requests
from requests.auth import HTTPBasicAuth
import pandas
from census import Census
from us import states
from income_builder import IncomeBuilder
from population_handler import PopulationHandler
from trace_generator import TraceGenerator
from layout_generator import LayoutGenerator

#api key to access data using us census api (acs5)
apikey = "d8fa9f7c0841efecfb91b98bf8cbe056cf654cec"

#url to access
request_url = "http://citysdk.commerce.gov"

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

    return us_tot_pop

def income_150k_plot():
    income_cali = [cali_income(year) for year in years]
    # households with income >150k in United States
    income_us = [us_income(year) for year in years]

    population_cali = [cali_population(year) for year in years]
    # households with income in United States
    population_us = [us_population(year) for year in years]

    # share of households with income greater than 150k in California state
    ratio_cali = share(income_cali, population_cali)
    # share of households with income greater than 150k in United states
    ratio_us = share(income_us, population_us)

def main():
    county_ids = dict(
        san_mateo='081',
        santa_clara='085',
        san_fransisco='075'
    )
    years = [2011, 2012, 2013, 2014, 2015]

    income_handler = IncomeBuilder()
    population_handler = PopulationHandler()

    ratio_sv = []
    ratio_sf = []
    ratio_ca = []
    ration_us = []

    for year in years:
        san_mateo_income_total = income_handler.get_total_from_county(county_ids['san_mateo'], year)
        santa_clara_total = income_handler.get_total_from_county(county_ids['santa_clara'], year)
        san_mateo_population = population_handler.get_population('B19051_002E', county_ids['san_mateo'], year)
        santa_clara_population = population_handler.get_population('B19051_002E', county_ids['santa_clara'], year)

        income_total_silicon_valley = san_mateo_income_total + santa_clara_total
        population_total_silicon_valley = san_mateo_population + santa_clara_population

        ratio = (income_total_silicon_valley / population_total_silicon_valley * 100)
        rounded_ratio_sv = round(ratio, 1)
        ratio_sv.append(rounded_ratio_sv)

        income_total_sf = income_handler.get_total_from_county(county_ids['san_fransisco'], year)
        population_total_sf = population_handler.get_population('B19051_002E', county_ids['san_fransisco'], year)

        ratio = (income_total_sf / population_total_sf * 100)
        rounded_ratio_sf = round(ratio, 1)
        ratio_sf.append(rounded_ratio_sf)

    # print(ratio_sv)
    # print(ratio_sf)
    traces = []
    trace_handler = TraceGenerator()
    trace_sv = trace_handler.get_trace(ratio_sv, years, 'Silicon Valley', 'rgb(205, 12, 24)')
    trace_sf = trace_handler.get_trace(ratio_sf, years, 'San Fransisco', 'rgb(22, 96, 167)')
    traces.append(trace_sv)
    traces.append(trace_sf)

    layout_handler = LayoutGenerator()
    layout_handler.get_layout(traces, years)

if __name__ == "__main__":
    main()


# color codes: 'rgb(205, 12, 24)', 'rgb(22, 96, 167)'