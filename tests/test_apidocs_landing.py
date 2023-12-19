import re
from playwright.sync_api import Page, expect


LANDING_URL = "https://developers.redhat.com/api-catalog/"


def navigate_to_landing(page: Page):
    page.goto(LANDING_URL)
    expect(page).to_have_title("Home | API Catalog and Documentation")
    # Dismiss the pop-up
    page.get_by_text("Close").click()


def visit_card(page: Page, cardName: str):
    # css=article is required to disambiguate from the two matches 
    page.get_by_role("link", name=cardName).and_(page.locator("css=article")).click()


def doc_page_title_exists(page: Page, doc_page_title:str):
    expect(page.get_by_role("heading", name=doc_page_title)).to_be_visible()
    # expect doc_page_title to be in the page title
    expect(page).to_have_title(re.compile(doc_page_title))


def test_landing_navigation(page: Page):
    navigate_to_landing(page)
    # Visit one of the cards
    visit_card(page, "Advisor")
    # Confirm the doc page loaded
    doc_page_title_exists(page, "Advisor")


def test_search_filter(page: Page):
    pass

def test_clear_search_filter(page: Page):
    pass

def test_checkbox_selection(page: Page):
    pass

def test_nav_menu_presence(page: Page):
    pass

