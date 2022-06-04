# dynamic_dungeon.py
A dynamic dungeon crawler written in Python.
This dungeon crawler game reads an external file and generates a map layout from it.

layout.txt:
```
#   means nothing
# + means room
# S means start
# B means boss
# T means treasure
# D means dragon/end
S+++++
+
++++++BT
+
++++++BD
      T
```

would generate:

![selected-19-06-21-14-44-00](https://user-images.githubusercontent.com/86153674/122644382-d3504d00-d10c-11eb-8595-310e258421de.jpg)

On Windows, the Unicode block characters would be replaced with a "+" due to formatting issues.

This project is still under development so many features may change.
