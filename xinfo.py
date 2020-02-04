import subprocess

def get_recent_application_name():

    # get window class name having id ( second last window in stack ) 
    # stack : recent , Knote                                            <-- system dependent??
    recent_application = subprocess.check_output("xprop -id $(xprop -root  _NET_CLIENT_LIST_STACKING | awk '{print $(NF-1)}') WM_CLASS | awk '{print $NF}'", shell = True)
    return recent_application[1:-2]
