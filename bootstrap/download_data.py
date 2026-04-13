import os
from dotenv import load_dotenv
import zipfile

dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=dotenv_path)

os.environ['KAGGLE_USERNAME'] = os.getenv('KAGGLE_USERNAME')
os.environ['KAGGLE_KEY'] = os.getenv('KAGGLE_API_KEY')


def download_data():
    DATASET = "abhayayare/e-commerce-dataset"
    TARGET_FILES = "./data/ecommerce_dataset"
    OUTPUT_DIR = "./data"   # Relative to where the command is exec

    if os.path.exists(TARGET_FILES):
        print(f"Output dir {TARGET_FILES} already exists, resuming download")
        return

    from kaggle.api.kaggle_api_extended import KaggleApi # The api looks for credentials when charged

    api = KaggleApi()
    api.authenticate()

    api.dataset_download_files(DATASET, path=OUTPUT_DIR, unzip=False)

    with zipfile.ZipFile('data/e-commerce-dataset.zip', 'r') as zip_ref:
        zip_ref.extract(member='ecommerce_dataset/orders.csv', path='data')
        zip_ref.extract(member='ecommerce_dataset/order_items.csv', path='data')
        zip_ref.extract(member='ecommerce_dataset/users.csv',  path='data')
        zip_ref.extract(member='ecommerce_dataset/products.csv', path='data')

    if os.path.exists('data/e-commerce-dataset.zip'):
        os.remove('data/e-commerce-dataset.zip')
        print(f"Zip File {'data/e-commerce-dataset.zip'} deleted.")

    print(f"Dataset downloaded to {OUTPUT_DIR}")

if __name__ == "__main__":
    download_data()