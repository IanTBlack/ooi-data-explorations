#!/usr/bin/env bash
#
# harvest_cp_phsen.sh
#
# Harvest the phsen data from all of the OOI Coastal Endurance moorings. Data
# sets include telemetered, recovered host and instrument data. Data is
# downloaded from OOI Net and reworked to create a cleaner and more consistent
# set of files named and organized by the mooring, mooring sub-location, data
# delivery method and deployment.
#
# C. Wingard, 2019-07-22 -- Initial code

# set the base directory python command for all subsequent processing
cd /home/ooiuser/code/ooi-data-explorations
PYTHON="python -m instruments.python.uncabled.request_phsen"

### CE01ISSM ###
BASE_FLAGS="-s CE01ISSM -n RID16 -sn 06-PHSEND000"
BASE_FILE="ce01issm/nsif/phsen/ce01issm.nsif.phsen"
for i in $(seq -f "%02g" 1 11); do
	$PYTHON $BASE_FLAGS -mt telemetered -st phsen_abcdef_dcl_instrument -dp $i -o "$BASE_FILE.deploy$i.telemetered.phsen_abcdef_dcl_instrument.nc"
	$PYTHON $BASE_FLAGS -mt recovered_host -st phsen_abcdef_dcl_instrument_recovered -dp $i -o "$BASE_FILE.deploy$i.recovered_host.phsen_abcdef_dcl_instrument_recovered.nc"
	$PYTHON $BASE_FLAGS -mt recovered_inst -st phsen_abcdef_instrument -dp $i -o "$BASE_FILE.deploy$i.recovered_inst.phsen_abcdef_instrument.nc"
done
# Current deployment
$PYTHON $BASE_FLAGS -mt telemetered -st phsen_abcdef_dcl_instrument -dp 12 -o "$BASE_FILE.deploy12.telemetered.phsen_abcdef_dcl_instrument.nc"

BASE_FLAGS="-s CE01ISSM -n MFD35 -sn 06-PHSEND000"
BASE_FILE="ce01issm/seafloor/phsen/ce01issm.seafloor.phsen"
for i in $(seq -f "%02g" 1 11); do
	$PYTHON $BASE_FLAGS -mt telemetered -st phsen_abcdef_dcl_instrument -dp $i -o "$BASE_FILE.deploy$i.telemetered.phsen_abcdef_dcl_instrument.nc"
	$PYTHON $BASE_FLAGS -mt recovered_host -st phsen_abcdef_dcl_instrument_recovered -dp $i -o "$BASE_FILE.deploy$i.recovered_host.phsen_abcdef_dcl_instrument_recovered.nc"
	$PYTHON $BASE_FLAGS -mt recovered_inst -st phsen_abcdef_instrument -dp $i -o "$BASE_FILE.deploy$i.recovered_inst.phsen_abcdef_instrument.nc"
done
# Current deployment
$PYTHON $BASE_FLAGS -mt telemetered -st phsen_abcdef_dcl_instrument -dp 12 -o "$BASE_FILE.deploy12.telemetered.phsen_abcdef_dcl_instrument.nc"

### CE02SHSM ###
BASE_FLAGS="-s CE02SHSM -n RID26 -sn 06-PHSEND000"
BASE_FILE="ce02shsm/nsif/phsen/ce02shsm.nsif.phsen"
for i in $(seq -f "%02g" 1 9); do
  $PYTHON $BASE_FLAGS -mt telemetered -st phsen_abcdef_dcl_instrument -dp $i -o "$BASE_FILE.deploy$i.telemetered.phsen_abcdef_dcl_instrument.nc"
  $PYTHON $BASE_FLAGS -mt recovered_host -st phsen_abcdef_dcl_instrument_recovered -dp $i -o "$BASE_FILE.deploy$i.recovered_host.phsen_abcdef_dcl_instrument_recovered.nc"
  $PYTHON $BASE_FLAGS -mt recovered_inst -st phsen_abcdef_instrument -dp $i -o "$BASE_FILE.deploy$i.recovered_inst.phsen_abcdef_instrument.nc"
done
# Current deployment
$PYTHON $BASE_FLAGS -mt telemetered -st phsen_abcdef_dcl_instrument -dp 10 -o "$BASE_FILE.deploy10.telemetered.phsen_abcdef_dcl_instrument.nc"

