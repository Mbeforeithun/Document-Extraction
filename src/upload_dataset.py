import json

from dotenv import load_dotenv
from langsmith import Client

load_dotenv()

DATASET_NAME = "invoice-extraction-v1"

client = Client()

if client.has_dataset(dataset_name=DATASET_NAME):
    print(f"Dataset '{DATASET_NAME}' already exists. Nothing uploaded.")
else:
    with open("src/ground_truth.json", encoding="utf-8") as f:
        ground_truth = json.load(f)

    dataset = client.create_dataset(
        dataset_name=DATASET_NAME,
        description="Invoice PDFs with expected fields and whether validation should pass.",
    )
    client.create_examples(
        dataset_id=dataset.id,
        inputs=[{"file_path": path} for path in ground_truth],
        outputs=list(ground_truth.values()),
    )
    print(f"Uploaded {len(ground_truth)} examples to '{DATASET_NAME}'.")