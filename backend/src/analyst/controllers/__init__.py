"""
Controllers — business logic layer.

Each controller handles the logic for one resource.
Routers call controllers. Controllers call services and the DB.
Controllers never know about HTTP — they receive plain Python objects
and return plain Python objects.
"""
