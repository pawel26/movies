import omdb

import .config

class OMDBApi:
    def __init__(self):
        self.api = omdb.set_default('apikey', config.omdb_api_key)
        omdb.set_default('apikey', '4a41d844')
        omdb.set_default('tomatoes', True)
        movie_data = omdb.get(title=f"{self.validated_data['title']}")
    
    def search_by_title():
        pass

    def search_by_id():
        pass
