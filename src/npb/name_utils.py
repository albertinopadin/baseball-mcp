"""Japanese name handling utilities for NPB."""

import re
from typing import List, Tuple

# Common romanization variations
ROMANIZATION_VARIANTS = {
    'ou': ['o', 'oh', 'oo'],
    'oo': ['o', 'oh', 'ou'],
    'oh': ['o', 'oo', 'ou'],
    'uu': ['u', 'uh'],
    'ei': ['e'],
    'ii': ['i'],
    'shi': ['si'],
    'chi': ['ti'],
    'tsu': ['tu'],
    'fu': ['hu'],
    'ji': ['zi', 'di'],
    'zu': ['du'],
    'sha': ['sya'],
    'shu': ['syu'],
    'sho': ['syo'],
    'cha': ['tya'],
    'chu': ['tyu'],
    'cho': ['tyo'],
    'ja': ['zya', 'dya'],
    'ju': ['zyu', 'dyu'],
    'jo': ['zyo', 'dyo'],
}

# Common name order patterns
JAPANESE_NAME_PATTERNS = [
    # Last First (Western order)
    r'^([A-Z][a-z]+)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)$',
    # First Last (Japanese order)
    r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+([A-Z][a-z]+)$',
]


def normalize_name(name: str) -> str:
    """Normalize a name for searching.
    
    Args:
        name: Name to normalize
        
    Returns:
        Normalized name
    """
    # Basic normalization
    normalized = name.lower().strip()
    
    # Remove special characters
    normalized = re.sub(r'[^\w\s-]', '', normalized)
    
    # Normalize whitespace
    normalized = re.sub(r'\s+', ' ', normalized)
    
    # Apply common romanization normalizations
    for variant, replacements in ROMANIZATION_VARIANTS.items():
        if variant in normalized:
            # Use the first (most common) replacement
            normalized = normalized.replace(variant, replacements[0])
    
    return normalized


def generate_name_variants(name: str) -> List[str]:
    """Generate possible variants of a name.
    
    Args:
        name: Original name
        
    Returns:
        List of name variants
    """
    variants = [name]
    normalized = normalize_name(name)
    
    # Add normalized version
    if normalized != name.lower():
        variants.append(normalized)
    
    # Generate romanization variants
    for original, replacements in ROMANIZATION_VARIANTS.items():
        for replacement in replacements:
            if original in normalized:
                variant = normalized.replace(original, replacement)
                if variant not in variants:
                    variants.append(variant)
    
    # Try swapping first/last name order
    parts = name.split()
    if len(parts) == 2:
        swapped = f"{parts[1]} {parts[0]}"
        variants.append(swapped)
        variants.append(normalize_name(swapped))
    
    return list(set(variants))  # Remove duplicates


def parse_japanese_name(name: str) -> Tuple[str, str]:
    """Parse a name into first and last components.
    
    Args:
        name: Full name
        
    Returns:
        Tuple of (first_name, last_name)
    """
    parts = name.strip().split()
    
    if len(parts) == 0:
        return "", ""
    elif len(parts) == 1:
        return parts[0], ""
    elif len(parts) == 2:
        # Could be either order
        # For NPB, typically see Last First format
        return parts[1], parts[0]
    else:
        # Multiple parts - assume last part is first name
        return parts[-1], " ".join(parts[:-1])


def match_name(search_name: str, candidate_name: str, strict: bool = False) -> bool:
    """Check if two names match.
    
    Args:
        search_name: Name being searched for
        candidate_name: Name to match against
        strict: If True, only exact normalized matches count
        
    Returns:
        True if names match
    """
    if strict:
        return normalize_name(search_name) == normalize_name(candidate_name)
    
    # Try exact match first
    if normalize_name(search_name) == normalize_name(candidate_name):
        return True
    
    # Handle "Last, First" format used by NPB
    if ',' in candidate_name:
        parts = candidate_name.split(',')
        if len(parts) == 2:
            last_name = parts[0].strip()
            first_name = parts[1].strip()
            # Check if search matches last name
            if normalize_name(search_name) == normalize_name(last_name):
                return True
            # Check if search matches first name
            if normalize_name(search_name) == normalize_name(first_name):
                return True
            # Check if search matches "First Last" format
            western_format = f"{first_name} {last_name}"
            if normalize_name(search_name) == normalize_name(western_format):
                return True
    
    # Try variants
    search_variants = generate_name_variants(search_name)
    candidate_normalized = normalize_name(candidate_name)
    
    for variant in search_variants:
        if variant == candidate_normalized:
            return True
    
    # Try partial matching (last name only)
    search_parts = search_name.split()
    candidate_parts = candidate_name.replace(',', '').split()
    
    if len(search_parts) == 1:
        # Searching by single name - check if it matches any part
        search_norm = normalize_name(search_parts[0])
        for part in candidate_parts:
            if normalize_name(part) == search_norm:
                return True
    
    return False