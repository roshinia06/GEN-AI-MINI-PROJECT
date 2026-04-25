import wikipedia

def get_wiki_data(place):
    try:
        # Try to get the page directly
        try:
            page = wikipedia.page(place, auto_suggest=False)
        except wikipedia.DisambiguationError as e:
            # If disambiguation occurs, take the first option
            page = wikipedia.page(e.options[0], auto_suggest=False)
        except wikipedia.PageError:
            # If page not found, try searching
            search_results = wikipedia.search(place)
            if not search_results:
                return ""
            page = wikipedia.page(search_results[0], auto_suggest=False)
        
        summary = page.summary
        content = page.content[:2000]  # limit length

        return summary + "\n" + content
    except Exception as e:
        print(f"Error fetching Wikipedia data for {place}: {e}")
        return ""
