# Product Requirements Document (PRD) - Gerenciamento de Livros

## 1. Escopo e Interface Web
- **Interface Web:** A aplicação deve fornecer uma interface web acessível localmente em `http://localhost:3000`, contendo página(s) HTML para visualização e interação com os fluxos de livros.
- **Massa de Dados Inicial:** Para fins de teste, o sistema deve ser inicializado com exatamente 3 livros pré-cadastrados em memória.

## 2. Especificação das Rotas (API)
- `GET /livros`: Retorna a lista de todos os livros cadastrados.
- `POST /livros`: Cadastra um novo livro recebendo um payload com `titulo`, `autor` e `generos`.
- `PATCH /livros/{id}`: Atualiza os dados (parcial ou totalmente) de um livro existente identificado pelo `{id}`.
- `DELETE /livros/{id}`: Remove um livro específico do sistema utilizando o `{id}`.

---

## 3. Requisitos de Segurança (ISO 25010)
As validações abaixo devem ser implementadas (preferencialmente utilizando os validadores do Pydantic):

- O `titulo` e o `autor` devem ser textos (strings) e não podem ser vazios.
- Os `generos` devem ser representados por uma lista de textos e deve conter pelo menos um gênero.
- **Sanitização:** Espaços extras no início ou no fim do `titulo` e do `autor` devem ser removidos (strip) automaticamente antes da validação.
- Se o `titulo` ou `autor` forem vazios após a sanitização, o sistema deve lançar um erro (ou retornar HTTP 422) com a mensagem: "O campo {campo} deve ser um texto não vazio."
- Se a lista de `generos` estiver vazia, o sistema deve lançar um erro com a mensagem: "O livro deve possuir pelo menos um gênero cadastrado."
- Proteção de Injeção/Tipagem: Se os campos enviados não corresponderem aos tipos esperados (ex: enviar número no lugar de texto para o autor), o sistema deve barrar a requisição indicando tipo inválido.

## 4. Requisitos de Eficiência (ISO 25010)
- Os livros devem ser armazenados em memória (simulando um banco de dados) associados aos seus identificadores únicos (UUID ou inteiros incrementais), estruturados em um dicionário/hash map.
- As operações de busca (`GET` por ID, caso exista), atualização (`PATCH`) e remoção (`DELETE`) devem localizar o livro diretamente pelo identificador (complexidade O(1)), sem a necessidade de percorrer todos os itens cadastrados em loop (evitar complexidade O(N)).
- A listagem geral (`GET`) deve retornar somente os itens atualmente cadastrados, convertendo a estrutura de armazenamento para lista no momento da resposta, mantendo a ordem de inserção ou identificação.
- O sistema deve manter apenas a estrutura principal de armazenamento, sem criar arrays ou estruturas auxiliares permanentes desnecessárias, mantendo o consumo de memória estritamente proporcional à quantidade de livros cadastrados.