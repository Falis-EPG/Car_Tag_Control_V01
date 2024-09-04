# Car_Tag_Control_V01
##Pré Requisitos##

Instalação das seguintes dependencias:
  • !pip install tkinter
  • !pip install pyserial
  • !pip install pymysql

Instalação do banco de dados MySQL e criação das seguintes tabelas:
| users
  • user - VARCHAR
  • phone - VARCHAR
  • doc - VARCHAR
  • type - VARCHAR
  • email - VARCHAR
  • tag - VARCHAR
  • situation -VARCHAR
  • plate - VARCHAR
  
| cars
  • marca - VARCHAR
  • model - VARCHAR
  • year - VARCHAR
  • plate - VARCHAR
  • renavan - VARCHAR
  • usability - VARCHAR
  
| registers
  • name - VARCHAR
  • time - VARCHAR
  • date - VARCHAR
  • plate - VARCHAR
  • reason - VARCHAR
  • id - VARCHAR - Auto_Increment

A tabela user registrará todos os usuários, a cars todos os carros e a registers irá registrar todas as movimentações de coletas e devoluções para futuros relatórios.


Este projeto tem como objetivo realizar o controle de uma frota de veiculos de uma empresa, podendo registrar tags NFE para cada usuário e vincula-los a coleta dos veículos.

###Funcionalidades###

O projeto inicial se comunica com equipamentos em ARDUINO, sendo mais específico:

• Arduino UNO
• LED
• Buzzer
• Leitor NFC RFID - RC522

(Para o leitor descrito acima, somente TAGS e CARTÕES nfc de frequencia proxima a 13,56mhz são funcionais.)

O sistema feit em python, ao ser iniciado, chama a função:

  def __init__(self):

que de inicio gera uma tela feita na biblioteca TKINTER do Python e também inicia a função:

  def read_tag():
    while True:

Ela iniciar a leitura continua nas entradas USB na qual o equipamento esta conectado. E sempre que alguma tag é aproxiamada ao equipamento, o arduino envia a porta USB o código da tag, o que é lido pela função acima e salva em uma variável - tag_id -.

Quando uma nova TAG é lida (uma tag sem cadastro no banco de dados) ele chama uma outra função:

  def open_driverReg(tag_id):

Essa função inicia uma nova tela sobreposta a root, que oferece alguns campos a serem preenchidos, cadastrando asism um novo usuário ao sistema e o vinculando a TAG.

Caso a mesma tag (já registrada) seja lida novamente, o sistema vai identificar o seu registro e então chamará uma outa função:

  def open_tag_window(tag_id):

Ela abrirá uma outra tela sobreposta a root, que permitirá com que você registre a coleta de um novo veículo vinculado ao usuário da TAG.
Grande parte dos campos nesta tela estarão preenchidos com os dados registrados do usuário.

Mia a baixo, dois campos de tipo seleção em lista mostrarão os carros disponíveis para selecionar, estes que já estão salvos pela funcionalidade de registro deveículos. (será mostrado mais a baixo)

Após selecionar o veículo e clicar em confirmar, o sistema irá definir o carro como em uso e também definirá o usuário como em posse atualmente de um veículo.

O veículo ja selecionado, não será mostrado na lista de veiculos caso outro usuário queira realizar a retirada de um veículo.

Quando o mesmo usuário apróximar a TAG no equipamento, o sistema abrirá a mesma tela e identificará que ele está realizando a devolução do veículo ja coletado anteriormente. E após o manipulador do sistema clicar em confirmar, o usuário é definico como sem veículo em posse e também é definido o carro em específico como disponível novamente.

