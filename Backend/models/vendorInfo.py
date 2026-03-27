# Deprecated compatibility wrapper.
# Keep this file for old import paths while the new layered implementation lives in:
# - models/vendor_models.py
# - repositories/vendor_repository.py
# - services/vendor_service.py

from .vendor_models import Vendor as vendor, Product as product


# Note: this file no longer contains direct DB logic; use services.vendor_service.
