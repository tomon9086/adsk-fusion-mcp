def generate_uuid() -> str:
    """
    Generate a unique identifier (UUID4)

    Returns:
        str: The generated UUID as a string
    """
    import uuid

    return str(uuid.uuid4())
