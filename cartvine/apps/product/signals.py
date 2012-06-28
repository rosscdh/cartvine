import django.dispatch as dispatch
from django.core.signals import request_finished

# ----- Signals -----

add_variant_property = dispatch.Signal(providing_args=["new_property"])
delete_variant_property = dispatch.Signal(providing_args=["option_id"])


# ----- Recievers -----
# DEFINED IN models.py