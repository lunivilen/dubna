# Tracks visualization tool

Required libraries: PyQt6, pyqtgraph, numpy, PyOpenGL

To run, you need to place drawing_tracks.py in the same folder as the event.txt and run the module from console using
command "python3 drawing_tracks.py"

event.py must contain data of the form:
1) One line - one track
2) Hits in the track follow each other without any separators
3) Hits characteristics have the following content - (hit-index, x, y, z, phi, theta, q/p, t, chi2),
and are separated by a comma with a space