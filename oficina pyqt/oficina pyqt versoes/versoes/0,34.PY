import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QListWidget, QPushButton, QFormLayout, QLineEdit, QLabel, QMessageBox

class VeiculosApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
        self.clientes = self.carregar_clientes()
        self.veiculos = self.carregar_veiculos()
        self.manutencoes = self.carregar_manutencoes()

        self.listar_clientes()
        self.listar_veiculos()
        self.listar_manutencoes()

    def initUI(self):
        self.setWindowTitle('Sistema de Gerenciamento de Oficina')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        self.setup_clientes_tab()
        self.setup_veiculos_tab()
        self.setup_manutencoes_tab()

    def setup_clientes_tab(self):
        self.tab_clientes = QWidget()
        self.tabs.addTab(self.tab_clientes, "Clientes")

        # Layout for the clients tab
        self.tab_clientes_layout = QVBoxLayout(self.tab_clientes)

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText('Buscar por nome...')
        self.search_bar.textChanged.connect(self.filtrar_clientes)

        # List widget and buttons
        self.listaClientes = QListWidget()
        self.btnAdicionarCliente = QPushButton('Adicionar Cliente')
        self.btnEditarCliente = QPushButton('Editar Cliente')
        self.btnExcluirCliente = QPushButton('Excluir Cliente')

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
        self.tabs.addTab(self.tab_veiculos, "Veículos")

        self.listaVeiculos = QListWidget()
        self.btnAdicionarVeiculo = QPushButton('Adicionar Veículo')
        self.btnEditarVeiculo = QPushButton('Editar Veículo')
        self.btnExcluirVeiculo = QPushButton('Excluir Veículo')

        self.listaVeiculos.itemSelectionChanged.connect(self.selecionar_veiculo)
        self.btnAdicionarVeiculo.clicked.connect(self.adicionar_veiculo)
        self.btnEditarVeiculo.clicked.connect(self.editar_veiculo)
        self.btnExcluirVeiculo.clicked.connect(self.excluir_veiculo)

        self.tab_veiculos_layout = QVBoxLayout(self.tab_veiculos)
        self.tab_veiculos_layout.addWidget(self.listaVeiculos)
        self.tab_veiculos_layout.addWidget(self.btnAdicionarVeiculo)
        self.tab_veiculos_layout.addWidget(self.btnEditarVeiculo)
        self.tab_veiculos_layout.addWidget(self.btnExcluirVeiculo)

    def setup_manutencoes_tab(self):
        self.tab_manutencoes = QWidget()
        self.tabs.addTab(self.tab_manutencoes, "Manutenções")

        self.listaManutencoes = QListWidget()
        self.btnAdicionarManutencao = QPushButton('Adicionar Manutenção')
        self.btnEditarManutencao = QPushButton('Editar Manutenção')
        self.btnExcluirManutencao = QPushButton('Excluir Manutenção')

        self.listaManutencoes.itemSelectionChanged.connect(self.selecionar_manutencao)
        self.btnAdicionarManutencao.clicked.connect(self.adicionar_manutencao)
        self.btnEditarManutencao.clicked.connect(self.editar_manutencao)
        self.btnExcluirManutencao.clicked.connect(self.excluir_manutencao)

        self.tab_manutencoes_layout = QVBoxLayout(self.tab_manutencoes)
        self.tab_manutencoes_layout.addWidget(self.listaManutencoes)
        self.tab_manutencoes_layout.addWidget(self.btnAdicionarManutencao)
        self.tab_manutencoes_layout.addWidget(self.btnEditarManutencao)
        self.tab_manutencoes_layout.addWidget(self.btnExcluirManutencao)

    def filtrar_clientes(self):
        search_text = self.search_bar.text().lower()
        self.listaClientes.clear()
        for cliente in self.clientes:
            if search_text in cliente['nome'].lower():
                self.listaClientes.addItem(f"Nome: {cliente['nome']} - RG: {cliente['rg']} - Endereço: {cliente['endereco']} - Telefone: {cliente['telefone']} - WhatsApp: {cliente['whatsapp']}")

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
                    'whatsapp': whatsapp.text()
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
            self.listaClientes.addItem(f"Nome: {cliente['nome']} - RG: {cliente['rg']} - Endereço: {cliente['endereco']} - Telefone: {cliente['telefone']} - WhatsApp: {cliente['whatsapp']}")

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
        # Implementar adicionar veículo aqui
        pass

    def listar_veiculos(self):
        self.listaVeiculos.clear()  # Limpa a lista antes de atualizar
        for veiculo in self.veiculos:
            self.listaVeiculos.addItem(f"Placa: {veiculo['placa']} - Modelo: {veiculo['modelo']} - Ano: {veiculo['ano']}")

    def editar_veiculo(self):
        # Implementar editar veículo aqui
        pass

    def excluir_veiculo(self):
        # Implementar excluir veículo aqui
        pass

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
        # Implementar adicionar manutenção aqui
        pass

    def listar_manutencoes(self):
        self.listaManutencoes.clear()  # Limpa a lista antes de atualizar
        for manutencao in self.manutencoes:
            self.listaManutencoes.addItem(f"Data: {manutencao['data']} - Veículo: {manutencao['placa']} - Descrição: {manutencao['informacoes']}")

    def editar_manutencao(self):
        # Implementar editar manutenção aqui
        pass

    def excluir_manutencao(self):
        # Implementar excluir manutenção aqui
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = VeiculosApp()
    mainWin.show()
    sys.exit(app.exec_())
