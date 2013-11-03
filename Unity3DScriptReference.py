# written by Jacob Pennock (www.jacobpennock.com)
# based on WordPress Codex Search Plugin by Matthias Krok (www.welovewordpress.de)

# available commands
#   unity_reference_open_selection
#   unity_reference_search_selection
#   unity_reference_search_from_input

import sublime
import sublime_plugin

import subprocess
import webbrowser

def SearchUnityScriptReferenceFor(text):
    url = 'http://docs.unity3d.com/Documentation/ScriptReference/30_search.html?q=' + text.replace(' ','%20')
    webbrowser.open_new_tab(url)

def OpenUnityFunctionReference(text):
    url = 'http://docs.unity3d.com/Documentation/ScriptReference/' + text.replace(' ','%20') + '.html'
    webbrowser.open_new_tab(url)

class UnityReferenceOpenSelectionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for selection in self.view.sel():
            # if the user didn't select anything, search the currently highlighted word
            if selection.empty():
                selection = self.view.word(selection)

            text = self.view.substr(selection)
            
            # test for function and adjust string to match unity HTML scheme
            if text.find('(') == -1:
                n = text.find('.') + 1
                if text[n].isupper() == False:
                    text = text.replace('.', '-')
                    text = text[0].capitalize() + text[1:]
            else:
                text = text.replace('(','')
                text = text[0].capitalize() + text[1:]
                
            OpenUnityFunctionReference(text)

class UnityReferenceSearchSelectionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for selection in self.view.sel():
            # if the user didn't select anything, search the currently highlighted word
            if selection.empty():
                selection = self.view.word(selection)

            text = self.view.substr(selection)            
            SearchUnityScriptReferenceFor(text)

class UnityReferenceSearchFromInputCommand(sublime_plugin.WindowCommand):
    def run(self):
        # Check for any user selected text
        for selection in self.window.active_view().sel():
            # check to see if the user has anything selected
            if selection.empty() == False:
                # if the user has text selected, use that as the input
                selection = self.window.active_view().word(selection)
                text = self.window.active_view().substr(selection)
            else:
                # leave input blank if nothing selected
                text = ''
            
            # Open input panel using selection, if available; use input box to add text or modify
            self.window.show_input_panel('Search Unity Reference for', text,
                self.on_done, self.on_change, self.on_cancel)
    
    def on_done(self, input):
        SearchUnityScriptReferenceFor(input)

    def on_change(self, input):
        pass

    def on_cancel(self):
        pass
    
