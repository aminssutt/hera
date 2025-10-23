import json
import os
from deep_translator import GoogleTranslator

# Language codes mapping for deep-translator
LANGUAGES = {
    'fr': 'fr',  # French
    'ko': 'ko',  # Korean
    'zh': 'zh-CN',  # Chinese Simplified
    'ja': 'ja',  # Japanese
    'es': 'es'   # Spanish
}

def load_json(filepath):
    """Load JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading {filepath}: {e}")
        return {}

def save_json(filepath, data):
    """Save JSON file with proper formatting"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ Saved: {filepath}")
    except Exception as e:
        print(f"❌ Error saving {filepath}: {e}")

def translate_text(text, target_lang):
    """Translate text using Google Translate (free)"""
    try:
        # Skip if text contains template variables
        if '{' in text or '<' in text:
            return text
        
        translator = GoogleTranslator(source='en', target=target_lang)
        translated = translator.translate(text)
        return translated
    except Exception as e:
        print(f"    ⚠️ Translation error: {e}")
        return text  # Return original if translation fails

def get_value_from_dict(d, key_path):
    """Get value from nested dict using dot notation"""
    keys = key_path.split('.')
    current = d
    for key in keys:
        if key not in current:
            return None
        current = current[key]
    return current

def set_nested_key(d, key_path, value):
    """Set a value in nested dict using dot notation"""
    keys = key_path.split('.')
    current = d
    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]
    current[keys[-1]] = value

def get_all_keys_from_dict(d, parent_key=''):
    """Recursively get all keys from nested dict"""
    keys = []
    for k, v in d.items():
        current_key = f"{parent_key}.{k}" if parent_key else k
        if isinstance(v, dict):
            keys.extend(get_all_keys_from_dict(v, current_key))
        else:
            keys.append(current_key)
    return keys

def translate_missing_keys():
    """Main function to translate missing keys"""
    base_path = 'src/i18n/locales'
    
    # Load English (source)
    en_file = os.path.join(base_path, 'en.json')
    print(f"📖 Loading English translations from {en_file}")
    en_data = load_json(en_file)
    
    if not en_data:
        print("❌ Failed to load English file. Exiting.")
        return
    
    # Get all English keys
    en_keys = get_all_keys_from_dict(en_data)
    print(f"📚 Found {len(en_keys)} keys in English file\n")
    
    # Process each target language
    for lang_code, translator_code in LANGUAGES.items():
        print(f"🌍 Processing {lang_code.upper()}...")
        
        target_file = os.path.join(base_path, f'{lang_code}.json')
        target_data = load_json(target_file)
        
        if not target_data:
            print(f"  ⚠️ Creating new file for {lang_code}")
            target_data = {}
        
        # Get existing keys in target language
        existing_keys = get_all_keys_from_dict(target_data)
        
        # Find missing keys
        missing_keys = [k for k in en_keys if k not in existing_keys]
        
        if not missing_keys:
            print(f"  ✅ No missing keys for {lang_code}\n")
            continue
        
        print(f"  🔄 Found {len(missing_keys)} missing keys. Translating...")
        
        # Translate missing keys
        for i, key_path in enumerate(missing_keys, 1):
            en_value = get_value_from_dict(en_data, key_path)
            if en_value:
                print(f"  [{i}/{len(missing_keys)}] {key_path}")
                translated_value = translate_text(en_value, translator_code)
                set_nested_key(target_data, key_path, translated_value)
        
        # Save updated file
        save_json(target_file, target_data)
        print(f"  ✨ Completed {lang_code}\n")

if __name__ == "__main__":
    print("="*60)
    print("🚀 AUTOMATIC TRANSLATION SCRIPT")
    print("="*60 + "\n")
    
    try:
        translate_missing_keys()
        print("\n" + "="*60)
        print("🎉 Translation complete!")
        print("="*60)
    except Exception as e:
        print(f"\n❌ Script error: {e}")
        import traceback
        traceback.print_exc()
