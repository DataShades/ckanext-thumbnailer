from __future__ import annotations

import ckan.plugins.toolkit as tk

from ckan.lib.files import FileData, get_storage
from ckanext.toolbelt.decorators import Collector

from .utils import resource_file

helper, get_helpers = Collector("thumbnailer").split()


@helper
def resource_thumbnail_url(id_: str, qualified: bool = False):
    info = resource_file(id_)
    if not info:
        return

    data = FileData.from_dict(info)
    storage = get_storage("thumbnail")
    link = storage.permanent_link(data)
    return tk.h.url_for_static_or_external(link, _external=qualified)
