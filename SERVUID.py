import tkinter as tk
from tkinter import *
from tkinter import messagebox
import pymysql.connections
import pymysql.cursors
import serial
import threading
from datetime import datetime
import pymysql
import serial.tools.list_ports
from tkinter import ttk

# Configuração da porta serial
def find_device():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "USB-SERIAL CH340" in port.description:
            print(port.device)
            return port.device
        return None
device_port = str(find_device())
if device_port:
    ser = serial.Serial(device_port, 9600)
    print(f"Conectado ao dispositivo na porta {device_port}")
else:
    print("Dispositivo não encontrado.")


db_config ={
    'host': 'localhost',
    'user': 'taguser',
    'password': 'FigaroFertMinas@8956',
    'database': 'tag_car_control'
}

#....................................................................................................
#start Screen Builds............................
#....................................................................................................

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Sistema de Leitura de Tags")
        self.geometry("800x600")
        self.resizable(False, False)
        
        def driverRegisterBtn():
            self.open_driverReg()
            
        def carRegisterBtn():
            self.open_carReg()
            
        def closeAll():
            self.destroy()
        
        principalbg = r'C:\Car_Tag_Control_V01-main\Car_Tag_Control_V01-main\images\principalBG.png'
        btnaddcar = r'C:\Car_Tag_Control_V01-main\Car_Tag_Control_V01-main\images\btnAddCar.png'
        btnadddriver = r'C:\Car_Tag_Control_V01-main\Car_Tag_Control_V01-main\images\btnAddDriver.png'
        btnexit = r'Car_Tag_Control_V01-main/images/btnExit.png'
            
        self.background_image_Principal = tk.PhotoImage(file=principalbg)
        self.addCarBtn = tk.PhotoImage(file=btnaddcar)
        self.addDriverBtn = tk.PhotoImage(file=btnadddriver)
        self.exitBnt = tk.PhotoImage(file=btnexit)

        lab_background_Principal = tk.Label(self, image=self.background_image_Principal)
        lab_background_Principal.place(x=0, y=0, relwidth=1, relheight=1)

        # Frame para os botões laterais
        self.sidebar = tk.Frame(self, width=65, bg='#69B67C', pady=5, padx=5)
        self.sidebar.pack(expand=False, fill='both', side='left', anchor='nw')

        btn_car = tk.Button(self.sidebar, image=self.addCarBtn, command=lambda: [carRegisterBtn()])
        btn_car.place(width=40, height=40, x=10, y=20)
        
        btn_sair = tk.Button(self.sidebar, image=self.exitBnt, command=lambda: [closeAll()])
        btn_sair.place(width=40, height=40, x=10, y=80)

        self.message = tk.Label(self, text="Aguardando Aproximação da Tag", font=("Arial", 24), bg='#3c3f41', fg='white')
        self.message.pack(expand=True)

        # Inicia a thread para leitura das tags
        self.thread = threading.Thread(target=self.read_tag)
        self.thread.daemon = True
        self.thread.start()

    def read_tag(self):
        while True:
            if ser.in_waiting > 0:
                tag_id =ser.readline().decode('utf-8').strip()
                connect = pymysql.connect(**db_config)
                cursor = connect.cursor()
                confirmation = "SELECT tag=%s FROM users"
                valor = tag_id
                cursor.execute(confirmation, valor)
                result_confirmation = cursor.fetchone()
                print("o result é:", result_confirmation)
                if result_confirmation != (0,) and result_confirmation != None:
                    self.open_tag_window(tag_id)
                else:
                    self.open_driverReg(tag_id)
                cursor.close()
                connect.close()

