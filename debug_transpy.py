import sublime
import sublime_plugin

class TranspyDebugCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        print("ðŸ”§ Transpy: Debug command executed!")
        sublime.status_message("Transpy: Debug command working!")
        
        # Test selection
        selections = self.view.sel()
        print("Selections:", len(selections))
        
        for i, region in enumerate(selections):
            if region.empty():
                line = self.view.line(region)
                text = self.view.substr(line)
                print("Selection", i, ": LINE - '" + text + "'")
            else:
                text = self.view.substr(region)
                print("Selection", i, ": TEXT - '%s'" % text)