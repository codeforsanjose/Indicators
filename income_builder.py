from census import Census
from us import states


class IncomeBuilder():
    def __init__(self):
        self.locations = []
        self.census = Census("d8fa9f7c0841efecfb91b98bf8cbe056cf654cec")
        self.income_range_ids = ['B19001_016E', 'B19001_017E']

    def make_api_call_with_income_range_id(self, income_range_id, county_id, year):
        data = self.census.acs5.state_county(income_range_id, states.CA.fips, county_id, year=year)
        return data[0]

    def get_total_from_county(self, county_id, year):
        #data = [self.census.acs5.state_county(income, states.CA.fips, county_id, year=year) for income in self.income_range_ids]
        data = [self.make_api_call_with_income_range_id(income_range, county_id, year) for income_range in self.income_range_ids]
        total = 0.0
        for data in data:
            key = list(data.keys())[0]
            value_needed = int(data[key])
            total += value_needed

        return total


class CensusAPI():
    def __init__(self):
        if self.census is None:
            self.census = Census("d8fa9f7c0841efecfb91b98bf8cbe056cf654cec")

    def call_API(self, indicator_id, county_id, year):
        return self.census.acs5.state_county(indicator_id, states.CA.fips, county_id, year=year)         




