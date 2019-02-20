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
      Currently processing is limited to printing out the server response.

TODO: - Test download method
      - Decide how to handle the output from each request
        - Perhaps add an option to print JSON response
      Potential workflow:
      - login
      - hits
      - search -> pass result to downloadoptions
      - downloadoptions -> check if required prod types available -> pass available types to download
      - download available prod types -> pass retrieved links to...
        - new Python downloader that I need to write
        - external utility (wget, curl, etc)
        - save links to file
      - logout
"""

from collections import OrderedDict
import json
import logging
import logging.config
import os
import sys

import click
import yaml

import api
import datamodels
import payloads

USGS_API_ENDPOINT = api.USGS_API_ENDPOINT
KEY_FILE = api.KEY_FILE
PRINT = False

with open('logging.conf', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
logger = logging.getLogger(__name__)

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below
    ctx.ensure_object(dict)

    logger.debug("Starting new USGS Inventory API Client run.")
    logger.info("USGS API endpoint is {}".format(USGS_API_ENDPOINT))
    if not os.path.exists(KEY_FILE):
        logger.info("API key file does not exist. Consider running the login command first.")
    else:
        logger.info("API key file found. Will try to reuse the key.")

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
    logger.info('Calling login().')
    if conf_file:
        with open(conf_file, 'r') as f:
            conf = yaml.load(f)
    else:
        logger.info("No configuration file supplied - using interactive login.")
        conf = {}
        conf['username'] = click.prompt('Username')
        conf['password'] = click.prompt('Password', hide_input=True)
    logger.info("Using username = {}. Password not shown.".format(conf['username']))
    response = api.login(**conf)
    logger.debug("Received response:\n{}".format(json.dumps(response, indent=4)))
    logger.info("Your new API session key is {}".format(response['data']))

@cli.command()
@click.argument('apikey', required=False)
def logout(apikey=None):
    """
    End the current API session.
    If API key is supplied, tries to end the corresponding session.
    Otherwise tries the API key in the saved ~/.usgs_api_key file.
    """
    logger.info('Calling logout().')
    response = api.logout(apikey)
    logger.debug("Received response:\n{}".format(json.dumps(response, indent=4)))
    if response['errorCode'] is None:
        logger.info("API session successfully ended. Key file removed.")

@cli.command()
def status():
    """
    Get the current status of the API endpoint.
    This method does not require any parameters.
    The response contains a status orject relfecting
    the current status of the called API.
    """
    logger.info('Calling status().')
    response = api.status()
    logger.debug("Received response:\n{}".format(json.dumps(response, indent=4)))
    # TODO: The datamodels.Status() use might be overkill. Check later if this is a good idea.
    logger.info("API status is: {}.".format(datamodels.Status(response['data']['build_date'])))

@cli.command()
@click.argument('apikey', required=False)
@click.option('--save', required=False, type=click.Path(exists=False))
def notifications(apikey=None,save=None):
    """
    Get all system notifications for the current application context.
    Valid API key is required for this request - use login() to obtain.
    The response contains a list of notifications - see Notification() class in datamodels.py.
    """
    logger.info('Calling notifications().')
    response = api.notifications(apikey)
    logger.debug("Received response:\n{}".format(json.dumps(response, indent=4)))
    n_list = sorted(response['data'], key=lambda k: k['notificationId'])
    if len(n_list) > 0:
        logger.info("Begin system notifications:")
        for note in n_list:
            od = OrderedDict(note)
            for key in ['notificationId','title','severity','message']:
                od[key] = od.pop(key)
            print_dict_items(od)
        logger.info("End of notifications.")
    else:
        logger.info("No notifications.\n")
        print_dict_items(response)
    if save:
        write_to_yaml(n_list, save)

@cli.command()
@click.pass_context
@click.argument('conf_file', required=False, type=click.Path(exists=True))
def cleardownloads(ctx, apikey=None, conf_file=None):
    """
    Clear all pending donwloads from the user's download queue.
    Valid API key is required for this request.
    The request does not have a response.
    Successful execution is assumed if no errors are thrown.
    """
    logger.info("Calling cleardownloads().")
    if conf_file:
        logger.info("Using conf file {}".format(conf_file))
        conf = load_conf_file(conf_file)
        api.cleardownloads(apikey, conf['labels'])
    else:
        logger.info("No conf file provided, clearing all downloads.")
        api.cleardownloads(apikey)
    logger.info('The cleardownloads() API call does not provide a response upon successful execution.')

@cli.command()
@click.pass_context
@click.argument('conf_file', required=True, type=click.Path(exists=True))
@click.option('--save', required=False, type=click.Path(exists=False))
def grid2ll(ctx, conf_file=None, save=None):
    """
    Translate grid reference to coordinates.
    The response contains a list of coordinates defining the shape.
    TODO: Can, and probably should, be adapted to specific needs later on.
    """
    logger.info("Calling grd2ll().")
    if conf_file:
        logger.info("Using conf file {}".format(conf_file))
        conf = load_conf_file(conf_file)
        response = api.grid2ll(conf)
        logger.debug("Received response:\n{}".format(json.dumps(response, indent=4)))
        if save:
            write_to_yaml(response['data'], save)

@cli.command()
@click.pass_context
@click.argument('conf_file', required=True, type=click.Path(exists=True))
@click.option('--save', required=False, type=click.Path(exists=False))
def idlookup(ctx, apikey=None, conf_file=None, save=None):
    """
    Translate from one ID type to another: entityId (Landsat Scene ID) <-> displayId (Landsat Product ID).
    The response contains a dictionary of objects - keys are inputField value,
    values are the corresponding translations.
    TODO: format output.
    """
    logger.info("Calling idlookup().")
    if conf_file:
        logger.info("Using conf file {}".format(conf_file))
        conf = load_conf_file(conf_file)
        response = api.idlookup(apikey, conf)
        logger.debug("Received response:\n{}".format(json.dumps(response, indent=4)))
        if save:
            write_to_yaml(response['data'], save)

@cli.command()
@click.pass_context
@click.argument('conf_file', required=True, type=click.Path(exists=True))
@click.option('--save', required=False, type=click.Path(exists=False))
def search(ctx, apikey=None, conf_file=None, save=None):
    """
    Perform a product search using supplied criteria.
    Valid API key is required for this request - use login() to obtain.
    See params/search.yaml for the structure of payload.
    The request returns a SearchResponse() object - see datamodels.py.
    """
    logger.info("Calling search().")
    if conf_file:
        logger.info("Using conf file {}".format(conf_file))
        conf = load_conf_file(conf_file)
        response = api.search(apikey, conf)
        logger.debug("Received response:\n{}".format(json.dumps(response, indent=4)))
        if save:
            write_to_yaml(response['data'], save)

@cli.command()
@click.pass_context
@click.argument('conf_file', required=True, type=click.Path(exists=True))
@click.option('--save', required=False, type=click.Path(exists=False))
def hits(ctx, apikey=None, conf_file=None, save=None):
    """
    Perform a product search and return the number of products matching
    supplied criteria (as an integer).
    Valid API key is required for this request - use login() to obtain.
    See params/hits.yaml for the structure of payload.
    """
    logger.info("Calling hits().")
    if conf_file:
        logger.info("Using conf file {}".format(conf_file))
        conf = load_conf_file(conf_file)
        response = api.hits(apikey, conf)
        logger.debug("Received response:\n{}".format(json.dumps(response, indent=4)))
        if save:
            write_to_yaml(response['data'], save)

@cli.command()
@click.pass_context
@click.argument('conf_file', required=True, type=click.Path(exists=True))
@click.option('--save', required=False, type=click.Path(exists=False))
def datasets(ctx, apikey=None, conf_file=None, save=None):
    """
    Get a list of datasets available to the user.
    Valid API key is required for this request - use login() to obtain.
    See params/datasets.yaml for the structure of payload argument.
    The response contains a list of dataset objects - see Dataset() class in datamodels.py.
    """
    logger.info("Calling datasets().")
    if conf_file:
        logger.info("Using conf file {}".format(conf_file))
        conf = load_conf_file(conf_file)
        response = api.datasets(apikey, conf)
        logger.debug("Received response:\n{}".format(json.dumps(response, indent=4)))
        if save:
            write_to_yaml(response['data'], save)

@cli.command()
@click.pass_context
@click.argument('conf_file', required=True, type=click.Path(exists=True))
#@click.argument('datasetname', required=False)
# TODO: Check if possible to make conf_file optional and supply datasetname
# directly as a string in command line.
@click.option('--save', required=False, type=click.Path(exists=False))
def datasetfields(ctx, apikey=None, conf_file=None, datasetname=None, save=None):
    """
    Get a list of fields available in the supplied dataset.
    Valid API key is required for this request - use login() to obtain.
    See params/datasetfields.yaml for the structure of the payload argument.
    The response contains a list of dataset field objects - see MetadataField() class in datamodels.py.
    """
    logger.info("Calling datasetfields().")
    if conf_file:
        logger.info("Using conf file {}".format(conf_file))
        datasetname = load_conf_file(conf_file)['datasetName']
    logger.info('Calling datasetfields() with dataset name \'{}\''.format(datasetname))
    response = api.datasetfields(apikey, datasetname)
    logger.debug("Received response:\n{}".format(json.dumps(response, indent=4)))
    if save:
        write_to_yaml(response['data'], save)

@cli.command()
@click.pass_context
@click.argument('conf_file', required=True, type=click.Path(exists=True))
@click.option('--save', required=False, type=click.Path(exists=False))
def downloadoptions(ctx, apikey=None, conf_file=None, save=None):
    """
    Get download options for the supplied list of entity IDs.
    Valid API key is required for this request - use login() to obtain.
    See params/downloadoptions.yaml for the structure of payload.
    Returns a list of DownloadOption() objects - see datamodels.py.
    """
    logger.info("Calling downloadoptions().")
    if conf_file:
        logger.info("Using conf file {}".format(conf_file))
        conf = load_conf_file(conf_file)
        response = api.downloadoptions(apikey, conf)
        logger.debug("Received response:\n{}".format(json.dumps(response, indent=4)))
        if save:
            write_to_yaml(response['data'], save)

@cli.command()
@click.pass_context
@click.argument('conf_file', required=True, type=click.Path(exists=True))
@click.option('--save', required=False, type=click.Path(exists=False))
# TODO: Test me
def download(ctx, apikey=None, conf_file=None, save=None):
    """
    Get download URLs for the supplied list of entity IDs.
    Valid API key is required for this request - use login() to obtain.
    See params/download.yaml for the structure of payload.
    Returns a list of DownloadRecord() (or does it?) objects - see datamodels.py.
    """
    logger.info("Calling download().")
    if conf_file:
        logger.info("Using conf file {}".format(conf_file))
        conf = load_conf_file(conf_file)
        response = api.download(apikey, conf)
        logger.debug("Received response:\n{}".format(json.dumps(response, indent=4)))
        if save:
            write_to_yaml(response['data'], save)

@cli.command()
@click.pass_context
@click.argument('conf_file', required=True, type=click.Path(exists=True))
@click.option('--save', required=False, type=click.Path(exists=False))
def metadata(ctx, apikey=None, conf_file=None, save=None):
    """
    Find (metadata for) downloadable products for each dataset.
    If a download is marked as not available, an order must be placed to generate that product.
    Valid API key is required for this request - use login() to obtain.
    See params/metadata.yaml for the structure of payload.
    The request returns a list of SceneMetdata() objects - see datamodels.py.
    """
    logger.info("Calling metadata().")
    if conf_file:
        logger.info("Using conf file {}".format(conf_file))
        conf = load_conf_file(conf_file)
        response = api.metadata(apikey, conf)
        logger.debug("Received response:\n{}".format(json.dumps(response, indent=4)))
        if save:
            write_to_yaml(response['data'], save)

@cli.command()
@click.pass_context
@click.argument('conf_file', required=True, type=click.Path(exists=True))
@click.option('--save', required=False, type=click.Path(exists=False))
def deletionsearch(ctx, apikey=None, conf_file=None, save=None):
    """
    Detect deleted scenes in a dataset that supports it.
    Valid API key is required for this request - use login() to obtain.
    See params/deletionsearch.yaml for the structure of payload.
    The request returns a DeletionSearchResponse() object - see datamodels.py.
    """
    logger.info("Calling deletionsearch().")
    if conf_file:
        logger.info("Using conf file {}".format(conf_file))
        conf = load_conf_file(conf_file)
        response = api.deletionsearch(apikey, conf)
        logger.debug("Received response:\n{}".format(json.dumps(response, indent=4)))
        if save:
            write_to_yaml(response['data'], save)

def print_dict_items(d):
    """
    Print items in a dictionary, one item per line.
    Avoid using this for responses with complex 'data' elements.
    """
    for k, v in d.items():
        logger.info("{}: {}".format(k, v))

def load_conf_file(conf_file):
    """
    Open a YAML file and return its contents as a data structure.
    """
    with open(conf_file, 'r') as f:
        return yaml.load(f)

def write_to_yaml(data, file_name):
    """
    Write the provided dictionary to YAML file.
    """
    with open(file_name, 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)
