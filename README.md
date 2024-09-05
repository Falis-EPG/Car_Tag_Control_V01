-

# **Sistema de Leitura de Tags de Veículos**

## **Descrição Geral**

Este projeto é uma aplicação de controle de veículos e motoristas usando a biblioteca Tkinter para a interface gráfica, PyMySQL para a comunicação com o banco de dados MySQL, e `pySerial` para a leitura de dados de um dispositivo serial USB. A aplicação é voltada para a gestão de entrada e saída de veículos em uma empresa, com registro de informações de motoristas e veículos associados.

### **Funcionalidades Principais:**
- **Leitura de tags RFID** de motoristas ou veículos, utilizando um leitor serial USB.
- **Registro de motoristas e veículos** no banco de dados.
- **Consulta de veículos disponíveis** e gerenciamento de estado (em uso ou disponível).
- **Registro de entrada e saída de veículos**, vinculando motoristas e veículos em cada operação.

---

## **Requisitos**
- **Python 3.x**
- **Tkinter** (Interface gráfica)
- **PyMySQL** (Integração com MySQL)
- **pySerial** (Comunicação com porta serial)
- **Banco de Dados MySQL**

---

## **Estrutura do Código**

### **1. Configuração da Porta Serial**

O código utiliza a biblioteca `serial.tools.list_ports` para detectar automaticamente um dispositivo serial com a descrição "USB-SERIAL CH340". Caso o dispositivo seja encontrado, a aplicação se conecta a ele para a leitura de tags RFID.

```python
def find_device():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "USB-SERIAL CH340" in port.description:
            return port.device
    return None
```

---

### **2. Interface Gráfica Principal**

A classe `MainApplication` define a janela principal do sistema, onde o usuário pode acessar funcionalidades como registro de motoristas, veículos e leitura de tags.

- **Título e Dimensões**: A janela é criada com título "Sistema de Leitura de Tags" e tem tamanho fixo de 800x600.
- **Botões Laterais**: Contém botões que permitem o registro de novos veículos, motoristas e a opção de sair do sistema.
- **Leitura de Tags**: A aplicação inicia uma thread separada para leitura contínua das tags por meio do dispositivo serial.

```python
class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        # Configurações da janela principal
        # Botões para abrir as telas de registro
        self.thread = threading.Thread(target=self.read_tag)
        self.thread.daemon = True
        self.thread.start()
```

#### **Leitura de Tags**

Ao identificar a aproximação de uma tag, a aplicação consulta o banco de dados para verificar se a tag está associada a um motorista registrado. Caso sim, abre a janela de detalhes; se não, abre a tela de registro de motorista.

```python
def read_tag(self):
    while True:
        if ser.in_waiting > 0:
            tag_id = ser.readline().decode('utf-8').strip()
            # Conecta ao banco de dados e realiza consulta
```

---

### **3. Janelas de Registro**

#### **Registro de Motorista**
A janela de registro de motorista permite inserir informações como nome, telefone, documento, tipo de habilitação, e-mail, e a tag RFID associada.

```python
def open_driverReg(self, tag_id):
    # Interface gráfica para o registro de motoristas
    def confirm_driver():
        # Insere os dados do motorista no banco de dados
```

#### **Registro de Veículo**
A janela de registro de veículos permite inserir dados do veículo, como marca, modelo, ano, placa e número do Renavam. Os veículos são marcados como "disponíveis" no momento do registro.

```python
def open_carReg(self):
    # Interface gráfica para o registro de veículos
    def confirm_car():
        # Insere os dados do veículo no banco de dados
```

#### **Registro de Entrada e Saída de Veículos**
Ao aproximar uma tag, caso o motorista esteja registrado, a janela de detalhes do veículo é exibida, onde o usuário pode confirmar as informações para registrar a entrada ou saída de um veículo.

```python
def open_tag_window(self, tag_id):
    # Interface gráfica para registrar movimentação de veículos
    def confirm_tag():
        # Insere ou atualiza o estado do motorista e do veículo no banco de dados
```

---

### **4. Conexão com o Banco de Dados**

O sistema utiliza a biblioteca `PyMySQL` para se conectar ao banco de dados MySQL. A configuração da conexão é definida em um dicionário:

```python
db_config = {
    'host': 'host',
    'user': 'user',
    'password': 'password',
    'database': 'db'
}
```

Para cada operação (registro, consulta, atualização), uma conexão é aberta e fechada após a execução das consultas SQL.

---

## **Como Executar o Projeto**

1. **Instale as dependências**:
   ```bash
   pip install pyserial pymysql
   ```

2. **Configure o banco de dados**:
   - Crie um banco de dados MySQL com as tabelas necessárias para armazenar informações de motoristas e veículos.

3. **Execute a aplicação**:
   ```bash
   python main.py
   ```

---

## **Tabelas do Banco de Dados**

### **Tabela `users` (Motoristas)**

| Campo     | Tipo        | Descrição                         |
|-----------|-------------|-----------------------------------|
| `user`    | VARCHAR(50) | Nome do motorista                 |
| `phone`   | VARCHAR(20) | Telefone do motorista             |
| `doc`     | VARCHAR(20) | Documento (RG ou CPF)             |
| `type`    | VARCHAR(10) | Tipo de habilitação               |
| `email`   | VARCHAR(50) | E-mail                            |
| `tag`     | VARCHAR(50) | Código da tag RFID                |
| `situation`| VARCHAR(10) | Situação (onDrive/devolucao)      |

### **Tabela `cars` (Veículos)**

| Campo       | Tipo        | Descrição                         |
|-------------|-------------|-----------------------------------|
| `marca`     | VARCHAR(50) | Marca do veículo                  |
| `model`     | VARCHAR(50) | Modelo do veículo                 |
| `year`      | INT         | Ano de fabricação                 |
| `plate`     | VARCHAR(10) | Placa do veículo                  |
| `renavan`   | VARCHAR(20) | Número do Renavam                 |
| `usability` | VARCHAR(15) | Disponibilidade (disponivel/indisponivel) |

---

## **Considerações Finais**

Este sistema foi desenvolvido para otimizar o controle de entrada e saída de veículos utilizando RFID e uma interface simples e eficiente.
