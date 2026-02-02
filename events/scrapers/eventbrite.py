from playwright.sync_api import sync_playwright
from events.models import Event


def scrape_eventbrite():
    url = "https://www.eventbrite.com.au/d/australia--sydney/events/"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_timeout(5000)  # JS load hone do

        cards = page.query_selector_all("div.search-event-card-wrapper")
        print(f"Found {len(cards)} events")

        for card in cards:
            try:
                title_el = card.query_selector("h3")
                link_el = card.query_selector("a")

                if not title_el or not link_el:
                    continue

                title = title_el.inner_text().strip()
                link = link_el.get_attribute("href")

                obj, created = Event.objects.get_or_create(
                    source_url=link,
                    defaults={
                        "title": title,
                        "source_name": "Eventbrite",
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

        browser.close()
