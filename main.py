import gui
import window_stack
class Main():

    def __init__(self):
        self.loop = 1

    def run(self):
        application_name = window_stack.get()
        gui_objects = gui.Main()
        gui_objects.present_application_name.config(text = application_name)
        gui_objects.new_button.config(command = lambda application = application_name : gui_objects.add_new(application))
        gui_objects.quit_button.config(command = self.stop)
        gui_objects.display_notes(application_name)
	

        while self.loop:	
            gui_objects.main_window.update_idletasks()
            gui_objects.main_window.update()
	    gui_objects.refresh()
            current_app = window_stack.get()
            if current_app != application_name:
                application_name = current_app
                gui_objects.present_application_name.config(text = application_name)
                gui_objects.new_button.config(command = lambda application = application_name : gui_objects.add_new(application))
                for child in gui_objects.framefornote.winfo_children():
                    child.destroy()
		#gui_objects.framefornote.destroy()
		gui_objects.display_notes(application_name)

    def stop(self):
        self.loop = 0

start = Main()
start.run()
