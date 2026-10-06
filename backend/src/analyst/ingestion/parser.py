import os
import hashlib
from typing import List, Dict, Any
from unstructured.partition.pdf import partition_pdf

def compute_sha256(file_path: str) -> str:
    """Computes the SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def parse_pdf_document(file_path: str) -> List[Dict[str, Any]]:
    """
    Parses a PDF document using the unstructured library.
    Returns a list of blocks containing page numbers and text.
    """
    # Using partition_pdf from unstructured
    elements = partition_pdf(filename=file_path)
    
    blocks = []
    for i, element in enumerate(elements):
        text = str(element).strip()
        if not text:
            continue
        
        # unstructured elements sometimes contain page numbers in metadata
        page_num = 1
        if hasattr(element, "metadata") and element.metadata.page_number:
            page_num = element.metadata.page_number
            
        blocks.append({
            "block_index": i,
            "page": page_num,
            "text": text,
            "element_type": type(element).__name__
        })
        
    return blocks
