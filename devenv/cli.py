# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import

import os
import urllib.request

import docker
import click
import yaml

from devenv import config

dock = docker.from_env()


def load_config():
    with open('.devenv.yml') as f:
        config = yaml.load(f)

    return config


def get_container_infos(config):
    default_container_config = {
        'network_mode': config.get('network_mode', 'host'),
        'detach': True,
    }

    for container_name in config.get('run', []):
        container_config = {}
        container_config.update(default_container_config)
        container_config.update(config['run'][container_name])
        container_config['name'] = config['project_name'] + '-' + container_name
        if container_config.get('user', None) == '$current':
            container_config['user'] = os.getuid()
        yield container_config


def remove_all(config):
    used_names = [c.name for c in dock.containers.list(all=True)]
    for container_config in get_container_infos(config):
        name = container_config['name']
        if name in used_names:
            click.echo('removing container ' + name)
            dock.containers.get(name).remove(force=True)


def run(config):
    remove_all(config)
    for container_config in get_container_infos(config):
        volumes = {}
        for volume in container_config.get('volumes', []):
            src_path, dst_path = volume.split(':')
            src_path = os.path.abspath(src_path)
            volumes[src_path] = {'bind': dst_path, 'mode': 'rw'}

            click.echo('starting container ' + container_config['name'])
        container_config['volumes'] = volumes

        if container_config.get('user', 'root') not in ('root', 0):
            env = container_config.setdefault('environment', {})
            env.setdefault('HOME', '/tmp/')
        result = dock.containers.run(**container_config)


@click.group()
def main(args=None):
    """Console script for devenv"""
    click.echo('WARNING: ALPHA STAGE')
    click.echo('Unstalbe.  API and config format might (and probably will) change.')


@main.command()
@click.argument('source')
def clone(source):
    if source.startswith('http'):
        fd = urllib.request.urlopen(source)
    elif os.path.exists(source):
        fd = open(source)
    else:
        click.echo('Could not get {}'.format(source))
        return 1

    config_data = yaml.load(fd)
    fd.close()
    cfg = config.Config(config_data)
    cfg.ensure_checkout('.')
    return 0


@main.command()
def dev():
    config = load_config()
    run(config)


@main.command()
def down():
    config = load_config()
    remove_all(config)


if __name__ == "__main__":
    main()
