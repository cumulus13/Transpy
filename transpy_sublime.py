import sublime
import sublime_plugin
import threading
import os
import sys

print("🚀 Transpy: Loading plugin...")

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

try:
    from transpy_sync import SyncTranslator, TranslationResult
    from transpy_history import HistoryManager
    print("✅ Transpy: All modules imported successfully")
except ImportError as e:
    error_msg = "❌ Transpy: Failed to import core module - {}".format(e)
    print(error_msg)
    sublime.error_message(error_msg)

class TranspyTranslateCommand(sublime_plugin.TextCommand):
    def run(self, edit, src_lang="auto", dest_lang="id", reverse=False, show_notification=True):
        print("🎯 Transpy: Command executed with args: src={}, dest={}".format(src_lang, dest_lang))
        
        # Get selected text or current line
        selections = self.view.sel()
        if not selections:
            sublime.status_message("Transpy: No text selected")
            return
        
        regions_to_translate = []
        
        for region in selections:
            if region.empty():
                # Get current line
                line = self.view.line(region)
                text = self.view.substr(line)
                if text.strip():
                    regions_to_translate.append((line, text))
            else:
                # Get selected text
                text = self.view.substr(region)
                if text.strip():
                    regions_to_translate.append((region, text))
        
        if not regions_to_translate:
            sublime.status_message("Transpy: No text to translate")
            return
        
        # Show progress
        sublime.status_message("🔄 Transpy: Translating {} selection(s)...".format(len(regions_to_translate)))
        
        # Translate each region
        for region, text in regions_to_translate:
            self.translate_region(region, text, src_lang, dest_lang, show_notification)

    def translate_region(self, region, text, src_lang, dest_lang, show_notification):
        """Translate text using threading"""
        
        def do_translation():
            try:
                # Perform translation (sync)
                translator = SyncTranslator()
                result = translator.translate(text, src_lang, dest_lang)
                
                # ✅ FIX: Check if result has is_error method dan jika error
                if hasattr(result, 'is_error') and result.is_error():
                    error_msg = result.get_error_message() if hasattr(result, 'get_error_message') else "Translation failed"
                    sublime.set_timeout(lambda: self.show_error(error_msg), 0)
                    return
                
                # Update UI in main thread
                sublime.set_timeout(lambda: self.replace_text(region, result.text, text, result, show_notification), 0)
                
            except Exception as e:
                error_msg = "Translation failed: {}".format(e)
                sublime.set_timeout(lambda: self.show_error(error_msg), 0)
        
        # Start translation in background thread
        thread = threading.Thread(target=do_translation)
        thread.daemon = True
        thread.start()
    
    def replace_text(self, region, translated_text, original_text, result, show_notification):
        """Replace text in the view - called from main thread"""
        try:
            # Use fresh edit object
            self.view.run_command("transpy_replace_text", {
                "region": [region.a, region.b],
                "text": translated_text,
                "original_text": original_text,
                "show_notification": show_notification
            })
                
        except Exception as e:
            self.show_error("Failed to replace text: {}".format(e))
    
    def show_success_notification(self, original, translated):
        """Show success notification"""
        # Shorten text for display
        if len(original) > 30:
            orig_short = original[:30] + "..."
        else:
            orig_short = original
            
        if len(translated) > 30:
            trans_short = translated[:30] + "..."
        else:
            trans_short = translated
        
        # Status bar message
        status_msg = "✅ Transpy: {} -> {}".format(orig_short, trans_short)
        sublime.status_message(status_msg)
        
        # Show in output panel
        self.show_in_output_panel(original, translated)
    
    def show_in_output_panel(self, original, translated):
        """Show translation in output panel"""
        try:
            panel = self.view.window().create_output_panel("transpy_output")
            panel.set_syntax_file("Packages/Text/Plain text.tmLanguage")
            
            output_text = "🌍 TRANSLATION RESULT:\n\nOriginal:\n{}\n\nTranslated:\n{}\n\n---\n".format(original, translated)
            panel.run_command("append", {"characters": output_text})
            self.view.window().run_command("show_panel", {"panel": "output.transpy_output"})
        except Exception as e:
            print("Transpy: Output panel error - {}".format(e))
    
    def show_error(self, message):
        """Show error message"""
        sublime.status_message("❌ Transpy: {}".format(message))
        # Jangan show error dialog untuk error biasa, cukup status message
        print("Transpy Error: {}".format(message))

