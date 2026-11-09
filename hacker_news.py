
import requests
import time


# Hacker News API configuration
BASE_URL = "https://hacker-news.firebaseio.com/v0"

HEADERS = {
    "User-Agent": "PythonHackerNewsTop10/1.0"
}

TIMEOUT = 10
REQUEST_DELAY = 0.2
TOP_STORY_COUNT = 10


def get_json(url):
    """
    Send an HTTP GET request and return the JSON response.
    """

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=TIMEOUT
    )

    # Raise an exception if the server returns an error.
    response.raise_for_status()

    # Convert the JSON response into Python data.
    return response.json()


def get_top_story_ids():
    """
    Retrieve the IDs of the current top Hacker News stories.
    """

    url = f"{BASE_URL}/topstories.json"

    story_ids = get_json(url)

    return story_ids


def get_story(story_id):
    """
    Retrieve the details of an individual story.
    """

    url = f"{BASE_URL}/item/{story_id}.json"

    story = get_json(url)

    return story


def get_top_stories():
    """
    Retrieve the top 10 actual stories, skipping jobs
    and unavailable or invalid items.
    """

    story_ids = get_top_story_ids()

    stories = []

    for story_id in story_ids:

        # Stop once we have collected 10 stories.
        if len(stories) >= TOP_STORY_COUNT:
            break

        try:
            story = get_story(story_id)

            # Ignore missing items and non-story items.
            if not story or story.get("type") != "story":
                continue

            if not story.get("title"):
                continue

            # Some Hacker News posts don't have an external URL.
            # For those, use the Hacker News discussion page.
            link = story.get(
                "url",
                f"https://news.ycombinator.com/item?id={story_id}"
            )

            stories.append({
                "title": story["title"],
                "score": story.get("score", 0),
                "link": link
            })

        except (requests.RequestException, ValueError) as error:
            print(f"Could not retrieve story {story_id}: {error}")

        # Pause before making the next API request.
        time.sleep(REQUEST_DELAY)

    return stories


def display_stories(stories):
    """
    Print the top stories in a readable format.
    """

    print("\n" + "=" * 70)
    print("             HACKER NEWS - TOP 10 STORIES")
    print("=" * 70)

    for index, story in enumerate(stories, start=1):

        print(f"\n{index}. {story['title']}")
        print(f"   Score: {story['score']} points")
        print(f"   Link:  {story['link']}")

    print("\n" + "=" * 70)
    print(f"Retrieved {len(stories)} stories.")
    print("=" * 70)


def main():
    """
    Main program execution.
    """

    print("Retrieving Hacker News top stories...")

    try:
        stories = get_top_stories()

        if stories:
            display_stories(stories)
        else:
            print("No stories could be retrieved.")

    except (requests.RequestException, ValueError) as error:
        print(f"Error communicating with Hacker News: {error}")


if __name__ == "__main__":
    main()