### CE04OSSM ###
BASE_FLAGS="-s CE04OSSM -n RID26 -sn 06-PHSEND000"
BASE_FILE="ce04ossm/nsif/phsen/ce04ossm.nsif.phsen"
for i in $(seq -f "%02g" 1 8); do
  $PYTHON $BASE_FLAGS -mt telemetered -st phsen_abcdef_dcl_instrument -dp $i -o "$BASE_FILE.deploy$i.telemetered.phsen_abcdef_dcl_instrument.nc"
  $PYTHON $BASE_FLAGS -mt recovered_host -st phsen_abcdef_dcl_instrument_recovered -dp $i -o "$BASE_FILE.deploy$i.recovered_host.phsen_abcdef_dcl_instrument_recovered.nc"
  $PYTHON $BASE_FLAGS -mt recovered_inst -st phsen_abcdef_instrument -dp $i -o "$BASE_FILE.deploy$i.recovered_inst.phsen_abcdef_instrument.nc"
done
# Current deployment
$PYTHON $BASE_FLAGS -mt telemetered -st phsen_abcdef_dcl_instrument -dp 09 -o "$BASE_FILE.deploy09.telemetered.phsen_abcdef_dcl_instrument.nc"

### CE06ISSM ###
BASE_FLAGS="-s CE06ISSM -n RID16 -sn 06-PHSEND000"
BASE_FILE="ce06issm/nsif/phsen/ce06issm.nsif.phsen"
for i in $(seq -f "%02g" 1 10); do
	$PYTHON $BASE_FLAGS -mt telemetered -st phsen_abcdef_dcl_instrument -dp $i -o "$BASE_FILE.deploy$i.telemetered.phsen_abcdef_dcl_instrument.nc"
	$PYTHON $BASE_FLAGS -mt recovered_host -st phsen_abcdef_dcl_instrument_recovered -dp $i -o "$BASE_FILE.deploy$i.recovered_host.phsen_abcdef_dcl_instrument_recovered.nc"
	$PYTHON $BASE_FLAGS -mt recovered_inst -st phsen_abcdef_instrument -dp $i -o "$BASE_FILE.deploy$i.recovered_inst.phsen_abcdef_instrument.nc"
done
# Current deployment
$PYTHON $BASE_FLAGS -mt telemetered -st phsen_abcdef_dcl_instrument -dp 11 -o "$BASE_FILE.deploy11.telemetered.phsen_abcdef_dcl_instrument.nc"

BASE_FLAGS="-s CE06ISSM -n MFD35 -sn 06-PHSEND000"
BASE_FILE="ce06issm/seafloor/phsen/ce06issm.seafloor.phsen"
for i in $(seq -f "%02g" 1 9); do
	$PYTHON $BASE_FLAGS -mt telemetered -st phsen_abcdef_dcl_instrument -dp $i -o "$BASE_FILE.deploy$i.telemetered.phsen_abcdef_dcl_instrument.nc"
	$PYTHON $BASE_FLAGS -mt recovered_host -st phsen_abcdef_dcl_instrument_recovered -dp $i -o "$BASE_FILE.deploy$i.recovered_host.phsen_abcdef_dcl_instrument_recovered.nc"
	$PYTHON $BASE_FLAGS -mt recovered_inst -st phsen_abcdef_instrument -dp $i -o "$BASE_FILE.deploy$i.recovered_inst.phsen_abcdef_instrument.nc"
done
# Current deployment
$PYTHON $BASE_FLAGS -mt telemetered -st phsen_abcdef_dcl_instrument -dp 11 -o "$BASE_FILE.deploy11.telemetered.phsen_abcdef_dcl_instrument.nc"

### CE07SHSM ###
BASE_FLAGS="-s CE07SHSM -n RID26 -sn 06-PHSEND000"
BASE_FILE="ce07shsm/nsif/phsen/ce07shsm.nsif.phsen"
for i in $(seq -f "%02g" 1 9); do
  $PYTHON $BASE_FLAGS -mt telemetered -st phsen_abcdef_dcl_instrument -dp $i -o "$BASE_FILE.deploy$i.telemetered.phsen_abcdef_dcl_instrument.nc"
  $PYTHON $BASE_FLAGS -mt recovered_host -st phsen_abcdef_dcl_instrument_recovered -dp $i -o "$BASE_FILE.deploy$i.recovered_host.phsen_abcdef_dcl_instrument_recovered.nc"
  $PYTHON $BASE_FLAGS -mt recovered_inst -st phsen_abcdef_instrument -dp $i -o "$BASE_FILE.deploy$i.recovered_inst.phsen_abcdef_instrument.nc"
