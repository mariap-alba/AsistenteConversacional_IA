from app.pipelines.ingest_pipeline import Ingestion

if __name__ == "__main__":

    ing = Ingestion()
    text = ing.indexing("Guia_de_instalacion_Tailwind.pdf")

    