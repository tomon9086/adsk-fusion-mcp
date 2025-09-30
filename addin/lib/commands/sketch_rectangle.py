import adsk.core
import adsk.fusion

from .sketch import create_sketch


def create_sketch_rectangle(
    component: adsk.fusion.Component,
    plane: adsk.fusion.ConstructionPlane,
    point_one: adsk.core.Point3D,
    point_two: adsk.core.Point3D,
) -> adsk.fusion.Sketch:
    """
    Create a rectangle in the given sketch from point_one to point_two.

    Args:
        sketch (adsk.fusion.Sketch): The sketch to add the rectangle to.
        point_one (adsk.core.Point3D): The starting point of the rectangle.
        point_two (adsk.core.Point3D): The ending point of the rectangle.

    Returns:
        adsk.fusion.SketchRectangle: The created sketch rectangle object.
    """
    try:
        sketch = create_sketch(component, plane)
        lines = sketch.sketchCurves.sketchLines
        lines.addTwoPointRectangle(point_one, point_two)

        return sketch

    except Exception as e:
        print(f"Error creating sketch rectangle: {e}")
        return None
