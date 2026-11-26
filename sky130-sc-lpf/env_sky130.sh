#!/bin/bash
# Environment switcher for sky130-sc-lpf on iic-osic-tools
# Usage: source /headless/ANN/sky130-sc-lpf/env_sky130.sh

export PDK_ROOT="/foss/pdks"
export PDK="sky130A"
export PDKPATH="${PDK_ROOT}/${PDK}"
export STD_CELL_LIBRARY="sky130_fd_sc_hd"
export SPICE_USERINIT_DIR="/headless/ANN/sky130-sc-lpf/ngspice"
export KLAYOUT_PATH="/headless/.klayout:${PDKPATH}/libs.tech/klayout"
export SKYWATER_MODELS="${PDKPATH}/libs.tech/combined"
export XSCHEM_USER_LIBRARY_PATH="/headless/ANN/sky130-sc-lpf/xschem"

echo "[sky130-sc-lpf] Environment switched to PDK=${PDK} (${PDKPATH})"
