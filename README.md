# End-to-end Batch Pipeline

## Project Structure

```
├── README.md
├── .gitignore
├── .env  # Env variables (db credentials, kaggle credentials)
├── conda-env.yaml # Conda environment for python tools
├── notebook.ipynb
│
├── docker-compose.yml
│
├── bootstrap/  # Scripts to adjust data to get more realistic data for future SCD
│   ├── download_data.py
│   ├── products_tf.py
│   ├── users_tf.py
│   ├── order_items_tf.py
│   └── load_2_source.py
│
├── data/
│   ├── ecommerce_dataset/
│   │   ├── order_items.csv
│   │   ├── orders.csv
│   │   ├── products.csv
│   │   └── users.csv
│   │ 
│   └── processed/
│       ├── order_items_processed.csv
│       ├── orders_processed.csv
│       ├── products_processed.csv
│       └── users_processed.csv
│ 
├── infra/
│   ├── init.sh
│   └── policies/
│       ├── orch_policy.json
│       ├── job_policy.json
│       └── bi_policy.json
│
├── sources/
│   ├── prepare_systems.py  # Script to populate orders and catalog dbs
│   ├── postgres/
│   │   └── init.sql
│   ├── api/
│   │   ├── Dockerfile
│   │   ├── main.py
│   │   ├── connection.py
│   │   ├── products_model.py
│   │   ├── products_schema.py
│   │   └── catalog.db  # Sqlite db, not commited
│   └── crm/
│   │   ├── year=2024/
│   │   │   ├── month=01/
│   │   │   │   ├── day=01/
│   │   │   │   │   ├── users.csv   
│   │   :   :
│   │   :   :
│   │   :   :
│
├── ingestion/
│   ├── ingest_users.py
│   ├── ingest_products.py
│   ├── ingest_orders.py
│   └── ingest_order_items.py
│
├── spark-app/
│   ├──Dockerfile
│   │
│   ├── jobs/
│   │   ├── users_bronze_to_silver.py
│   │   ├── products_bronze_to_silver.py
│   │   ├── orders_bronze_to_silver.py
│   │   ├── order_items_bronze_to_silver.py
│   │   └── gold_business_value.py
│   │
│   ├── common/
│   │   ├── spark_session.py
│   │   ├── schemas.py
│   │   └── config.py
│   │
│   └── transfomrations/
│       ├── users_tf.py
│       ├── products_tf.py
│       ├── orders_tf.py
│       ├── order_items_tf.py
│       └── scd2_tf.py
│    
│       
├── airflow/

```
## Upstream Data Modeling Strategy

Although the original dataset was static, it was extended to simulate change events over time by introducing multiple versions of the same entities (e.g., users and products).

Instead of representing a traditional OLTP system with only the latest state, the source data behaves as an event-based or CDC-like system, where each record reflects a change at a given point in time.

This approach enables:

* Simulation of real-world data evolution
* Event-driven ingestion patterns
* Reconstruction of entity state at any point in time

### Implications for the Data Lake

Even though historical records are available upstream, the Silver layer standardizes this data into a formal Slowly Changing Dimension Type 2 (SCD2) structure by:

* Ordering records chronologically
* Defining `valid_from` and `valid_to` intervals
* Flagging current vs historical records

This ensures consistency and usability for downstream analytical models.

## Data Augmentation & Change Simulation

To better approximate real-world data behavior, the original static dataset was extended with synthetic changes across multiple entities. This process simulates how data evolves over time in production systems.

### Users

User records were augmented with changes in attributes such as email and city. These updates emulate real-world scenarios like profile updates or user relocation.

Depending on the downstream modeling approach, these changes can be interpreted as:

Slowly Changing Dimensions (SCD Type 1): overwriting previous values
Slowly Changing Dimensions (SCD Type 2): preserving historical versions

### Products

Product data was modified to include variations in price and rating over time, reflecting:

Dynamic pricing strategies
Changes in customer feedback

### Orders and Order Items

To ensure data consistency:

Order item prices were updated to match the modified product prices
Order totals were recalculated accordingly

This guarantees referential and numerical integrity across transactional data.

### Objective

These transformations aim to:

- Simulate temporal data evolution
- Introduce realistic inconsistencies and updates
- Enable testing of downstream data pipelines under changing conditions

## Source System Data Preparation

The original dataset was transformed into source-specific representations to simulate realistic upstream data systems.

Each source system exposes a different data contract and ingestion pattern:

* **PostgreSQL (OLTP)**: transactional data (`orders`, `order_items`) is stored in a normalized relational schema with enforced primary and foreign keys, simulating an operational database.

* **API (Products)**: product data is exposed via a REST API with cursor-based pagination, enabling incremental extraction based on (`updated_at`, `product_id`).

* **File-based CRM (Users)**: user data is delivered as partitioned files organized by date (`year/month/day`), simulating periodic batch exports from external systems (e.g. CRM platforms). This pattern enables incremental ingestion via partition discovery.

- SQLite was chosen for simplicity and portability
- FastAPI was used to simulate an external service
- Cursor-based pagination was implemented instead of offset-based pagination to support incremental ingestion

These transformations ensure that each source behaves according to its real-world counterpart, enabling realistic ingestion patterns in the pipeline.

### Common pitfalls

- Relative paths in SQLite depend on the container working directory
- Docker containers do not share filesystem with host unless volumes are mounted
- Mismatched database paths can lead to "no such table" errors
- API serialization requires proper Pydantic configuration (`from_attributes = True`)

## Pipeline Lifecycle

### Incremental Ingestion Strategy

Data ingestion is designed to simulate an incremental loading pattern, where new records are appended over time instead of replacing existing data.

Each ingestion batch contains only new or updated records, identified by their `updated_at` timestamp, and is stored in date-partitioned directories in the Bronze layer.

This approach reflects real-world ingestion patterns such as:

* Change Data Capture (CDC)
* Event-based systems
* Incremental API exports

### Historical Data Handling

The Bronze layer preserves all historical changes in an append-only format, it serves as a reliable source of truth for reconstructing entity state over time.

In the Silver layer, this historical data is transformed into a formal Slowly Changing Dimension Type 2 (SCD2) model by deriving validity intervals and identifying current records.

This separation ensures both:

* Raw data traceability (Bronze)
* Analytical consistency (Silver)


#### Bronze Layer (Unique Source of Truth)

Data is ingested incrementally into the Bronze layer using an append-only strategy. Each ingestion batch is stored in date-partitioned directories and contains only new or updated records received at that time.

No transformations or deduplication are applied at this stage, preserving the raw history of changes as emitted by the source systems.

#### Silver Layer (SCD Type 2 Modeling)

The Silver layer processes the accumulated Bronze data to construct a Slowly Changing Dimension Type 2 (SCD2) model.

For each entity:

* Records are ordered chronologically using `updated_at`
* Validity intervals (`valid_from`, `valid_to`) are derived
* Current and historical records are explicitly identified

This transformation converts raw change events into a structured, queryable historical model suitable for analytics.
