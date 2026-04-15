# End-to-end Batch Pipeline

## Project Structure

```
├── README.md
├── .gitignore
├── .env  # Env variables (db credentials, kaggle credentials)
├── conda-env.yaml # Conda environment for python tools
│
├── bootstrap/  # Scripts to adjust data to get more realistic data for future SCD
│   ├── download_data.py
│   ├── products_tf.py
│   ├── users_tf.py
│   ├── order_items_tf.py
│   └── load_2_source.py
│       

```

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