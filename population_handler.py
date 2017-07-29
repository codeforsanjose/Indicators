from census import Census
from us import states

from census_api_handler import CensusAPI


class PopulationHandler():
    def __init__(self):
        self.census_api = CensusAPI()

    def get_population(self, indicator_id, county_id, year):
        population = self.census_api.call_API(indicator_id, county_id, year=year)
        return int(population[0][indicator_id])
