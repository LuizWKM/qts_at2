from locust import HttpUser, between, task


class BibliotecaUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def listar_livros(self) -> None:
        self.client.get("/livros", name="GET /livros")

    @task(1)
    def acessar_interface(self) -> None:
        self.client.get("/", name="GET /")
