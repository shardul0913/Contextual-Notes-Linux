import subprocess
def get():
    stacking_window_ids = subprocess.check_output("xprop -root  _NET_CLIENT_LIST_STACKING", shell = True)[:-1]              # exclude \n


    lable, window_ids = stacking_window_ids.split("# ")
    window_ids = window_ids.split(", ")

    window_stack = []

    for window_id in window_ids:
        window = subprocess.check_output("xprop -id "+window_id+" WM_CLASS | awk '{print $NF}'", shell = True)[1:-2]        # exclude ""\n
        if window == 'Tk' or window == 'Toplevel':
            continue
        else:
            window_stack.append(window)

    return window_stack[-1]
