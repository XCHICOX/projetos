import sys
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QListWidget, QPushButton, 
                             QFormLayout, QLineEdit, QLabel, QMessageBox, QComboBox, QDialog, QDialogButtonBox)
from PyQt5.QtGui import QIcon


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login')
        self.setGeometry(300, 300, 300, 150)
        self.create_ui()

    def create_ui(self):
        layout = QFormLayout()

        self.username_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)

        layout.addRow('Username:', self.username_edit)
        layout.addRow('Password:', self.password_edit)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        help_button = QPushButton()
        help_button.setIcon(QIcon('icon/help.png'))  # Supondo que você tenha um ícone chamado 'question.png' na pasta 'icons'
        help_button.setFixedSize(24, 24,)  # Ajuste o tamanho do botão aqui
        help_button.clicked.connect(self.show_help)
        

        layout.addWidget(self.buttons)
        layout.addWidget(help_button)
        self.setLayout(layout)

    def show_help(self):
        QMessageBox.information(self, 'ajuda', 'Por favor entre com seu usuario e senha.')


    def get_credentials(self):
        return self.username_edit.text(), self.password_edit.text()
    
    def check_credentials(self, username, password):
        try:
            with open('usuarios.json', 'r') as file:
                users = json.load(file)
                for user in users:
                    if user['username'] == username and user['password'] == password:
                        return True
        except FileNotFoundError:
            QMessageBox.warning(self, 'Error', 'User file not found.')
        return False
    

class VeiculosApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.logged_in_username = None  # Inicializa como None
        self.login()     

        self.clientes = self.carregar_clientes()
        self.veiculos = self.carregar_veiculos()
        self.manutencoes = self.carregar_manutencoes()

        self.listar_clientes()
        self.listar_veiculos()
        self.listar_manutencoes()


    def login(self):
        login_dialog = LoginDialog()
        if login_dialog.exec_() == QDialog.Accepted:
            username, password = login_dialog.get_credentials()
            if login_dialog.check_credentials(username, password):
                self.logged_in_username = username  # Armazena o nome do usuário logado
                self.initUI()
                self.show()
            else:
                QMessageBox.warning(self, 'Login Failed', 'Nome de usuário ou senha inválido')
                self.close()
        else:
            self.close()


    def initUI(self):
        self.setWindowTitle('Sistema de Gerenciamento de Oficina')
        self.setGeometry(100, 100, 800, 600)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        # Adiciona um QLabel na barra de status para exibir o nome do usuário
        self.statusBar().showMessage(f'Usuário: {self.logged_in_username}' if self.logged_in_username else 'Não logado')


        self.setup_clientes_tab()
        self.setup_veiculos_tab()
        self.setup_manutencoes_tab()

    # Implementação das abas e métodos para clientes, veículos e manutenções
    
    def setup_clientes_tab(self):
        self.tab_clientes = QWidget()
        icon_clientes = QIcon('icon/adicionar_cliente.png')
        self.tabs.addTab(self.tab_clientes, icon_clientes, "Clientes")

        self.tab_clientes_layout = QVBoxLayout(self.tab_clientes)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText('Buscar por nome...')
        self.search_bar.textChanged.connect(self.filtrar_clientes)

        self.listaClientes = QListWidget()

        self.btnAdicionarCliente = QPushButton('Adicionar')
        self.btnAdicionarCliente.setIcon(QIcon('icon/adicionar_cliente.png'))
        self.btnAdicionarCliente.setToolTip('Adicionar Cliente')

        self.btnEditarCliente = QPushButton('Editar')
        self.btnEditarCliente.setIcon(QIcon('icon/editar.png'))
        self.btnEditarCliente.setToolTip('Editar Cliente')

        self.btnExcluirCliente = QPushButton('Excluir')
        self.btnExcluirCliente.setIcon(QIcon('icon/excluir_cliente.png'))
        self.btnExcluirCliente.setToolTip('Excluir Cliente')

        self.listaClientes.itemSelectionChanged.connect(self.selecionar_cliente)
        self.btnAdicionarCliente.clicked.connect(self.adicionar_cliente)
        self.btnEditarCliente.clicked.connect(self.editar_cliente)
        self.btnExcluirCliente.clicked.connect(self.excluir_cliente)

        self.tab_clientes_layout.addWidget(self.search_bar)
        self.tab_clientes_layout.addWidget(self.listaClientes)
        self.tab_clientes_layout.addWidget(self.btnAdicionarCliente)
        self.tab_clientes_layout.addWidget(self.btnEditarCliente)
        self.tab_clientes_layout.addWidget(self.btnExcluirCliente)


    def setup_veiculos_tab(self):
        self.tab_veiculos = QWidget()
        icon_veiculos = QIcon('icon/adicionar_veiculo.png')
        self.tabs.addTab(self.tab_veiculos, icon_veiculos, "Veículos")

        self.tab_veiculos_layout = QVBoxLayout(self.tab_veiculos)

        self.search_bar_veiculos = QLineEdit()
        self.search_bar_veiculos.setPlaceholderText('Buscar por placa ou modelo...')
        self.search_bar_veiculos.textChanged.connect(self.filtrar_veiculos)

        self.listaVeiculos = QListWidget()

        self.btnAdicionarVeiculo = QPushButton('Adicionar')
        self.btnAdicionarVeiculo.setIcon(QIcon('icon/adicionar_veiculo.png'))
        self.btnAdicionarVeiculo.setToolTip('Adicionar Veículo')

        self.btnEditarVeiculo = QPushButton('Editar')
        self.btnEditarVeiculo.setIcon(QIcon('icon/editar.png'))
        self.btnEditarVeiculo.setToolTip('Editar Veículo')

        self.btnExcluirVeiculo = QPushButton('Excluir')
        self.btnExcluirVeiculo.setIcon(QIcon('icon/excluir_veiculo.png'))
        self.btnExcluirVeiculo.setToolTip('Excluir Veículo')

        self.listaVeiculos.itemSelectionChanged.connect(self.selecionar_veiculo)
        self.btnAdicionarVeiculo.clicked.connect(self.adicionar_veiculo)
        self.btnEditarVeiculo.clicked.connect(self.editar_veiculo)
        self.btnExcluirVeiculo.clicked.connect(self.excluir_veiculo)

        self.tab_veiculos_layout.addWidget(self.search_bar_veiculos)
        self.tab_veiculos_layout.addWidget(self.listaVeiculos)
        self.tab_veiculos_layout.addWidget(self.btnAdicionarVeiculo)
        self.tab_veiculos_layout.addWidget(self.btnEditarVeiculo)
        self.tab_veiculos_layout.addWidget(self.btnExcluirVeiculo)


    def setup_manutencoes_tab(self):
        self.tab_manutencoes = QWidget()
        icon_manutencoes = QIcon('icon/adicionar_manutencao.png')
        self.tabs.addTab(self.tab_manutencoes, icon_manutencoes, "Manutenções")

        self.tab_manutencoes_layout = QVBoxLayout(self.tab_manutencoes)

        self.search_manutencoes_bar = QLineEdit()
        self.search_manutencoes_bar.setPlaceholderText('Buscar por placa e data...')
        self.search_manutencoes_bar.textChanged.connect(self.filtrar_manutencoes)

        self.listaManutencoes = QListWidget()

        self.soma_valores_label = QLabel('Soma dos Valores: R$ 0.00')

        self.btnAdicionarManutencao = QPushButton('Adicionar')
        self.btnAdicionarManutencao.setIcon(QIcon('icon/adicionar_manutencao.png'))
        self.btnAdicionarManutencao.setToolTip('Adicionar Manutenção')

        self.btnEditarManutencao = QPushButton('Editar')
        self.btnEditarManutencao.setIcon(QIcon('icon/editar.png'))
        self.btnEditarManutencao.setToolTip('Editar Manutenção')

        self.btnExcluirManutencao = QPushButton('Excluir')
        self.btnExcluirManutencao.setIcon(QIcon('icon/excluir.png'))
        self.btnExcluirManutencao.setToolTip('Excluir Manutenção')

        self.listaManutencoes.itemSelectionChanged.connect(self.selecionar_manutencao)
        self.btnAdicionarManutencao.clicked.connect(self.adicionar_manutencao)
        self.btnEditarManutencao.clicked.connect(self.editar_manutencao)
        self.btnExcluirManutencao.clicked.connect(self.excluir_manutencao)

        self.tab_manutencoes_layout.addWidget(self.search_manutencoes_bar)
        self.tab_manutencoes_layout.addWidget(self.listaManutencoes)
        self.tab_manutencoes_layout.addWidget(self.soma_valores_label)
        self.tab_manutencoes_layout.addWidget(self.btnAdicionarManutencao)
        self.tab_manutencoes_layout.addWidget(self.btnEditarManutencao)
        self.tab_manutencoes_layout.addWidget(self.btnExcluirManutencao)


    def filtrar_clientes(self):
        search_text = self.search_bar.text().lower()
        self.listaClientes.clear()
        for cliente in self.clientes:
            if search_text in cliente['nome'].lower():
                self.listaClientes.addItem(f"Nome: {cliente['nome']} - RG: {cliente['rg']} - Endereço: {cliente['endereco']} - Telefone: {cliente['telefone']} - WhatsApp: {cliente['whatsapp']}")
  
  
    def filtrar_veiculos(self):
        search_text = self.search_bar_veiculos.text().lower()
        self.listaVeiculos.clear()
        for veiculo in self.veiculos:
            if search_text in veiculo['placa'].lower() or search_text in veiculo['modelo'].lower():
                self.listaVeiculos.addItem(f"Placa: {veiculo['placa']} - Modelo: {veiculo['modelo']} - Ano: {veiculo['ano']}")


    def filtrar_manutencoes(self):
        search_text = self.search_manutencoes_bar.text().lower()
        self.listaManutencoes.clear()  # Limpa a lista antes de atualizar

        total_valor = 0.0
        for manutencao in self.manutencoes:
            if (search_text in manutencao['placa'].lower() or search_text in manutencao['data'].lower()):
                try:
                    valor = float(manutencao.get('valor', '0.00'))
                    total_valor += valor
                except ValueError:
                    valor = 0.00

                self.listaManutencoes.addItem(f"Data: {manutencao['data']} - Veículo: {manutencao['placa']} - Informações: {manutencao['informacoes']} - Mecânico: {manutencao['mecanico']} - Valor: R$ {valor:.2f}")

        self.soma_valores_label.setText(f'Soma dos Valores: R$ {total_valor:.2f}')
        

    def selecionar_cliente(self):
        selected_item = self.listaClientes.currentItem()
        self.btnEditarCliente.setEnabled(selected_item is not None)
        self.btnExcluirCliente.setEnabled(selected_item is not None)


    def selecionar_veiculo(self):
        selected_item = self.listaVeiculos.currentItem()
        self.btnEditarVeiculo.setEnabled(selected_item is not None)
        self.btnExcluirVeiculo.setEnabled(selected_item is not None)


    def selecionar_manutencao(self):
        selected_item = self.listaManutencoes.currentItem()
        self.btnEditarManutencao.setEnabled(selected_item is not None)
        self.btnExcluirManutencao.setEnabled(selected_item is not None)


    def carregar_clientes(self):
        try:
            with open('clientes.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []


    def salvar_clientes(self):
        with open('clientes.json', 'w') as file:
            json.dump(self.clientes, file, indent=4)


    def adicionar_cliente(self):
        dialog = QWidget()
        form = QFormLayout()
        nome = QLineEdit()
        rg = QLineEdit()
        endereco = QLineEdit()
        telefone = QLineEdit()
        whatsapp = QLineEdit()

        form.addRow("Nome:", nome)
        form.addRow("RG:", rg)
        form.addRow("Endereço:", endereco)
        form.addRow("Telefone:", telefone)
        form.addRow("WhatsApp:", whatsapp)

        def save():
            if nome.text() and rg.text() and endereco.text() and telefone.text():
                cliente = {
                    'nome': nome.text(),
                    'rg': rg.text(),
                    'endereco': endereco.text(),
                    'telefone': telefone.text(),
                    'whatsapp': whatsapp.text(),
                    'usuario_cadastro': self.logged_in_username  # Adiciona o usuário que cadastrou o cliente
                    
                }
                self.clientes.append(cliente)
                self.salvar_clientes()
                QMessageBox.information(self, 'Sucesso', 'Cliente adicionado com sucesso!')
                dialog.close()
                self.listar_clientes()  # Atualiza a lista de clientes
            else:
                QMessageBox.warning(self, 'Erro', 'Preencha todos os campos!')

        btnSalvar = QPushButton('Salvar', dialog)
        btnSalvar.clicked.connect(save)
        form.addRow(btnSalvar)

        dialog.setLayout(form)
        dialog.setWindowTitle('Adicionar Cliente')
        dialog.show()


    def listar_clientes(self):
        self.listaClientes.clear()  # Limpa a lista antes de atualizar
        for cliente in self.clientes:
            if 'usuario_cadastro' in cliente:
                usuario_cadastro = cliente['usuario_cadastro']
            else:
                usuario_cadastro = 'Desconhecido'    
            self.listaClientes.addItem(f"Nome: {cliente['nome']} - RG: {cliente['rg']} - Endereço: {cliente['endereco']} - Telefone: {cliente['telefone']} - WhatsApp: {cliente['whatsapp']} - Cadastro por:{usuario_cadastro}")


    def editar_cliente(self):
        selected_item = self.listaClientes.currentItem()
        if selected_item:
            cliente_info = selected_item.text()
            nome, rg, endereco, telefone, whatsapp = self.extract_cliente_info(cliente_info)

            dialog = QWidget()
            form = QFormLayout()
            nome_edit = QLineEdit(nome)
            rg_edit = QLineEdit(rg)
            endereco_edit = QLineEdit(endereco)
            telefone_edit = QLineEdit(telefone)
            whatsapp_edit = QLineEdit(whatsapp)

            form.addRow("Nome:", nome_edit)
            form.addRow("RG:", rg_edit)
            form.addRow("Endereço:", endereco_edit)
            form.addRow("Telefone:", telefone_edit)
            form.addRow("WhatsApp:", whatsapp_edit)

            def save():
                if nome_edit.text() and rg_edit.text() and endereco_edit.text() and telefone_edit.text():
                    cliente = {
                        'nome': nome_edit.text(),
                        'rg': rg_edit.text(),
                        'endereco': endereco_edit.text(),
                        'telefone': telefone_edit.text(),
                        'whatsapp': whatsapp_edit.text()
                    }
                    for i, c in enumerate(self.clientes):
                        if c['rg'] == rg:  # Assuming RG is unique
                            self.clientes[i] = cliente
                            break
                    self.salvar_clientes()
                    QMessageBox.information(self, 'Sucesso', 'Cliente atualizado com sucesso!')
                    dialog.close()
                    self.listar_clientes()  # Atualiza a lista de clientes
                else:
                    QMessageBox.warning(self, 'Erro', 'Preencha todos os campos!')

            btnSalvar = QPushButton('Salvar', dialog)
            btnSalvar.clicked.connect(save)
            form.addRow(btnSalvar)

            dialog.setLayout(form)
            dialog.setWindowTitle('Editar Cliente')
            dialog.show()


    def extract_cliente_info(self, cliente_info):
        parts = cliente_info.split(' - ')
        nome = parts[0].split(': ')[1]
        rg = parts[1].split(': ')[1]
        endereco = parts[2].split(': ')[1]
        telefone = parts[3].split(': ')[1]
        whatsapp = parts[4].split(': ')[1]
        return nome, rg, endereco, telefone, whatsapp


    def excluir_cliente(self):
        selected_item = self.listaClientes.currentItem()
        if selected_item:
            cliente_info = selected_item.text()
            rg = self.extract_cliente_info(cliente_info)[1]

            resposta = QMessageBox.question(self, 'Confirmação', 'Tem certeza de que deseja excluir este cliente?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if resposta == QMessageBox.Yes:
                self.clientes = [c for c in self.clientes if c['rg'] != rg]
                self.salvar_clientes()
                QMessageBox.information(self, 'Sucesso', 'Cliente excluído com sucesso!')
                self.listar_clientes()  # Atualiza a lista de clientes


    def carregar_veiculos(self):
        try:
            with open('veiculos.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []


    def salvar_veiculos(self):
        with open('veiculos.json', 'w') as file:
            json.dump(self.veiculos, file, indent=4)


    def adicionar_veiculo(self):
        dialog = QWidget()
        form = QFormLayout()
        placa = QLineEdit()
        modelo = QLineEdit()
        ano = QLineEdit()

        form.addRow("Placa:", placa)
        form.addRow("Modelo:", modelo)
        form.addRow("Ano:", ano)

        def save():
            placa_text = placa.text().upper().strip()  # Transformar para maiúsculas e remover espaços em branco
            modelo_text = modelo.text().upper().strip()
            ano_text = ano.text().strip()

            if placa_text and modelo_text and ano_text:
                # Verificar se a placa já existe
                for veiculo in self.veiculos:
                    if veiculo['placa'] == placa_text:
                        QMessageBox.warning(self, 'Erro', 'A placa já está cadastrada!')
                        return

                veiculo = {
                    'placa': placa_text,
                    'modelo': modelo_text,
                    'ano': ano_text,
                    'usuario_cadastro': self.logged_in_username  # Adiciona o usuário que cadastrou o veículo
                }
                self.veiculos.append(veiculo)
                self.salvar_veiculos()
                QMessageBox.information(self, 'Sucesso', 'Veículo adicionado com sucesso!')
                dialog.close()
                self.listar_veiculos()  # Atualiza a lista de veículos
            else:
                QMessageBox.warning(self, 'Erro', 'Preencha todos os campos!')

        btnSalvar = QPushButton('Salvar', dialog)
        btnSalvar.clicked.connect(save)
        form.addRow(btnSalvar)

        dialog.setLayout(form)
        dialog.setWindowTitle('Adicionar Veículo')
        dialog.show()


    def listar_veiculos(self):
        self.listaVeiculos.clear()  # Limpa a lista antes de atualizar
        for veiculo in self.veiculos:
            if 'usuario_cadastro' in veiculo:
                usuario_cadastro = veiculo['usuario_cadastro']
            else:
                usuario_cadastro = 'Desconhecido'
            self.listaVeiculos.addItem(f"Placa: {veiculo['placa']} - Modelo: {veiculo['modelo']} - Ano: {veiculo['ano']} - Cadastro por: {usuario_cadastro}")


    def editar_veiculo(self):
        selected_item = self.listaVeiculos.currentItem()
        if selected_item:
            veiculo_info = selected_item.text()
            placa, modelo, ano = self.extract_veiculo_info(veiculo_info)

            dialog = QWidget()
            form = QFormLayout()
            placa_edit = QLineEdit(placa)
            modelo_edit = QLineEdit(modelo)
            ano_edit = QLineEdit(ano)

            form.addRow("Placa:", placa_edit)
            form.addRow("Modelo:", modelo_edit)
            form.addRow("Ano:", ano_edit)

            def save():
                if placa_edit.text() and modelo_edit.text() and ano_edit.text():
                    veiculo = {
                        'placa': placa_edit.text(),
                        'modelo': modelo_edit.text(),
                        'ano': ano_edit.text()
                    }
                    for i, v in enumerate(self.veiculos):
                        if v['placa'] == placa:  # Assuming Placa is unique
                            self.veiculos[i] = veiculo
                            break
                    self.salvar_veiculos()
                    QMessageBox.information(self, 'Sucesso', 'Veículo atualizado com sucesso!')
                    dialog.close()
                    self.listar_veiculos()  # Atualiza a lista de veículos
                else:
                    QMessageBox.warning(self, 'Erro', 'Preencha todos os campos!')

            btnSalvar = QPushButton('Salvar', dialog)
            btnSalvar.clicked.connect(save)
            form.addRow(btnSalvar)

            dialog.setLayout(form)
            dialog.setWindowTitle('Editar Veículo')
            dialog.show()


    def extract_veiculo_info(self, veiculo_info):
        parts = veiculo_info.split(' - ')
        placa = parts[0].split(': ')[1]
        modelo = parts[1].split(': ')[1]
        ano = parts[2].split(': ')[1]
        return placa, modelo, ano


    def excluir_veiculo(self):
        selected_item = self.listaVeiculos.currentItem()
        if selected_item:
            veiculo_info = selected_item.text()
            placa = self.extract_veiculo_info(veiculo_info)[0]

            resposta = QMessageBox.question(self, 'Confirmação', 'Tem certeza de que deseja excluir este veículo?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if resposta == QMessageBox.Yes:
                self.veiculos = [v for v in self.veiculos if v['placa'] != placa]
                self.salvar_veiculos()
                QMessageBox.information(self, 'Sucesso', 'Veículo excluído com sucesso!')
                self.listar_veiculos()  # Atualiza a lista de veículos


    def carregar_manutencoes(self):
        try:
            with open('manutencoes.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []


    def salvar_manutencoes(self):
        with open('manutencoes.json', 'w') as file:
            json.dump(self.manutencoes, file, indent=4)


    def adicionar_manutencao(self):
        dialog = QWidget()
        form = QFormLayout()
        data = QLineEdit()

        # Criar um QComboBox para selecionar a placa do veículo
        placa_combo = QComboBox()
        for veiculo in self.veiculos:
            placa_combo.addItem(veiculo['placa'])

        informacoes = QLineEdit()
        mecanico = QLineEdit()
        valor = QLineEdit()

        form.addRow("Data:", data)
        form.addRow("Placa:", placa_combo)
        form.addRow("Informações:", informacoes)
        form.addRow("Mecânico:", mecanico)
        form.addRow("Valor:", valor)

        def save():
            if data.text() and placa_combo.currentText() and informacoes.text() and mecanico.text() and valor.text():
                try:
                    float(valor.text())  # Verifica se o valor é um número
                except ValueError:
                    QMessageBox.warning(self, 'Erro', 'O valor deve ser numérico!')
                    return
                
                manutencao = {
                    'data': data.text(),
                    'placa': placa_combo.currentText(),
                    'informacoes': informacoes.text(),
                    'mecanico': mecanico.text(),
                    'valor': valor.text(),
                    'usuario_cadastro': self.logged_in_username  # Adiciona o usuário que cadastrou o veículo
                }
                self.manutencoes.append(manutencao)
                self.salvar_manutencoes()
                QMessageBox.information(self, 'Sucesso', 'Manutenção adicionada com sucesso!')
                dialog.close()
                self.listar_manutencoes()  # Atualiza a lista de manutenções
            else:
                QMessageBox.warning(self, 'Erro', 'Preencha todos os campos!')

        btnSalvar = QPushButton('Salvar', dialog)
        btnSalvar.clicked.connect(save)
        form.addRow(btnSalvar)

        dialog.setLayout(form)
        dialog.setWindowTitle('Adicionar Manutenção')
        dialog.show()


    def listar_manutencoes(self):
        self.listaManutencoes.clear()  # Limpa a lista antes de atualizar
        for manutencao in self.manutencoes:
            data = manutencao.get('data', 'N/A')
            placa = manutencao.get('placa', 'N/A')
            informacoes = manutencao.get('informacoes', 'N/A')
            mecanico = manutencao.get('mecanico', 'N/A')
            valor = manutencao.get('valor', 'N/A')
            self.listaManutencoes.addItem(f"Data: {data} - Veículo: {placa} - Informações: {informacoes} - Mecânico: {mecanico} - Valor: {valor}")


    def editar_manutencao(self):
        selected_item = self.listaManutencoes.currentItem()
        if selected_item:
            manutencao_info = selected_item.text()
            data, placa, informacoes, mecanico, valor = self.extract_manutencao_info(manutencao_info)

            # Criação do diálogo de edição
            dialog = QWidget()
            form = QFormLayout()
            data_edit = QLineEdit(data)
            placa_edit = QLineEdit(placa)
            informacoes_edit = QLineEdit(informacoes)
            mecanico_edit = QLineEdit(mecanico)
            valor_edit = QLineEdit(valor)

            form.addRow("Data:", data_edit)
            form.addRow("Placa:", placa_edit)
            form.addRow("Informações:", informacoes_edit)
            form.addRow("Mecânico:", mecanico_edit)
            form.addRow("Valor:", valor_edit)

            def save():
                if (data_edit.text() and placa_edit.text() and informacoes_edit.text() and 
                    mecanico_edit.text() and valor_edit.text()):
                    
                    # Atualiza a manutenção
                    manutencao = {
                        'data': data_edit.text(),
                        'placa': placa_edit.text(),
                        'informacoes': informacoes_edit.text(),
                        'mecanico': mecanico_edit.text(),
                        'valor': valor_edit.text()
                    }

                    # Encontra e atualiza a manutenção correspondente
                    for i, m in enumerate(self.manutencoes):
                        if m['data'] == data and m['placa'] == placa:  # Verifica se data e placa coincidem
                            self.manutencoes[i] = manutencao
                            break
                    
                    self.salvar_manutencoes()
                    QMessageBox.information(self, 'Sucesso', 'Manutenção atualizada com sucesso!')
                    dialog.close()
                    self.listar_manutencoes()  # Atualiza a lista de manutenções
                else:
                    QMessageBox.warning(self, 'Erro', 'Preencha todos os campos!')

            btnSalvar = QPushButton('Salvar', dialog)
            btnSalvar.clicked.connect(save)
            form.addRow(btnSalvar)

            dialog.setLayout(form)
            dialog.setWindowTitle('Editar Manutenção')
            dialog.show()


    def excluir_manutencao(self):
        selected_item = self.listaManutencoes.currentItem()
        if selected_item:
            manutencao_info = selected_item.text()
            try:
                data, placa, _, _, _ = self.extract_manutencao_info(manutencao_info)
            except ValueError as e:
                QMessageBox.warning(self, 'Erro', f'Erro ao extrair informações: {e}')
                return

            resposta = QMessageBox.question(self, 'Confirmação', 'Tem certeza de que deseja excluir esta manutenção?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if resposta == QMessageBox.Yes:
                self.manutencoes = [m for m in self.manutencoes if not (m['data'] == data and m['placa'] == placa)]
                self.salvar_manutencoes()
                QMessageBox.information(self, 'Sucesso', 'Manutenção excluída com sucesso!')
                self.listar_manutencoes()  # Atualiza a lista de manutenções


    def extract_manutencao_info(self, manutencao_info):
        parts = manutencao_info.split(' - ')
        if len(parts) < 5:
            raise ValueError("Formato de manutenção inválido")
        data = parts[0].split(': ')[1]
        placa = parts[1].split(': ')[1]
        informacoes = parts[2].split(': ')[1]
        mecanico = parts[3].split(': ')[1]
        valor = parts[4].split(': ')[1]
        return data, placa, informacoes, mecanico, valor


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = VeiculosApp()
    mainWin.show()
    sys.exit(app.exec_())