from census import Census
from us import states

from census_api_handler import CensusAPI


class PopulationHandler():
    def __init__(self):
        self.census_api = CensusAPI()

    def get_population(self, indicator_id, county_id, year):
        population = self.census_api.call_API(indicator_id, county_id, year=year)
        return int(population[0][indicator_id])

    def get_population_state(self, indicator_id, year):
        population = self.census_api.call_API_state(indicator_id, year=year)
        return int(population[0][indicator_id])

    def get_population_us(self, indicator_id, year):
        population = self.census_api.call_API_us(indicator_id, year=year)
        return int(population[0][indicator_id])
