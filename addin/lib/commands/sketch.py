import adsk.core
import adsk.fusion


def create_sketch(
    component: adsk.fusion.Component, plane: adsk.core.Plane, sketch_name: str
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
        sketch.name = sketch_name
        return sketch
    except Exception as e:
        print(f"Error creating sketch: {e}")
        return None
