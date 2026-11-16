# CommerceGraph

Projeto de demonstração de modelagem e análise de dados de e-commerce com
Neo4j. Um gerador Python cria dados sintéticos e reproduzíveis; um importador
envia os CSVs locais ao Neo4j Aura em lotes, preservando os tipos das
propriedades.

> **Dados fictícios:** este projeto não usa dados reais de clientes ou de
> empresas. Os registros são destinados a aprendizado e demonstração.

## Objetivos

- Representar clientes, pedidos, produtos e entidades relacionadas como grafo.
- Explorar perguntas de negócio usando consultas Cypher com múltiplos saltos.
- Demonstrar geração determinística e importação repetível com `MERGE`.

## Tecnologias

- Python 3.10 ou superior
- Neo4j Aura e Cypher
- Neo4j Python Driver
- CSV para armazenar e transportar os dados gerados

## Dados gerados

O gerador usa uma seed fixa (`42`) e cria:

| Entidade/arquivo | Quantidade |
| --- | ---: |
| Categorias (`categories.csv`) | 8 |
| Marcas (`brands.csv`) | 12 |
| Fornecedores (`suppliers.csv`) | 18 |
| Clientes (`customers.csv`) | 150 |
| Produtos (`products.csv`) | 100 |
| Pedidos (`orders.csv`) | 400 |
| Itens de pedido (`order_items.csv`) | 990 |
| Pagamentos (`payments.csv`) | 400 |
| Envios (`shipments.csv`) | 400 |
| Avaliações (`reviews.csv`) | 180 |

Os nove tipos de nós totalizam 1.668 registros. Os itens de pedido são
representados por propriedades do relacionamento `CONTAINS`, não por nós.

## Modelo do grafo

### Nós e identificadores

| Label | Identificador único |
| --- | --- |
| `Customer` | `customer_id` |
| `Order` | `order_id` |
| `Product` | `product_id` |
| `Category` | `category_id` |
| `Brand` | `brand_id` |
| `Supplier` | `supplier_id` |
| `Payment` | `payment_id` |
| `Shipment` | `shipment_id` |
| `Review` | `review_id` |

### Relacionamentos

| Tipo | Direção | Significado |
| --- | --- | --- |
| `PLACED` | `Customer` → `Order` | Cliente fez o pedido |
| `CONTAINS` | `Order` → `Product` | Pedido contém produto |
| `IN_CATEGORY` | `Product` → `Category` | Produto pertence à categoria |
| `BELONGS_TO` | `Product` → `Brand` | Produto pertence à marca |
| `SUPPLIES` | `Supplier` → `Product` | Fornecedor abastece o produto |
| `HAS_PAYMENT` | `Order` → `Payment` | Pedido tem pagamento |
| `HAS_SHIPMENT` | `Order` → `Shipment` | Pedido tem envio |
| `WROTE` | `Customer` → `Review` | Cliente escreveu avaliação |
| `REVIEWS` | `Review` → `Product` | Avaliação refere-se ao produto |

`CONTAINS` armazena `quantity` e `unit_price`. O preço no relacionamento
preserva o valor no momento da compra, independentemente do preço atual do
produto.

### Tipos de propriedades

| Propriedade | Tipo no Neo4j |
| --- | --- |
| `Product.price` | `FLOAT` |
| `Review.rating` | `INTEGER` |
| `Order.order_date` | `DATE` |
| `CONTAINS.quantity` | `INTEGER` |
| `CONTAINS.unit_price` | `FLOAT` |

O CSV representa os valores como texto. O importador converte esses campos
antes de enviá-los ao Neo4j. Os demais campos do modelo são textos.

## Configuração e execução

Execute os comandos a partir da pasta do projeto, onde estão `scripts/` e
`requirements.txt`.

### 1. Criar ambiente e instalar dependências

No PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### 2. Gerar os CSVs

```powershell
python scripts/generate_dataset.py
```

Os arquivos são criados em `data/generated/`. Eles são ignorados pelo Git;
apenas os arquivos `.gitkeep` dessa pasta são versionados.

### 3. Configurar a conexão com o Neo4j Aura

Copie `.env.example` para `.env` e preencha as credenciais da sua instância:

```powershell
Copy-Item .env.example .env
```

O arquivo `.env` deve conter:

```env
NEO4J_URI=neo4j+s://<seu-id-aura>.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=<sua-senha>
NEO4J_DATABASE=neo4j
```

Não versione nem compartilhe o `.env`, tokens ou senhas. O `.gitignore` já
exclui esse arquivo.

### 4. Importar os dados

```powershell
python scripts/import_to_aura.py
```

O importador lê os CSVs localmente, converte os campos tipados e envia lotes
de até 500 linhas usando o driver oficial, parâmetros Cypher e `UNWIND`. O Aura
não precisa acessar os arquivos locais diretamente.

## Reimportação e validação

O importador cria constraints de unicidade com `IF NOT EXISTS` e usa `MERGE`
para nós e relacionamentos. Reexecutar a importação dos mesmos CSVs não deve
duplicar essas entidades; as propriedades dos nós são atualizadas com os
valores importados.

O processo não remove do banco nós que tenham deixado de existir nos CSVs.
Valores inválidos nos campos convertidos interrompem a importação com o nome
do arquivo e o número da linha.

No Neo4j Browser, execute:

- [`cypher/02_schema_counts.cypher`](cypher/02_schema_counts.cypher) para
  inspecionar o esquema e as contagens.
- [`cypher/03_validation.cypher`](cypher/03_validation.cypher) para validar
  rótulos, relacionamentos e possíveis nós sem conexões esperadas.

As constraints também podem ser criadas manualmente com
[`cypher/01_constraints.cypher`](cypher/01_constraints.cypher); o importador
já as cria automaticamente.

## Consultas de negócio

As consultas Cypher de exemplo estão em `cypher/queries/`:

- `01_customer_behavior.cypher`: comportamento de compra dos clientes.
- `02_product_affinity.cypher`: produtos comprados juntos.
- `03_supplier_coverage.cypher`: cobertura de produtos por fornecedor.
- `04_customer_recommendations.cypher`: recomendações para clientes.

## Estrutura do repositório

```text
commercegraph-neo4j/
├── cypher/                # Constraints, validações e consultas de negócio
├── data/
│   ├── generated/         # CSVs gerados localmente (ignorados pelo Git)
│   └── sample/
├── docs/                  # Arquitetura, modelo de dados e troubleshooting
├── scripts/
│   ├── generate_dataset.py
│   └── import_to_aura.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Documentação

- [Arquitetura](docs/architecture.md)
- [Modelo de dados](docs/data-model.md)
- [Solução de problemas](docs/troubleshooting.md)

## Autor

- GitHub: [Vi-MaSSa](https://github.com/Vi-MaSSa)
- LinkedIn: [Vinicius Massagardi](https://www.linkedin.com/in/vinicius01/)
