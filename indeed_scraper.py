from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://in.indeed.com/jobs?q=python+developer&l=India")
    page.wait_for_timeout(4000)

    jobs = page.query_selector_all("div.job_seen_beacon")

    for job in jobs[:5]:
        title_el = job.query_selector("h2")
        company_el = job.query_selector("[data-testid='company-name']")
        location_el = job.query_selector("[data-testid='text-location']")

        title = title_el.inner_text() if title_el else "N/A"
        company = company_el.inner_text() if company_el else "N/A"
        location = location_el.inner_text() if location_el else "N/A"

        print("Job:", title)
        print("Company:", company)
        print("Location:", location)
        print("--------")

    browser.close()
