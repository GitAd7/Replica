import fitz

def build_translated_pdf(translated_elements, output_path):
    doc = fitz.open()
    
    current_page_num = 0
    current_page = None
    
    for block in translated_elements:
        if block["page"] != current_page_num:
            current_page = doc.new_page(width=595, height=842)
            current_page_num = block["page"]
            
        if block["type"] == "text":
            x0,y0,x1,y1 = block["bbox"]
            rect = fitz.Rect(x0,y0,x1,y1)
            try:
                current_page.insert_textbox(
                    rect,
                    block["content"],
                    fontsize=11,
                    fontname='helv',
                    color = (0,0,0)
                )
            except Exception as e:
                print(f"Error inserting block on page {current_page}:{e}")
                continue
    doc.save(output_path)
    doc.close()