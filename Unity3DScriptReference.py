# written by Jacob Pennock (www.jacobpennock.com)
# based on WordPress Codex Search Plugin by Matthias Krok (www.welovewordpress.de)
# modified by Nicholas Killen (11/10/2013)

# available commands
#   unity_reference_open_selection
#   unity_reference_search_selection
#   unity_reference_search_from_input

import sublime
import sublime_plugin
import threading
import Queue

import subprocess
import webbrowser

def SearchUnityScriptReferenceFor(text):
    url = 'http://docs.unity3d.com/Documentation/ScriptReference/30_search.html?q=' + text.replace(' ','%20')
    webbrowser.open_new_tab(url)

def OpenUnityFunctionReference(text):
    url = 'http://docs.unity3d.com/Documentation/ScriptReference/' + text.replace(' ','%20') + '.html'
    webbrowser.open_new_tab(url)

def startProcess(processes, result_queue, text):
    process = threading.Thread(target=crawl, args=[result_queue, text])
    process.start()
    processes.append(process)

def crawl(result_queue, text):
    import urllib2
    try:
        url = 'http://docs.unity3d.com/Documentation/ScriptReference/' + text.replace(' ','%20') + '.html'
        data = urllib2.urlopen(url).read()
        result_queue.put(text) # send successful result back to parent thread
    except urllib2.URLError, e:
        pass
   
class UnityReferenceOpenSelectionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        processes = []
        result_queue = Queue.Queue()

        for selection in self.view.sel():
            # if the user didn't select anything, search the currently highlighted word
            if selection.empty():
                selection = self.view.word(selection)

            text = self.view.substr(selection)

            # spin off first thread to search for the unmodified selection
            startProcess(processes, result_queue, text)

            # second thread to search with capitalized selection
            secondText = text[0].capitalize() + text[1:]
            startProcess(processes, result_queue, secondText)

            # third thread to search for attributes instead of functions
            thirdText = text.replace('.', '-')
            thirdText = thirdText[0].capitalize() + thirdText[1:]
            startProcess(processes, result_queue, thirdText)

            # wait a short time for any results from threads
            try:
                # checks for a .put() from processes
                result = result_queue.get(True, 1) 
                OpenUnityFunctionReference(result)
            except:
                # if no hits, pass orignal text to Unity search page
                SearchUnityScriptReferenceFor(text)

            # join threads
            for process in processes: 
                process.join()

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
