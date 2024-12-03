# Holosense 

https://drive.google.com/file/d/1k3cVlt_3bQBe7xAW-vKBGgm0f23gfn2V/view?usp=sharing

Tracks the location of your face in 3 dimensions relative to the camera, using coordinates from MediaPipe FaceMesh. 

It's accurate to within an inch 95% of the time even when the user is 5 feet away from the camera. (Tested on webcam of a Dell Precision 5570 laptop, against ground truth value from HC-SR04 ultrasonic rangefinder)

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




 
