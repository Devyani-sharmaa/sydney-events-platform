import requests
from bs4 import BeautifulSoup
from django.utils import timezone
from events.models import Event


def scrape_sydney_events():
    url = "https://www.sydney.com/events"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    event_cards = soup.find_all("article")
    print(f"Found {len(event_cards)} events")

    for card in event_cards[:10]:

        title_tag = card.find(["h2", "h3", "h4"])
        link_tag = card.find("a")
        img_tag = card.find("img")

        if not title_tag or not link_tag:
            continue

        title = title_tag.text.strip()
        link = link_tag.get("href")

        if not link.startswith("http"):
            link = "https://www.sydney.com" + link

        image_url = ""
        if img_tag and img_tag.get("src"):
            image_url = img_tag.get("src")

        # Dummy values (website doesn't always show these)
        venue_name = "Sydney Venue"
        venue_address = "Sydney, Australia"
        category = "General Event"
        description = "Event imported automatically from Sydney.com"

        obj, created = Event.objects.update_or_create(
            source_url=link,  # UNIQUE FIELD (important)
            defaults={
                "title": title,
                "date_time": timezone.now(),
                "venue_name": venue_name,
                "venue_address": venue_address,
                "city": "Sydney",
                "description": description,
                "category": category,
                "image_url": image_url,
                "source_name": "Sydney.com",
                "status": "new",
                "last_scraped_at": timezone.now(),
            }
        )

        if created:
            print(f"🆕 Added: {title}")
        else:
            print(f"♻️ Updated: {title}")

    print("✅ Scraping + saving complete.")
