from census import Census
from us import states


class PopulationHandler():
    def __init__(self):
        self.population_code = 'B19051_002E'
        self.census = Census("d8fa9f7c0841efecfb91b98bf8cbe056cf654cec")

    def get_population(self, some_id, county_id, year):
        population = self.census.acs5.state_county(some_id, states.CA.fips, county_id, year=year)
        return int(population[0][some_id])