#....................................................................................................
#Tag resgister movimentation Screen............................
#....................................................................................................

    def open_tag_window(self, tag_id):
        # Nova janela
        tag_window = tk.Toplevel(self)
        tag_window.title("Detalhes da Tag")
        tag_window.geometry("1200x600")
        tag_window.resizable(False, False)
        
        def confirm_tag():
            name = name_entry.get()
            hora = hora_entry.get()
            data = data_entry.get()
            placa = placa_entry.get()
            motivo = motivo_entry.get()

            connect = pymysql.connect(**db_config)
            cursor = connect.cursor()

            query_insert_register = 'INSERT INTO registers (name, time, date, plate, reason) VALUES (%s, %s, %s, %s, %s)'
            values_to_insert = (name, hora, data, placa, motivo)
            cursor.execute(query_insert_register, values_to_insert)
            connect.commit()
            drive_update = ''
            if user_situation == 'devolucao':
                query_update = "UPDATE users SET PLATE=%s"
                update_value = ''
                drive_update = 'noDrive'
                query_update_car = 'UPDATE cars SET usability=%s WHERE plate=%s'
                value_update_car = ('disponivel', placa)
            else:
                query_update = "UPDATE users SET plate=%s"
                update_value = placa
                drive_update = 'onDrive'
                query_update_car = 'UPDATE cars SET usability=%s WHERE plate=%s'
                value_update_car = ('indisponivel', placa)
            cursor.execute(query_update, update_value)
            connect.commit()
            cursor.execute(query_update_car, value_update_car)
            connect.commit()

            update_user_situation = 'UPDATE users SET situation = %s'
            cursor.execute(update_user_situation, drive_update)
            connect.commit()
            print('registered')
            messagebox.showinfo("Informação", f"Registro do {name} confirmado com sucesso!")
            cursor.close()
            connect.close()
            tag_window.destroy()
        
        def closeActionRegister():
            tag_window.destroy()

        def consultCars():
            connect = pymysql.connect(**db_config)
            cursor = connect.cursor()
            query_consult = "SELECT model, plate FROM cars WHERE usability=%s"
            usabilidade = 'disponivel'
            cursor.execute(query_consult, usabilidade)
            avaliableCars = cursor.fetchall()
            model = [cars[0] for cars in avaliableCars]
            plate = [cars[1] for cars in avaliableCars]

            return model, plate
        
        def on_plate_selected(event):
            selected_plate = placa_entry.get()
            connect = pymysql.connect(**db_config)
            cursor = connect.cursor()
            query_compare_plate = "SELECT model FROM cars WHERE plate=%s"
            cursor.execute(query_compare_plate, selected_plate)
            model = cursor.fetchall()
            veiculo_entry.delete(0, 'end')
            veiculo_entry.insert(0, model)
            print('ok')
            cursor.close()
            connect.close()

        
        model, plate = consultCars()

        datetime_Atual = datetime.now()
        data_formatada = datetime_Atual.strftime("%D/%m/%Y")
        hora_formatada = datetime_Atual.strftime("%H:%M:%S")

        connect = pymysql.connect(**db_config)
        cursor = connect.cursor()
        query_user = "SELECT user, phone, doc FROM users WHERE tag=%s"
        query_situation = "SELECT situation FROM users"
        tag = tag_id
        cursor.execute(query_user, tag)
        result_user = cursor.fetchone()
        cursor.execute(query_situation)
        situation = cursor.fetchone()
        print('a situation é:', situation)
        drive = 'onDrive'
        if drive in situation:
            user_situation = 'devolucao'
            query_colect_used_car = 'SELECT plate FROM users WHERE tag=%s'
            cursor.execute(query_colect_used_car, tag_id)
            placa = cursor.fetchone()
            print('é:', user_situation)
        else:
            user_situation = 'coleta'
            placa = ''
            print('é:', user_situation)
        cursor.close()
        connect.close()
        
        if result_user:
            user = result_user[0]
            phone = result_user[1]
            doc = result_user[2]
       
        tagregisteraction = r'C:\Car_Tag_Control_V01-main\Car_Tag_Control_V01-main\images\tagRegisterAction.png'
        self.background_image = tk.PhotoImage(file=tagregisteraction)

        lab_background = tk.Label(tag_window, image=self.background_image)
        lab_background.place(x=0, y=0, relwidth=1, relheight=1)
        
        tag_entry = tk.Entry(tag_window, font=("Arial", 18))
        tag_entry.place(x=50, y= 195, width=290, height=35)
        tag_entry.insert(0, tag_id)

        name_entry = tk.Entry(tag_window, font=("Arial", 18))
        name_entry.place(x=50, y= 265, width=290, height=35)
        name_entry.insert(0, user)

        tel_entry = tk.Entry(tag_window, font=("Arial", 18))
        tel_entry.place(x=495, y=265, width=290, height=35)
        tel_entry.insert(0, phone)
        
        doc_entry = tk.Entry(tag_window, font=("Arial", 18))
        doc_entry.place(x=890, y=265, width=240, height=35)
        doc_entry.insert(0, doc)
        
        hora_entry = tk.Entry(tag_window, font=("Arial", 18))
        hora_entry.place(x=50, y=340, width=290, height=35)
        hora_entry.insert(0, hora_formatada)
        
        data_entry = tk.Entry(tag_window, font=("Arial", 18))
        data_entry.place(x=495, y=340, width=290, height=35)
        data_entry.insert(0, data_formatada)
        
        colect_entry = tk.Entry(tag_window,font=("Arial", 18))
        colect_entry.place(x=890, y=340, width=240, height=35)
        colect_entry.insert(0, user_situation)
        
        veiculo_entry = ttk.Combobox(tag_window, values=model, font=("Arial", 18))
        veiculo_entry.place(x=50, y=418, width=290, height=35)
        
        placa_entry = ttk.Combobox(tag_window, values=plate, font=("Arial", 18))
        placa_entry.place(x=496, y=418, width=290, height=35)
        placa_entry.bind("<<ComboboxSelected>>", on_plate_selected)
        if placa != '':
            placa_entry.insert(0, placa)
        else:
            pass
        
        motivo_entry = tk.Entry(tag_window, font=("Arial", 18))
        motivo_entry.place(x=890, y=418, width=240, height=35)
        
        cancel_button = tk.Button(tag_window, text="cancelar", command=lambda: [closeActionRegister()])
        cancel_button.place(x=830, y=508, width=110, height=40)
        
        confirm_button = tk.Button(tag_window, text="Confirmar", command=lambda: [confirm_tag()])
        confirm_button.place(x=970, y=508, width=110, height=40)
