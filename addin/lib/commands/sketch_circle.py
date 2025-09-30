import adsk.core
import adsk.fusion
from lib.utils.uuid import generate_uuid

from .sketch import create_sketch


def create_sketch_circle(
    component: adsk.fusion.Component,
    plane: adsk.fusion.ConstructionPlane,
    coords: adsk.core.Point3D,
    radius: float,
) -> adsk.fusion.SketchCircle:
    """
    Create a circular sketch on the XY plane

    Args:
        component (adsk.fusion.Component): Target component to create the sketch in
        plane (adsk.fusion.ConstructionPlane): Construction plane to create the sketch on
        coords (adsk.core.Point3D): Center coordinates of the circle
        radius (float): Radius of the circle

    Returns:
        adsk.fusion.SketchCircle: The created sketch circle object
    """
    # Create sketch using base function
    sketch = create_sketch(component, plane)

    # Display the sketch
    sketch.isLightBulbOn = True

    # Draw a circle
    circle = sketch.sketchCurves.sketchCircles.addByCenterRadius(coords, radius)

    return circle
