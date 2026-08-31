"""
Configuration — reads .env into typed settings.

Uses pydantic-settings so the app crashes immediately with a clear error
if a required env var is missing, instead of failing later at runtime.
"""
