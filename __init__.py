# module level doc-string
__doc__ = """
derby_runner - an event management module for Scouting competions written in 
Python
===============================================================================
** derby_runner is ...
"""

# Check for hard dependencies
# hard_dependencies = ("","","")
missing_dependencies = []

for dependency in hard_dependencies:
    try:
        __import__(dependency)
    except ImportError as e:
        missing_dependencies.append(f"{dependency}: {e}")

if missing_dependencies:
    raise ImportError(
        "Unable to import required dependencies:\n" + "\n".join(missing_dependencies)
    )
del hard_dependencies, dependency, missing_dependencies