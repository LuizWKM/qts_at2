from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .main import Book


def notify_book_created(book: Book) -> None:
    """Ponto de integração substituível por um serviço externo em produção."""
    return None
