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

        self.listaClientes = QListWidget()
        self.btnAdicionarCliente = QPushButton('Adicionar Cliente')
        self.btnEditarCliente = QPushButton('Editar Cliente')
        self.btnExcluirCliente = QPushButton('Excluir Cliente')

        self.listaClientes.itemSelectionChanged.connect(self.selecionar_cliente)
        self.btnAdicionarCliente.clicked.connect(self.adicionar_cliente)
        self.btnEditarCliente.clicked.connect(self.editar_cliente)
        self.btnExcluirCliente.clicked.connect(self.excluir_cliente)

        self.tab_clientes_layout = QVBoxLayout(self.tab_clientes)
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
                    QMessageBox.information(self, 'Sucesso', 'Cliente editado com sucesso!')
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

    def excluir_cliente(self):
        selected_item = self.listaClientes.currentItem()
        if selected_item:
            cliente_info = selected_item.text()
            nome, rg, endereco, telefone, whatsapp = self.extract_cliente_info(cliente_info)

            reply = QMessageBox.question(self, 'Excluir Cliente',
                                         f"Tem certeza de que deseja excluir o cliente {nome} com RG {rg}?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.clientes = [c for c in self.clientes if c['rg'] != rg]
                self.salvar_clientes()
                self.listar_clientes()  # Atualiza a lista de clientes

    def extract_cliente_info(self, cliente_info):
        # Extrair informações do cliente do texto
        parts = cliente_info.split(' - ')
        nome = parts[0].replace("Nome: ", "")
        rg = parts[1].replace("RG: ", "")
        endereco = parts[2].replace("Endereço: ", "")
        telefone = parts[3].replace("Telefone: ", "")
        whatsapp = parts[4].replace("WhatsApp: ", "")
        return nome, rg, endereco, telefone, whatsapp

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
        cliente = QLineEdit()  # Inclua o cliente

        form.addRow("Marca:", marca)
        form.addRow("Modelo:", modelo)
        form.addRow("Ano:", ano)
        form.addRow("Placa:", placa)
        form.addRow("Cliente:", cliente)

        def save():
            if marca.text() and modelo.text() and ano.text() and placa.text() and cliente.text():
                veiculo = {
                    'marca': marca.text(),
                    'modelo': modelo.text(),
                    'ano': ano.text(),
                    'placa': placa.text(),
                    'cliente': cliente.text()  # Removido 'cor'
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
        self.listaVeiculos.clear()  # Limpa a lista antes de atualizar
        for veiculo in self.veiculos:
            placa = veiculo.get('placa', 'N/A')
            modelo = veiculo.get('modelo', 'N/A')
            ano = veiculo.get('ano', 'N/A')
            cliente = veiculo.get('cliente', 'N/A')  # Removido 'cor'
            self.listaVeiculos.addItem(f"Placa: {placa} - Modelo: {modelo} - Ano: {ano} - Cliente: {cliente}")

    def editar_veiculo(self):
        selected_item = self.listaVeiculos.currentItem()
        if selected_item:
            veiculo_info = selected_item.text()
            placa, modelo, ano, cliente = self.extract_veiculo_info(veiculo_info)  # Removido 'cor'

            dialog = QWidget()
            form = QFormLayout()
            placa_edit = QLineEdit(placa)
            modelo_edit = QLineEdit(modelo)
            ano_edit = QLineEdit(ano)
            cliente_edit = QLineEdit(cliente)  # Inclua o cliente

            form.addRow("Placa:", placa_edit)
            form.addRow("Modelo:", modelo_edit)
            form.addRow("Ano:", ano_edit)
            form.addRow("Cliente:", cliente_edit)  # Removido 'cor'

        def save():
            if placa_edit.text() and modelo_edit.text() and ano_edit.text() and cliente_edit.text():
                veiculo = {
                    'placa': placa_edit.text(),
                    'modelo': modelo_edit.text(),
                    'ano': ano_edit.text(),
                    'cliente': cliente_edit.text()  # Removido 'cor'
                }
                for i, v in enumerate(self.veiculos):
                    if v['placa'] == placa:
                        self.veiculos[i] = veiculo
                        break
                self.salvar_veiculos()
                QMessageBox.information(self, 'Sucesso', 'Veículo editado com sucesso!')
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

    def excluir_veiculo(self):
        selected_item = self.listaVeiculos.currentItem()
        if selected_item:
            veiculo_info = selected_item.text()
            placa, modelo, ano, cor, cliente = self.extract_veiculo_info(veiculo_info)

            reply = QMessageBox.question(self, 'Excluir Veículo',
                                         f"Tem certeza de que deseja excluir o veículo com placa {placa}?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.veiculos = [v for v in self.veiculos if v['placa'] != placa]
                self.salvar_veiculos()
                self.listar_veiculos()  # Atualiza a lista de veículos

    def extract_veiculo_info(self, veiculo_info):
        # Extrair informações do veículo do texto
        parts = veiculo_info.split(' - ')
        placa = parts[0].replace("Placa: ", "")
        modelo = parts[1].replace("Modelo: ", "")
        ano = parts[2].replace("Ano: ", "")
        cliente = parts[3].replace("Cliente: ", "")  # Removido 'cor'
        return placa, modelo, ano, cliente

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
            self.listaManutencoes.addItem(f"Placa: {manutencao['placa']} - Data: {manutencao['data']} - Informações: {manutencao['informacoes']} - Valor: R${manutencao['valor']} - Mecânico: {manutencao['mecanico']}")

    def editar_manutencao(self):
        selected_item = self.listaManutencoes.currentItem()
        if selected_item:
            manutencao_info = selected_item.text()
            placa, data, informacoes, valor, mecanico = self.extract_manutencao_info(manutencao_info)

            dialog = QWidget()
            form = QFormLayout()
            placa_edit = QLineEdit(placa)
            data_edit = QLineEdit(data)
            informacoes_edit = QLineEdit(informacoes)
            valor_edit = QLineEdit(valor)
            mecanico_edit = QLineEdit(mecanico)

            form.addRow("Placa do Veículo:", placa_edit)
            form.addRow("Data:", data_edit)
            form.addRow("Informações:", informacoes_edit)
            form.addRow("Valor (R$):", valor_edit)
            form.addRow("Mecânico:", mecanico_edit)

            def save():
                if placa_edit.text() and data_edit.text() and informacoes_edit.text() and valor_edit.text():
                    if not any(v['placa'] == placa_edit.text() for v in self.veiculos):
                        QMessageBox.warning(self, 'Erro', 'Placa não cadastrada! Cadastre o veículo primeiro.')
                        return

                    valor_tratado = valor_edit.text().replace('R$', '').replace(',', '').strip()
                    try:
                        valor_float = float(valor_tratado)
                    except ValueError:
                        QMessageBox.warning(self, 'Erro', 'Valor inválido! Informe um número.')
                        return

                    manutencao = {
                        'placa': placa_edit.text(),
                        'data': data_edit.text(),
                        'informacoes': informacoes_edit.text(),
                        'valor': valor_float,
                        'mecanico': mecanico_edit.text()
                    }
                    for i, m in enumerate(self.manutencoes):
                        if m['placa'] == placa and m['data'] == data:  # Assuming Placa and Data are unique together
                            self.manutencoes[i] = manutencao
                            break
                    self.salvar_manutencoes()
                    QMessageBox.information(self, 'Sucesso', 'Manutenção editada com sucesso!')
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
            placa, data, informacoes, valor, mecanico = self.extract_manutencao_info(manutencao_info)

            reply = QMessageBox.question(self, 'Excluir Manutenção',
                                         f"Tem certeza de que deseja excluir a manutenção do veículo com placa {placa} realizada em {data}?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.manutencoes = [m for m in self.manutencoes if not (m['placa'] == placa and m['data'] == data)]
                self.salvar_manutencoes()
                self.listar_manutencoes()  # Atualiza a lista de manutenções

    def extract_manutencao_info(self, manutencao_info):
        # Extrair informações da manutenção do texto
        parts = manutencao_info.split(' - ')
        placa = parts[0].replace("Placa: ", "")
        data = parts[1].replace("Data: ", "")
        informacoes = parts[2].replace("Informações: ", "")
        valor = parts[3].replace("Valor: R$", "").replace(',', '').strip()
        mecanico = parts[4].replace("Mecânico: ", "")
        return placa, data, informacoes, valor, mecanico

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VeiculosApp()
    ex.show()
    sys.exit(app.exec_())
