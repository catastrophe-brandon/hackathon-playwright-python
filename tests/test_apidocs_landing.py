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


def card_count(page: Page):
    """Computes the total number of cards displayed"""
    return visible_cards(page).count()


def visible_cards(page: Page):
    """Returns all cards that are visible"""
    return page.locator("css=.pf-c-card").and_(page.locator("css=:visible"))


def doc_page_title_exists(page: Page, doc_page_title:str):
    expect(page.get_by_role("heading", name=doc_page_title)).to_be_visible()
    # expect doc_page_title to be in the page title
    expect(page).to_have_title(re.compile(doc_page_title))


def search_for(page: Page, search_str: str):
    """Searches for the specified search string"""
    page.get_by_placeholder("Find by product or service").fill(search_str)


def clear_search(page: Page):
    page.get_by_placeholder("Find by product or service").clear()


def select_checkbox(page: Page, checkbox_labels: list[str]):
    """ Select the checkboxes with the provided label text """
    for checkbox_lbl in checkbox_labels:
        page.locator("label").filter(has_text=checkbox_lbl).set_checked(True)


def clear_checkboxes(page: Page):
    """ Ensure all the checkboxes are unchecked """
    all_checkboxes = page.get_by_role('checkbox')
    checkbox_count = all_checkboxes.count()
    for i in range(0, checkbox_count):
        all_checkboxes.nth(i).set_checked(False)


def test_landing_navigation(page: Page):
    """Verify that we can navigate to the API docs page and load a specific API doc"""
    navigate_to_landing(page)
    # Visit one of the cards
    visit_card(page, "Advisor")
    # Confirm the doc page loaded
    doc_page_title_exists(page, "Advisor")


def test_search_filter(page: Page):
    """Verify that if we search for a phrase, only expected matches are shown"""
    navigate_to_landing(page)
    search_for(page, "Advisor")
    assert card_count(page) == 3
    search_for(page, "Comp")
    assert card_count(page) == 1
    search_for(page, "potato")
    assert card_count(page) == 0


def test_clear_search_filter(page: Page):
    """Verify that if the search filter is cleared, we get all the cards again"""
    navigate_to_landing(page)
    search_for(page, "Hamburger")
    assert card_count(page) == 0
    clear_search(page)
    # By default 12 cards are displayed
    assert card_count(page) == 12


def test_checkbox_selection(page: Page):
    """Verify that if a checkbox is selected only appropriate cards are shown"""
    navigate_to_landing(page)
    select_checkbox(page, ["Automation", "Deploy"])
    assert card_count(page) == 6
    clear_checkboxes(page)
    assert card_count(page) == 12


def test_nav_menu_presence(page: Page):
    """Verify that the nav menu appears when clicked and has the right headings"""
    pass

