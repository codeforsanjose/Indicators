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
        san_mateo_population = population_handler.get_population(county_ids['san_mateo'], year)
        santa_clara_population = population_handler.get_population(county_ids['santa_clara'], year)

        income_total_silicon_valley = san_mateo_income_total + santa_clara_total
        population_total_silicon_valley = san_mateo_population + santa_clara_population

        ratio = (income_total_silicon_valley / population_total_silicon_valley * 100)
        rounded_ratio_sv = round(ratio, 1)
        ratio_sv.append(rounded_ratio_sv)

        income_total_sf = income_handler.get_total_from_county(county_ids['san_fransisco'], year)
        population_total_sf = population_handler.get_population(county_ids['san_fransisco'], year)

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
