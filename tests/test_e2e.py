import pytest
from playwright.sync_api import Page, expect


class CatalogPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.title = page.get_by_role("heading", name="Biblioteca Viva")
        self.catalog = page.get_by_role("heading", name="Livros cadastrados")

    def open(self, base_url: str) -> None:
        self.page.goto(base_url)


@pytest.mark.e2e
def test_usuario_visualiza_catalogo(page: Page, base_url: str):
    catalog = CatalogPage(page)
    catalog.open(base_url)
    expect(catalog.title).to_be_visible()
    expect(catalog.catalog).to_be_visible()
    expect(page.get_by_text("Dom Casmurro")).to_be_visible()
