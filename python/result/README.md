# Tracks visualization tool

Required libraries: PyQt6, pyqtgraph,PyOpenGL, numpy, pandas

When you run the main.py, event.txt must be located in the "data" folder,
 just like it is in the repository

    event.py must contain data of the form:
    1) One line - one track
    2) Hits in the track follow each other without any separators
    3) Hits characteristics have the following content - (multitraj-index, hit-index, x, y, z, phi, theta, q/p, t, chi2),
    and are separated by a comma with a space
