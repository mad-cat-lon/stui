from stackapi import StackAPI
from .src import Client

if __name__ == '__main__':
    stackAPI = StackAPI('stackoverflow', key="9XXRaYFBeJ*32qbNBYZRTA((")
    stackAPI.max_pages = 1 
    stackAPI.page_size = 100
    app = Client()
    app.set_stackAPI(stackAPI)
    app.run()