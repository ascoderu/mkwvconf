#!/usr/bin/env bash

set -euo pipefail
configDir="$(mktemp -d)"

cleanup() { rm -rf "${configDir}" || true; }
trap cleanup EXIT

echo "
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Running test with simple configuration
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"

countryCode="za"
provider="1"
modemLocation="/dev/ttyUSB1"
profileName="testProfile"
configPath="${configDir}/simpleConfiguration-actual.ini"
expectedConfig="${configDir}/simpleConfiguration-expected.ini"

echo -e "${countryCode}\n${provider}\nY\n${modemLocation}\nY\n${profileName}\nY\n" \
| python -m mkwvconf --configPath="${configPath}"

cat > "${expectedConfig}" << EOF

[Dialer testProfile]
Modem Type = Analog Modem
Phone = *99***1#
ISDN = 0
Baud = 460800
Username = 
Password = 
Modem = /dev/ttyUSB1
Init1 = ATZ
Init2 = at+cgdcont=1,"ip","internet"
Stupid Mode = 1
EOF

diff --side-by-side "${expectedConfig}" "${configPath}"

echo "
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Running test with custom apn
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"

countryCode="ug"
provider="1"
apn="0"
modemLocation="/dev/ttyUSB2"
profileName="testProfile2"
configPath="${configDir}/apnConfiguration-actual.ini"
expectedConfig="${configDir}/apnConfiguration-expected.ini"

echo -e "${countryCode}\n${provider}\nY\n${apn}\nY\n${modemLocation}\nY\n${profileName}\nY\n" \
| python -m mkwvconf --configPath="${configPath}"

cat > "${expectedConfig}" << EOF

[Dialer testProfile2]
Modem Type = Analog Modem
Phone = *99***1#
ISDN = 0
Baud = 460800
Username = 
Password = 
Modem = /dev/ttyUSB2
Init1 = ATZ
Init2 = at+cgdcont=1,"ip","orange.ug"
Stupid Mode = 1
EOF

diff --side-by-side "${expectedConfig}" "${configPath}"
