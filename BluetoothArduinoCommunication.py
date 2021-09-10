import bluetooth
import serial

class BluetoothArduinoCommunication:
    def __init__(self, connect=True, serial_port="COM4", ativa_laser=False):
        self.connected = False
        self.fire_threshold = 6
        self.pos_threshold = 2
        self.connect = connect
        self.posX = 1500
        self.inicial_y_pos = 1100
        self.posY = 1500
        self.send_direita_pos = True
        self.send_desce_pos = True
        self.bluetooth=False
        self.xMaxPos = 2100 # 2000
        self.xMinPos = 1600 #1000
        self.yMaxPos = 2000
        self.yMinPos = 1000

        self.usa_scan_vertical = True

        self.balanco_y_max = 1130
        self.balanco_y_min = 1000

        self.use_angulo = False
        self.use_angulo_data = "1" if self.use_angulo else "0"
        self.ativa_laser = ativa_laser

        self.achou_count_threshold = 4
        self.nada_count_threshold = 4
        
        self.achou_count = 0
        self.nada_count = 0

        self.serial_port = serial_port

        self.sig_map_sobe = "1"
        self.sig_map_desce = "0"
        self.sig_map_direita = "2"
        self.sig_map_esquerda = "3"
        self.sig_map_atira = "4"
        self.sig_map_reset = "5"
                
    def do_connect(self):
        if not self.connect:
            return
        if self.bluetooth:
            pass
            nearby_devices = bluetooth.discover_devices(lookup_names=True)
            print("Found {} devices.".format(len(nearby_devices)))
            linvor_addr = None
            for addr, name in nearby_devices:
                print("  {} - {}".format(addr, name))
                if name == "linvor":
                    linvor_addr = addr
                    print("Achou !")

            print("Connecting to \"{}\" on {}".format(linvor_addr, "linvor"))

            port = 1
            # Create the client socket
            self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.sock.connect((linvor_addr, port))
        else:
            #self.arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=0)
            self.arduino = serial.Serial(port=self.serial_port, baudrate=115200, timeout=0)

        print("Connected")
        self.send_reset()
        self.connected = True
        return self.connected

    def send_message(self, message):
        #print("Enviando : ", message)
        if self.connected:
            try:
                if self.bluetooth:
                    self.sock.send(message.encode())
                else:
                    self.arduino.flush()
                    self.arduino.reset_input_buffer()
                    self.arduino.reset_output_buffer()
                    self.arduino.write(message.encode())
                    #print("Recebido - ", self.arduino.readline())
                    self.arduino.flush()
                    self.arduino.reset_input_buffer()
                    self.arduino.reset_output_buffer()
            except:
                pass
            

    
    def send_sobe(self, vel):
        vel = str(vel)
        multi = self.vel_multi(vel)
        nextPosY = self.posY + multi
        if nextPosY <= self.yMaxPos:
            self.posY = nextPosY
        data_send = self.posY if self.use_angulo else vel
        #print("SOBE - ", vel , " - ", multi, " - ", nextPosY, " - ", data_send)
        self.send_message(self.sig_map_sobe+self.use_angulo_data+str(data_send)+"|")
        #self.send_message("0"+str(data_send)+"0000"+self.use_angulo_data+"|")
    
    def send_desce(self, vel):
        vel = str(vel)
        multi = self.vel_multi(vel)
        nextPosY = self.posY - multi
        if nextPosY >= self.yMinPos:
            self.posY = nextPosY
        data_send = self.posY if self.use_angulo else vel
        #print("DESCE - ", vel , " - ", multi, " - ", nextPosY, " - ", data_send)
        self.send_message(self.sig_map_desce+self.use_angulo_data+str(data_send)+"|")
        #self.send_message(str(data_send)+"00000"+self.use_angulo_data+"|")
        
    
    def send_direita(self, vel):
        vel = str(vel)
        multi = self.vel_multi(vel)
        nextPosX = self.posX - multi
        if nextPosX >= self.xMinPos:
            self.posX = nextPosX
        data_send = self.posX if self.use_angulo else vel
        #print("DIREITA - ", vel , " - ", multi, " - ", nextPosX, " - ", data_send)
        self.send_message(self.sig_map_direita+self.use_angulo_data+str(data_send)+"|")
        #self.send_message("00"+str(data_send)+"000"+self.use_angulo_data+"|")
    
    def send_esquerda(self, vel):
        vel = str(vel)
        multi = self.vel_multi(vel)
        nextPosX = self.posX + multi
        if nextPosX <= self.xMaxPos:
            self.posX = nextPosX
        data_send = self.posY if self.use_angulo else vel
        #print("ESQUERDA - ", vel , " - ", multi, " - ", nextPosX, " - ", data_send)
        self.send_message(self.sig_map_esquerda+self.use_angulo_data+str(data_send)+"|")
        #self.send_message("000"+str(data_send)+"00"+self.use_angulo_data+"|")
    
    def send_atira(self):
        print("ENQUADROU !")
        if self.ativa_laser:
            data_send = 0 if self.use_angulo else 0
            self.send_message(self.sig_map_atira+self.use_angulo_data+str(data_send)+"|")
        #self.send_message("000010"+self.use_angulo_data+"|")

    def scan(self):
        print(self.posX, " - ", self.posY)
        if self.posX - 10 <=self.xMinPos :
            self.send_direita_pos = False
        elif self.posX + 10 >=self.xMaxPos:
            self.send_direita_pos = True
        if self.send_direita_pos:
            self.send_direita(2)
        else:
            self.send_esquerda(2)


        if self.usa_scan_vertical:
            if self.posY - 10 <=self.balanco_y_min :
                self.send_desce_pos = False
            elif self.posY + 10 >=self.balanco_y_max:
                self.send_desce_pos = True
            if self.send_desce_pos:
                self.send_desce(2)
            else:
                self.send_sobe(2)
        else:
            meio = self.inicial_y_pos
            #print(meio)
            if self.posY > meio:
                self.send_desce(2)
            elif self.posY < meio:
                self.send_sobe(2)
    
    def send_reset(self):
        print("RESET !")
        self.send_message(self.sig_map_reset+"|")
    
    def encontrado(self):
        self.achou_count += 1
        if self.nada_count > 0:
            self.nada_count -= 1
        self.trigger_verifica_enquadro_persistente()

    def print_counts(self):
        print(self.achou_count, " - ", self.nada_count)

    def nao_encontrado(self):
        self.nada_count += 1
        if self.achou_count > 0:
            self.achou_count -= 1
        self.trigger_verifica_enquadro_persistente()
        
    def trigger_verifica_enquadro_persistente(self):
        #self.print_counts()
        if self.achou_count >= self.achou_count_threshold:
            self.nada_count = 0
            self.achou_count = self.achou_count_threshold
            self.enquadro_persistente()
        if self.nada_count >= self.nada_count_threshold:
            self.achou_count = 0
            self.nada_count = self.nada_count_threshold
            self.zero_enquadro()
            
    def zero_enquadro(self):
        self.scan()
        #print("zero_enquadro !")
    
    def enquadro_persistente(self):
        pass
        #print("Enquadro Persistente !")

    def determina_target(self, diff_X, diff_Y):
        #print("[INFO] X : {:.6f}, Y : {:.6f}".format(diff_X, diff_Y))
        if abs(diff_Y) < self.fire_threshold and abs(diff_X) < self.fire_threshold:
            self.send_atira()
            self.in_target = True
        else:
            self.in_target = False
            
        if (diff_Y < 0) and abs(diff_Y) > self.pos_threshold:
            if not self.in_target:
                self.send_desce(self.determina_velocidade(diff_Y))
        elif abs(diff_Y) > self.pos_threshold:
            if not self.in_target:
                self.send_sobe(self.determina_velocidade(diff_Y))
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
        if diff >= 100:
            return 3
        elif diff < 100 and diff >20:
            return 2
        else:
            return 1
        #return 1
    def vel_multi(self, vel):
        if vel == "1":
            return 1
        elif vel == "2":
            return 5
        elif vel == "3":
            return 15
        else:
            return int(2*int(vel))
        #return 1

    @staticmethod
    def calcula_maior_quadrado(detectados_arr):
        target = None
        last_box_area = None
        for item in detectados_arr:
            distancia = item[0]
            if not last_box_area:
                last_box_area = distancia
                target = item
            elif distancia > last_box_area:
                last_box_area = distancia
                target = item
        return target