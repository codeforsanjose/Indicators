from census import Census
from us import states

from census_api_handler import CensusAPI


class PopulationHandler():
    def __init__(self):
        self.census_api = CensusAPI()
        self.populationID = 'B19051_002E'

    def get_population(self, county_id, year):
        population = self.census_api.call_API(self.populationID, county_id, year=year)
        return int(population[0][self.populationID])
