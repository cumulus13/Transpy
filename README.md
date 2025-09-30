# 🌍 Transpy - Sublime Text Translation Plugin

[![Sublime Text](https://img.shields.io/badge/Sublime_Text-3+-orange.svg)](https://www.sublimetext.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-None!-success.svg)]()
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

> **Zero-dependency** instant translation right in your editor. No pip install required!

> Instant translation right in your editor. Select text and translate in real-time without leaving Sublime Text.

## ✨ Features

- 🚀 **Instant Translation**: Translate selected text or current line with hotkeys
- 🌐 **100+ Languages**: Support for all major languages via Google Translate
- 📝 **Smart Text Replacement**: Automatically replaces original text with translation
- 🔍 **Language Detection**: Auto-detect source language
- 📚 **Translation History**: Keep track of your translations
- ⌨️ **Customizable Hotkeys**: Configure your preferred key bindings
- 🎯 **Multi-Platform**: Works on Windows, macOS, and Linux
- 📊 **Output Panel**: View detailed translation results
- ⚡ **Non-Blocking**: Background translation without freezing UI

## 📋 Requirements

### System Requirements
- **Sublime Text 3+** or **Sublime Text 4**
- **Internet connection** (for Google Translate API)
- **No additional Python packages required**

### Zero Dependencies
This package uses only Python standard library and built-in Sublime Text APIs:
- `urllib.request` for HTTP requests
- `json` for data parsing  
- `threading` for background processing
- No `pip install` required!

### Network Access
The plugin requires internet access to:
- Google Translate API (`translate.googleapis.com`)
- No API key required (uses public endpoint)

## 🚀 Installation

### Via Package Control (Recommended)
1. Open Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`)
2. Type `Package Control: Install Package`
3. Search for `Transpy` and install

### Manual Installation
1. Download or clone this repository
2. Copy the `Transpy` folder to your Sublime Text Packages directory:
   - **Windows**: `%APPDATA%\Sublime Text\Packages\`
   - **macOS**: `~/Library/Application Support/Sublime Text/Packages/`
   - **Linux**: `~/.config/sublime-text/Packages/`
3. Restart Sublime Text

## 🎯 Quick Start

### Basic Translation
1. **Select text** or place cursor on a line
2. Press `Ctrl+Alt+T` (Windows/Linux) or `Cmd+Alt+T` (macOS)
3. Text is instantly translated and replaced!

### Available Commands
- `Ctrl+Alt+T` - Translate to Indonesian (default)
- `Ctrl+Alt+E` - Translate to English
- `Ctrl+Alt+Shift+T` - Reverse translation
- `Ctrl+Alt+D` - Detect language
- `Ctrl+Alt+H` - Show translation history

### Command Palette
Access all features via Command Palette (`Ctrl+Shift+P`):
- `Transpy: Translate Selection/Line`
- `Transpy: Translate to English` 
- `Transpy: Translate to Indonesian`
- `Transpy: Reverse Translation`
- `Transpy: Detect Language`
- `Transpy: Show Translation History`

## ⚙️ Configuration

### Settings
Access settings via:
- Command Palette: `Transpy: Open Settings`
- Menu: `Preferences > Package Settings > Transpy > Settings`

**Example Settings:**
```json
{
    "default_src_lang": "auto",
    "default_dest_lang": "id",
    "show_output_panel": true,
    "auto_copy_to_clipboard": false,
    "enable_history": true
}
```

### Key Bindings
Customize key bindings via:
- Command Palette: `Transpy: Key Bindings`
- Menu: `Preferences > Package Settings > Transpy > Key Bindings`

**Example Key Bindings:**
```json
{
    "keys": ["ctrl+alt+t"],
    "command": "transpy_translate",
    "args": {"dest_lang": "id"}
}
```

## 🌐 Supported Languages

Transpy supports 100+ languages including:

| Code | Language | Code | Language |
|------|----------|------|----------|
| `en` | English | `id` | Indonesian |
| `es` | Spanish | `fr` | French |
| `de` | German | `ja` | Japanese |
| `ko` | Korean | `zh-cn` | Chinese (Simplified) |
| `ar` | Arabic | `ru` | Russian |
| `pt` | Portuguese | `it` | Italian |

[View all supported languages](https://cloud.google.com/translate/docs/languages)

## 🛠️ Usage Examples

### Translate Selected Text
```javascript
// Select this text and press Ctrl+Alt+T
const greeting = "Hello World";

// Becomes:
const greeting = "Halo Dunia";
```

### Translate Current Line
```python
# Place cursor anywhere on this line and press Ctrl+Alt+E
print("Selamat pagi")

# Becomes:
print("Good morning")
```

### Reverse Translation
```python
# Select text and press Ctrl+Alt+Shift+T
print("Good morning")

# Becomes (if original was Indonesian):
print("Selamat pagi")
```

## 🔧 Advanced Features

### Language Detection
Select text and use `Ctrl+Alt+D` to detect the language. Results show in the output panel with confidence score.

### Translation History
Access your last 100 translations with `Ctrl+Alt+H`. Select any entry to copy the translation to clipboard.

### Output Panel
Detailed translation results are shown in the output panel, including:
- Original text
- Translated text  
- Detected language
- Confidence score

### Custom Language Pairs
Override default languages in key bindings:
```json
{
    "keys": ["ctrl+alt+f"],
    "command": "transpy_translate",
    "args": {"src_lang": "en", "dest_lang": "fr"}
}
```

## ❓ Troubleshooting

### Common Issues

**Q: Do I need to install Python packages?**
A: **No!** This package has zero dependencies. Everything works out of the box.

**Q: Translation fails with connection error**
A: Check your internet connection and firewall settings. The plugin needs access to `translate.googleapis.com`.

**Q: "No module named..." error**
A: This shouldn't happen with the latest version. Please ensure you have the complete package files.

**Q: Plugin works but very slow**
A: Translation speed depends on your internet connection and Google Translate API response times.

### Debug Mode
Enable verbose logging in settings:
```json
{
    "verbose_logging": true
}
```

Check the console (`Ctrl+``) for detailed logs.

## 📏 Limits & Best Practices

### Translation Limits
- **Character Limit**: 4,500 characters per translation
- **Line Limit**: 50 lines per translation  
- **Rate Limit**: ~100 requests per 100 seconds (Google API)

### Best Practices
1. **For long documents**: Split into paragraphs and translate separately
2. **For code files**: Translate comments selectively, not entire files
3. **Optimal size**: 100-1000 characters for fastest results
4. **Multiple selections**: Translate multiple small selections instead of one large block

### Error Messages
You may encounter these limits:
- `"Text too long (XXXX characters). Maximum is 4500 characters."`
- `"Too many lines (XX). Maximum is 50 lines per translation."`

### Performance Tips
- Smaller texts translate faster and more accurately
- Internet connection affects translation speed
- Complex sentences may take longer to process

## 🤝 Contributing

We welcome contributions! Please feel free to submit pull requests, report bugs, or suggest new features.

### Development Setup
1. Fork the repository
2. Clone to your Sublime Text Packages directory
3. Make changes and test
4. Submit a pull request

### Reporting Issues
When reporting issues, please include:
- Sublime Text version
- Operating system
- Error messages from console
- Steps to reproduce

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Translate API for translation services
- Sublime Text team for the amazing editor
- Contributors and testers

---

**Happy Translating!** 🌍✨

If you find this plugin useful, please consider giving it a ⭐ on GitHub!
```

## 🚀 **DEPLOYMENT STEPS:**

1. **Create GitHub Repository** named "Transpy"
2. **Upload all files** from the package structure
3. **Create release** `v1.0.0` with zip package
4. **Submit to Package Control** (optional but recommended)
5. **Update documentation** with your GitHub repo links

## 📋 **PRE-DEPLOYMENT CHECKLIST:**

- [ ] Test on all platforms (Windows, Mac, Linux)
- [ ] Verify all key bindings work
- [ ] Test internet connectivity requirements
- [ ] Check console for any errors
- [ ] Update README with actual repository links
- [ ] Add screenshots/GIFs to README (optional but helpful)

Your package is now ready for public release! 🎉

## author
[Hadi Cahyadi](mailto:cumulus13@gmail.com)
    

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/cumulus13)

[![Donate via Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/cumulus13)

[Support me on Patreon](https://www.patreon.com/cumulus13)