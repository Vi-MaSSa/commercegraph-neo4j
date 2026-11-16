# CommerceGraph — E-commerce Intelligence with Neo4j

> Este projeto é um exercício de modelagem de dados de e-commerce em Neo4j. Criei um gerador de dados fictícios em Python para testar relações entre clientes, pedidos, produtos e fornecedores sem usar informações reais. Quero usar o projeto para praticar consultas Cypher e comparar perguntas que dependem de percorrer essas relações.
> **Status:** Fase 1 — Base de projeto e conjuntos de dados.

## 1. Problema de negócio

> Os dados de um e-commerce possuem várias entidades conectadas entre si. Clientes fazem pedidos, pedidos possuem produtos, produtos estão ligados a categorias e marcas, fornecedores abastecem esses produtos, e cada pedido também tem suas informações de pagamento e entrega.

A ideia do CommerceGraph é representar todas essas relações no Neo4j, permitindo explorar as conexões entre os dados e realizar consultas de múltiplos saltos (multi-hop) de forma mais intuitiva utilizando Cypher.

## 2. Por que plataforma de banco de dados de grafos?

> O modelo de grafos se destaca quando precisamos analisar as relações entre os dados, como identificar produtos que costumam ser comprados juntos, entender as dependências entre fornecedores ou descobrir conexões entre clientes e produtos.

A proposta deste projeto é justamente explorar esses cenários em que o banco de grafos faz diferença, mostrando suas vantagens sem desconsiderar a importância dos bancos relacionais.

## 3. Technology

- Neo4j Aura (managed graph database)
- Cypher
- Python 3.10+
- Neo4j Python Driver
- CSV for portable source data

## 4. Modelo de grafo

### Node labels

`Customer`, `Order`, `Product`, `Category`, `Brand`, `Supplier`, `Payment`, `Shipment`, `Review`

### Relacionamentos

| Relationship   | Pattern            | Meaning                       |
| -------------- | ------------------ | ----------------------------- |
| `PLACED`       | Customer → Order   | Customer placed an order      |
| `CONTAINS`     | Order → Product    | Order contains a product      |
| `IN_CATEGORY`  | Product → Category | Product belongs to a category |
| `BELONGS_TO`   | Product → Brand    | Product belongs to a brand    |
| `SUPPLIES`     | Supplier → Product | Supplier supplies a product   |
| `HAS_PAYMENT`  | Order → Payment    | Order has a payment           |
| `HAS_SHIPMENT` | Order → Shipment   | Order has a shipment          |
| `WROTE`        | Customer → Review  | Customer wrote a review       |
| `REVIEWS`      | Review → Product   | Review refers to a product    |

### Sobre a modelagem

- Cada node (nó) possui um identificador ne negócio (id).
- Os relacionamentos são criados pelo 'MERGE' para tomar as importações reptíveis.
- Um pedido contém varios produtos e um produto pode conter diversos pedidos.
- Os dados são fictícios, ou seja, nunca deve interpreta-los como informações de clientes/dados comerciais reais.

## 5. Estrutura Repository

```text
commercegraph-neo4j/
├── data/                  # Generated CSV files
├── cypher/                # Constraints, schema and analytical queries
├── docs/                  # Architecture, model and troubleshooting
├── scripts/               # Dataset generation and Aura import
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## 6. Quick start

### Requirements

- Python 3.10 ou última versão (mais recente)
- Neo4j Aura database e conexão URI
- Acesso a instância Aura

### Instalação de dependencias

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
```

### Dataset fictício

```bash
python scripts/generate_dataset.py
```

### Configuração de credenciais (env)

Copie `.env.example` para `.env` e preencha os detalhes de conexão para Neo4j Aura:

```env
NEO4J_URI=neo4j+s://<your-aura-id>.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password
NEO4J_DATABASE=neo4j
```

Nunca commit .env ou credenciais do database.

### Create constraints - import

```bash
python scripts/import_to_aura.py
```

O import lê arquivos CSV locais e envia lotes parametrizados, utilizando `UNWIND`, por meio do driver oficial do Neo4j para Python. Essa abordagem funciona com o Aura, sem a necessidade de que o servidor de banco de dados acesse os arquivos locais do seu computador.

## 7. Validação

Após a importação, execute as consultas presentes em `cypher/03_validation.cypher` no Neo4j Browser. Confirme se todos os rótulos esperados existem, se os identificadores são únicos e se a contagem de relacionamentos é diferente de zero.

## 8. Regras de negócio

As consultas vão responder perguntas como:

1. Quais clientes realizam o maior número de pedidos?
2. Quais pares de produtos aparecem com mais frequência no mesmo pedido?
3. Quais produtos possuem as melhores avaliações?
4. Quais fornecedores oferecem a maior variedade de produtos?
5. Quais produtos poderiam ser recomendados a um cliente com base no comportamento de compra conjunta?

## 9. Dados e limitações

Todos os registros são fictícios. O gerador foi projetado para fins de aprendizado e demonstração em portfólios.

## 10. Roadmap

- [x] Definir o escopo do projeto e o esquema do grafo
- [x] Adicionar gerador determinístico de dados sintéticos
- [x] Adicionar importador para o Aura usando `UNWIND` em lotes
- [ ] Validar o grafo importado e registrar evidências no Neo4j Browser
- [ ] Adicionar conjunto de consultas de negócio e analisar planos de execução
- [ ] Documentar decisões de desempenho e solução de problemas
- [ ] Publicar a arquitetura final e capturas de tela dos resultados

## 11. Autor

- GitHub: [Vi-MaSSa](https://github.com/Vi-MaSSa)
- E-mail: [vinimassa100@gmail.com](mailto:vinimassa100@gmail.com)
- LinkedIn: [Vinicius Massagardi](https://www.linkedin.com/in/vinicius01/)
