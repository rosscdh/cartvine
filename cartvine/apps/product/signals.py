import django.dispatch as dispatch
from django.core.signals import request_finished

# ----- Signals -----

add_variant_property = dispatch.Signal(providing_args=["user_id","new_property"])
delete_variant_property = dispatch.Signal(providing_args=["user_id","option_id"])


# ----- Recievers -----
# DEFINED IN models.py