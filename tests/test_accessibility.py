import pytest
from axe_playwright_python.sync_playwright import Axe
from playwright.sync_api import Page, expect


@pytest.mark.accessibility
def test_home_sem_violacoes_wcag(page: Page, base_url: str):
    page.goto(base_url)
    results = Axe().run(page)
    assert results.violations_count == 0


@pytest.mark.accessibility
def test_navegacao_por_teclado(page: Page, base_url: str):
    page.goto(base_url)
    page.keyboard.press("Tab")
    expect(page.get_by_role("heading", name="Biblioteca Viva")).to_be_focused()
