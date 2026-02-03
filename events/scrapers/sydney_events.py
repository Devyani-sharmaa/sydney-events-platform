import requests
from bs4 import BeautifulSoup
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from events.models import Event


def get_event_description(event_url):
    try:
        res = requests.get(event_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        p = soup.find("p")
        return p.text.strip() if p else "No description available."
    except:
        return "No description available."


def scrape_sydney_events():
    url = "https://www.sydney.com/events"

    headers = {"User-Agent": "Mozilla/5.0"}

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
        if img_tag:
            image_url = img_tag.get("src") or img_tag.get("data-src") or ""

        # DATE PARSE
        date_time = timezone.now()
        time_tag = card.find("time")
        if time_tag and time_tag.get("datetime"):
            parsed_date = parse_datetime(time_tag["datetime"])
            if parsed_date:
                date_time = parsed_date

        description = get_event_description(link)

        obj, created = Event.objects.update_or_create(
            source_url=link,
            defaults={
                "title": title,
                "date_time": date_time,
                "venue_name": "Sydney Venue",
                "venue_address": "Sydney, Australia",
                "city": "Sydney",
                "description": description,
                "category": "General Event",
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