#....................................................................................................
#Driver Register Screen............................
#....................................................................................................
   
    def open_driverReg(self, tag_id):
        # Nova janela
        driveReg = tk.Toplevel(self)
        driveReg.title("Detalhes da Tag")
        driveReg.geometry("1200x600")
        driveReg.resizable(False, False)
        
        def confirm_driver():
            name = name_DriveReg.get()
            tel = tel_DriveReg.get()
            doc = doc_DriveReg.get()
            email = email_entryDriveReg.get()
            typeLicense = licenseType_entryDriveReg.get()
            situation = 'onDrive'
            connect = pymysql.connect(**db_config)
            cursor = connect.cursor()
        # Aqui você pode adicionar a lógica para salvar os dados
            if (name != '' and tel != '' and doc != '' and typeLicense != '' and email != ''):
                messagebox.showinfo("Informação", f"Motorista: {name} cadastrado com sucesso!")
                tagNumber_entryDriveReg.insert(0, tag_id)
                query_driver = "INSERT INTO users (user, phone, doc, type, email, tag, situation) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                values_driver = (name, tel, doc, typeLicense, email, tag_id, situation)
                cursor.execute(query_driver, values_driver)
                connect.commit()
                driveReg.destroy()
            else:
                messagebox.showerror("Dados Incompletos", "Preencha todas as informações para continuar!")
            cursor.close()
            connect.close()
            
        def closeDriveReg():
            driveReg.destroy()
        
        driverregister = r'C:\Car_Tag_Control_V01-main\Car_Tag_Control_V01-main\images\driverRegistrer.png'
        self.background_image_driverReg = tk.PhotoImage(file=driverregister)

        lab_backgroundDriveReg = tk.Label(driveReg, image=self.background_image_driverReg)
        lab_backgroundDriveReg.place(x=0, y=0, relwidth=1, relheight=1)
        
        name_DriveReg = tk.Entry(driveReg, font=("Arial", 18))
        name_DriveReg.place(x=50, y= 195, width=490, height=35)
        
        tel_DriveReg = tk.Entry(driveReg, font=("Arial", 18))
        tel_DriveReg.place(x=52, y=265, width=290, height=35)
        
        doc_DriveReg = tk.Entry(driveReg, font=("Arial", 18))
        doc_DriveReg.place(x=495, y=265, width=240, height=35)
                
        licenseType_entryDriveReg = tk.Entry(driveReg, font=("Arial", 18))
        licenseType_entryDriveReg.place(x=890, y=265, width=240, height=35)
                
        email_entryDriveReg = tk.Entry(driveReg, font=("Arial", 18))
        email_entryDriveReg.place(x=50, y=340, width=290, height=35)        
        
        tagNumber_entryDriveReg = tk.Entry(driveReg, font=("Arial", 18))
        tagNumber_entryDriveReg.place(x=495, y=340, width=290, height=35)
        tagNumber_entryDriveReg.insert(0, tag_id)
               
        cancel_buttonDriveReg = tk.Button(driveReg, text="cancelar", command=lambda: [closeDriveReg()])
        cancel_buttonDriveReg.place(x=830, y=508, width=110, height=40)
        
        confirm_buttonDriveReg = tk.Button(driveReg, text="Confirmar", command=lambda: [confirm_driver()])
        confirm_buttonDriveReg.place(x=970, y=508, width=110, height=40)

