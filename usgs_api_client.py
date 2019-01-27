#!/usr/bin/env python
"""
Author: Max Solomcuk, max.solomcuk@cgi.com
Command line interface for the USGS API downloader tool.

TODO: Each command should:
        - Accept API key (if applicable)
        - Accept payload/params (from YAML)
        - Call api.method(apiKey, payload) or equivalent
        - Capture the response
        - Process response if applicable

TODO: Methods:
        - datasetfields
        - datasets
        - deletionsearch
        - metadata
        - search
        - hits
        - downloads
        - downloadoptions
"""

import json
import os

import click
import yaml

import api
import datamodels
import payloads

USGS_API_ENDPOINT = api.USGS_API_ENDPOINT
KEY_FILE = api.KEY_FILE

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    click.echo("----------------------------------------------------------------------")
    click.echo("USGS API endpoint is {}\n".format(USGS_API_ENDPOINT))
    if not os.path.exists(KEY_FILE):
        click.echo("API key file does not exist. Consider running the login command first.")
    else:
        click.echo("API key file found. Will try to reuse the key.")
    click.echo("----------------------------------------------------------------------\n")
    
    if ctx.invoked_subcommand is None:
        click.echo(cli.get_help(ctx))

@cli.command()
@click.argument('conf_file', required=False, type=click.Path(exists=True))
def login(conf_file):
    """
    Login to get the API session key.
    Credentials can be read from a YAML configuration file (optional argument).
    If no argument is provided, user is asked to provide the username/password 
    interactively.
    The API key is saved in ~/.usgs_api_key.
    """
    if conf_file:
        with open(conf_file, 'r') as f:
            conf = yaml.load(f)
    else:
        click.echo("No configuration file supplied - using interactive login.\n")
        conf = {}
        conf['username'] = click.prompt('Username')
        conf['password'] = click.prompt('Password', hide_input=True)
    response = api.login(**conf)
    click.echo("Your new API session key is {}\n".format(response['data']))
    click.echo("API endpoint response was:")
    print_dict_items(response)


@cli.command()
@click.argument('apikey', required=False)
def logout(apikey=None):
    """
    End the current API session.
    If API key is supplied, tries to end the corresponding session.
    Otherwise tries the API key in the saved ~/.usgs_api_key file.
    """
    response = api.logout(apikey)
    if response['errorCode'] is None:
        click.echo("API session successfully ended. Key file removed.\n")
    click.echo("API endpoint response was:")
    print_dict_items(response)

@cli.command()
def status():
    """
    Get the current status of the API endpoint.
    This method does not require any parameters.
    The response contains a status orject relfecting
    the current status of the called API.
    """
    response = api.status()
    # TODO: The datamodels.Status() use might be overkill. Check later if this is a good idea.
    click.echo("API status is: {}.\n".format(datamodels.Status(response['data']['build_date'])))
    click.echo("API endpoint response was:")
    print_dict_items(response)

@cli.command()
@click.argument('apikey', required=False)
def notifications(apikey=None):
    """
    Get all system notifications for the current application context.
    Valid API key is required for this request - use login() to obtain.
    The response contains a list of notifications - see Notification() class in datamodels.py.
    """
    response = api.notifications(apikey)
    n_list = response['data']
    if len(n_list) > 0:
        click.echo("System notifications:")
        for note in n_list:
            print_dict_items(note)
            click.echo("\n")
    else:
        click.echo("No new notifications.\n")
        print_dict_items(response)

@cli.command()
@click.argument('conf_file', required=False, type=click.Path(exists=True))
def cleardownloads(apikey=None, conf_file=None):
    """
    Clear all pending donwloads from the user's download queue.
    Valid API key is required for this request.
    The request does not have a response.
    Successful execution is assumed if no errors are thrown.
    """
    if conf_file:
        with open(conf_file, 'r') as f:
            conf = yaml.load(f)
        print(conf)
        api.cleardownloads(apikey, conf['labels'])
    else:
        api.cleardownloads(apikey)

@cli.command()
@click.argument('conf_file', required=True, type=click.Path(exists=True))
def grid2ll(conf_file=None):
    """
    Translate grid reference to coordinates.
    The response contains a list of coordinates defining the shape.
    Currently the command dumps the JSON of the request and response.
    TODO: Can, and probably should, be adapted to specific needs later on.
    """
    if conf_file:
        with open(conf_file, 'r') as f:
            conf = yaml.load(f)
        print(conf)
        print(json.dumps(api.grid2ll(conf)['data'], indent=4))

@cli.command()
@click.argument('conf_file', required=True, type=click.Path(exists=True))
def idlookup(apikey=None, conf_file=None):
    """
    Translate from one ID type to another: entityId (Landsat Scene ID) <-> displayId (Landsat Product ID).
    The response contains a dictionary of objects - keys are inputField value,
    values are the corresponding translations.
    TODO: format output.
    """
    if conf_file:
        with open(conf_file, 'r') as f:
            conf = yaml.load(f)
        print(conf)
        print(json.dumps(api.idlookup(apikey, conf)['data'], indent=4))

@cli.command()
@click.argument('conf_file', required=True, type=click.Path(exists=True))
def search(apikey=None, conf_file=None):
    """
    Perform a product search using supplied criteria.
    Valid API key is required for this request - use login() to obtain.
    See params/search.yaml for the structure of payload.
    The request returns a SearchResponse() object - see datamodels.py.
    """
    if conf_file:
        with open(conf_file, 'r') as f:
            conf = yaml.load(f)
        print(conf)
        print(json.dumps(api.search(apikey, conf)['data'], indent=4)) 

def print_dict_items(d):
    """
    Print items in a dictionary, one item per line.
    Avoid using this for responses with complex 'data' elements.
    """
    for k, v in d.items():
        click.echo("{}={}".format(k, v))
