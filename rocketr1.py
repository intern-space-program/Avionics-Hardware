import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_mma8451
import adafruit_rfm9x
import adafruit_bmp280
from datetime import datetime


# Configure LoRa Radio
CS = DigitalInOut(board.D5)
RESET = DigitalInOut(board.D6)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
rfm9x.tx_power = 23
packet_num = 0

#Configure BMP (0x77)and MMA (0x1d)
i2c = busio.I2C(board.SCL, board.SDA)
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
bmp280.sea_level_pressure = 1013.25

#Configure Accelerometer
mma= adafruit_mma8451.MMA8451(i2c)
mma.range = adafruit_mma8451.RANGE_8G
mma.data_rate = adafruit_mma8451.DATARATE_400HZ

#configure file to werite to
file=open("rocketdata.txt", "a")
file.write("Intern Space Program\n")
file.write(datetime.now().strftime('%Y -%m-%d %H:%M:%S'))
file.write("\n\n")
file.close()


# GPS Code
# Will wait for a fix and print a message every second with the current location
# and other details.
import adafruit_gps
import serial

# Create a serial connection for the GPS connection using default speed and
# a slightly higher timeout (GPS modules typically update once a second).
#uart = busio.UART(TX, RX, baudrate=9600, timeout=30)

# for a computer, use the pyserial library for uart access
import serial
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=3000)

# Create a GPS module instance.
gps = adafruit_gps.GPS(uart, debug=False)

# Initialize the GPS module by changing what data it sends and at what rate.
# These are NMEA extensions for PMTK_314_SET_NMEA_OUTPUT and
# PMTK_220_SET_NMEA_UPDATERATE but you can send anything from here to adjust
# the GPS module behavior:
#   https://cdn-shop.adafruit.com/datasheets/PMTK_A11.pdf

# Turn on the basic GGA and RMC info (what you typically want)
gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
# Turn on just minimum info (RMC only, location):
#gps.send_command(b'PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
# Turn off everything:
#gps.send_command(b'PMTK314,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
# Tuen on everything (not all of it is parsed!)
#gps.send_command(b'PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0')

# Set update rate to once a second (1hz) which is what you typically want.
gps.send_command(b'PMTK220,1000')
# Or decrease to once every two seconds by doubling the millisecond value.
# Be sure to also increase your UART timeout above!
#gps.send_command(b'PMTK220,2000')
# You can also speed up the rate, but don't go too fast or else you can lose
# data during parsing.  This would be twice a second (2hz, 500ms delay):
#gps.send_command(b'PMTK220,500')

# Main loop runs forever printing the location, etc. every second.
last_print = time.monotonic()
while True:
    # Make sure to call gps.update() every loop iteration and at least twice
    # as fast as data comes from the GPS unit (usually every second).
    # This returns a bool that's true if it parsed new data (you can ignore it
    # though if you don't care and instead look at the has_fix property).
    gps.update()
    # Every second print out current location details if there's a fix.
    current = time.monotonic()
    if current - last_print >= 1.0:
        last_print = current
        if not gps.has_fix:
            # Try again if we don't have a fix yet.
            print('Waiting for fix...')
            continue
        # We have a fix! (gps.has_fix is true)
        # Print out details about the fix like location, date, etc.
        print('=' * 40)  # Print a separator line.
        print('Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}'.format(
            gps.timestamp_utc.tm_mon,   # Grab parts of the time from the
            gps.timestamp_utc.tm_mday,  # struct_time object that holds
            gps.timestamp_utc.tm_year,  # the fix time.  Note you might
            gps.timestamp_utc.tm_hour,  # not get all data like year, day,
            gps.timestamp_utc.tm_min,   # month!
            gps.timestamp_utc.tm_sec))
        print('Latitude: {0:.6f} degrees'.format(gps.latitude))
        print('Longitude: {0:.6f} degrees'.format(gps.longitude))
        print('Fix quality: {}'.format(gps.fix_quality))
        # Some attributes beyond latitude, longitude and timestamp are optional
        # and might not be present.  Check if they're None before trying to use!
        if gps.satellites is not None:
            print('# satellites: {}'.format(gps.satellites))
        if gps.altitude_m is not None:
            print('Altitude: {} meters'.format(gps.altitude_m))
        if gps.speed_knots is not None:
            print('Speed: {} knots'.format(gps.speed_knots))
        if gps.track_angle_deg is not None:
            print('Track angle: {} degrees'.format(gps.track_angle_deg))
        if gps.horizontal_dilution is not None:
            print('Horizontal dilution: {}'.format(gps.horizontal_dilution))
        if gps.height_geoid is not None:
            print('Height geo ID: {} meters'.format(gps.height_geoid))
   #print("Running Continous Program")
    file=open("rocketdata.txt", "a")
    x, y, z = mma.acceleration
    packet_num=packet_num+1
    timej=datetime.now().time()
    file.write(str(timej))
    print('\nPacket Num: '+ str(packet_num))
    file.write('\nPacket Num: '+ str(packet_num)+"\n")
    print('Acceleration: x={0:0.3f} m/s^2 y={1:0.3f} m/s^2 z={2:0.3f} m/s^2'.format(x, y, z))
    file.write('Acceleration: x={0:0.3f} m/s^2 y={1:0.3f} m/s^2 z={2:0.3f} m/s^2'.format(x, y, z)+"\n")
    orientation = mma.orientation
    print('Orientation: {0}'.format(orientation))
    file.write('Orientation: {0}'.format(orientation)+"\n")
    print("Temperature: %0.1f C" % bmp280.temperature)
    file.write("Temperature: %0.1f C" % bmp280.temperature+"\n")
    print("Pressure: %0.1f hPa" % bmp280.pressure)
    file.write("Pressure: %0.1f hPa" % bmp280.pressure+"\n")
    print("Altitude = %0.2f meters" % bmp280.altitude)
    file.write("Altitude = %0.2f meters" % bmp280.altitude+"\n\n")
    print("Latitude: " + str(gps.latitude))
    file.write("Latitude: " + str(gps.latitude))
    print("Longitude: " + str(gps.longitude))
    file.write("Longitude: " + str(gps.longitude))
    print("Speed: " + str(gps.speed_knots))
    file.write("Speed: " + str(gps.speed_knots)) 
    rfm9x.send(bytes(str(packet_num)+" "+"InsertAcceleration"+" "+str(orientation)+" "+str(bmp280.temperature)+" "+str(bmp280.pressure)+" "+str(bmp280.altitude)+" "+str(gps.latitude)+" "+str(gps.longitude)+" "+str(gps.speed_knots), "utf-8" ))
   #rfm9x.send(bytes('Hello world!\r\n',"utf-8"))

    print("sent Lora packet")
    time.sleep(.5)
    file.close()
