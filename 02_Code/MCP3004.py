#!/usr/bin/python
import spidev
import time
import sys

# TODO: Rename.
class MCP3004():

    """Class to represent MCP3004 analog to digital Converter"""

    def __init__(self):
        # TODO: Make class attributes.
        # Voltage dividors 1kOhm/1kOhm (channel 0-2) - 22kOhm/10kOhm(channel 3)
        self._facCh012 = 2
        self._facCh3   = 3.195

        self._spi = spidev.SpiDev()
        self._spi.open(0,0)

    # TODO: Move explanations into docstring, otherwise can't find on
    # introspection.
    # TODO: Only 1 preceding underscore.
    def __buildReadCommand(self,channel):
        startBit = 0x01
        singleEnded = 0x08

        # Return python list of 3 bytes
        #   First byte is the start bit
        #   Second byte contains single ended along with channel #
        #   3rd byte is 0x00
        return [startBit, (singleEnded + channel) <<4, 0x00] #[startBit,128,0x00]

    # TODO: Only 1 preceding underscore.
    # TODO: DRY, self._facCh* can be replaced by setting before, then less
    # chances for error if something changes.
    # TODO: Docstring
    def __processAdcValue(self,channel,result):
        if channel < 3:
            return (((result[1] & 3) << 8) + result[2])*0.00322*self._facCh012
        else:
            return (((result[1] & 3) << 8) + result[2])*0.00322*self._facCh3

    # TODO: Rename, PEP8
    def readAdc(self,channel):
        """
        Read ADC channel(0,1,2,3)
        """
        assert 0 <= channel <= 3, 'ADC number must be a value of 0-3!'
        r = self._spi.xfer2(self.__buildReadCommand(channel)) #([1, 8 << 4, 0])
        return self.__processAdcValue(channel,r)

    # TODO: Make this the exit method for context, make class context manager
    def exitMCP3004(self):
        self._spi.close()

if __name__ == '__main__':
    try:
        mcp3004 = MCP3004()
        while True:
            val0 = mcp3004.readAdc(0)
            val1 = mcp3004.readAdc(1)
            val2 = mcp3004.readAdc(2)
            val3 = mcp3004.readAdc(3)

            print "ADC Ch0 [V]: ", str(val0)
            print "ADC Ch1 [V]: ", str(val1)
            print "ADC Ch2 [V]: ", str(val2)
            print "ADC ch3 [V]: ", str(val3)
            print "_____________________"
            print ""
            time.sleep(2)
    except KeyboardInterrupt:
        mcp3004.exitMCP3004()
        sys.exit(0)
