import threading
import PySimpleGUI as sg
import inspect
import os
def expandable(size:tuple=(None, None)):
    return {"size": size,"resizable": True,"scrollable": True,"auto_size_text": True,"expand_x":True,"expand_y": True}
def change_glob(string:str,obj:any):
  globals()[string]=obj
  return obj
change_glob('all_windows',{'last_window':{'name':'','values':{},'event':''}})
def get_glob(obj:str='',glob=globals()):
    try:
        return glob[obj]
    except KeyError:
        print(f"No global object named '{obj}'")
        return None
def call_functions(function_name: str, args: dict = None, instance=None, glob=globals()):
    if glob == None:
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
#progress_bars
def update_progress(win:str='progress_window',st:str='bar',progress:(int or float)=0):
    win[st].update_bar(progress)
def get_progress_bar(max_value:int=100, size:tuple=(30,10),key:str='bar'):
    return get_gui_fun('ProgressBar',{"max_value":max_value, "size":size, "key":key})
#windows
def get_window(title:str='basic window',layout:list=[[]]):
    return sg.Window(title, layout)
def verify_window(win:any=None):
  if type(win) == str:
    win = get_glob(obj=win)
  if type(win) == type(get_window()):
    return True
  return False
def close_window(win:any=None):
  if verify_window(win):
    win.close()
#components
def get_gui_fun(name:str='',args:dict={}):
  import PySimpleGUI
  return get_fun({"instance":PySimpleGUI,"name":name,"args":args})
#check_whiles
def win_closed(event:str=''):
    return T_or_F_obj_eq(event=event,obj=sg.WIN_CLOSED)
#check_bools
def T_or_F_obj_eq(event:any='',obj:any=''):
  return True if event == obj else False
def det_bool_T(obj:(tuple or list or bool)=False):
  if isinstance(obj, bool):
    return obj 
  return any(obj)
def det_bool_F(obj:(tuple or list or bool)=False):
  if isinstance(obj, bool):
    return obj
  return all(obj)
#number_verifications
def out_of_bounds(upper:(int or float)=100,lower:(int or float)=0,obj:(int or float)=-1):
  return det_bool_T(obj > 100 or obj < 0)
def create_win_name():
  all_windows = get_glob('all_windows')
  keys = list(all_windows.keys())
  i,curr_try = 'default_window',0
  while curr_try in keys:
    curr_try = f'default_window_{i}'
    i +=1
  return curr_try
#while_windows
def js_horis_for(js,st,ls,ls2):
    js[st][[each for each in ls]]=[each for each in ls2]
    return js
def update_read(curr_win:type(get_window()),win_name:str=create_win_name()):
    all_windows = get_glob('all_windows')
    event, values = curr_win.read()
    if win_name not in all_windows:
      all_windows[win_name] = {'event':'','values':{}}
      change_glob(win_name,curr_win)
    change_glob('all_windows',js_horis_for(all_windows,win_name,['event','values'],[event,values]))
    change_glob('all_windows',js_horis_for(all_windows,'last_window',['name','event','values'],[win_name,event,values]))
def get_js_st(js,st):
  if st in js:
    return js[st]
def while_basic_events(event_win:type(get_window())=get_window(),win_name:str=create_win_name(),events:dict={}):
    while verify_window(event_win):
        update_read(curr_win=event_win,win_name='event_win')
        if win_closed(get_event(event_win)):
            break
        keys = list(events.keys())
        for k in range(0,len(keys)):
          key = keys[k]
          if T_or_F_obj_eq(event=get_event(curr_win=win_name),obj=key):
            func_specs = events[key]
            args = process_args(func_specs['args'])
            call_functions(args=args, instance=get_js_st(func_specs,'instance'), function_name=get_js_st(func_specs,'name'))
    close_window(event_win)
def while_basic(win=None):
    if win is None:
        win = get_glob(obj='window')
    while verify_window(win):
        event, values = win.read()
        if win_closed(event):
            break
    close_window(win)
def get_last_window():
    return get_glob('all_windows')['last_window']['name']
def while_progress(win=None, progress:int=0, step:int=5, thread=None):
    if win is None:
        win = get_last_window()
    while verify_window(win):
      event, values = win.read(timeout=100)
      if win_closed(event) or not thread_alive(thread):
          break
      win.read(timeout=100)
      update_progress(win=win,st='bar',progress=progress)
      progress += step
      if out_of_bounds(upper=100,lower=0,obj=progress):
        step *= -1
    close_window(win)
#values
def get_value(curr_win:(str or type(get_window()))='last_window',st:str=''):
  all_windows=get_glob('all_windows')
  win_name = curr_win
  if type(curr_win) == type(get_window()):
    update_read(curr_win)
    win_name = 'last_window'
  curr_js = all_windows[curr_win]
  if st in curr_js['values']:
    return curr_js['values'][st]
def get_event(curr_win:(str or type(get_window()))='last_window',st:str=''):
  all_windows=get_glob('all_windows')
  win_name = curr_win
  if type(curr_win) == type(get_window()):
    update_read(curr_win)
    win_name = 'last_window'
  curr_js = all_windows[win_name]
  return curr_js['event']
#threading
def get_thread(target=None,args=(),daemon=True):
    return threading.Thread(target=target, args=args, daemon=daemon)
def start_thread(thread=None):
  if verify_thread(thread):
    thread.start()
def verify_thread(thread=None):
  return T_or_F_obj_eq(type(thread),type(threading.Thread()))
def thread_alive(thread):
  if verify_thread(thread):
    return thread.is_alive()
  return False
#text to audio
def save_audio(text:str='',file_path:str="welcome.mp3"):
  from gtts import gTTS
  myobj = gTTS(text=text, lang='en', slow=False)
  myobj.save(f"{file_path}")
  os.system(f"mpg321 {file_path}")
def play_audio(file_path:str="welcome.mp3"):
  from playsound import playsound
  if os.path.isfile(file_path):
      playsound(file_path)
def save_play_audio(text:str='',file_path:str="welcome.mp3"):
  save_audio(text=text,file_path=file_path)
  thread = threading.Thread(target=play_audio, args=(file_path,))
  thread.start()
def simple():
  #example of simple modularization
  while_basic(win=get_gui_fun('Window',{'title':'display',"layout":[[get_gui_fun('Multiline',{"sdasdfsdf":"","default_text":"hey"})]]}))
def complex():
  #ecample of complex modularization
  while_basic_events(
    get_gui_fun('Window',{'title':'chat GPT output', 'layout':[[
      get_gui_fun('T',{'text':'query: '}),
      get_gui_fun('Multiline',{'default_text':'this is a question',**expandable()})],[
        get_gui_fun('T',{'text':'response: '}),
        get_gui_fun('Multiline', {'default_text': 'this is an answer', 'key': "-RESPONSE-",**expandable()}),[
          get_gui_fun('Button', {"button_text": 'Play Audio', "key": '-PLAY_AUDIO-'})]]],**expandable(size=(300,300))}),
    events={'-PLAY_AUDIO-': {"type": "get","name": "save_play_audio",
                             "args": {"text": {"type": "get", "name": "get_value", "args": {"st": "-RESPONSE-"}}, "file_path": "new_audio.mp3"}}}
    )
