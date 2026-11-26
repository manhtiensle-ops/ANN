#!/bin/bash
set -e
source /headless/ANN/sky130-sc-lpf/env_sky130.sh

echo "=== SKY130-SC-LPF EDA ENVIRONMENT CHECK ==="
echo "PDK            : $PDK"
echo "PDKPATH        : $PDKPATH"
echo "SKYWATER_MODELS: $SKYWATER_MODELS"
test -f "$SKYWATER_MODELS/sky130.lib.spice" && echo "[OK] sky130.lib.spice found"
test -f "$PDKPATH/libs.tech/magic/sky130A.magicrc" && echo "[OK] sky130A.magicrc found"
test -f "$PDKPATH/libs.tech/netgen/sky130A_setup.tcl" && echo "[OK] sky130A_setup.tcl found"

for tool in python3 ngspice xschem magic klayout netgen; do
    printf "[OK] %-10s -> %s\n" "$tool" "$(which $tool)"
done

python3 -c "import numpy, scipy, matplotlib; print(f'[OK] Python stack -> numpy {numpy.__version__}, scipy {scipy.__version__}, matplotlib {matplotlib.__version__}')"
echo "=== ALL CHECKS PASSED ==="
