import threading
import PySimpleGUI as sg
import inspect
import os

# Function to create a dictionary with parameters for an expandable GUI element
def expandable(size: tuple = (None, None)):
    return {"size": size, "resizable": True, "scrollable": True, "auto_size_text": True, "expand_x": True, "expand_y": True}

# Function to change a global variable with the given name to a new value
def change_glob(string: str, obj: any):
    globals()[string] = obj
    return obj

# Initialize 'all_windows' global variable to store information about active windows
change_glob('all_windows', {'last_window': {'name': '', 'values': {}, 'event': ''}})

# Function to get the value of a global variable by name
def get_glob(obj: str = '', glob=globals()):
    try:
        return glob[obj]
    except KeyError:
        print(f"No global object named '{obj}'")
        return None

# Function to call a function dynamically, either from globals or an instance
def call_functions(function_name: str, args: dict = None, instance=None, glob=globals()):
    if glob is None:
        glob = globals()
    if args is None:
        args = {}
    if instance is not None:
        # Calls method on instance
        method = getattr(instance, function_name)
        return method(*args) if isinstance(args, list) else method(**args)
    else:
        # Calls function from globals
        function = glob[function_name]
        return function(*args) if isinstance(args, list) else function(**args)

# Function to process arguments, checking for 'get' key and calling the corresponding function if needed
def process_args(args):
    for key, value in args.items():
        # check if value is a dict and has a 'type' key with value 'get'
        if isinstance(value, dict) and value.get('type') == 'get':
            function_name = value['name']
            function_args = value.get('args', {})
            instance = value.get('instance')
            glob = value.get('global')
            # call the function and replace the arg with its result
            args[key] = call_functions(function_name, function_args, instance, glob)
    return args

# Function to retrieve function details from a dictionary, process arguments, and call the function
def get_fun(js):
    # Get function details
    function_name = js['name']
    function_args = js.get('args', {})
    instance = js.get('instance')
    glob = js.get('global')
    # Process arguments
    function_args = process_args(function_args)
    # If instance is not None, get the function from the instance, else get from globals
    if instance is not None:
        function = getattr(instance, function_name)
    else:
        function = glob[function_name]
    # Get function's valid parameter keys
    sig = inspect.signature(function)
    valid_keys = sig.parameters.keys()
    # Filter arguments to only those accepted by the function
    filtered_args = {k: v for k, v in function_args.items() if k in valid_keys}
    return call_functions(function_name, filtered_args, instance, glob)

# Functions related to progress bars

# Function to update the progress of a ProgressBar element in the GUI
def update_progress(win: str = 'progress_window', st: str = 'bar', progress: (int or float) = 0):
    win[st].update_bar(progress)

# Function to create a ProgressBar element
def get_progress_bar(max_value: int = 100, size: tuple = (30, 10), key: str = 'bar'):
    return get_gui_fun('ProgressBar', {"max_value": max_value, "size": size, "key": key})

# Functions related to creating windows

# Function to create a PySimpleGUI Window
def get_window(title: str = 'basic window', layout: list = [[]]):
    return sg.Window(title, layout)

# Function to verify if an object is a PySimpleGUI Window
def verify_window(win: any = None):
    if type(win) == str:
        win = get_glob(obj=win)
    if type(win) == type(get_window()):
        return True
    return False

# Function to close a PySimpleGUI Window
def close_window(win: any = None):
    if verify_window(win):
        win.close()

# Function to get a GUI element using PySimpleGUI's Element methods
def get_gui_fun(name: str = '', args: dict = {}):
    import PySimpleGUI
    return get_fun({"instance": PySimpleGUI, "name": name, "args": args})

# Functions related to checking conditions

# Function to check if a window was closed
def win_closed(event: str = ''):
    return T_or_F_obj_eq(event=event, obj=sg.WIN_CLOSED)

# Function to check if two objects are equal
def T_or_F_obj_eq(event: any = '', obj: any = ''):
    return True if event == obj else False

# Functions to check boolean conditions

# Function to check if any element in a tuple, list, or bool is True
def det_bool_T(obj: (tuple or list or bool) = False):
    if isinstance(obj, bool):
        return obj
    return any(obj)

# Function to check if all elements in a tuple, list, or bool are True
def det_bool_F(obj: (tuple or list or bool) = False):
    if isinstance(obj, bool):
        return obj
    return all(obj)