class TranspyReplaceTextCommand(sublime_plugin.TextCommand):
    """Helper command to replace text with fresh edit object"""
    def run(self, edit, region, text, original_text, show_notification):
        try:
            # Convert list back to Region
            region_obj = sublime.Region(region[0], region[1])
            
            # Replace the text
            self.view.replace(edit, region_obj, text)
            
            # Show notification
            if show_notification:
                self.show_success_notification(original_text, text)
                
        except Exception as e:
            sublime.status_message("❌ Transpy: Replace failed - {}".format(e))
    
    def show_success_notification(self, original, translated):
        """Show success notification"""
        if len(original) > 30:
            orig_short = original[:30] + "..."
        else:
            orig_short = original
            
        if len(translated) > 30:
            trans_short = translated[:30] + "..."
        else:
            trans_short = translated
        
        sublime.status_message("✅ Transpy: {} -> {}".format(orig_short, trans_short))

class TranspyDebugCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        print("🔧 Transpy: DEBUG COMMAND EXECUTED!")
        sublime.message_dialog("🚀 Transpy Debug: Plugin is working!")
        
        # Test selections
        selections = self.view.sel()
        print("🔧 Transpy: Found {} selections".format(len(selections)))
        
        for i, region in enumerate(selections):
            if region.empty():
                line = self.view.line(region)
                text = self.view.substr(line)
                print("🔧 Selection {}: LINE - '{}'".format(i, text))
            else:
                text = self.view.substr(region)
                print("🔧 Selection {}: SELECTED - '{}'".format(i, text))

class TranspyDetectLanguageCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        selections = self.view.sel()
        if not selections:
            sublime.status_message("Transpy: No text selected for detection")
            return
        
        for region in selections:
            if region.empty():
                line = self.view.line(region)
                text = self.view.substr(line)
            else:
                text = self.view.substr(region)
            
            if text.strip():
                self.detect_language(text)
    
    def detect_language(self, text):
        def do_detection():
            try:
                translator = SyncTranslator()
                lang, confidence = translator.detect_language(text)
                sublime.set_timeout(lambda: self.show_detection_result(text, lang, confidence), 0)
            except Exception as e:
                sublime.set_timeout(lambda: sublime.status_message("❌ Transpy: Detection failed - {}".format(e)), 0)
        
        thread = threading.Thread(target=do_detection)
        thread.daemon = True
        thread.start()
    
    def show_detection_result(self, text, lang, confidence):
        """Show language detection result"""
        translator = SyncTranslator()
        lang_name = translator.get_language_name(lang)
        
        # Shorten text for display
        text_short = text[:40] + "..." if len(text) > 40 else text
        
        message = "🔍 Language: {} ({}) - Confidence: {:.2f}".format(lang, lang_name, confidence)
        sublime.status_message("Transpy: {}".format(message))
        
        # Show in output panel
        panel = self.view.window().create_output_panel("transpy_output")
        panel.run_command("append", {"characters": "🔍 LANGUAGE DETECTION:\n\nText: {}\nDetected: {} ({})\nConfidence: {:.2f}\n\n---\n".format(text, lang, lang_name, confidence)})
        self.view.window().run_command("show_panel", {"panel": "output.transpy_output"})


class TranspyShowHistoryCommand(sublime_plugin.WindowCommand):
    def run(self):
        """Show translation history"""
        sublime.status_message("Transpy: Loading history...")
        
        def show_history_async():
            try:
                history_mgr = HistoryManager()
                history = history_mgr.load_history()
                
                if not history:
                    sublime.set_timeout(lambda: sublime.status_message("📝 Transpy: No history found"), 0)
                    return
                
                # Create quick panel items - FIX: No f-strings!
                items = []
                for entry in history[-20:]:  # Last 20 entries
                    timestamp = entry['timestamp'][11:19]  # Time only
                    lang_pair = "{}→{}".format(entry['from_lang'], entry['to_lang'])
                    original_short = entry['original'][:30] + "..." if len(entry['original']) > 30 else entry['original']
                    # FIX: Gunakan format() bukan f-string
                    display_text = "{} {}: {}".format(timestamp, lang_pair, original_short)
                    items.append([display_text, entry['translated']])
                
                sublime.set_timeout(lambda: self.show_quick_panel(items), 0)
                
            except Exception as e:
                sublime.set_timeout(lambda: sublime.status_message("❌ Transpy: History error - {}".format(e)), 0)
        
        thread = threading.Thread(target=show_history_async)
        thread.daemon = True
        thread.start()
    
    def show_quick_panel(self, items):
        """Show history in quick panel"""
        def on_select(index):
            if index >= 0:
                # Copy selected translation to clipboard
                sublime.set_clipboard(items[index][1])
                sublime.status_message("✅ Transpy: Translation copied to clipboard")
        
        self.window.show_quick_panel(
            [item[0] for item in items],
            on_select,
            placeholder="Select translation to copy to clipboard"
        )

print("✅ Transpy: Plugin loaded successfully!")