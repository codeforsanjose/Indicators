from census import Census
from us import states

from census_api_handler import CensusAPI

class IncomeBuilder():
    def __init__(self):
        self.census_api = CensusAPI()
        self.income_range_ids = ['B19001_016E', 'B19001_017E']

    def make_api_call_with_income_range_id(self, income_range_id, county_id, year):
        data = self.census_api.call_API(income_range_id, county_id, year)
        return data[0]

    def make_api_call_with_income_range_id_state(self, income_range_id, year):
        data = self.census_api.call_API_state(income_range_id, year)
        return data[0]

    def make_api_call_with_income_range_id_us(self, income_range_id, year):
        data = self.census_api.call_API_us(income_range_id, year)
        return data[0]

    def get_total_from_county(self, county_id, year):
        data = [self.make_api_call_with_income_range_id(income_range, county_id, year) for income_range in self.income_range_ids]
        total = 0.0
        for data in data:
            key = list(data.keys())[0]
            value_needed = int(data[key])
            total += value_needed

        return total

    def get_total_from_state(self, year):
        data = [self.make_api_call_with_income_range_id_state(income_range, year) for income_range in self.income_range_ids]
        total = 0.0
        for data in data:
            key = list(data.keys())[0]
            value_needed = int(data[key])
            total += value_needed

        return total

    def get_total_from_us(self, year):
        data = [self.make_api_call_with_income_range_id_us(income_range, year) for income_range in
                self.income_range_ids]
        total = 0.0
        for data in data:
            key = list(data.keys())[0]
            value_needed = int(data[key])
            total += value_needed

        return total