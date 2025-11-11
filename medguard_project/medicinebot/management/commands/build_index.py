# medicinebot/management/commands/build_index.py

import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings
from llama_index.core import Document, VectorStoreIndex

class Command(BaseCommand):
    help = 'Builds the vector store index from the medicine CSV data.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to build the index...'))

        # Load the dataset using the path from settings
        try:
            df = pd.read_csv(settings.MEDICINE_DATA_PATH)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Error: The file at {settings.MEDICINE_DATA_PATH} was not found."))
            return

        # Prepare documents for LlamaIndex
        documents = []
        for _, row in df.iterrows():
            # Combine all relevant columns into a single text block for each medicine
            content = f"""
            Name: {row.get('Name', 'N/A')}
            Type: {row.get('Type', 'N/A')}
            Uses: {row.get('Uses', 'N/A')}
            Content: {row.get('Content', 'N/A')}
            SideEffects: {row.get('SideEffects', 'N/A')}
            Dosage: {row.get('Dosage', 'N/A')}
            Manufacturer: {row.get('Manufacturer', 'N/A')}
            Description: {row.get('Description', 'N/A')}
            """
            documents.append(Document(text=content))

        self.stdout.write(self.style.SUCCESS(f'Loaded {len(documents)} documents from CSV.'))

        # Create the index from the documents
        index = VectorStoreIndex.from_documents(documents)

        # Save the index to the disk for later use
        index.storage_context.persist(persist_dir=settings.INDEX_STORAGE_PATH)

        self.stdout.write(self.style.SUCCESS(f'Index built and saved successfully to {settings.INDEX_STORAGE_PATH}'))