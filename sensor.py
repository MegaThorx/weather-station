import bluetooth
import json

def get_data(bd_addr):
  sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
  sock.connect((bd_addr, 1))

  try:
    buffer = ""
    while True:
      data = sock.recv(2048)
      if len(data) == 0: break
      buffer = buffer + str(data)[2:-1]
      if "\\r\\n" in buffer:
        result = parse_result(buffer.replace("\\r\\n", ""))
        if result:
          break
        buffer = ""
  except IOError:
    pass

  sock.close()
  return result

def parse_result(data):
  try:
    data = json.loads(data)
    return data
  except ValueError:
    pass
  return False


# print(get_data('98:D3:71:F9:66:2B'))
