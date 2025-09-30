import adsk.core
import adsk.fusion
from lib.utils.uuid import generate_uuid


def create_sketch(
    component: adsk.fusion.Component,
    plane: adsk.core.Plane,
) -> adsk.fusion.Sketch:
    """
    Create a new sketch on the specified plane with the given name.

    Args:
        component (adsk.fusion.Component): The target component to create the sketch in.
        plane (adsk.core.Plane): The construction plane where the sketch will be created.
        sketch_name (str): The name of the new sketch.

    Returns:
        adsk.fusion.Sketch: The created sketch object.
    """
    try:
        sketches = component.sketches
        sketch = sketches.add(plane)
        if not isinstance(sketch, adsk.fusion.Sketch):
            raise RuntimeError("Failed to create sketch")

        sketch.name = generate_uuid()

        return sketch

    except Exception as e:
        print(f"Error creating sketch: {e}")
        return None
