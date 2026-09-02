"""
Multilingual Pedagogical Translation Service
Translates educational scripts and captions between English, Hindi, and Hinglish while preserving concept state.
"""

from typing import Dict, Any

class MultilingualEngineService:
    def __init__(self):
        self.translations: Dict[str, Dict[str, Dict[str, str]]] = {
            "voltage": {
                "English": {
                    "title": "Visual Model: Voltage as Electric Pressure",
                    "caption": '"Voltage is the force that pushes electrical charge through a circuit."',
                    "status": "Dr. Aris is explaining..."
                },
                "Hindi": {
                    "title": "दृश्य मॉडल: विद्युत दबाव के रूप में वोल्टेज",
                    "caption": '"वोल्टेज वह विद्युत दबाव है जो किसी परिपथ में आवेश को प्रवाहित करता है।"',
                    "status": "डॉ. एरिस समझा रहे हैं..."
                },
                "Hinglish": {
                    "title": "Visual Model: Voltage as Electric Pressure",
                    "caption": '"Voltage basically ek electric pressure ya push hai jo charges ko circuit mein aage badhata hai."',
                    "status": "Dr. Aris samjha rahe hain..."
                }
            },
            "resistance": {
                "English": {
                    "title": "Resistance: Material Opposition & Thermal Dissipation",
                    "caption": '"Resistance measures how strongly a material resists current flow, turning electrical energy into light and warmth."',
                    "status": "Dr. Aris is explaining..."
                },
                "Hindi": {
                    "title": "प्रतिरोध: सामग्री का विरोध और तापीय अपव्यय",
                    "caption": '"प्रतिरोध यह मापता है कि कोई सामग्री धारा प्रवाह का कितना विरोध करती है।"',
                    "status": "डॉ. एरिस समझा रहे हैं..."
                },
                "Hinglish": {
                    "title": "Resistance: Material Opposition & Thermal Dissipation",
                    "caption": '"Resistance basically electron ke raste ki rukawat hai jo current ke flow ko slow karti hai."',
                    "status": "Dr. Aris samjha rahe hain..."
                }
            },
            "water_pipe": {
                "English": {
                    "title": "Alternative Model: Water-Pipe Analogy",
                    "caption": '"Think of resistance as narrowing a water pipe: with the same pressure, fewer gallons flow per minute. That is why current must drop."',
                    "status": "Dr. Aris adapted the explanation"
                },
                "Hindi": {
                    "title": "वैकल्पिक मॉडल: पानी की पाइप उपमा",
                    "caption": '"प्रतिरोध को एक संकीर्ण पानी के पाइप की तरह समझें: समान दबाव के साथ, कम पानी प्रवाहित होता है। इसीलिए धारा घटती है।"',
                    "status": "डॉ. एरिस ने व्याख्या को अनुकूलित किया"
                },
                "Hinglish": {
                    "title": "Alternative Model: Water-Pipe Analogy",
                    "caption": '"Resistance ko ek patle water-pipe ki tarah samjhein: same pressure hone par bhi kam paani flow hota hai. Isliye current decrease hota hai."',
                    "status": "Dr. Aris ne explanation adapt kiya"
                }
            }
        }

    def translate_lesson_context(self, concept: str, target_language: str) -> Dict[str, Any]:
        """
        Translates current concept title, caption, and teacher status into the requested target language.
        """
        normalized_concept = concept.lower()
        if "pipe" in normalized_concept:
            concept_key = "water_pipe"
        elif "resist" in normalized_concept:
            concept_key = "resistance"
        else:
            concept_key = "voltage"

        lang_data = self.translations.get(concept_key, {}).get(target_language)
        if not lang_data:
            lang_data = self.translations[concept_key]["Hinglish"]

        return {
            "concept": concept,
            "target_language": target_language,
            "title": lang_data["title"],
            "caption": lang_data["caption"],
            "status": lang_data["status"]
        }
