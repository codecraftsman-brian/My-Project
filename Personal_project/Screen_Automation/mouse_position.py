from pynput.mouse import Listener

def click(x, y, button, pressed):
    if pressed:
        print('Mouse clicked at ({0}, {1})'.format(x, y))

with Listener(on_click=click) as listener:
    listener.join()
    

