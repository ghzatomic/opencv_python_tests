import bluetooth
import serial

class BluetoothArduinoCommunication:
    def __init__(self):
        self.connected = False
        self.fire_threshold = 20
        self.pos_threshold = 20
        self.connect = True
        self.posX = 180
        self.send_direita_pos = True
        self.bluetooth=False
        
    def do_connect(self):
        if not self.connect:
            return
        if self.bluetooth:
            pass
            # nearby_devices = bluetooth.discover_devices(lookup_names=True)
            # print("Found {} devices.".format(len(nearby_devices)))
            # linvor_addr = None
            # for addr, name in nearby_devices:
            #     print("  {} - {}".format(addr, name))
            #     if name == "linvor":
            #         linvor_addr = addr
            #         print("Achou !")

            # print("Connecting to \"{}\" on {}".format(linvor_addr, "linvor"))

            # port = 1
            # # Create the client socket
            # self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            # self.sock.connect((linvor_addr, port))
        else:
            self.arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=None)

        print("Connected")
        self.send_reset()
        self.connected = True
        return self.connected

    def send_message(self, message):
        if self.connected:
            if self.bluetooth:
                self.sock.send(message.encode())
            else:
                self.arduino.write(message.encode())
                self.arduino.flush()
                self.arduino.reset_input_buffer()
                self.arduino.reset_output_buffer()

    
    def send_sobe(self, vel):
        vel = str(vel)
        #print("SOBE !")
        self.send_message(vel+"00000|")
    
    def send_desce(self, vel):
        vel = str(vel)
        #print("DESCE !")
        self.send_message("0"+vel+"0000|")
    
    def send_direita(self, vel):
        vel = str(vel)
        #print("DIREITA !")
        nextPosX = self.posX - 1
        if nextPosX >= 0:
            self.posX = nextPosX
        self.send_message("00"+vel+"000|")
    
    def send_esquerda(self, vel):
        vel = str(vel)
        nextPosX = self.posX + 1
        if nextPosX <= 360:
            self.posX = nextPosX
        #print("ESQUERDA !")
        self.send_message("000"+vel+"00|")
    
    def send_atira(self):
        print("ATIRA !")
        self.send_message("000010|")

    def scan(self):
        print(self.posX)
        if self.posX <=0 :
            self.send_direita_pos = False
        elif self.posX >=360:
            self.send_direita_pos = True
        if self.send_direita_pos:
            self.send_direita(1)
        else:
            self.send_esquerda(1)
    
    def send_reset(self):
        print("RESET !")
        self.send_message("000001|")
    
    def nao_encontrado(self):
        self.scan()
        
    def determina_target(self, diff_X, diff_Y):
        #print("[INFO] X : {:.6f}, Y : {:.6f}".format(diff_X, diff_Y))
        if abs(diff_Y) < self.fire_threshold and abs(diff_X) < self.fire_threshold:
            self.send_atira()
            self.in_target = True
        else:
            self.in_target = False
            
        if (diff_Y < 0) and abs(diff_Y) > self.pos_threshold:
            if not self.in_target:
                self.send_sobe(self.determina_velocidade(diff_Y))
        elif abs(diff_Y) > self.pos_threshold:
            if not self.in_target:
                self.send_desce(self.determina_velocidade(diff_Y))
        if (diff_X > 0) and abs(diff_X) > self.pos_threshold:
            if not self.in_target:
                self.send_direita(self.determina_velocidade(diff_X))
        elif abs(diff_X) > self.pos_threshold:
            if not self.in_target:
                self.send_esquerda(self.determina_velocidade(diff_X))
        # else:
        #     if not self.in_target:
        #         self.send_reset()
                
    def determina_velocidade(self, diff):
        diff = abs(diff)
        # if diff >= 100:
        #     return 3
        # elif diff < 100 and diff >20:
        #     return 2
        # else:
        #     return 1
        return 1