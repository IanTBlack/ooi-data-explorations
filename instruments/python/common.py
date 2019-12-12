#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author Christopher Wingard
@brief Provides common base classes, definitions and other utilities used to access and download OOI data via the
    M2M interface
"""
import argparse
import collections
import netrc
import numpy as np
import os
import re
import requests
import sys
import time
import xarray as xr
import yaml

from bs4 import BeautifulSoup
from tqdm import tqdm

# setup constants used to access the data from the different M2M interfaces
BASE_URL = 'https://ooinet.oceanobservatories.org/api/m2m/'  # base M2M URL
ANNO_URL = '12580/anno/'                                     # Annotation Information
ASSET_URL = '12587/asset/'                                   # Asset and Calibration Information
DEPLOY_URL = '12587/events/deployment/inv/'                  # Deployment Information
SENSOR_URL = '12576/sensor/inv/'                             # Sensor Information
VOCAB_URL = '12586/vocab/inv/'                               # Vocabulary Information
STREAM_URL = '12575/stream/byname/'                          # Stream Information
PARAMETER_URL = '12575/parameter/'                           # Parameter Information

# setup access credentials
nrc = netrc.netrc()  # best option is user has their own account
AUTH = nrc.authenticators('ooinet.oceanobservatories.org')
if AUTH is None:
    # Use our default user credentials.
    AUTH = ['OOIAPI-853A3LA6QI3L62', 'WYAN89W5X4Z0QZ']
    raise Warning('Using default access credentials for the OOI Coastal Endurance Data Team. ' +
                  'User is encouraged to setup their own access credentials in a netrc file ' +
                  'maintained in their home directory using ooinet.oceanobservatories.org as the ' +
                  'machine name.')

# load configuration settings
if '__file__' in vars():
    wk_dir = os.path.dirname(os.path.realpath(__file__))
    config_file = os.path.join(wk_dir, 'config.yaml')
else:
    wk_dir = os.getcwd()
    config_file = os.path.join(wk_dir, 'instruments', 'python', 'config.yaml')

if os.path.isfile(config_file):
    CONFIG = yaml.safe_load(open(config_file))
else:
    raise SystemError('Unable to load configuration file. User needs to edit the config.yaml file (using the ' +
                      'config.yaml.changeme file as a template) to set directory paths for where the data ' +
                      'will be saved.')


def list_nodes(site):
    """
    Based on the site name, list the nodes that are available.

    :param site: Site name to query
    :return: List of the the available nodes for this site
    """
    r = requests.get(BASE_URL + DEPLOY_URL + site, auth=(AUTH[0], AUTH[2]))
    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        return None


def list_sensors(site, node):
    """
    Based on the site and node name, list the sensors that are available.

    :param site: Site name to query
    :param node: Node name to query
    :return: list of the the available sensors for this site and node
    """
    r = requests.get(BASE_URL + DEPLOY_URL + site + '/' + node, auth=(AUTH[0], AUTH[2]))
    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        return None


def list_methods(site, node, sensor):
    """
    Based on the site, node and sensor name, list the data delivery methods that are available.

    :param site: Site name to query
    :param node: Node name to query
    :param sensor: Sensor name to query
    :return: list of the data delivery methods associated with this site, node and sensor
    """
    r = requests.get(BASE_URL + SENSOR_URL + site + '/' + node + '/' + sensor, auth=(AUTH[0], AUTH[2]))
    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        return None


def list_streams(site, node, sensor, method):
    """
    Based on the site, node and sensor name and the data delivery method, list the data streams that are available.

    :param site: Site name to query
    :param node: Node name to query
    :param sensor: Sensor name to query
    :param method: Data delivery method to query
    :return: list of the data streams associated with this site, node, sensor and data delivery method
    """
    # Determine the streams associated with the delivery method available for this sensor
    r = requests.get(BASE_URL + SENSOR_URL + site + '/' + node + '/' + sensor + '/' + method, auth=(AUTH[0], AUTH[2]))
    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        return None


def list_deployments(site, node, sensor):
    """
    Based on the site, node and sensor name, list the deployment numbers that are available.

    :param site: Site name to query
    :param node: Node name to query
    :param sensor: Sensor name to query
    :return: list of the deployments of this site, node and sensor combination
    """
    r = requests.get(BASE_URL + DEPLOY_URL + site + '/' + node + '/' + sensor, auth=(AUTH[0], AUTH[2]))
    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        return None


def deployment_dates(site, node, sensor, deploy):
    """
    Based on the site, node and sensor names and the deployment number, determine the start and end times for a
    deployment.

    :param site: Site name to query
    :param node: Node name to query
    :param sensor: Sensor name to query
    :param deploy: Deployment number
    :return: start and stop dates for the deployment of interest
    """
    # request deployment metadata
    r = requests.get(BASE_URL + DEPLOY_URL + site + '/' + node + '/' + sensor + '/' + str(deploy), auth=(AUTH[0],
                                                                                                         AUTH[2]))
    if r.status_code == requests.codes.ok:
        data = r.json()
    else:
        return None, None

    # use the metadata to extract the start and end times for the deployment
    if data:
        start = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime(data[0]['eventStartTime'] / 1000.))
    else:
        return None, None

    if data[0]['eventStopTime']:
        # check to see if there is a stop time for the deployment, if so use it ...
        stop = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime(data[0]['eventStopTime'] / 1000.))
    else:
        # ... otherwise use the current time as this is an active deployment
        stop = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime(time.time()))

    return start, stop


def get_vocabulary(site, node, sensor):
    """
    Based on the site, node and sensor name download the vocabulary record defining this sensor.

    :param site: Site name to query
    :param node: Node name to query
    :param sensor: Sensor name to query
    :return: json object with the site-node-sensor specific vocabulary
    """
    r = requests.get(BASE_URL + VOCAB_URL + site + '/' + node + '/' + sensor, auth=(AUTH[0], AUTH[2]))
    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        return None


def get_stream_information(stream):
    """
    Use the stream name to retrieve information about the stream contents: parameters, units, sources, etc.

    :param stream: Stream name
    :return: json object with information on the contents of the stream
    """
    r = requests.get(BASE_URL + STREAM_URL + stream, auth=(AUTH[0], AUTH[2]))
    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        return None


def get_parameter_information(parameter_id):
    """
    Use the Parameter ID# to retrieve information about the parameter: units, sources, data product ID, comments,etc.

    :param parameter_id: Stream name
    :return: json object with information on the parameter of interest
    """
    r = requests.get(BASE_URL + PARAMETER_URL + parameter_id, auth=(AUTH[0], AUTH[2]))
    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        return None


def m2m_request(site, node, sensor, method, stream, start=None, stop=None):
    """
    Request data from OOINet for a particular instrument (as defined by the reference designator), delivery method
    and stream name via the M2M system. Optionally, can bound the data with a beginning and ending date and time range.

    :param site: Site designator, extracted from the first part of the reference designator
    :param node: Node designator, extracted from the second part of the reference designator
    :param sensor: Sensor designator, extracted from the third and fourth part of the reference designator
    :param method: Delivery method for the data (either telemetered, recovered_host, or recovered_inst)
    :param stream: Stream name that contains the data of interest
    :param start: Start time for data request (Optional, default is beginning of record)
    :param stop: Stop time for data request (Optional, default is through the end of the record)
    :return: The results of the data request detailing where the data is located for download
    """
    # setup the beginning and ending date/time
    if start:
        begin_date = '?beginDT=' + start
    else:
        begin_date = '?beginDT=0'   # use default of 0 to request all data from the beginning of the record

    if stop:
        end_date = '&endDT=' + stop
    else:
        end_date = ''

    options = begin_date + end_date + '&format=application/netcdf'
    r = requests.get(BASE_URL + SENSOR_URL + site + '/' + node + '/' + sensor + '/' + method + '/' + stream + options,
                     auth=(AUTH[0], AUTH[2]))
    if r.status_code == requests.codes.ok:
        data = r.json()
    else:
        return None

    # wait until the request is completed
    print('Waiting for OOINet to process and prepare data request, this may take up to 10 minutes\n')
    check_complete = data['allURLs'][1] + '/status.txt'
    with tqdm(total=200, desc='Processing Request') as bar:
        for i in range(200):
            r = requests.get(check_complete)
            bar.update(1)
            if r.status_code == requests.codes.ok:
                bar.n = 200
                bar.last_print_n = 200
                bar.refresh()
                print('\nrequest completed in %f minutes.' % elapsed)
                break
            else:
                time.sleep(3)
                elapsed = (i * 3) / 60

    return data


def m2m_collect(data, tag=''):
    """
    Use a regex tag combined with the results of the M2M data request to collect the data from the THREDDS catalog.
    Collected data is gathered into an xarray dataset for further processing.

    :param data: JSON object returned from M2M data request with details on where the data is to be found for download
    :param tag: regex tag to use in discriminating the data files, so we only collect the correct ones
    :return: the collected data as an xarray dataset
    """
    # Create a list of the files from the request above using a simple regex as a tag to discriminate the files
    files = list_files(data['allURLs'][0], tag)

    # Process the data files found above and concatenate into a single data set
    frames = [process_file(f) for f in files]
    m2m = xr.concat(frames, 'time')
    m2m = m2m.sortby('time')

    return m2m


def list_files(url, tag=''):
    """
    Function to create a list of the NetCDF data files in the THREDDS catalog created by a request to the M2M system.

    :param url: URL to user's THREDDS catalog specific to a data request
    :param tag: regex pattern used to distinguish files of interest
    :return: list of files in the catalog with the URL path set relative to the catalog
    """
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    pattern = re.compile(tag)
    return [node.get('href') for node in soup.find_all('a', text=pattern)]


def process_file(catalog_file):
    """
    Function to download one of the NetCDF files as an xarray data set, convert to time as the appropriate dimension
    instead of obs, and drop the extraneous timestamp variables (these were originally not intended to be exposed to
    users and lead to confusion as to their meaning). The ID and provenance variables are better off obtained directly
    from the M2M system via a different process. Having them included imposes unnecessary constraints.

    :param catalog_file: Unique file, referenced by a URL relative to the catalog, to download and convert the data
        file to an xarray data set.
    :return: downloaded data in an xarray dataset.
    """
    dods_url = 'https://opendap.oceanobservatories.org/thredds/dodsC/'
    url = re.sub('catalog.html\?dataset=', dods_url, catalog_file)
    with xr.open_dataset(url, cache=False) as xrd:
        ds = xrd.load()

    ds = ds.swap_dims({'obs': 'time'})
    ds = ds.drop(['obs', 'id', 'driver_timestamp', 'ingestion_timestamp', 'port_timestamp', 'preferred_timestamp'])
    ds = ds.sortby('time')

    # resetting cdm_data_type from Point to Station and the featureType from point to timeSeries
    ds.attrs['cdm_data_type'] = 'Station'
    ds.attrs['featureType'] = 'timeSeries'

    # clear-up some global attributes we will no longer be using
    keys = ['DODS.strlen', 'DODS.dimName', 'DODS_EXTRA.Unlimited_Dimension', '_NCProperties', 'feature_Type']
    for key in keys:
        if key in ds.attrs:
            del(ds.attrs[key])

    # update some of the global attributes
    ds.attrs['acknowledgement'] = 'National Science Foundation'
    ds.attrs['comment'] = 'Data collected from the OOI M2M API and reworked for use in locally stored NetCDF files.'
    ds.attrs['publisher_email'] = 'ooice.platforms@gmail.com'
    ds.attrs['creator_email'] = 'ooice.platforms@gmail.com'

    return ds


def update_dataset(ds, depth):
    """
    Updates a data set with global and variable level metadata attributes and sets appropriate dimensions and
    coordinate axes.

    :param ds: Data set to update
    :param depth: instrument deployment depth
    :return ds: The updated data set
    """
    # add a default station identifier as a coordinate variable to the data set
    ds.coords['station'] = 0
    ds = ds.expand_dims('station', axis=None)
    ds['station'].attrs = dict({
        'cf_role': 'timeseries_id',
        'long_name': 'Station Identifier',
        'comment': ds.attrs['subsite'].upper()
    })

    # determine if the latitude and longitude are set as global attribute or a variable, and parse accordingly
    if 'lat' in ds.variables:
        lat = ds.lat.values[0][0]
        lon = ds.lon.values[0][0]
        ds.drop(['lat', 'lon'])
    else:
        lat = ds.attrs['lat']
        lon = ds.attrs['lon']
        del(ds.attrs['lat'])
        del(ds.attrs['lon'])

    # add the geospatial coordinates using the station identifier from above as the dimension
    geo_coords = xr.Dataset({
        'lat': ('station', [lat]),
        'lon': ('station', [lon]),
        'z': ('station', [depth])
    }, coords={'station': [0]})

    geo_attrs = dict({
        'station': {
            'cf_role': 'timeseries_id',
            'long_name': 'Station Identifier',
            'comment': ds.attrs['subsite'].upper()
        },
        'lon': {
            'long_name': 'Longitude',
            'standard_name': 'longitude',
            'units': 'degrees_east',
            'axis': 'X',
            'comment': 'Deployment location'
        },
        'lat': {
            'long_name': 'Latitude',
            'standard_name': 'latitude',
            'units': 'degrees_north',
            'axis': 'Y',
            'comment': 'Deployment location'
        },
        'z': {
            'long_name': 'Depth',
            'standard_name': 'depth',
            'units': 'm',
            'comment': 'Instrument deployment depth',
            'positive': 'down',
            'axis': 'Z'
        }
    })
    for v in geo_coords.variables:
        geo_coords[v].attrs = geo_attrs[v]

    # merge the geospatial coordinates into the data set
    ds = ds.merge(geo_coords)

    # update coordinate attributes for all variables
    for v in ds.variables:
        if v not in ['time', 'lat', 'lon', 'z', 'station']:
            ds[v].attrs['coordinates'] = 'time lon lat z'

    # update some variable attributes to get somewhat closer to IOOS compliance, more importantly convert QC variables
    # to bytes and set the attributes to define the flag masks and meanings.
    ds['deployment'].attrs['long_name'] = 'Deployment Number'   # add missing long_name attribute
    qc_pattern = re.compile(r'^.+_qc_.+$')
    executed_pattern = re.compile(r'^.+_qc_executed$')
    results_pattern = re.compile(r'^.+_qc_results$')
    flag_masks = np.array([1, 2, 4, 8, 16, 32, 64, 128], dtype=np.uint8)
    for v in ds.variables:
        if qc_pattern.match(v):     # update QC variables
            ds[v] = (('station', 'time'), [[np.uint8(x) for x in ds[v].values[0]]])
            ds[v].attrs['long_name'] = re.sub('Qc', 'QC', re.sub('_', ' ', v.title()))

            if executed_pattern.match(v):   # *_qc_executed variables
                ds[v].attrs['flag_masks'] = flag_masks
                ds[v].attrs['flag_meanings'] = ('global_range_test local_range_test spike_test poly_trend_test ' +
                                                'stuck_value_test gradient_test propogate_flags')
                ds[v].attrs['comment'] = 'Automated QC tests executed for the associated named variable.'

                ancillary = re.sub('_qc_executed', '', v)
                ds[v].attrs['ancillary_variables'] = ancillary
                if 'standard_name' in ds[ancillary].attrs:
                    ds[v].attrs['standard_name'] = ds[ancillary].attrs['standard_name'] + ' qc_tests_executed'

            if results_pattern.match(v):    # *_qc_results variables
                ds[v].attrs['flag_masks'] = flag_masks
                ds[v].attrs['flag_meanings'] = ('global_range_test_passed local_range_test_passed spike_test_passed ' +
                                                'poly_trend_test_passed stuck_value_test_passed gradient_test_passed ' +
                                                'all_tests_passed')
                ds[v].attrs['comment'] = ('QC result flags are set to true (1) if the test passed. Otherwise, if ' +
                                          'the test failed or was not executed, the flag is set to false (0).')

                ancillary = re.sub('_qc_results', '', v)
                ds[v].attrs['ancillary_variables'] = ancillary
                if 'standard_name' in ds[ancillary].attrs:
                    ds[v].attrs['standard_name'] = ds[ancillary].attrs['standard_name'] + ' qc_tests_results'

    # convert the time values from a datetime64[ns] object to a floating point number with the time in seconds
    ds['time'] = dt64_epoch(ds.time)
    ds['time'].attrs = dict({
        'long_name': 'Time',
        'standard_name': 'time',
        'units': 'seconds since 1970-01-01 00:00:00 0:00',
        'axis': 'T',
        'calendar': 'gregorian'
    })

    # return the data set for further work
    return ds


def dt64_epoch(dt64):
    """
    Convert a panda or xarray date/time value represented as a datetime64 object (nanoseconds since 1970) to a float,
    representing an epoch time stamp (seconds since 1970-01-01).

    :param dt64: panda or xarray datatime64 object
    :return epts: epoch time as seconds since 1970-01-01
    """
    epts = dt64.values.astype(float) / 10.0 ** 9
    return epts


def dict_update(source, overrides):
    """
    Update a nested dictionary or similar mapping. Modifies ``source`` in place.

    From https://stackoverflow.com/a/30655448. Replaces original dict_update used by poceans-core, also pulled from
    the same thread.
    """
    for key, value in overrides.items():
        if isinstance(value, collections.Mapping) and value:
            returned = dict_update(source.get(key, {}), value)
            source[key] = returned
        else:
            source[key] = overrides[key]
    return source


def inputs(argv=None):
    """
    Sets the main input arguments that would be passed by the M2M requesting module.
    """
    if argv is None:
        argv = sys.argv[1:]

    # initialize argument parser
    parser = argparse.ArgumentParser(description="""Request and obtain data from the OOI M2M system""",
                                     epilog="""Obtain data from the OOI M2M system""")

    # assign input arguments.
    parser.add_argument("-s", "--site", dest="site", type=str, required=True)
    parser.add_argument("-n", "--node", dest="node", type=str, required=True)
    parser.add_argument("-sn", "--sensor", dest="sensor", type=str, required=True)
    parser.add_argument("-mt", "--method", dest="method", type=str, required=True)
    parser.add_argument("-st", "--stream", dest="stream", type=str, required=True)
    parser.add_argument("-dp", "--deploy", dest="deploy", type=int, required=False)
    parser.add_argument("-bt", "--beginDT", dest="start", type=str, required=False)
    parser.add_argument("-et", "--endDT", dest="stop", type=str, required=False)
    parser.add_argument("-ba", "--burst_average", dest="burst", default=False, action='store_true')
    parser.add_argument("-o", "--outfile", dest="outfile", type=str, required=True)

    # parse the input arguments and create a parser object
    args = parser.parse_args(argv)

    return args
