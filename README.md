# Holosense 

Tracks the location of your face in 3 dimensions relative to the camera, using coordinates from MediaPipe FaceMesh.

## How to use


Holosense is setup like this.

```Python
from holosense import SpatialTracker

spatial_tracker = SpatialTracker(
    fov=78.5,
    aspectratio=16/9,
    eyedistance=4,
    eyenosedistance=3,
    single_output=True
    )
```

The keyword arguments represent the camera's field of view, image aspect ratio, distance between the corners of the eye of the user, distance between the corner of the eye and tip of the nose of the user, and whether the program provides a single set of coordinates (if it is set to true) or a list with the coordinates of both eyes and the nose.

Now, to use the tracker, run:

```Python
res = spatial_tracker.calculatePosition(face_landmarks)
```
where face_landmarks are the facial landmarks determined by mediapipe facemesh




 