from celery import Celery
from app.services.translator import translate_text
from app.services.pdf_builder import build_translated_pdf
from app.services.pdf_parser import extract_pdf_elements

celery_app = Celery(
    "replica_task",
    broker = "redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

@celery_app.task
def process_pdf_task(input_pdf_path:str, output_pdf_path:str):
    structured_elements = extract_pdf_elements(input_pdf_path)
    
    translated_elements = []
    for block in structured_elements:
        if block["type"] == "text":
            translated_text = translate_text(block["content"])
            block["content"] = translated_text
        translated_elements.append(block)
        
    build_translated_pdf(translated_elements, output_pdf_path)
    
    return {"status":"success", "output_file":output_pdf_path}