# Functions related to number verifications

# Function to check if a number is out of bounds
def out_of_bounds(upper: (int or float) = 100, lower: (int or float) = 0, obj: (int or float) = -1):
    return det_bool_T(obj > 100 or obj < 0)

# Function to create a unique window name based on existing window names
def create_win_name():
    all_windows = get_glob('all_windows')
    keys = list(all_windows.keys())
    i, curr_try = 'default_window', 0
    while curr_try in keys:
        curr_try = f'default_window_{i}'
        i += 1
    return curr_try

# Functions for handling while loops with windows

# Function to update the 'event' and 'values' of the current window in the 'all_windows' dictionary
def update_read(curr_win: type(get_window()), win_name: str = create_win_name()):
    all_windows = get_glob('all_windows')
    event, values = curr_win.read()
    if win_name not in all_windows:
        all_windows[win_name] = {'event': '', 'values': {}}
        change_glob(win_name, curr_win)
    change_glob('all_windows', js_horis_for(all_windows, win_name, ['event', 'values'], [event, values]))
    change_glob('all_windows', js_horis_for(all_windows, 'last_window', ['name', 'event', 'values'], [win_name, event, values]))

# Function to get a value from a dictionary based on the keys provided
def get_js_st(js, st):
    if st in js:
        return js[st]

# Function to handle events in a while loop and call specified functions based on the event
def while_basic_events(event_win: type(get_window()) = get_window(), win_name: str = create_win_name(), events: dict = {}):
    while verify_window(event_win):
        update_read(curr_win=event_win, win_name='event_win')
        if win_closed(get_event(event_win)):
            break
        keys = list(events.keys())
        for k in range(0, len(keys)):
            key = keys[k]
            if T_or_F_obj_eq(event=get_event(curr_win=win_name), obj=key):
                func_specs = events[key]
                args = process_args(func_specs['args'])
                call_functions(args=args, instance=get_js_st(func_specs, 'instance'), function_name=get_js_st(func_specs, 'name'))
    close_window(event_win)

# Function for a basic while loop
def while_basic(win=None):
    if win is None:
        win = get_glob(obj='window')
    while verify_window(win):
        event, values = win.read()
        if win_closed(event):
            break
    close_window(win)

# Function to get the name of the last active window
def get_last_window():
    return get_glob('all_windows')['last_window']['name']

# Function for a while loop to update progress of a ProgressBar
def while_progress(win=None, progress: int = 0, step: int = 5, thread=None):
    if win is None:
        win = get_last_window()
    while verify_window(win):
        event, values = win.read(timeout=100)
        if win_closed(event) or not thread_alive(thread):
            break
        win.read(timeout=100)
        update_progress(win=win, st='bar', progress=progress)
        progress += step
        if out_of_bounds(upper=100, lower=0, obj=progress):
            step *= -1
    close_window(win)

# Functions for handling values in windows

# Function to get the value of a specific GUI element in a given window
def get_value(curr_win: (str or type(get_window())) = 'last_window', st: str = ''):
    all_windows = get_glob('all_windows')
    win_name = curr_win
    if type(curr_win) == type(get_window()):
        update_read(curr_win)
        win_name = 'last_window'
    curr_js = all_windows[curr_win]
    if st in curr_js['values']:
        return curr_js['values'][st]

# Function to get the last event triggered in a given window
def get_event(curr_win: (str or type(get_window())) = 'last_window', st: str = ''):
    all_windows = get_glob('all_windows')
    win_name = curr_win
    if type(curr_win) == type(get_window()):
        update_read(curr_win)
        win_name = 'last_window'
    curr_js = all_windows[win_name]
    return curr_js['event']

# Functions for handling threading

# Function to create a new threading.Thread object
def get_thread(target=None, args=(), daemon=True):
    return threading.Thread(target=target, args=args, daemon=daemon)

# Function to start a thread if it's a valid thread object
def start_thread(thread=None):
    if verify_thread(thread):
        thread.start()

# Function to check if an object is a valid threading.Thread object
def verify_thread(thread=None):
    return T_or_F_obj_eq(type(thread), type(threading.Thread()))

# Function to check if a thread is alive
def thread_alive(thread):
    if verify_thread(thread):
        return thread.is_alive()
    return False
