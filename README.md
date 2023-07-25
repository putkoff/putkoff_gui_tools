# dynamic_gui.py

This Python script, `dynamic_gui.py`, provides a set of utility functions for creating and managing dynamic user interfaces using the PySimpleGUI library. It introduces an abstraction layer over PySimpleGUI that enables developers to create GUI elements, manage their state, and handle their events in a more intuitive and efficient way.

## Features

- **Expandable GUI Elements**: Create GUI elements that can automatically resize and scroll.
- **Global Variables Management**: Easily change and retrieve global variables from anywhere in your code.
- **Function and Method Invocation**: Call global functions or instance methods dynamically with custom arguments.
- **Window Management**: Create, verify, and close PySimpleGUI windows.
- **Event Handling**: Define custom event handlers for your GUI elements.
- **Multithreading**: Easily create and manage threads for non-blocking operations.
- **Progress Bars**: Create and update progress bars to provide visual feedback on the progress of a task.

## Example Usage

The following example creates a window with a resizable, scrollable text area and a progress bar that fills up over time.

```python
import dynamic_gui as dg

#####basic_implimentation
while_basic(win=get_gui_fun('Window',{'title':'display',"layout":[[get_gui_fun('Multiline',{"sdasdfsdf":"","default_text":"hey"})]]}))


#####complex implimentation
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

```

## Getting Started

1. Ensure you have Python 3 installed.
2. Install the PySimpleGUI library using pip:

    ```
    pip install PySimpleGUI
    ```
3. Clone the repository or download `dynamic_gui.py` into your project.
4. Import `dynamic_gui` in your script:

    ```python
    import dynamic_gui as dg
    ```

## Contributions

Contributions are always welcome. Please fork the repository and create a pull request with your changes.

## License

This project is released under the MIT License.

---
