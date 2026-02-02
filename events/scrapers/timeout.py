import requests
from bs4 import BeautifulSoup
from events.models import Event


def scrape_timeout():
    url = "https://www.timeout.com/sydney/events"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    cards = soup.select("div.card-content")
    print(f"Found {len(cards)} events")

    for card in cards:
        try:
            title_el = card.select_one("h3")
            link_el = card.find("a")

            if not title_el or not link_el:
                continue

            title = title_el.text.strip()
            link = "https://www.timeout.com" + link_el["href"]

            obj, created = Event.objects.get_or_create(
                source_url=link,
                defaults={
                    "title": title,
                    "source_name": "TimeOut Sydney",
                }
            )

            if created:
                print("NEW:", title)
            else:
                if obj.title != title:
                    obj.title = title
                    obj.status = "updated"
                    obj.save()
                    print("UPDATED:", title)

        except Exception as e:
            print("Error:", e)
