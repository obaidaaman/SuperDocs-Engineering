import os
import hashlib
from typing import List, Dict, Any
from unstructured_transform_client import TransformClient
from dotenv import load_dotenv
import certifi

# Fix macOS SSL Certificate error
os.environ["SSL_CERT_FILE"] = certifi.where()

load_dotenv()

def compute_sha256(file_path: str) -> str:
    """Computes the SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def parse_pdf_document(file_path: str, filename: str) -> List[Dict[str, Any]]:
    """
    Parses a PDF document using the Unstructured Transform API.
    Returns a list of blocks containing page numbers and text.
    """
    client = TransformClient(
        api_key=os.getenv("UNSTRUCTURED_API_KEY")
    )

    try:
        with open(file_path, "rb") as f:
            response = client.parse.run(input=f, output="elements")
        
        # We need to adapt the response into our standard block format
        blocks = []
        # I get a list of elements directly or inside a result 
        elements = response.elements if hasattr(response, 'elements') else response
        
        # added the return for diff response format
        if not hasattr(elements, '__iter__') or isinstance(elements, dict):
            elements = getattr(elements, 'elements', getattr(response, 'items', response))
            
        # enumeration happening , looping through all elements.
        for i, element in enumerate(elements):
            
            
            text = element.get("text", "") if isinstance(element, dict) else getattr(element, "text", "")
            if not text:
                continue
                
            text = str(text).strip()
            if not text:
                continue
                
       
            page_num = 1
            metadata = element.get("metadata", {}) if isinstance(element, dict) else getattr(element, "metadata", {})
            
            if hasattr(metadata, "page_number"):
                page_num = getattr(metadata, "page_number")
            elif isinstance(metadata, dict) and "page_number" in metadata:
                page_num = metadata["page_number"]
                
            element_type = element.get("type", "Unknown") if isinstance(element, dict) else getattr(element, "type", "Unknown")
                
            blocks.append({
                "block_index": i,
                "page": page_num,
                "text": text,
                "element_type": element_type
            })

        print(f"\\n--- PARSER SUCCESS ---")
        print(f"Total Blocks Extracted: {len(blocks)}")
        
        
        return blocks

    except Exception as e:
        print(f"Error parsing document via Unstructured Transform API: {e}")
        raise e
