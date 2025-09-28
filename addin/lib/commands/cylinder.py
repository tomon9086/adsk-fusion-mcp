import adsk.core
import adsk.fusion


def create_cylinder(
    app: adsk.core.Application, coords: adsk.core.Point3D, radius: float, height: float
):
    """
    Create a cylinder with the specified coordinates, radius, and height

    Args:
        coords (tuple): Center coordinates of the cylinder (x, y, z)
        radius (float): Radius of the cylinder
        height (float): Height of the cylinder

    Returns:
        bool: True if creation is successful, False if it fails
    """

    try:
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        root_component = design.rootComponent
        sketches = root_component.sketches
        xy_plane = root_component.xYConstructionPlane

        # Create a sketch
        sketch = sketches.add(xy_plane)
        cylinder_base_name = "cylinder_base_" + str(len(sketches))
        sketch.name = cylinder_base_name

        # Display the sketch
        sketch.isLightBulbOn = True

        # Draw a circle
        sketch.sketchCurves.sketchCircles.addByCenterRadius(coords, radius)

        # Get the profile
        profile = root_component.sketches.itemByName(cylinder_base_name)
        circle_base_prof = profile.profiles.item(0)

        # Execute extrusion
        extrudes = root_component.features.extrudeFeatures
        extrude_input = extrudes.createInput(
            circle_base_prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )

        extrusion_distance = adsk.core.ValueInput.createByReal(height)
        extrude_input.setDistanceExtent(False, extrusion_distance)
        extrudes.add(extrude_input)

        return True

    except Exception as e:
        # Output error log (use logging system as needed)
        print(f"Cylinder creation error: {e}")
        return False
