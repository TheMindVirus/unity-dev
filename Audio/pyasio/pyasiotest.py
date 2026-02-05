import pyasio

print(dir(pyasio))
drivers = pyasio.PyAsioDrivers()
drvlist = pyasio.PyAsioDriverList()

max_drivers = 0
max_drivers = drvlist.asioGetNumDev()
print("drivers:", max_drivers)

names = [0] * 32 * max_drivers
data = [0] * 255
drv_id = 0

for i in range(0, max_drivers):
    name = [0] * 32
    result = drvlist.asioGetDriverName(i, name, 32)
    names[(i * 32):(i * 32) + 32] = name
    if bytes(name[0:11]) == b"ASIO4ALL v2":
        drv_id = i

names = [0] * 32 * max_drivers
result = drivers.getDriverNames(names, max_drivers)
print("get_names:", result)
for i in range(0, max_drivers):
    nm = bytes(names[(i * 32):(i * 32) + 32]).decode()
    print(nm)
    
result = drvlist.asioOpenDriver(drv_id, data)
print("open:", result)

name2 = [0] * 32
data2 = [0] * 255
name3 = [0] * 32

drvlist.asioGetDriverName(drv_id, name2, 32)
result = drivers.loadDriver(name2)
print("load_driver:", result)

result = drivers.getCurrentDriverIndex()
print("driver_index:", result)

result = drivers.getCurrentDriverName(name3)
print("driver_name:", result)
print(bytes(name3)[0:32].decode())

result = pyasio.PyASIOInit(data2)
print("init:", result)
for i in range(0, 255):
    if data2[i] != 0:
        print(chr(data2[i]), end = "")
print()

result = pyasio.PyASIOControlPanel()
print("control_panel:", result)

result = drvlist.asioCloseDriver(drv_id)
print("close:", result)
