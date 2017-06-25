#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sanic import Sanic
from .views import main
from .docker_tools import init_docker_client


def create_app():
    app = Sanic(__name__)
    app.blueprint(main, url_prefix="/v1")

    init_docker_client()
    return app
