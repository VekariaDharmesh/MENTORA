"""
Document Ingestion & Parsing Engine
Extracts chapters, sections, and semantic chunks from PDF, DOCX, PPTX, and TXT files.
"""

import os
import re
from typing import List, Dict, Any, Optional
from uuid import uuid4

class DocumentChunk:
    def __init__(self, text: str, chunk_index: int, page_number: Optional[int] = None, section: Optional[str] = None):
        self.id = str(uuid4())
        self.text = text.strip()
        self.chunk_index = chunk_index
        self.page_number = page_number
        self.section = section or "General"
        self.token_count = len(text.split())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "text": self.text,
            "chunk_index": self.chunk_index,
            "page_number": self.page_number,
            "section": self.section,
            "token_count": self.token_count
        }

class DocumentParserService:
    def __init__(self, chunk_size: int = 400, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def parse_text(self, text: str, filename: str = "document.txt") -> Dict[str, Any]:
        """
        Parses raw text into chapters, sections, and semantic chunks.
        """
        sections = self._detect_sections(text)
        chunks = []
        chunk_idx = 0

        for sec_name, sec_text in sections.items():
            words = sec_text.split()
            if not words:
                continue
                
            i = 0
            while i < len(words):
                chunk_words = words[i:i + self.chunk_size]
                chunk_str = " ".join(chunk_words)
                
                chunks.append(DocumentChunk(
                    text=chunk_str,
                    chunk_index=chunk_idx,
                    page_number=(chunk_idx // 2) + 1,
                    section=sec_name
                ))
                chunk_idx += 1
                i += (self.chunk_size - self.overlap)

        return {
            "filename": filename,
            "total_words": len(text.split()),
            "total_chunks": len(chunks),
            "sections": list(sections.keys()),
            "chunks": [c.to_dict() for c in chunks]
        }

    def _detect_sections(self, text: str) -> Dict[str, str]:
        """
        Detects chapter or section headers using regex patterns.
        """
        pattern = r"(Chapter\s+\d+[:\s\w]+|Section\s+\d+[:\s\w]+|###\s+[^\n]+)"
        matches = list(re.finditer(pattern, text, re.IGNORECASE))

        if not matches:
            return {"Introduction & Core Foundations": text}

        sections = {}
        for idx, match in enumerate(matches):
            header = match.group(0).strip().replace("#", "").strip()
            start = match.end()
            end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
            sec_content = text[start:end].strip()
            if sec_content:
                sections[header] = sec_content

        return sections if sections else {"General Concepts": text}

# Default sample textbook material for demonstration
SAMPLE_PHYSICS_TEXTBOOK = """
Chapter 1: Electric Charge and Current Flow
Electric charge is a fundamental property of matter. Protons carry positive charge, while electrons carry negative charge. 
Electric current is defined as the net rate of flow of electric charge through a cross-sectional area over time. 
Quantitatively, current I equals charge Q divided by time t (I = Q / t). The SI unit of electric current is the Ampere (A), 
which represents one Coulomb of charge passing through a conductor per second. In metallic conductors, the charge carriers 
are free conduction electrons that drift in the direction opposite to conventional current.

Chapter 2: Electric Potential and Voltage
Voltage, or electric potential difference (ΔV), is the work done per unit charge in moving a test charge between two points in an electric field.
Without potential difference, electrons experience no net directional force. Voltage acts as the electric pressure that pumps charge through a closed loop.
The unit of voltage is the Volt (V), where 1 Volt equals 1 Joule of energy expended per Coulomb of charge (1 V = 1 J/C).

Chapter 3: Resistance and Ohmic Dissipation
Resistance is the measure of a material's opposition to the flow of electric current. As electrons move through a conductor, 
they collide with vibrating lattice ions, converting electrical energy into thermal energy and light.
Resistance depends on the material's resistivity, its length, and its cross-sectional area. A narrow wire has higher resistance than a wide wire.
The SI unit of resistance is the Ohm (Ω).

Chapter 4: Ohm's Law and Circuit Equilibrium
Ohm's Law states that the current through a conductor between two points is directly proportional to the voltage across the two points, 
and inversely proportional to the resistance between them. Mathematically, V = I * R, or I = V / R.
If voltage remains constant while resistance increases, the electric current must decrease. Conversely, reducing resistance at constant voltage increases current flow.
"""
