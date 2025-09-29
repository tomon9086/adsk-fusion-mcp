import adsk.core
import adsk.fusion

from .sketch import create_sketch


def create_sketch_circle(
    component: adsk.fusion.Component,
    plane: adsk.core.Plane,
    coords: adsk.core.Point3D,
    radius: float,
) -> adsk.fusion.Sketch:
    """
    Create a circular sketch on the XY plane

    Args:
        component (adsk.fusion.Component): Target component to create the sketch in
        coords (adsk.core.Point3D): Center coordinates of the circle
        radius (float): Radius of the circle

    Returns:
        adsk.fusion.Sketch: The created sketch object
    """
    sketches = component.sketches
    sketch_name = "sketch_circle_" + str(len(sketches))

    # Create sketch using base function
    sketch = create_sketch(component, plane, sketch_name)
    if sketch is None:
        return None

    # Display the sketch
    sketch.isLightBulbOn = True

    # Draw a circle
    sketch.sketchCurves.sketchCircles.addByCenterRadius(coords, radius)

    return sketch
