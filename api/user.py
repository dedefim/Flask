from combojsonapi.permission.permission_system import (
from flask_combo_jsonapi import ResourceDetail, ResourceList
from blog.schemas import UserSchema
from blog.models.database import db
from blog.models import User
from blog.permissions.user import UserPermission
    PermissionForPatch,


class UserList(ResourceList):
    schema = UserSchema
    data_layer = {
        "session": db.session,
        "model": User,
    }

class UserDetail(ResourceDetail):
    schema = UserSchema
    data_layer = {
        "session": db.session,
        "model": User,
        "permission_get": [UserPermission],
    }

    class UserPermission(PermissionMixin):
    PATCH_AVAILABLE_FIELDS = [
        "first_name",
        "last_name",
    ]

    def patch_permission(self, *args, user_permission: PermissionUser = None, **kwargs) ->
PermissionForPatch:
        self.permission_for_patch.allow_columns = (self.PATCH_AVAILABLE_FIELDS, 10)
        return self.permission_for_patch

    def patch_data(self, *args, data: dict = None, obj: User = None, user_permission:
PermissionUser = None, **kwargs) -> dict:
        permission_for_patch = user_permission.permission_for_patch_permission(model=User)

        return {
            i_key: i_val
            for i_key, i_val in data.items()
            if i_key in permission_for_patch.columns
        }