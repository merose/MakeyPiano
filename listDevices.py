from evdev import InputDevice, list_devices
devices = map(InputDevice, list_devices())
for dev in devices:
  print( '%-20s %-32s %s' % (dev.fn, dev.name, dev.phys) )

