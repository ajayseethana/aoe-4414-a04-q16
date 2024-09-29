# script_name.py
# 
# Usage: python3 ecef_to_sez.py o_x_km o_y_km o_z_km x_km y_km z_km
#  Text explaining script usage
# Parameters:
#  arg1: description of argument 1
#  arg2: description of argument 2
#  ...
# Output:
#  A description of the script output
#
# Written by Ajay Seethana
# Other contributors: None
#
# Optional license statement, e.g., See the LICENSE file for the license.

# import Python modules
# e.g., import math # math module
import sys # argv
import math

# "constants"
# e.g., R_E_KM = 6378.137

R_E_KM = 6378.1363
e_E = 0.081819221456

# helper functions

## function description
# def calc_something(param1, param2):
#   pass

def calc_denom(ecc, lat_rad):
  return math.sqrt(1.0 - ecc ** 2 * math.pow(math.sin(lat_rad), 2))

# initialize script arguments
# arg1 = '' # description of argument 1
# arg2 = '' # description of argument 2
# parse script arguments
if len(sys.argv)==7:
  o_x_km = float(sys.argv[1])
  o_y_km = float(sys.argv[2])
  o_z_km = float(sys.argv[3])
  x_km = float(sys.argv[4])
  y_km = float(sys.argv[5])
  z_km = float(sys.argv[6])
  ...
else:
  print(\
   'Usage: '\
   'python3 arg1 arg2 ...'\
  )
  exit()

# write script below this line

r_x_km = o_x_km - x_km
r_y_km = o_y_km - y_km
r_z_km = o_z_km - z_km

lon_rad = math.atan2(y_km, x_km)

lat_rad = math.asin(z_km/math.sqrt(x_km**2 + y_km**2 + z_km**2))
r_lon_km = math.sqrt(x_km ** 2 + y_km ** 2)
prev_lat_rad = float('nan')

C_E = float('nan')
count = 0
while (math.isnan(prev_lat_rad) or abs(lat_rad - prev_lat_rad) > 10e-7) and count < 5:
    denom = calc_denom(e_E, lat_rad)
    C_E = R_E_KM/denom
    prev_lat_rad = lat_rad
    lat_rad = math.atan((z_km + C_E*(e_E ** 2)*math.sin(lat_rad))/r_lon_km)
    count += 1

hae_km = r_lon_km / math.cos(lat_rad) - C_E

clat = math.cos(lat_rad)
slat = math.sin(lat_rad)

slon = math.sin(lon_rad)
clon = math.cos(lon_rad)

ry_x = r_x_km * clon + r_y_km * slon
ry_y = r_y_km * clon - r_x_km * slon
ry_z = r_z_km

s_km = ry_x * slat - ry_z * clat
e_km = ry_y
z_km = ry_x * clat + ry_z * slat

print(s_km)
print(e_km)
print(z_km)