done
# Current deployment
$PYTHON $BASE_FLAGS -mt telemetered -st phsen_abcdef_dcl_instrument -dp 10 -o "$BASE_FILE.deploy10.telemetered.phsen_abcdef_dcl_instrument.nc"

BASE_FLAGS="-s CE07SHSM -n MFD35 -sn 06-PHSEND000"
BASE_FILE="ce07shsm/seafloor/phsen/ce07shsm.seafloor.phsen"
for i in $(seq -f "%02g" 1 9); do
    $PYTHON $BASE_FLAGS -mt telemetered -st phsen_abcdef_dcl_instrument -dp $i -o "$BASE_FILE.deploy$i.telemetered.phsen_abcdef_dcl_instrument.nc"
    $PYTHON $BASE_FLAGS -mt recovered_host -st phsen_abcdef_dcl_instrument_recovered -dp $i -o "$BASE_FILE.deploy$i.recovered_host.phsen_abcdef_dcl_instrument_recovered.nc"
    $PYTHON $BASE_FLAGS -mt recovered_inst -st phsen_abcdef_instrument -dp $i -o "$BASE_FILE.deploy$i.recovered_inst.phsen_abcdef_instrument.nc"
done
# Current deployment
$PYTHON $BASE_FLAGS -mt telemetered -st phsen_abcdef_dcl_instrument -dp 10 -o "$BASE_FILE.deploy10.telemetered.phsen_abcdef_dcl_instrument.nc"

### CE09OSSM ###
BASE_FLAGS="-s CE09OSSM -n RID26 -sn 06-PHSEND000"
BASE_FILE="ce09ossm/nsif/phsen/ce09ossm.nsif.phsen"
for i in $(seq -f "%02g" 1 9); do
  # no longer using burst mode, just collect and rework
  $PYTHON $BASE_FLAGS -mt telemetered -st phsen_abcdef_dcl_instrument -dp $i -o "$BASE_FILE.deploy$i.telemetered.phsen_abcdef_dcl_instrument.nc"
  $PYTHON $BASE_FLAGS -mt recovered_host -st phsen_abcdef_dcl_instrument_recovered -dp $i -o "$BASE_FILE.deploy$i.recovered_host.phsen_abcdef_dcl_instrument_recovered.nc"
  $PYTHON $BASE_FLAGS -mt recovered_inst -st phsen_abcdef_instrument -dp $i -o "$BASE_FILE.deploy$i.recovered_inst.phsen_abcdef_instrument.nc"
done
# Current deployment
$PYTHON $BASE_FLAGS -mt telemetered -st phsen_abcdef_dcl_instrument -dp 10 -o "$BASE_FILE.deploy10.telemetered.phsen_abcdef_dcl_instrument.nc"

BASE_FLAGS="-s CE09OSSM -n MFD35 -sn 06-PHSEND000"
BASE_FILE="ce09ossm/seafloor/phsen/ce09ossm.seafloor.phsen"
for i in $(seq -f "%02g" 1 9); do
    $PYTHON $BASE_FLAGS -mt telemetered -st phsen_abcdef_dcl_instrument -dp $i -o "$BASE_FILE.deploy$i.telemetered.phsen_abcdef_dcl_instrument.nc"
    $PYTHON $BASE_FLAGS -mt recovered_host -st phsen_abcdef_dcl_instrument_recovered -dp $i -o "$BASE_FILE.deploy$i.recovered_host.phsen_abcdef_dcl_instrument_recovered.nc"
    $PYTHON $BASE_FLAGS -mt recovered_inst -st phsen_abcdef_instrument -dp $i -o "$BASE_FILE.deploy$i.recovered_inst.phsen_abcdef_instrument.nc"
done
# Current deployment
$PYTHON $BASE_FLAGS -mt telemetered -st phsen_abcdef_dcl_instrument -dp 10 -o "$BASE_FILE.deploy10.telemetered.phsen_abcdef_dcl_instrument.nc"
