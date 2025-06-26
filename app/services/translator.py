import fitz
from openai import OpenAI
import os
import time
from dotenv import load_dotenv
from app.utils.logger import logger
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def chunk_text(text, max_length=2000):
    chunks = []
    current_chunk = ""
    
    for paragraph in text.split("\n"):
        if len(current_chunk) + len(paragraph) < max_length:
            current_chunk += paragraph+"\n"
        else:
            chunks.append(current_chunk.stip())
            current_chunk = paragraph + "\n"
            
    if current_chunk:
        chunks.append(current_chunk.strip())
        
    return chunks

def translate_text(text:str) -> str:
    try:
        response = client.chat.completions.create(
            model = "gpt-4o",
            messages=[
                {"role":"system", "content":(
                    "You are an expert Multilingual translator. Translate all the provided context into natural and fluent english."
                    "Preserve numbers, formatting hints and technical terms. Avoind Unecessary interpretation"
                )},
                {"role":"user", "content":text}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Translation failed due to {e}")
        print(f"translation error:{e}")
        return "[Translation Failed!]"

def translate_pdf_preserving_layout(input_pdf_path:str, output_pdf_path:str):
    original_doc = fitz.open(input_pdf_path)
    translated_doc = fitz.open()
    
    for page_num, page in enumerate(original_doc,1):
        print()
        text_blocks = page.get_text("blocks")
        new_page = translated_doc.new_page(width=page.rect.width, height=page.rect.height)
        
        for block in text_blocks:
            x0, y0, x1, y1, text, _, _, _ = block
            if not text.strip():
                continue
            
            chunks = chunk_text(text)
            translated_chunks = [translate_text(chunk) for chunk in chunks]
            translated_text = "\n".join(translated_chunks)
            
            try: 
                new_page.insert_textbox(
                    fitz.Rect(x0,y0,x1,y1),
                    translated_text,
                    fontsize = 10,
                    font = "helv",
                    color = (0,0,0),
                    align = 0
                )
            except Exception as e:
                logger.error(f"Page Insertion failed due to {e}")
                print(f"Failed Inserting text on page {page_num}: {e}")
        
        time.sleep(1.5)
        
    translated_doc.save(output_pdf_path)
    translated_doc.close()
    original_doc.close()