from algoliasearch.search_client import SearchClient

client = SearchClient.create(APPLICATION_ID, API_KEY)
index = client.init_index('reports')

object_ids = [str(x) for x in range(10001, 10411)]
index.delete_objects(object_ids)
