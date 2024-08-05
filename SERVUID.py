import tkinter as tk
from tkinter import *
from tkinter import messagebox
import serial
import threading

# Configuração da porta serial
ser = serial.Serial('COM4', 9600)  # Atualize 'COM3' para a porta correta

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Sistema de Leitura de Tags")
        self.geometry("800x600")
        
        def driverRegisterBtn():
            self.open_driverReg()
            
        def carRegisterBtn():
            self.open_carReg()
            
        def closeAll():
            self.destroy()
            
        self.background_image_Principal = tk.PhotoImage(file="images\\principalBG.png")
        self.addCarBtn = tk.PhotoImage(file="images\\btnAddCar.png")
        self.addDriverBtn = tk.PhotoImage(file="images\\btnAddDriver.png")
        self.exitBnt = tk.PhotoImage(file="images\\btnExit.png")

        # Adiciona a imagem de fundo ao Label
        lab_background_Principal = tk.Label(self, image=self.background_image_Principal)
        lab_background_Principal.place(x=0, y=0, relwidth=1, relheight=1)

        # Frame para os botões laterais
        self.sidebar = tk.Frame(self, width=65, bg='#69B67C', pady=5, padx=5)
        self.sidebar.pack(expand=False, fill='both', side='left', anchor='nw')

        # Botões laterais


        btn_driver = tk.Button(self.sidebar, image=self.addCarBtn, command=lambda: [driverRegisterBtn()])
        btn_driver.place(width=40, height=40, x=10, y=10)
        
        btn_car = tk.Button(self.sidebar, image=self.addDriverBtn, command=lambda: [carRegisterBtn()])
        btn_car.place(width=40, height=40, x=10, y=70)
        
        btn_sair = tk.Button(self.sidebar, image=self.exitBnt, command=lambda: [closeAll()])
        btn_sair.place(width=40, height=40, x=10, y=130)

        # Mensagem central
        self.message = tk.Label(self, text="Aguardando Aproximação da Tag", font=("Arial", 24), bg='#3c3f41', fg='white')
        self.message.pack(expand=True)

        # Inicia a thread para leitura das tags
        self.thread = threading.Thread(target=self.read_tag)
        self.thread.daemon = True
        self.thread.start()

    def read_tag(self):
        while True:
            if ser.in_waiting > 0:
                tag_id = ser.readline().decode('utf-8').strip()
                self.open_tag_window(tag_id)
                
    
    
    

    def open_tag_window(self, tag_id):
        # Nova janela
        tag_window = tk.Toplevel(self)
        tag_window.title("Detalhes da Tag")
        tag_window.geometry("1200x600")
        
        def confirm_tag(self, tag_id, name, description):
        # Aqui você pode adicionar a lógica para salvar os dados
            messagebox.showinfo("Informação", f"Tag {tag_id} confirmada com sucesso!")
        
        def closeActionRegister():
            tag_window.destroy()
        
        
        self.background_image = tk.PhotoImage(file="images\\tagRegisterAction.png")

        # Adiciona a imagem de fundo ao Label
        lab_background = tk.Label(tag_window, image=self.background_image)
        lab_background.place(x=0, y=0, relwidth=1, relheight=1)
        
        tag_entry = tk.Entry(tag_window, font=("Arial", 18))
        tag_entry.place(x=50, y= 195, width=290, height=35)
        tag_entry.insert(0, tag_id)

        name_entry = tk.Entry(tag_window, font=("Arial", 18))
        name_entry.place(x=50, y= 265, width=290, height=35)

        tel_entry = tk.Entry(tag_window, font=("Arial", 18))
        tel_entry.place(x=495, y=265, width=290, height=35)
        
        doc_entry = tk.Entry(tag_window, font=("Arial", 18))
        doc_entry.place(x=890, y=265, width=240, height=35)
        
        hora_entry = tk.Entry(tag_window)
        hora_entry.place(x=50, y=340, width=290, height=35)
        
        data_entry = tk.Entry(tag_window)
        data_entry.place(x=495, y=340, width=290, height=35)
        
        colect_entry = tk.Entry(tag_window)
        colect_entry.place(x=890, y=340, width=240, height=35)
        
        veiculo_entry = tk.Entry(tag_window)
        veiculo_entry.place(x=50, y=418, width=290, height=35)

        placa_entry = tk.Entry(tag_window)
        placa_entry.place(x=496, y=418, width=290, height=35)
        
        motivo_entry = tk.Entry(tag_window)
        motivo_entry.place(x=890, y=418, width=240, height=35)
        
        cancel_button = tk.Button(tag_window, text="cancelar", command=lambda: [closeActionRegister()])
        cancel_button.place(x=830, y=508, width=110, height=40)
        
        confirm_button = tk.Button(tag_window, text="Confirmar", command=lambda: self.confirm_tag(tag_entry.get(), name_entry.get(), desc_entry.get()))
        confirm_button.place(x=970, y=508, width=110, height=40)
        
        
    
    
    
    def open_driverReg(self):
        # Nova janela
        driveReg = tk.Toplevel(self)
        driveReg.title("Detalhes da Tag")
        driveReg.geometry("1200x600")
        
        def confirm_friver(self, tag_id, name, description):
        # Aqui você pode adicionar a lógica para salvar os dados
            messagebox.showinfo("Informação", f"Tag {tag_id} confirmada com sucesso!")
        
        def closeDriveReg():
            driveReg.destroy()
        
        
        self.background_image_driverReg = tk.PhotoImage(file="images\\driverRegistrer.png")

        # Adiciona a imagem de fundo ao Label
        lab_backgroundDriveReg = tk.Label(driveReg, image=self.background_image_driverReg)
        lab_backgroundDriveReg.place(x=0, y=0, relwidth=1, relheight=1)
        
        name_DriveReg = tk.Entry(driveReg, font=("Arial", 18))
        name_DriveReg.place(x=50, y= 195, width=490, height=35)


        user_DriveReg = tk.Entry(driveReg, font=("Arial", 18))
        user_DriveReg.place(x=50, y= 265, width=290, height=35)

        tel_DriveReg = tk.Entry(driveReg, font=("Arial", 18))
        tel_DriveReg.place(x=495, y=265, width=290, height=35)
        
        doc_DriveReg = tk.Entry(driveReg, font=("Arial", 18))
        doc_DriveReg.place(x=890, y=265, width=240, height=35)
        
        licenseType_entryDriveReg = tk.Entry(driveReg)
        licenseType_entryDriveReg.place(x=50, y=340, width=290, height=35)
        
        data_entryDriveReg = tk.Entry(driveReg)
        data_entryDriveReg.place(x=495, y=340, width=290, height=35)
        
        email_entryDriveReg = tk.Entry(driveReg)
        email_entryDriveReg.place(x=890, y=340, width=240, height=35)
        
        cargo_entryDriveReg = tk.Entry(driveReg)
        cargo_entryDriveReg.place(x=50, y=418, width=290, height=35)

        tagNumber_entryDriveReg = tk.Entry(driveReg)
        tagNumber_entryDriveReg.place(x=496, y=418, width=290, height=35)
        
        cancel_buttonDriveReg = tk.Button(driveReg, text="cancelar", command=lambda: [closeDriveReg()])
        cancel_buttonDriveReg.place(x=830, y=508, width=110, height=40)
        
        confirm_buttonDriveReg = tk.Button(driveReg, text="Confirmar", command=lambda: self.confirm_driver(tag_entry.get(), name_entry.get(), desc_entry.get()))
        confirm_buttonDriveReg.place(x=970, y=508, width=110, height=40)
        
    
    
    
    
    
    def open_carReg(self):
        # Nova janela
        carReg = tk.Toplevel(self)
        carReg.title("Detalhes da Tag")
        carReg.geometry("1200x600")
        
        def confirm_car(self, tag_id, name, description):
        # Aqui você pode adicionar a lógica para salvar os dados
            messagebox.showinfo("Informação", f"Tag {tag_id} confirmada com sucesso!")
        
        def closeCarReg():
            carReg.destroy()
        
        
        self.background_image_carReg = tk.PhotoImage(file="images\\carRegister.png")

        # Adiciona a imagem de fundo ao Label
        lab_backgroundCarReg = tk.Label(carReg, image=self.background_image_carReg)
        lab_backgroundCarReg.place(x=0, y=0, relwidth=1, relheight=1)
        
        marca_CarReg = tk.Entry(carReg, font=("Arial", 18))
        marca_CarReg.place(x=50, y= 195, width=290, height=35)


        modelo_CarReg = tk.Entry(carReg, font=("Arial", 18))
        modelo_CarReg.place(x=50, y= 265, width=290, height=35)

        ano_CarReg = tk.Entry(carReg, font=("Arial", 18))
        ano_CarReg.place(x=495, y=265, width=290, height=35)
        
        estado_CarReg = tk.Entry(carReg, font=("Arial", 18))
        estado_CarReg.place(x=890, y=265, width=240, height=35)
        
        placa_entryCarReg = tk.Entry(carReg)
        placa_entryCarReg.place(x=50, y=340, width=290, height=35)
        
        renavan_entryCarReg = tk.Entry(carReg)
        renavan_entryCarReg.place(x=495, y=340, width=290, height=35)
        
        locacao_entryCarReg = tk.Entry(carReg)
        locacao_entryCarReg.place(x=890, y=340, width=240, height=35)
        
        frotaFabrica_entryCarReg = tk.Entry(carReg)
        frotaFabrica_entryCarReg.place(x=50, y=418, width=290, height=35)

        seguro_entryCarReg = tk.Entry(carReg)
        seguro_entryCarReg.place(x=496, y=418, width=290, height=35)
        
        dataAquisicao_buttonCarReg = tk.Button(carReg, text="cancelar", command=lambda: [closeCarReg()])
        dataAquisicao_buttonCarReg.place(x=830, y=508, width=110, height=40)
        
        confirm_buttonCarReg = tk.Button(carReg, text="Confirmar", command=lambda: self.confirm_car(tag_entry.get(), name_entry.get(), desc_entry.get()))
        confirm_buttonCarReg.place(x=970, y=508, width=110, height=40)
        
        car_entry = tk.Entry(carReg)
        car_entry.place(x=890, y=418, width=240, height=35)



if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
