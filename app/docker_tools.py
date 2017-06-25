# -*- coding: utf-8 -*-
import docker
import logging

docker_client = None


def init_docker_client():
    global docker_client
    docker_client = docker.DockerClient(base_url='unix://var/run/docker.sock')


def get_container_list():
    docker_list = docker_client.containers.list(all=True)
    if docker_list is None:
        return "error", "cannot get container list"

    docker_list_res = [parse_container_info(el) for el in docker_list]
    return "ok", docker_list_res


def get_container_detail(container_id):
    try:
        container_info = docker_client.containers.get(container_id)
    except docker.errors.NotFound as e:
        container_info = None

    if container_info:
        return "ok", parse_container_info(container_info)
    else:
        return "error", "no such docker container"


def get_docker_version():
    return "ok", docker_client.version()


def run_container(form_data):
    image, ports, env_list = parse_deploy_args(form_data)

    try:
        logging.info("create {} with env: {}, port: {}".format(image, env_list, ports))
        container_info = docker_client.containers.run(
            image, environment=env_list, ports=ports, detach=True)
    except docker.errors.APIError as e:
        logging.error(e)
        container_info = None

    if container_info:
        return "ok", parse_container_info(container_info)
    else:
        return "error", "cannot create container"


def get_container_log(container_id):
    try:
        container_obj = docker_client.containers.get(container_id)
    except docker.errors.NotFound as e:
        return "error", "no such container"

    log_str = container_obj.logs()
    return "ok", parse_container_log(log_str)


def parse_container_info(container_obj):
    if container_obj is None:
        return None

    res = {
        'id': container_obj.id,
        'short_id': container_obj.short_id,
        'name': container_obj.name,
        'status': container_obj.status,
    }
    return res


def parse_deploy_args(form_data):
    image = 'playniuniu/weblogic-domain:12.2.1.2'
    port = form_data.get("port", "8001")
    domain = form_data.get("domain", "base_domain")
    password = form_data.get("password", "welcome1")

    ports = {port: port}
    env_list = [
        "DOMAIN_NAME={}".format(domain),
        "ADMIN_PASSWORD={}".format(password)
    ]
    return image, ports, env_list


def parse_container_log(log_str):
    log_str = log_str.decode("utf-8")
    log_str_list = log_str.split("\n")
    log_str_list.pop()
    log_str_list = [el.strip() for el in log_str_list]
    return log_str_list
