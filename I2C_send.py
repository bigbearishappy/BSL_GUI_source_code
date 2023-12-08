import smbus
from array import array
import struct
import time

class I2C_send:
    def __init__(self):
        pass

    def config_i2c(self, device_address, i2c_channel):
        self.device_address = device_address
        self.bus = smbus.SMBus(i2c_channel)

    def send_data(self, reg_buf, data):
        chunk_size = 32
        if len(data) + 1 > chunk_size:
            for i in range(0, len(data), chunk_size):
                if i == 0:
                    reg_buf_tmp = reg_buf
                    data_tmp = data[i:i + chunk_size - 1]
                else:
                    reg_buf_tmp = data[i - 1]
                    data_tmp = data[i:i + chunk_size]
                time.sleep(0.01)
                self.bus.write_i2c_block_data(self.device_address, reg_buf_tmp, data_tmp)
        else:
            self.bus.write_i2c_block_data(self.device_address, reg_buf, data)

    def read_data(self, reg_buf, num):
        chunk_size = 32
        data = []
        for i in range(0, num, chunk_size):
            if i + chunk_size > num:
                data += self.bus.read_i2c_block_data(self.device_address, reg_buf, num % chunk_size)
            else:
                data += self.bus.read_i2c_block_data(self.device_address, reg_buf, chunk_size)
        return bytes(data).hex()
    
    def close(self):
        self.bus.close()
