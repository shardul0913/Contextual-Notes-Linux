import Tkinter
GM_KEYS = set(
        vars(Tkinter.Place).keys() +
        vars(Tkinter.Pack).keys() +
        vars(Tkinter.Grid).keys()
        )

class ScrolledFrame(object):
    _managed = False
    # XXX These could be options
    x_incr = 5
    y_incr = 5

    def __init__(self, master=None, **kw):
        self.width = kw.pop('width', 200)
        self.height = kw.pop('height', 200)

        self._canvas = Tkinter.Canvas(master, **kw)
        self.master = self._canvas.master
        self._hsb = Tkinter.Scrollbar(orient='horizontal',
                command=self._canvas.xview)
        self._vsb = Tkinter.Scrollbar(orient='vertical',
                command=self._canvas.yview)
        self._canvas.configure(
                xscrollcommand=self._hsb.set,
                yscrollcommand=self._vsb.set)

        self._placeholder = Tkinter.Frame(self._canvas)
        self._canvas.create_window(0, 0, anchor='nw', window=self._placeholder)

        self._placeholder.bind('<Map>', self._prepare_scroll)
        for widget in (self._placeholder, self._canvas):
            widget.bind('<Button-4>', self.scroll_up)
            widget.bind('<Button-5>', self.scroll_down)



    def __getattr__(self, attr):
        if attr in GM_KEYS:
            if not self._managed:
                # Position the scrollbars now.
                self._managed = True
                if attr == 'pack':
                    self._hsb.pack(side='bottom', fill='x')
                    self._vsb.pack(side='right', fill='y')
                elif attr == 'grid':
                    self._hsb.grid(row=1, column=0, sticky='ew')
                    self._vsb.grid(row=0, column=1, sticky='ns')
            return getattr(self._canvas, attr)

        else:
            return getattr(self._placeholder, attr)


    def yscroll(self, *args):
        self._canvas.yview_scroll(*args)


    def scroll_up(self, event=None):
        self.yscroll(-self.y_incr, 'units')


    def scroll_down(self, event=None):
        self.yscroll(self.y_incr, 'units')


    def see(self, event):
        widget = event.widget
        w_height = widget.winfo_reqheight()
        c_height = self._canvas.winfo_height()
        y_pos = widget.winfo_rooty()

        if (y_pos - w_height) < 0:
            # Widget focused is above the current view
            while (y_pos - w_height) < self.y_incr:
                self.scroll_up()
                self._canvas.update_idletasks()
                y_pos = widget.winfo_rooty()
        elif (y_pos - w_height) > c_height:
            # Widget focused is below the current view
            while (y_pos - w_height - self.y_incr) > c_height:
                self.scroll_down()
                self._canvas.update_idletasks()
                y_pos = widget.winfo_rooty()


    def _prepare_scroll(self, event):
        frame = self._placeholder
        frame.unbind('<Map>')

        if not frame.children:
            # Nothing to scroll.
            return

        for child in frame.children.itervalues():
            child.bind('<FocusIn>', self.see)

        width, height = frame.winfo_reqwidth(), frame.winfo_reqheight()
        self._canvas.configure(scrollregion=(0, 0, width, height),
                yscrollincrement=self.y_incr, xscrollincrement=self.x_incr)

        self._canvas.configure(width=self.width, height=self.height)

root = Tkinter.Tk()

sf = ScrolledFrame()
sf.grid(row=0, column=0, sticky='nsew')
sf.master.grid_columnconfigure(0, weight=1)
sf.master.grid_rowconfigure(0, weight=1)

for _ in range(10):
    lbl = Tkinter.Label(sf, text="Hi")
    lbl.pack()
    btn = Tkinter.Button(sf, text="Buh")
    btn.pack()
    entry = Tkinter.Entry(sf)
    entry.pack()

root.mainloop()

'''
from  Xlib.display import Display
from Xlib.Xatom import STRING


display = Display()
root = display.screen().root
#view the current WM_NAME
print root.get_full_property(display.intern_atom('_NET_WM_NAME'), STRING)



import wnck
import subprocess
stacking_window_ids = subprocess.check_output("xprop -root  _NET_CLIENT_LIST_STACKING", shell = True)[:-1]              # exclude \n


lable, window_ids = stacking_window_ids.split("# ")
window_ids = window_ids.split(", ")

window_stack = []

for window_id in window_ids:

	print window_id #, wnck.wnck_window_get_name(wnck.wnck_window_get(window_id)) 


import window_name_stack
import sys
window_title = window_stack.get()
print window_title
while 1:
	new_window_title = window_stack.get()
	if new_window_title != window_title :
		window_title = new_window_title
		print window_title
'''
