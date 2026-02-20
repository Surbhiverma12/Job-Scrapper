from playwright.sync_api import sync_playwright
import csv


def scrape_jobs(query, location, pages=1):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        page = browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
        )

        query = query.replace(" ", "+")
        location = location.replace(" ", "+")

        job_list = []
        seen_jobs = set()

        for page_num in range(pages):
            start = page_num * 10

            url = f"https://in.indeed.com/jobs?q={query}&l={location}&start={start}"
            page.goto(url)

            try:
                page.wait_for_selector("div.job_seen_beacon", timeout=10000)
            except:
                print("Jobs not found on this page")
                continue

            jobs = page.query_selector_all("div.job_seen_beacon")

            for job in jobs:
                title_el = job.query_selector("h2")
                company_el = job.query_selector("[data-testid='company-name']")
                location_el = job.query_selector("[data-testid='text-location']")

                title = title_el.inner_text() if title_el else "N/A"
                company = company_el.inner_text() if company_el else "N/A"
                location = location_el.inner_text() if location_el else "N/A"

                job_key = (title, company, location)

                if job_key not in seen_jobs:
                    seen_jobs.add(job_key)

                    job_data = {
                        "title": title,
                        "company": company,
                        "location": location
                    }

                    job_list.append(job_data)

        browser.close()
        return job_list


def save_to_csv(data, filename="jobs.csv"):
    if not data:
        print("No data to save")
        return

    keys = data[0].keys()

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

    print("Data saved to", filename)


jobs = scrape_jobs("software developer", "Noida", pages=3)
save_to_csv(jobs)

for job in jobs:
    print(job)