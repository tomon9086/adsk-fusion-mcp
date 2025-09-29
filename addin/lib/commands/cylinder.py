import adsk.core
import adsk.fusion

from .extrude_profile import extrude_profile
from .sketch_circle import create_sketch_circle


def create_cylinder(
    component: adsk.fusion.Component,
    coords: adsk.core.Point3D,
    radius: float,
    height: float,
):
    """
    Create a cylinder with the specified coordinates, radius, and height

    Args:
        component (adsk.fusion.Component): Target component to create the cylinder in
        coords (adsk.core.Point3D): Center coordinates of the cylinder (x, y, z)
        radius (float): Radius of the cylinder
        height (float): Height of the cylinder

    Returns:
        bool: True if creation is successful, False if it fails
    """

    try:
        # Create circular sketch
        sketch = create_sketch_circle(
            component, component.xYConstructionPlane, coords, radius
        )
        # Extrude the sketch to create cylinder
        return extrude_profile(component, sketch, height)

    except Exception as e:
        print(f"Cylinder creation error: {e}")
        return False
