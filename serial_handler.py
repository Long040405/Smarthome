import serial

class DummySerial:
    """Fallback class to simulate serial port interaction when hardware is disconnected."""
    def __init__(self):
        self.is_open = False

    def write(self, data):
        print(f"[Dummy Serial] Gửi lệnh Arduino: {data}")

    def readline(self):
        # Simulate a fluctuating room temperature around 25-27 °C
        import random
        temp = 25 + random.choice([0, 1, 2])
        return f"{temp}".encode()

    def close(self):
        pass

class SerialHandler:
    """Manages connection and communication with the Arduino serial interface."""
    def __init__(self, port, baudrate, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            print(f"Đã kết nối thành công cổng {self.port}.")
        except Exception as e:
            print(f"Không thể kết nối cổng {self.port}: {e}")
            print("Đang khởi động chế độ giả lập (DummySerial)...")
            self.connection = DummySerial()

    def send_cmd(self, cmd):
        """Sends a command block to the serial connection."""
        if self.connection:
            try:
                self.connection.write(cmd)
                return True
            except Exception as e:
                print(f"Lỗi khi gửi dữ liệu serial: {e}")
        return False

    def read_line(self):
        """Reads a decoded string line from the serial connection."""
        if self.connection:
            try:
                return self.connection.readline().decode().strip()
            except Exception as e:
                print(f"Lỗi khi đọc dữ liệu serial: {e}")
        return ""

    def close(self):
        """Closes the serial connection."""
        if self.connection:
            self.connection.close()
