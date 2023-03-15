# Tracks visualization tool

Required libraries: PyQt6, pyqtgraph, numpy, PyOpenGL

[1] When you run the drawing_tracks.py, event.txt must be located in the "data" folder,
    just like it is in the repository

    event.py must contain data of the form:
    1) One line - one track
    2) Hits in the track follow each other without any separators
    3) Hits characteristics have the following content - (hit-index, x, y, z, phi, theta, q/p, t, chi2),
    and are separated by a comma with a space

[2] When you run the drawing_hits.py, hits.txt must be located in the "data" folder,
    just like it is in the repository

    hits.py must contain data of the form:
    1) One line - one hit
    2) Hits characteristics have the following content - (x, y, z, track_id, q),
    and are separated by a comma with a space
