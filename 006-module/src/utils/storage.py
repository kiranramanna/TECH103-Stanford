"""
Storage utilities for persisting embeddings and vector database.
"""
import os
import pickle
from pathlib import Path
import numpy as np
from typing import Optional, Tuple, Dict, Any

# Define storage paths
STORAGE_DIR = Path("storage")
EMBEDDINGS_DIR = STORAGE_DIR / "embeddings"
QDRANT_DIR = STORAGE_DIR / "qdrant_vdb"

def ensure_directories():
    """Create storage directories if they don't exist."""
    STORAGE_DIR.mkdir(exist_ok=True)
    EMBEDDINGS_DIR.mkdir(exist_ok=True)
    QDRANT_DIR.mkdir(exist_ok=True)

def save_embeddings(engine_name: str, embeddings: np.ndarray, metadata: Dict[str, Any]):
    """Save embeddings and metadata to disk.
    
    Args:
        engine_name: Name of the search engine
        embeddings: Numpy array of embeddings
        metadata: Dictionary of metadata
    """
    ensure_directories()
    
    # Save embeddings
    embeddings_path = EMBEDDINGS_DIR / f"{engine_name}_embeddings.npy"
    np.save(embeddings_path, embeddings)
    
    # Save metadata
    metadata_path = EMBEDDINGS_DIR / f"{engine_name}_metadata.pkl"
    with open(metadata_path, 'wb') as f:
        pickle.dump(metadata, f)

def load_embeddings(engine_name: str) -> Optional[Tuple[np.ndarray, Dict[str, Any]]]:
    """Load embeddings and metadata from disk.
    
    Args:
        engine_name: Name of the search engine
        
    Returns:
        Tuple of (embeddings, metadata) if found, None otherwise
    """
    embeddings_path = EMBEDDINGS_DIR / f"{engine_name}_embeddings.npy"
    metadata_path = EMBEDDINGS_DIR / f"{engine_name}_metadata.pkl"
    
    if not (embeddings_path.exists() and metadata_path.exists()):
        return None
    
    # Load embeddings
    embeddings = np.load(embeddings_path)
    
    # Load metadata
    with open(metadata_path, 'rb') as f:
        metadata = pickle.load(f)
    
    return embeddings, metadata

def get_qdrant_path() -> Path:
    """Get the path to the Qdrant vector database directory.
    
    Returns:
        Path to Qdrant directory
    """
    ensure_directories()
    return QDRANT_DIR 