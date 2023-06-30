# import importlib
# import glob

# # Define __all__ as an empty list
# __all__ = []

# # Get a list of all the blueprint files in the controllers folder
# blueprint_files = glob.glob('app_API/controllers/*_bp.py')

# # Import all the blueprints
# for blueprint_file in blueprint_files:
#     module_name = blueprint_file.replace('/', '.')[:-3]
#     module = importlib.import_module(module_name)
#     globals().update(vars(module))
#     # Append the blueprint name to __all__
#     __all__.append(module_name.split('.')[-1])

# # Print the updated globals dictionary
# print(globals())

from .venue import venue_bp
from .artist import artist_bp
from .show import show_bp

# Export the blueprints
__all__ = ['venue_bp', 'artist_bp', 'show_bp']