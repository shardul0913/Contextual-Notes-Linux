import subprocess
def get():
    stacking_window_ids = subprocess.check_output("xprop -root  _NET_CLIENT_LIST_STACKING", shell = True)[:-1]              # exclude \n


    lable, window_ids = stacking_window_ids.split("# ")
    window_ids = window_ids.split(", ")

    window_stack = []

    for window_id in window_ids:
        window = subprocess.check_output("xprop -id "+window_id+" WM_NAME", shell = True)[:-1]      # exclude ""\n
	lable, window = window.split("= ")
	window = window[1:-1]
        if window == 'Tk' or window == 'Toplevel':
            continue
        else:
            window_stack.append(window)

    return window_stack[-1]
