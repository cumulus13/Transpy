#!/usr/bin/env python3
# file: Transpy/transpy_sync.py
# Author: Hadi Cahyadi <cumulus13@gmail.com>
# Date: 2025-09-30 10:33:08.517073
# Description: 
# Synchronous version for Python 3.3 compatibility
# ZERO DEPENDENCIES - Only standard library
# License: MIT

import urllib.request
import urllib.parse
import json
import re  # Untuk sentence splitting

class SyncTranslator:
    """Synchronous translator using Google Translate API - No dependencies!"""
    
    def __init__(self):
        self.base_url = "https://translate.googleapis.com/translate_a/single"
        self.languages = self._load_languages()
        self.max_chars = 4500  # Google limit ~5000, kita kasih buffer
        self.max_lines = 50    # Prevent huge blocks
    
    def _load_languages(self):
        return {
            'af': 'afrikaans', 'sq': 'albanian', 'am': 'amharic', 'ar': 'arabic',
            'hy': 'armenian', 'az': 'azerbaijani', 'eu': 'basque', 'be': 'belarusian',
            'bn': 'bengali', 'bs': 'bosnian', 'bg': 'bulgarian', 'ca': 'catalan',
            'ceb': 'cebuano', 'ny': 'chichewa', 'zh-cn': 'chinese (simplified)',
            'zh-tw': 'chinese (traditional)', 'co': 'corsican', 'hr': 'croatian',
            'cs': 'czech', 'da': 'danish', 'nl': 'dutch', 'en': 'english',
            'eo': 'esperanto', 'et': 'estonian', 'tl': 'filipino', 'fi': 'finnish',
            'fr': 'french', 'fy': 'frisian', 'gl': 'galician', 'ka': 'georgian',
            'de': 'german', 'el': 'greek', 'gu': 'gujarati', 'ht': 'haitian creole',
            'ha': 'hausa', 'haw': 'hawaiian', 'iw': 'hebrew', 'he': 'hebrew',
            'hi': 'hindi', 'hmn': 'hmong', 'hu': 'hungarian', 'is': 'icelandic',
            'ig': 'igbo', 'id': 'indonesian', 'ga': 'irish', 'it': 'italian',
            'ja': 'japanese', 'jw': 'javanese', 'kn': 'kannada', 'kk': 'kazakh',
            'km': 'khmer', 'ko': 'korean', 'ku': 'kurdish (kurmanji)', 'ky': 'kyrgyz',
            'lo': 'lao', 'la': 'latin', 'lv': 'latvian', 'lt': 'lithuanian',
            'lb': 'luxembourgish', 'mk': 'macedonian', 'mg': 'malagasy', 'ms': 'malay',
            'ml': 'malayalam', 'mt': 'maltese', 'mi': 'maori', 'mr': 'marathi',
            'mn': 'mongolian', 'my': 'myanmar (burmese)', 'ne': 'nepali', 'no': 'norwegian',
            'or': 'odia', 'ps': 'pashto', 'fa': 'persian', 'pl': 'polish',
            'pt': 'portuguese', 'pa': 'punjabi', 'ro': 'romanian', 'ru': 'russian',
            'sm': 'samoan', 'gd': 'scots gaelic', 'sr': 'serbian', 'st': 'sesotho',
            'sn': 'shona', 'sd': 'sindhi', 'si': 'sinhala', 'sk': 'slovak',
            'sl': 'slovenian', 'so': 'somali', 'es': 'spanish', 'su': 'sundanese',
            'sw': 'swahili', 'sv': 'swedish', 'tg': 'tajik', 'ta': 'tamil',
            'te': 'telugu', 'th': 'thai', 'tr': 'turkish', 'uk': 'ukrainian',
            'ur': 'urdu', 'ug': 'uyghur', 'uz': 'uzbek', 'vi': 'vietnamese',
            'cy': 'welsh', 'xh': 'xhosa', 'yi': 'yiddish', 'yo': 'yoruba',
            'zu': 'zulu'
        }
    
    def validate_text(self, text):
        """Validate text before translation"""
        if not text or not text.strip():
            return False, "No text to translate"
        
        # Check character limit
        if len(text) > self.max_chars:
            return False, "Text too long ({} characters). Maximum is {} characters.".format(
                len(text), self.max_chars)
        
        # Check line limit
        line_count = text.count('\n') + 1
        if line_count > self.max_lines:
            return False, "Too many lines ({}). Maximum is {} lines per translation.".format(
                line_count, self.max_lines)
        
        return True, "OK"
    
    def translate(self, text, src='auto', dest='en'):
        """Synchronous translation with length validation"""
        # Validate text first
        is_valid, validation_msg = self.validate_text(text)
        if not is_valid:
            return TranslationResult("[ERROR] {}".format(validation_msg), src, 0.0)
        
        params = {
            'client': 'gtx',
            'dt': 't',
            'q': text,
            'sl': src,
            'tl': dest,
            'ie': 'UTF-8',
            'oe': 'UTF-8'
        }
        
        try:
            # Build URL
            query_string = urllib.parse.urlencode(params)
            url = "{}?{}".format(self.base_url, query_string)
            
            # Make request with timeout
            req = urllib.request.Request(
                url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                result_data = response.read().decode('utf-8')
                result = json.loads(result_data)
                
                if result and len(result) > 0 and result[0]:
                    # Extract translated text
                    translated = ''.join([part[0] for part in result[0] if part[0]])
                    
                    # Extract detected language
                    detected_lang = result[2] if len(result) > 2 and result[2] else src
                    
                    return TranslationResult(
                        text=translated,
                        detected_lang=detected_lang,
                        confidence=0.9 if detected_lang != 'auto' else 0.5
                    )
                else:
                    return TranslationResult(
                        "[ERROR] Invalid response from translation service",
                        src,
                        0.0
                    )
        
        except urllib.error.URLError as e:
            error_msg = "Network error: {}".format(e.reason if hasattr(e, 'reason') else str(e))
            return TranslationResult("[ERROR] {}".format(error_msg), src, 0.0)
        
        except urllib.error.HTTPError as e:
            error_msg = "HTTP error {}: {}".format(e.code, e.reason)
            return TranslationResult("[ERROR] {}".format(error_msg), src, 0.0)
        
        except Exception as e:
            error_msg = "Translation failed: {}".format(str(e))
            return TranslationResult("[ERROR] {}".format(error_msg), src, 0.0)
    
    def translate_large_text(self, text, src='auto', dest='en'):
        """
        Advanced feature: Split and translate large text in chunks
        Note: This is experimental and may not preserve context perfectly
        """
        # Validate first
        is_valid, validation_msg = self.validate_text(text)
        if is_valid:
            # Text is within limits, use normal translation
            return self.translate(text, src, dest)
        
        # If text is too large, split into chunks
        if len(text) > self.max_chars:
            chunks = self._split_text_chunks(text, self.max_chars - 100)  # Buffer for safety
            if len(chunks) == 1:
                # Even after splitting, one chunk is still too large
                return TranslationResult(
                    "[ERROR] Text too large to process. Please split manually.",
                    src,
                    0.0
                )
            
            results = []
            for i, chunk in enumerate(chunks):
                # FIX: Gunakan format() bukan f-string
                print("Translating chunk {}/{} ({} chars)...".format(
                    i + 1, len(chunks), len(chunk)))
                
                result = self.translate(chunk, src, dest)
                if result.is_error():  # ✅ Method ini HARUS ada di TranslationResult
                    return result
                results.append(result.text)
            
            # Combine results
            combined_text = "\n\n".join(results)
            return TranslationResult(combined_text, src, 0.8)  # Lower confidence for chunks
        
        return TranslationResult("[ERROR] {}".format(validation_msg), src, 0.0)
    
    def _split_text_chunks(self, text, chunk_size):
        """Split text into chunks at paragraph boundaries"""
        # First try to split by paragraphs
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            # If single paragraph is larger than chunk_size, split by sentences
            if len(paragraph) > chunk_size:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = ""
                
                # Split large paragraph by sentences
                sentences = self._split_sentences(paragraph)
                for sentence in sentences:
                    if len(current_chunk) + len(sentence) + 2 <= chunk_size:
                        current_chunk += sentence + " "
                    else:
                        if current_chunk:
                            chunks.append(current_chunk.strip())
                        current_chunk = sentence + " "
            else:
                if len(current_chunk) + len(paragraph) + 2 <= chunk_size:
                    current_chunk += paragraph + "\n\n"
                else:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = paragraph + "\n\n"
        
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def _split_sentences(self, text):
        """Simple sentence splitting (basic implementation)"""
        # Basic sentence splitting by common endings
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def detect_language(self, text):
        """Detect language of given text"""
        if not text or not text.strip():
            return 'auto', 0.0
        
        # Use shorter text for detection
        detection_text = text[:500] if len(text) > 500 else text
        
        try:
            params = {
                'client': 'gtx',
                'dt': 'at',
                'q': detection_text,
                'sl': 'auto',
                'tl': 'en'
            }
            
            query_string = urllib.parse.urlencode(params)
            url = "{}?{}".format(self.base_url, query_string)
            
            req = urllib.request.Request(
                url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                result_data = response.read().decode('utf-8')
                result = json.loads(result_data)
                
                if result and len(result) > 2 and result[2]:
                    detected_lang = result[2]
                    confidence = 0.9 if detected_lang != 'auto' else 0.5
                    return detected_lang, confidence
        
        except Exception as e:
            print("Transpy: Language detection error - {}".format(e))
        
        return 'auto', 0.0
    
    def get_language_name(self, code):
        """Get human-readable language name from code"""
        return self.languages.get(code, code)


class TranslationResult:
    """Translation result container - FIXED dengan semua method"""
    
    def __init__(self, text, detected_lang, confidence=0.0):
        self.text = text
        self.detected_lang = detected_lang
        self.confidence = confidence
    
    def is_error(self):
        """Check if result is an error message - METHOD YANG DIBUTUHKAN"""
        return isinstance(self.text, str) and self.text.startswith("[ERROR]")
    
    def get_error_message(self):
        """Extract error message if result is error"""
        if self.is_error():
            return self.text[8:]  # Remove "[ERROR] " prefix
        return None


# Test function untuk verifikasi semua method work
if __name__ == "__main__":
    print("=== TESTING TRANSPY SYNC ===")
    
    translator = SyncTranslator()
    
    # Test 1: Normal translation
    print("\n1. Testing normal translation...")
    result = translator.translate("Hello world", "auto", "id")
    print("   Result: {}".format(result.text))
    print("   Is error: {}".format(result.is_error()))
    
    # Test 2: Error translation (text too long)
    print("\n2. Testing error translation...")
    long_text = "A" * 5000
    result = translator.translate(long_text, "auto", "id")
    print("   Result: {}".format(result.text))
    print("   Is error: {}".format(result.is_error()))
    print("   Error message: {}".format(result.get_error_message()))
    
    # Test 3: Large text translation
    print("\n3. Testing large text translation...")
    large_text = "This is a test sentence. " * 300  # ~6000 chars
    result = translator.translate_large_text(large_text, "auto", "id")
    print("   Is error: {}".format(result.is_error()))
    print("   Success: {}".format(not result.is_error()))
    
    # Test 4: Language detection
    print("\n4. Testing language detection...")
    lang, confidence = translator.detect_language("Bonjour le monde")
    print("   Detected: {} (confidence: {})".format(lang, confidence))
    
    print("\n=== ALL TESTS COMPLETED ===")