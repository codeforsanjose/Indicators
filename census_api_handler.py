from census import Census
from us import states


class CensusAPI():
    census = None

    def __init__(self):
        if self.census is None:
            self.census = Census("d8fa9f7c0841efecfb91b98bf8cbe056cf654cec")

    def call_API(self, indicator_id, county_id, year):
        return self.census.acs5.state_county(indicator_id, states.CA.fips, county_id, year=year)

    def call_API_state(self, indicator_id, year):
        return self.census.acs5.state(indicator_id, states.CA.fips, year=year)

    def call_API_us(self, indicator_id, year):
        return self.census.acs5.state(indicator_id, Census.ALL, year=year)

