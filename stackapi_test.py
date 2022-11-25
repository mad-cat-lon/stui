from stackapi import StackAPI
stackAPI = StackAPI('stackoverflow', key="9XXRaYFBeJ*32qbNBYZRTA((")
stackAPI.max_pages = 1 
stackAPI.page_size = 100
question = stackAPI.fetch(
            f"questions/58903690/answers",
        )["items"][0]
print(question)