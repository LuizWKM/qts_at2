from faker import Faker


fake = Faker("pt_BR")


class BookFactory:
    @staticmethod
    def build() -> dict[str, object]:
        return {
            "titulo": fake.sentence(nb_words=3).rstrip("."),
            "autor": fake.name(),
            "generos": [fake.word(), fake.word()],
        }