#....................................................................................................
#Car Register Screen............................
#....................................................................................................
         
    def open_carReg(self):
        # Nova janela
        carReg = tk.Toplevel(self)
        carReg.title("Detalhes da Tag")
        carReg.geometry("1200x600")
        carReg.resizable(False, False)
        
        def confirm_car():
            marca = marca_CarReg.get()
            modelo = modelo_CarReg.get()
            ano = ano_CarReg.get()
            placa = placa_entryCarReg.get()
            renavan = renavan_entryCarReg.get()
            usabilidade = 'disponivel'
            connect = pymysql.connect(**db_config)
            cursor = connect.cursor()
        # Aqui você pode adicionar a lógica para salvar os dados
            if (marca != '' and modelo != '' and ano != '' and placa != ''):
                query_car = "INSERT INTO cars (marca, model, year, plate, renavan, usability) VALUES (%s, %s, %s, %s, %s, %s)"
                values_car = (marca, modelo, ano, placa, renavan, usabilidade)
                cursor.execute(query_car, values_car)
                connect.commit()
                carReg.destroy()
                messagebox.showinfo("Informação", f"Carro: {modelo} cadastrado com sucesso!")
            else:
                messagebox.showerror("Dados Incompletos", "Preencha todas as informações para continuar!")
            cursor.close()
            connect.close()
        def closeCarReg():
            carReg.destroy()
        
        carregister = r'C:\Car_Tag_Control_V01-main\Car_Tag_Control_V01-main\images\carRegister.png'
        self.background_image_carReg = tk.PhotoImage(file=carregister)

        lab_backgroundCarReg = tk.Label(carReg, image=self.background_image_carReg)
        lab_backgroundCarReg.place(x=0, y=0, relwidth=1, relheight=1)
        
        marca_CarReg = tk.Entry(carReg, font=("Arial", 18))
        marca_CarReg.place(x=50, y= 195, width=290, height=35)

        modelo_CarReg = tk.Entry(carReg, font=("Arial", 18))
        modelo_CarReg.place(x=50, y= 265, width=290, height=35)

        ano_CarReg = tk.Entry(carReg, font=("Arial", 18))
        ano_CarReg.place(x=495, y=265, width=290, height=35)
        
        placa_entryCarReg = tk.Entry(carReg, font=("Arial", 18))
        placa_entryCarReg.place(x=50, y=340, width=290, height=35)
        
        renavan_entryCarReg = tk.Entry(carReg, font=("Arial", 18))
        renavan_entryCarReg.place(x=495, y=340, width=290, height=35)

        cancel_buttonCarReg = tk.Button(carReg, text="cancelar", command=lambda: [closeCarReg()])
        cancel_buttonCarReg.place(x=830, y=508, width=110, height=40)
        
        confirm_buttonCarReg = tk.Button(carReg, text="Confirmar", command=lambda: [confirm_car()])
        confirm_buttonCarReg.place(x=970, y=508, width=110, height=40)

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
