# etrog18-freecad
Stores the python code to create a freecad drawing for our house


In order to use in freecad, open the python console, add the directory that includes this file to `sys.path`, and then execute the following:
```python
import importlib; import freecad_utils; importlib.reload(freecad_utils) ; freecad_utils.draw_house()
```

This imports the module, reloads it if it was updated, and draws the house.