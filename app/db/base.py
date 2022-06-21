# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.api.endpoints.user.models import User  # noqa
from app.api.endpoints.text.models import Text, Stat  # noqa
