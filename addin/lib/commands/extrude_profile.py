import adsk.core
import adsk.fusion


def extrude_profile(
    component: adsk.fusion.Component, sketch: adsk.fusion.Sketch, distance: float
) -> bool:
    """
    Extrude a sketch profile to create a solid

    Args:
        component (adsk.fusion.Component): Target component to extrude in
        sketch (adsk.fusion.Sketch): The sketch to extrude
        distance (float): Distance of the extrusion

    Returns:
        bool: True if extrusion is successful, False if it fails
    """
    try:

        # Get the first profile from the sketch
        circle_base_prof = sketch.profiles.item(0)

        # Execute extrusion
        extrudes = component.features.extrudeFeatures
        extrude_input = extrudes.createInput(
            circle_base_prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )

        extrusion_distance = adsk.core.ValueInput.createByReal(distance)
        extrude_input.setDistanceExtent(False, extrusion_distance)
        extrudes.add(extrude_input)

        return True

    except Exception as e:
        print(f"Extrusion error: {e}")
        return False
