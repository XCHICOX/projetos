import json
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QMessageBox, QListWidget, QFormLayout, QTabWidget, QHBoxLayout, QSplitter
from PyQt5.QtGui import QIcon

class VeiculosApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.clientes = self.carregar_clientes()
        self.veiculos = self.carregar_veiculos()
        self.manutencoes = self.carregar_manutencoes()

    def initUI(self):
        self.setWindowTitle('Gerenciamento de Veículos')

        # Layout principal
        layout = QVBoxLayout()

        # Widget de abas
        self.tabs = QTabWidget()

        # Aba de Clientes
        self.tabClientes = QWidget()
        self.tabClientesLayout = QVBoxLayout()
        self.setup_clientes_tab()
        self.tabClientes.setLayout(self.tabClientesLayout)
        self.tabs.addTab(self.tabClientes, 'Clientes')

        # Aba de Veículos
        self.tabVeiculos = QWidget()
        self.tabVeiculosLayout = QVBoxLayout()
        self.setup_veiculos_tab()
        self.tabVeiculos.setLayout(self.tabVeiculosLayout)
        self.tabs.addTab(self.tabVeiculos, 'Veículos')

        # Aba de Manutenções
        self.tabManutencoes = QWidget()
        self.tabManutencoesLayout = QVBoxLayout()
        self.setup_manutencoes_tab()
        self.tabManutencoes.setLayout(self.tabManutencoesLayout)
        self.tabs.addTab(self.tabManutencoes, 'Manutenções')

        layout.addWidget(self.tabs)
        self.setLayout(layout)
        self.show()

    def setup_clientes_tab(self):
        # Layout para os botões e a lista
        buttonLayout = QVBoxLayout()

        self.btnAdicionarCliente = QPushButton('Adicionar Cliente', self)
        self.btnAdicionarCliente.setIcon(QIcon('icons/add_client.png'))
        self.btnAdicionarCliente.clicked.connect(self.adicionar_cliente)
        buttonLayout.addWidget(self.btnAdicionarCliente)

        self.btnListarClientes = QPushButton('Listar Clientes', self)
        self.btnListarClientes.setIcon(QIcon('icons/list_clients.png'))
        self.btnListarClientes.clicked.connect(self.listar_clientes)
        buttonLayout.addWidget(self.btnListarClientes)

        self.btnEditarCliente = QPushButton('Editar Cliente', self)
        self.btnEditarCliente.setIcon(QIcon('icons/edit_client.png'))
        self.btnEditarCliente.clicked.connect(self.editar_cliente)
        buttonLayout.addWidget(self.btnEditarCliente)

        self.btnExcluirCliente = QPushButton('Excluir Cliente', self)
        self.btnExcluirCliente.setIcon(QIcon('icons/delete_client.png'))
        self.btnExcluirCliente.clicked.connect(self.excluir_cliente)
        buttonLayout.addWidget(self.btnExcluirCliente)

        # Lista de Clientes
        self.listaClientes = QListWidget()
        self.listaClientes.setFixedHeight(200)  # Ajuste a altura conforme necessário

        # Adicionar layout de botões e lista ao layout da aba
        self.tabClientesLayout.addLayout(buttonLayout)
        self.tabClientesLayout.addWidget(self.listaClientes)

    def setup_veiculos_tab(self):
        self.btnAdicionarVeiculo = QPushButton('Adicionar Veículo', self)
        self.btnAdicionarVeiculo.setIcon(QIcon('icons/add_vehicle.png'))
        self.btnAdicionarVeiculo.clicked.connect(self.adicionar_veiculo)
        self.tabVeiculosLayout.addWidget(self.btnAdicionarVeiculo)

        self.btnListarVeiculos = QPushButton('Listar Veículos', self)
        self.btnListarVeiculos.setIcon(QIcon('icons/list_vehicles.png'))
        self.btnListarVeiculos.clicked.connect(self.listar_veiculos)
        self.tabVeiculosLayout.addWidget(self.btnListarVeiculos)

        self.btnEditarVeiculo = QPushButton('Editar Veículo', self)
        self.btnEditarVeiculo.setIcon(QIcon('icons/edit_vehicle.png'))
        self.btnEditarVeiculo.clicked.connect(self.editar_veiculo)
        self.tabVeiculosLayout.addWidget(self.btnEditarVeiculo)

        self.btnExcluirVeiculo = QPushButton('Excluir Veículo', self)
        self.btnExcluirVeiculo.setIcon(QIcon('icons/delete_vehicle.png'))
        self.btnExcluirVeiculo.clicked.connect(self.excluir_veiculo)
        self.tabVeiculosLayout.addWidget(self.btnExcluirVeiculo)

    def setup_manutencoes_tab(self):
        self.btnAdicionarManutencao = QPushButton('Adicionar Manutenção', self)
        self.btnAdicionarManutencao.setIcon(QIcon('icons/add_maintenance.png'))
        self.btnAdicionarManutencao.clicked.connect(self.adicionar_manutencao)
        self.tabManutencoesLayout.addWidget(self.btnAdicionarManutencao)

        self.btnListarManutencoes = QPushButton('Listar Manutenções', self)
        self.btnListarManutencoes.setIcon(QIcon('icons/list_maintenance.png'))
        self.btnListarManutencoes.clicked.connect(self.listar_manutencoes)
        self.tabManutencoesLayout.addWidget(self.btnListarManutencoes)

        self.btnEditarManutencao = QPushButton('Editar Manutenção', self)
        self.btnEditarManutencao.setIcon(QIcon('icons/edit_maintenance.png'))
        self.btnEditarManutencao.clicked.connect(self.editar_manutencao)
        self.tabManutencoesLayout.addWidget(self.btnEditarManutencao)

        self.btnExcluirManutencao = QPushButton('Excluir Manutenção', self)
        self.btnExcluirManutencao.setIcon(QIcon('icons/delete_maintenance.png'))
        self.btnExcluirManutencao.clicked.connect(self.excluir_manutencao)
        self.tabManutencoesLayout.addWidget(self.btnExcluirManutencao)

    # Funções de manipulação dos dados

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
        # Similar ao adicionar_cliente, mas preenchendo os campos com os valores existentes e salvando a edição
        pass

    def excluir_cliente(self):
        # Permitir selecionar um cliente e removê-lo da lista
        pass

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
        marca = QLineEdit()
        modelo = QLineEdit()
        ano = QLineEdit()
        placa = QLineEdit()

        form.addRow("Marca:", marca)
        form.addRow("Modelo:", modelo)
        form.addRow("Ano:", ano)
        form.addRow("Placa:", placa)

        def save():
            if marca.text() and modelo.text() and ano.text() and placa.text():
                veiculo = {
                    'marca': marca.text(),
                    'modelo': modelo.text(),
                    'ano': ano.text(),
                    'placa': placa.text()
                }
                self.veiculos.append(veiculo)
                self.salvar_veiculos()
                QMessageBox.information(self, 'Sucesso', 'Veículo adicionado com sucesso!')
                dialog.close()
            else:
                QMessageBox.warning(self, 'Erro', 'Preencha todos os campos!')

        btnSalvar = QPushButton('Salvar', dialog)
        btnSalvar.clicked.connect(save)
        form.addRow(btnSalvar)

        dialog.setLayout(form)
        dialog.setWindowTitle('Adicionar Veículo')
        dialog.show()

    def listar_veiculos(self):
        dialog = QWidget()
        layout = QVBoxLayout()
        lista = QListWidget()

        for veiculo in self.veiculos:
            lista.addItem(f"Marca: {veiculo['marca']} - Modelo: {veiculo['modelo']} - Ano: {veiculo['ano']} - Placa: {veiculo['placa']}")

        layout.addWidget(lista)
        dialog.setLayout(layout)
        dialog.setWindowTitle('Lista de Veículos')
        dialog.show()

    def editar_veiculo(self):
        # Similar ao adicionar_veiculo, mas preenchendo os campos com os valores existentes e salvando a edição
        pass

    def excluir_veiculo(self):
        # Permitir selecionar um veículo e removê-lo da lista
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
        dialog = QWidget()
        form = QFormLayout()
        placa = QLineEdit()
        data = QLineEdit()
        informacoes = QLineEdit()
        valor = QLineEdit()
        mecanico = QLineEdit()

        form.addRow("Placa do Veículo:", placa)
        form.addRow("Data:", data)
        form.addRow("Informações:", informacoes)
        form.addRow("Valor (R$):", valor)
        form.addRow("Mecânico:", mecanico)

        def save():
            if placa.text() and data.text() and informacoes.text() and valor.text():
                if not any(v['placa'] == placa.text() for v in self.veiculos):
                    QMessageBox.warning(self, 'Erro', 'Placa não cadastrada! Cadastre o veículo primeiro.')
                    return

                valor_tratado = valor.text().replace('R$', '').replace(',', '').strip()
                try:
                    valor_float = float(valor_tratado)
                except ValueError:
                    QMessageBox.warning(self, 'Erro', 'Valor inválido! Informe um número.')
                    return

                manutencao = {
                    'placa': placa.text(),
                    'data': data.text(),
                    'informacoes': informacoes.text(),
                    'valor': valor_float,
                    'mecanico': mecanico.text()
                }
                self.manutencoes.append(manutencao)
                self.salvar_manutencoes()
                QMessageBox.information(self, 'Sucesso', 'Manutenção adicionada com sucesso!')
                dialog.close()
            else:
                QMessageBox.warning(self, 'Erro', 'Preencha todos os campos!')

        btnSalvar = QPushButton('Salvar', dialog)
        btnSalvar.clicked.connect(save)
        form.addRow(btnSalvar)

        dialog.setLayout(form)
        dialog.setWindowTitle('Adicionar Manutenção')
        dialog.show()

    def listar_manutencoes(self):
        dialog = QWidget()
        layout = QVBoxLayout()
        lista = QListWidget()

        for manutencao in self.manutencoes:
            lista.addItem(f"Placa: {manutencao['placa']} - Data: {manutencao['data']} - Informações: {manutencao['informacoes']} - Valor: R${manutencao['valor']} - Mecânico: {manutencao['mecanico']}")

        layout.addWidget(lista)
        dialog.setLayout(layout)
        dialog.setWindowTitle('Lista de Manutenções')
        dialog.show()

    def editar_manutencao(self):
        # Similar ao adicionar_manutencao, mas preenchendo os campos com os valores existentes e salvando a edição
        pass

    def excluir_manutencao(self):
        # Permitir selecionar uma manutenção e removê-la da lista
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = VeiculosApp()
    sys.exit(app.exec_())
