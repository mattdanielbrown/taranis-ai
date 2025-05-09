# role_views.py
from models.admin import Role, Permissions
from frontend.data_persistence import DataPersistenceLayer
from frontend.views.base_view import BaseView


class RoleView(BaseView):
    model = Role

    @classmethod
    def get_extra_context(cls, object_id: int):
        dpl = DataPersistenceLayer()
        return {"permissions": [p.model_dump() for p in dpl.get_objects(Permissions)]}
