# -*- coding: utf-8 -*-
from sanic import Blueprint
from sanic.response import json
import app.docker_tools as docker
import asyncio
import logging

main = Blueprint('main')


@main.middleware('response')
async def enable_cors(request, response):
    if response:
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


@main.route('/container')
def route_container(request):
    status, container_list = docker.get_container_list()
    return json({
        'status': status,
        'container_list': container_list,
    })


@main.route('/container/<container_id>')
def route_container_detail(request, container_id):
    status, container_info = docker.get_container_detail(container_id)
    return json({
        'status': status,
        'container_info': container_info,
    })


@main.route('/sys/version')
async def route_version(request):
    status, version = docker.get_docker_version()
    return json({
        'status': status,
        'container_list': version,
    })


@main.route('/run/', methods=["POST"])
async def route_post_run(request):
    status, container_info = docker.run_container(request.form)
    return json({
        'status': status,
        'container_info': container_info,
    })


@main.route('/log/<container_id>')
async def route_container_log(request, container_id):
    status, log = docker.get_container_log(container_id, False)
    return json({
        'status': status,
        'log': log,
    })


@main.websocket('/ws/log/<container_id>')
async def route_websocket(request, ws, container_id):
    log_len = 0
    retry_time = 0

    while True:
        status, log_list = docker.get_container_log(container_id)
        if status == "error":
            return ""

        new_log_len = len(log_list)

        if retry_time == 3:
            logging.info("stop log retry")
            return ""

        if log_len >= new_log_len:
            logging.debug("sleep and retry")
            await asyncio.sleep(5)
            retry_time += 1
            continue

        for line in log_list[log_len:]:
            await ws.send("{}\r\n".format(line))

        log_len = new_log_len
        await asyncio.sleep(1)
