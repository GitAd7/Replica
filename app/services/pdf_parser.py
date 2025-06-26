import fitz

def extract_pdf_elements(pdf_path:str):
    document = fitz.open(pdf_path)
    parsed_elements = []
    
    for page_num, page in enumerate(document, start=1):
        blocks = page.get_text("blocks")
        for block in blocks:
            x0,y0,x1,y1,text,block_no,*_ = block
            parsed_elements.append({
                "page":page_num,
                "type": text,
                "bbox": (x0,y0,x1,y1),
                "content":text.strip()
            })
    document.close()
    return parsed_elements