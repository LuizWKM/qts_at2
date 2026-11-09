from __future__ import annotations

from pathlib import Path
from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, ConfigDict, field_validator

from . import services

app = FastAPI(title="Biblioteca Viva", version="1.0.0")
templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates")


class BookInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    titulo: str
    autor: str
    generos: list[str]

    @field_validator("titulo", "autor", mode="before")
    @classmethod
    def normalize_text(cls, value: object, info: object) -> object:
        if not isinstance(value, str):
            return value
        normalized = value.strip()
        if not normalized:
            field_name = getattr(info, "field_name", "campo")
            raise ValueError(f"O campo {field_name} deve ser um texto não vazio.")
        return normalized

    @field_validator("generos")
    @classmethod
    def validate_genres(cls, value: list[str]) -> list[str]:
        if not value:
            raise ValueError("O livro deve possuir pelo menos um gênero cadastrado.")
        return [genre.strip() for genre in value]


class Book(BookInput):
    id: UUID


class BookPatch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    titulo: str | None = None
    autor: str | None = None
    generos: list[str] | None = None

    @field_validator("titulo", "autor", mode="before")
    @classmethod
    def normalize_optional_text(cls, value: object, info: object) -> object:
        if value is None or not isinstance(value, str):
            return value
        normalized = value.strip()
        if not normalized:
            field_name = getattr(info, "field_name", "campo")
            raise ValueError(f"O campo {field_name} deve ser um texto não vazio.")
        return normalized

    @field_validator("generos")
    @classmethod
    def validate_optional_genres(cls, value: list[str] | None) -> list[str] | None:
        if value is not None and not value:
            raise ValueError("O livro deve possuir pelo menos um gênero cadastrado.")
        return [genre.strip() for genre in value] if value is not None else None


def _seed_books() -> dict[UUID, Book]:
    seeds = (
        ("Dom Casmurro", "Machado de Assis", ["Romance", "Clássico"]),
        ("O Hobbit", "J. R. R. Tolkien", ["Fantasia", "Aventura"]),
        ("Quarto de Despejo", "Carolina Maria de Jesus", ["Memórias", "Brasil"]),
    )
    return {
        book.id: book
        for book in (
            Book(id=uuid4(), titulo=title, autor=author, generos=genres)
            for title, author, genres in seeds
        )
    }


books: dict[UUID, Book] = _seed_books()


@app.get("/", response_class=HTMLResponse)
def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/livros", response_model=list[Book])
def list_books() -> list[Book]:
    return list(books.values())


@app.post("/livros", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(payload: BookInput) -> Book:
    book = Book(id=uuid4(), **payload.model_dump())
    books[book.id] = book
    try:
        services.notify_book_created(book)
    except RuntimeError as error:
        books.pop(book.id)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Serviço externo indisponível.",
        ) from error
    return book


@app.patch("/livros/{book_id}", response_model=Book)
def update_book(book_id: UUID, payload: BookPatch) -> Book:
    current = books.get(book_id)
    if current is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
    updated = current.model_copy(update=payload.model_dump(exclude_unset=True))
    books[book_id] = Book.model_validate(updated)
    return books[book_id]


@app.delete("/livros/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: UUID) -> None:
    if books.pop(book_id, None) is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=3000, reload=True)
