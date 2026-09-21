from __future__ import annotations

import logging

import ckan.plugins as p
import ckan.plugins.toolkit as tk
from ckan.exceptions import CkanConfigurationException

from . import cli, helpers, utils
from .logic import action, auth

log = logging.getLogger(__name__)


@tk.blanket.config_declarations
class ThumbnailerPlugin(p.SingletonPlugin):
    p.implements(p.IConfigurable)
    p.implements(p.ITemplateHelpers)
    p.implements(p.IClick)
    p.implements(p.IActions)
    p.implements(p.IAuthFunctions)
    p.implements(p.IResourceController, inherit=True)
    # IConfigurable

    def configure(self, config):
        if "files" not in config["ckan.plugins"]:
            raise CkanConfigurationException(
                "thumbnailer plugins requires files plugin"
            )

    # IClick
    def get_commands(self):
        return cli.get_commands()

    # IActions
    def get_actions(self):
        return action.get_actions()

    # IAuthFunctions
    def get_auth_functions(self):
        return auth.get_auth_functions()

    # ITemplateHelpers
    def get_helpers(self):
        return helpers.get_helpers()

    # IResourceController
    def after_resource_create(self, context, data_dict):
        utils.create_thumbnail(context, data_dict)

    def after_resource_update(self, context, data_dict):
        utils.create_thumbnail(context, data_dict)
