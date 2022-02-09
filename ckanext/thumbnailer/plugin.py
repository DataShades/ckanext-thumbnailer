from __future__ import annotations
import logging
from ckan.exceptions import CkanConfigurationException
import ckan.plugins as p
import ckan.plugins.toolkit as tk

from .logic import action, auth

log = logging.getLogger(__name__)

class ThumbnailerPlugin(p.SingletonPlugin):
    p.implements(p.IConfigurer)
    p.implements(p.IConfigurable)
    p.implements(p.IActions)
    p.implements(p.IAuthFunctions)

    if tk.check_ckan_version("2.10"):
        p.implements(p.IConfigDeclaration)
        def declare_config_options(self, declaration, key):
            declaration.declare_list("ckan.upload.thumbnail.types", [])
            declaration.declare_list("ckan.upload.thumbnail.mimetypes", [])

    # IConfigurable

    def configure(self, config):
        if "files" not in config["ckan.plugins"]:
            raise CkanConfigurationException(f"thumbnailer plugins requires files plugin")

    # IConfigurer

    def update_config(self, config_):
        ...

    # IActions
    def get_actions(self):
        return action.get_actions()

    # IAuthFunctions
    def get_auth_functions(self):
        return auth.get_auth_functions()
