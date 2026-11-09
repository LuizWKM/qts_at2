import pytest

from tests.factories import BookFactory


@pytest.mark.integration
def test_lista_inicia_com_tres_livros(client):
    # Arrange
    expected_count = 3
    # Act
    response = client.get("/livros")
    # Assert
    assert response.status_code == 200
    assert len(response.json()) == expected_count


@pytest.mark.integration
def test_cria_livro_com_sanitizacao_e_factory(client, mocker):
    # Arrange
    payload = BookFactory.build()
    payload["titulo"] = f"  {payload['titulo']}  "
    notifier = mocker.patch("app.main.services.notify_book_created")
    # Act
    response = client.post("/livros", json=payload)
    # Assert
    assert response.status_code == 201
    assert response.json()["titulo"] == payload["titulo"].strip()
    notifier.assert_called_once()


@pytest.mark.integration
def test_notificador_externo_falha_e_responde_erro(client, mocker):
    # Arrange
    mocker.patch(
        "app.main.services.notify_book_created",
        side_effect=RuntimeError("serviço indisponível"),
    )
    # Act
    response = client.post("/livros", json=BookFactory.build())
    # Assert
    assert response.status_code == 503


@pytest.mark.integration
@pytest.mark.parametrize(
    ("payload", "message"),
    [
        ({"titulo": " ", "autor": "Autor", "generos": ["Ficção"]}, "O campo titulo"),
        ({"titulo": "Livro", "autor": "Autor", "generos": []}, "pelo menos um gênero"),
    ],
)
def test_rejeita_dados_invalidos(client, payload, message):
    # Arrange
    # Act
    response = client.post("/livros", json=payload)
    # Assert
    assert response.status_code == 422
    assert message in response.text


@pytest.mark.integration
def test_atualiza_e_remove_por_id(client):
    # Arrange
    book = client.get("/livros").json()[0]
    # Act
    update = client.patch(f"/livros/{book['id']}", json={"autor": "  Novo Autor  "})
    deletion = client.delete(f"/livros/{book['id']}")
    # Assert
    assert update.status_code == 200
    assert update.json()["autor"] == "Novo Autor"
    assert deletion.status_code == 204
