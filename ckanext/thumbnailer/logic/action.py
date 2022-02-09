from __future__ import annotations

import tempfile
import os
from ckan.lib.uploader import get_resource_uploader
from preview_generator.manager import PreviewManager
from werkzeug.datastructures import FileStorage

import ckan.plugins.toolkit as tk
from ckanext.toolbelt.decorators import Collector

action, get_actions = Collector("thumbnailer").split()


@action
def resource_thumbnail_create(context, data_dict):
    tk.check_access("thumbnailer_resource_thumbnail_create", context, data_dict)

    res = tk.get_action("resource_show")(context, {"id": data_dict["id"]})

    filepath = _get_filepath(res)
    if not os.path.isfile(filepath):
        raise tk.ValidationError({"id": ["Cannot determine path to resource"]})

    manager = _get_manager()
    preview = manager.get_jpeg_preview(filepath)
    return tk.get_action("files_file_create")({"ignore_auth": True}, {
        "name": "Resource {id} thumbnail".format(id=res["id"]),
        "kind": "thumbnail",
        "upload": FileStorage(open(preview, "rb"))
    })


def _get_manager():

    cache = os.path.join(
        tempfile.gettempdir(),
        tk.config["ckan.site_id"],
        "ckanext-thumbnailer"
    )
    return PreviewManager(cache, create_folder=True)

def _get_filepath(res):
    # TODO: replace
    return "/home/sergey/Downloads/MarineHabitatDQS.pdf"
    uploader = get_resource_uploader(res)
    return uploader.get_path(res["id"])
