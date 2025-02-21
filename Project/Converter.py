import os
import fitz  # PyMuPDF
from llama_index.core import SimpleDirectoryReader

# Define paths relative to the script location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
documents_folder = os.path.join(BASE_DIR, "documents")  # Folder containing PDFs
output_folder = os.path.join(BASE_DIR, "pdf_pages")  # Extracted PDF pages
md_folder = os.path.join(BASE_DIR, "markdown_pages")  # Markdown output

# Create output directories if they don't exist
os.makedirs(output_folder, exist_ok=True)
os.makedirs(md_folder, exist_ok=True)

# Function to extract pages and save as individual PDFs
def extract_pages(pdf_path, output_folder, pdf_name):
    doc = fitz.open(pdf_path)
    for i, page in enumerate(doc):
        output_pdf = os.path.join(output_folder, f"{pdf_name}_page_{i+1}.pdf")
        new_doc = fitz.open()
        new_doc.insert_pdf(doc, from_page=i, to_page=i)
        new_doc.save(output_pdf)
        new_doc.close()
        print(f"Saved: {output_pdf}")

# Function to convert PDFs to Markdown
def convert_pdf_to_md(pdf_folder, md_folder):
    reader = SimpleDirectoryReader(pdf_folder)
    documents = reader.load_data()
    
    for i, doc in enumerate(documents):
        # Get the original filename and remove the ".pdf" extension
        original_name = doc.metadata["file_name"]
        cleaned_name = original_name.replace(".pdf", "")  # Removes the .pdf part

        md_path = os.path.join(md_folder, f"{cleaned_name}.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(doc.text)
        print(f"Converted: {md_path}")

# Process all PDF files in the documents folder
pdf_files = [f for f in os.listdir(documents_folder) if f.lower().endswith(".pdf")]

if not pdf_files:
    print("No PDF files found in the documents folder.")
else:
    for pdf_file in pdf_files:
        pdf_path = os.path.join(documents_folder, pdf_file)
        pdf_name = os.path.splitext(pdf_file)[0]  # Extract filename without extension
        print(f"Processing: {pdf_file}")

        # Extract pages and save them
        extract_pages(pdf_path, output_folder, pdf_name)

    # Convert extracted PDF pages to Markdown
    convert_pdf_to_md(output_folder, md_folder)
