
import PySimpleGUI as sg
import json

class VeiculosApp:
    def __init__(self):
        self.clientes = self.carregar_clientes()
        self.veiculos = self.carregar_veiculos()
        self.manutencoes = self.carregar_manutencoes()
        self.window = None

    def carregar_clientes(self):
        try:
            with open('clientes.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def salvar_clientes(self):
        with open('clientes.json', 'w') as file:
            json.dump(self.clientes, file, indent=4)

    def adicionar_cliente(self, values):
        nome = values['nome_cliente']
        rg = values['rg_cliente']
        endereco = values['endereco_cliente']
        telefone = values['telefone_cliente']
        whatsapp = values['whatsapp_cliente']

        if nome and rg and endereco and telefone:
            cliente = {
                'nome': nome,
                'rg': rg,
                'endereco': endereco,
                'telefone': telefone,
                'whatsapp': whatsapp
            }
            self.clientes.append(cliente)
            self.salvar_clientes()
            sg.popup("Cliente adicionado com sucesso!")
            self.listar_clientes()
        else:
            sg.popup("Preencha todos os campos!")

    def buscar_clientes_por_nome(self, nome_busca):
        clientes_encontrados = [c for c in self.clientes if nome_busca.lower() in c['nome'].lower()]
        self.window['listbox_busca_clientes'].update(values=[f"Nome: {c['nome']} - RG: {c['rg']} - Endereço: {c['endereco']} - Telefone: {c['telefone']} - WhatsApp: {c['whatsapp']}" for c in clientes_encontrados])
    
    def buscar_veiculo_por_placa(self, placa_busca):
        veiculos_encontrados = [v for v in self.veiculos if placa_busca.lower() in v['placa'].lower()]
        self.window['listbox_busca_veiculos'].update(values=[f"Marca: {v['marca']} - Modelo: {v['modelo']} - Ano: {v['ano']} - Placa: {v['placa']}" for v in veiculos_encontrados])

    def buscar_manutencoes_por_data(self, data_busca):
        manutencoes_encontradas = [m for m in self.manutencoes if m['data'] == data_busca]
        self.window['listbox_busca_manutencoes'].update(values=[f"{m['data']} - {m['informacoes']} - {m['valor']}" for m in manutencoes_encontradas])
        soma_valores = sum(float(m['valor'].replace('R$', '').replace(',', '').strip()) for m in manutencoes_encontradas)
        self.window['soma_valores_busca'].update(f"R${soma_valores:.2f}")

    def buscar_manutencoes_por_mecanico(self, mecanico_busca):
        manutencoes_encontradas = [m for m in self.manutencoes if m['mecanico'].lower() == mecanico_busca.lower()]
        self.window['listbox_busca_manutencoes'].update(values=[f"Placa: {m['placa']} - Data: {m['data']} - Informações: {m['informacoes']} - Valor: {m['valor']}" for m in manutencoes_encontradas])


    def editar_cliente(self, values):
        try:
            indice = self.window['listbox_clientes'].get_indexes()[0]
            cliente = self.clientes[indice]
            novo_nome = sg.popup_get_text('Novo Nome', default_text=cliente['nome'])
            novo_rg = sg.popup_get_text('Novo RG', default_text=cliente['rg'])
            novo_endereco = sg.popup_get_text('Novo Endereço', default_text=cliente['endereco'])
            novo_telefone = sg.popup_get_text('Novo Telefone', default_text=cliente['telefone'])
            novo_whatsapp = sg.popup_get_text('Novo WhatsApp', default_text=cliente['whatsapp'])

            if novo_nome and novo_rg and novo_endereco and novo_telefone:
                cliente['nome'] = novo_nome
                cliente['rg'] = novo_rg
                cliente['endereco'] = novo_endereco
                cliente['telefone'] = novo_telefone
                cliente['whatsapp'] = novo_whatsapp
                self.salvar_clientes()
                sg.popup("Cliente editado com sucesso!")
                self.listar_clientes()
            else:
                sg.popup("Preencha todos os campos!")
        except IndexError:
            sg.popup("Selecione um cliente para editar!")

    def excluir_cliente(self, values):
        try:
            indice = self.window['listbox_clientes'].get_indexes()[0]
            cliente = self.clientes[indice]
            confirmacao = sg.popup_yes_no(f"Tem certeza que deseja excluir o cliente {cliente['nome']}?")
            if confirmacao == 'Yes':
                del self.clientes[indice]
                self.salvar_clientes()
                sg.popup("Cliente excluído com sucesso!")
                self.listar_clientes()
        except IndexError:
            sg.popup("Selecione um cliente para excluir!")

    def listar_clientes(self):
        lista_clientes = []
        for cliente in self.clientes:
            info_cliente = f"Nome: {cliente['nome']} - RG: {cliente['rg']} - Endereço: {cliente['endereco']} - Telefone: {cliente['telefone']} - WhatsApp: {cliente['whatsapp']}"
            lista_clientes.append(info_cliente)

        self.window['listbox_clientes'].update(values=lista_clientes)

    def carregar_veiculos(self):
        try:
            with open('veiculos.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def salvar_veiculos(self):
        with open('veiculos.json', 'w') as file:
            json.dump(self.veiculos, file, indent=4)

    def adicionar_veiculo(self, values):
        marca = values['marca']
        modelo = values['modelo']
        ano = values['ano']
        placa = values['placa']

        if marca and modelo and ano and placa:
            veiculo = {
                'marca': marca,
                'modelo': modelo,
                'ano': ano,
                'placa': placa
            }
            self.veiculos.append(veiculo)
            self.salvar_veiculos()
            sg.popup(f"Veículo {marca} {modelo} {ano} {placa} adicionado com sucesso!")
            self.listar_veiculos()
        else:
            sg.popup("Preencha todos os campos!")

    def editar_veiculo(self, values):
        try:
            indice = self.window['listbox_veiculos'].get_indexes()[0]
            veiculo = self.veiculos[indice]
            nova_marca = sg.popup_get_text('Nova Marca', default_text=veiculo['marca'])
            novo_modelo = sg.popup_get_text('Novo Modelo', default_text=veiculo['modelo'])
            novo_ano = sg.popup_get_text('Novo Ano', default_text=veiculo['ano'])
            nova_placa = sg.popup_get_text('Nova Placa', default_text=veiculo['placa'])

            if nova_marca and novo_modelo and novo_ano and nova_placa:
                veiculo['marca'] = nova_marca
                veiculo['modelo'] = novo_modelo
                veiculo['ano'] = novo_ano
                veiculo['placa'] = nova_placa
                self.salvar_veiculos()
                sg.popup("Veículo editado com sucesso!")
                self.listar_veiculos()
            else:
                sg.popup("Preencha todos os campos!")
        except IndexError:
            sg.popup("Selecione um veículo para editar!")

    def excluir_veiculo(self, values):
        try:
            indice = self.window['listbox_veiculos'].get_indexes()[0]
            veiculo = self.veiculos[indice]
            confirmacao = sg.popup_yes_no(f"Tem certeza que deseja excluir o veículo {veiculo['marca']} {veiculo['modelo']} {veiculo['ano']} {veiculo['placa']}?")
            if confirmacao == 'Yes':
                del self.veiculos[indice]
                self.salvar_veiculos()
                sg.popup("Veículo excluído com sucesso!")
                self.listar_veiculos()
        except IndexError:
            sg.popup("Selecione um veículo para excluir!")

    def listar_veiculos(self):
        lista_veiculos = []
        for veiculo in self.veiculos:
            info_veiculo = f"Marca: {veiculo['marca']} - Modelo: {veiculo['modelo']} - Ano: {veiculo['ano']} - Placa: {veiculo['placa']}"
            lista_veiculos.append(info_veiculo)

        self.window['listbox_veiculos'].update(values=lista_veiculos)

    def carregar_manutencoes(self):
        try:
            with open('manutencoes.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def salvar_manutencoes(self):
        with open('manutencoes.json', 'w') as file:
            json.dump(self.manutencoes, file, indent=4)

    def adicionar_manutencao(self, values):
        # Método para adicionar uma nova manutenção
        placa = values['placa_manutencao']
        data = values['data_manutencao']
        informacoes = values['informacoes_manutencao']
        valor = values['valor_manutencao']
        mecanico = values.get('mecanico_manutencao', 'Não informado')


        if placa and data and informacoes and valor:
            if not any(v['placa'] == placa for v in self.veiculos):
                sg.popup("Placa não cadastrada! Cadastre o veículo primeiro.")
                return

            valor_tratado = valor.replace('R$', '').replace(',', '').strip()
            try:
                valor_float = float(valor_tratado)
            except ValueError:
                sg.popup("Valor de manutenção inválido. Use o formato correto.")
                return

            manutencao = {
                'placa': placa,
                'data': data,
                'informacoes': informacoes,
                'valor': f"R${valor_float:.2f}",
                'mecanico': mecanico  # Adiciona o nome do mecânico ao dicionário da manutenção
            }
            self.manutencoes.append(manutencao)
            self.salvar_manutencoes()
            sg.popup("Manutenção adicionada com sucesso!")
            self.listar_manutencoes()
        else:
            sg.popup("Preencha todos os campos!")

    def listar_manutencoes(self):
        # Método para listar manutenções
        lista_manutencoes = []
        for manutencao in self.manutencoes:
            info_manutencao = f"Placa: {manutencao['placa']} - Data: {manutencao['data']} - Informações: {manutencao['informacoes']} - Valor: {manutencao['valor']} - Mecânico: {manutencao.get('mecanico', 'Não informado')}"
            lista_manutencoes.append(info_manutencao)

        # Atualização da listbox na interface gráfica
        self.window['listbox_manutencoes'].update(values=lista_manutencoes)

    def editar_manutencao(self, values):
        try:
            indice = self.window['listbox_manutencoes'].get_indexes()[0]
            manutencao = self.manutencoes[indice]
            nova_placa = sg.popup_get_text('Nova Placa', default_text=manutencao['placa'])
            nova_data = sg.popup_get_text('Nova Data', default_text=manutencao['data'])
            novas_informacoes = sg.popup_get_text('Novas Informações', default_text=manutencao['informacoes'])
            novo_valor = sg.popup_get_text('Novo Valor ', default_text=manutencao['valor'])
            novo_mecanico = sg.popup_get_text('novo mecanico', default_text=manutencao['mecanico'])
            

            if nova_placa and nova_data and novas_informacoes and novo_valor and novo_mecanico:
                manutencao['placa'] = nova_placa
                manutencao['data'] = nova_data
                manutencao['informacoes'] = novas_informacoes
                manutencao['valor'] = f"{novo_valor}"
                manutencao['mecanico'] = novo_mecanico

                self.salvar_manutencoes()
                sg.popup("Manutenção editada com sucesso!")
                self.listar_manutencoes()
            else:
                sg.popup("Preencha todos os campos!")
        except IndexError:
            sg.popup("Selecione uma manutenção para editar!")

    def listar_ordens_servico(self):
        lista_ordens_servico = []
        for oservico in self.ordens_servico:
            info_ordem_servico = f"Cliente: {oservico['cliente']} - Veículo: {oservico['veiculo']} - Data: {oservico['data']} - Descrição: {oservico['descricao']}"
            lista_ordens_servico.append(info_ordem_servico)

        self.window['listbox_ordens_servico'].update(values=lista_ordens_servico)


    def buscar_manutencoes_por_mecanico_e_placa_e_data(self, mecanico_busca, placa_busca, data_busca):
        manutencoes_encontradas = [m for m in self.manutencoes if 
                           (not mecanico_busca or mecanico_busca.lower() in m.get('mecanico', '').lower()) and
                           (not placa_busca or placa_busca.lower() in m['placa'].lower()) and
                           (not data_busca or data_busca == m['data'])]

        self.window['listbox_busca_manutencoes'].update(values=[f"Placa: {m['placa']} - Data: {m['data']} - Informações: {m['informacoes']} - Valor: {m['valor']} - Mecânico: {m.get('mecanico', 'Não informado')}" for m in manutencoes_encontradas])

        soma_valores = sum(float(m['valor'].replace('R$', '').replace(',', '').strip()) for m in manutencoes_encontradas)
        self.window['soma_valores_busca'].update(f"R${soma_valores:.2f}")



    def excluir_manutencao(self, values):
        try:
            indice = self.window['listbox_manutencoes'].get_indexes()[0]
            manutencao = self.manutencoes[indice]
            confirmacao = sg.popup_yes_no(f"Tem certeza que deseja excluir a manutenção do veículo com placa {manutencao['placa']}?")
            if confirmacao == 'Yes':
                del self.manutencoes[indice]
                self.salvar_manutencoes()
                sg.popup("Manutenção excluída com sucesso!")
                self.listar_manutencoes()
        except IndexError:
            sg.popup("Selecione uma manutenção para excluir!")


    def build_interface(self):
        sg.theme('LightGrey1')

        tab1_layout = [
            [sg.Text('Nome do Cliente'), sg.InputText(key='nome_cliente')],
            [sg.Text('RG'), sg.InputText(key='rg_cliente')],
            [sg.Text('Endereço'), sg.InputText(key='endereco_cliente')],
            [sg.Text('Telefone'), sg.InputText(key='telefone_cliente')],
            [sg.Text('WhatsApp'), sg.InputText(key='whatsapp_cliente')],
            [sg.Button('Adicionar Cliente'), sg.Button('Editar Cliente'), sg.Button('Excluir Cliente')],
            [sg.Listbox(values=[], size=(120, 10), key='listbox_clientes')],
            [sg.Button('Listar Clientes')],
            [sg.Text('Buscar por Nome'), sg.InputText(key='nome_busca'), sg.Button('Buscar Cliente por Nome')],
            [sg.Listbox(values=[], size=(120, 10), key='listbox_busca_clientes')]
]

        tab2_layout = [
            [sg.Text('Marca'), sg.InputText(key='marca')],
            [sg.Text('Modelo'), sg.InputText(key='modelo')],
            [sg.Text('Ano'), sg.InputText(key='ano')],
            [sg.Text('Placa'), sg.InputText(key='placa')],
            [sg.Button('Adicionar Veículo'), sg.Button('Editar Veículo'), sg.Button('Excluir Veículo')],
            [sg.Listbox(values=[], size=(120, 10), key='listbox_veiculos')],
            [sg.Button('Listar Veículos')],
            [sg.Text('Buscar por Placa'), sg.InputText(key='placa_busca'), sg.Button('Buscar Veículo por Placa')],
            [sg.Listbox(values=[], size=(120, 10), key='listbox_busca_veiculos')]
]
        
        tab3_layout = [
            [sg.Text('Placa do Veículo'), sg.InputText(key='placa_manutencao')],
            [sg.Text('Data'), sg.InputText(key='data_manutencao')],
            [sg.Text('Informações'), sg.InputText(key='informacoes_manutencao')],  # Ensure this key matches
            [sg.Text('Valor (R$)'), sg.InputText(key='valor_manutencao')],
            [sg.Text('Mecânico'), sg.InputText(key='mecanico_manutencao')],
            [sg.Button('Adicionar Manutenção'), sg.Button('Editar Manutenção'), sg.Button('Excluir Manutenção')],
            [sg.Listbox(values=[], size=(120, 8), key='listbox_manutencoes')],
            [sg.Button('Listar Manutenções')],
            [sg.Text('Mecânico'), sg.Input(key='buscar_manutencao_mecanico_e_placa_mecanico')],
            [sg.Text('Placa'), sg.Input(key='buscar_manutencao_mecanico_e_placa_placa')],
            [sg.Text('Data'), sg.Input(key='buscar_manutencao_mecanico_e_placa_data')],
            [sg.Button('Buscar')],
            [sg.Listbox(values=[], size=(120, 8), key='listbox_busca_manutencoes')],
            [sg.Text('Soma dos Valores Encontrados:'), sg.Text('', key='soma_valores_busca')]
        ]
        layout = [
            [sg.TabGroup([
                [sg.Tab('Clientes', tab1_layout)],
                [sg.Tab('Veículos', tab2_layout)],
                [sg.Tab('Manutenções', tab3_layout)],
            ])],
            [sg.Button('Sair')]
        ]

        self.window = sg.Window('Sistema de Oficina', layout)

    def start(self):
        while True:
            event, values = self.window.read()

            if event == sg.WINDOW_CLOSED or event == 'Sair':
                break
            elif event == 'Adicionar Cliente':
                self.adicionar_cliente(values)
            elif event == 'Editar Cliente':
                self.editar_cliente(values)
            elif event == 'Excluir Cliente':
                self.excluir_cliente(values)
            elif event == 'Listar Clientes':
                self.listar_clientes()
            elif event == 'Adicionar Veículo':
                self.adicionar_veiculo(values)
            elif event == 'Editar Veículo':
                self.editar_veiculo(values)
            elif event == 'Excluir Veículo':
                self.excluir_veiculo(values)
            elif event == 'Listar Veículos':
                self.listar_veiculos()
            elif event == 'Adicionar Manutenção':
                self.adicionar_manutencao(values)
            elif event == 'Editar Manutenção':
                self.editar_manutencao(values)
            elif event == 'Excluir Manutenção':
                self.excluir_manutencao(values)
            elif event == 'Listar Manutenções':
                self.listar_manutencoes()
            elif event == 'Buscar Manutenções por Data':
                data_busca = values['data_busca']
                self.buscar_manutencoes_por_data(data_busca)
            elif event == 'Buscar Cliente por Nome':
                nome_busca = values['nome_busca']
                self.buscar_clientes_por_nome(nome_busca)
            elif event == 'Buscar Veículo por Placa':
                placa_busca = values['placa_busca']
                self.buscar_veiculo_por_placa(placa_busca)
            elif event == 'Buscar':
                mecanico_busca = values['buscar_manutencao_mecanico_e_placa_mecanico']
                placa_busca = values['buscar_manutencao_mecanico_e_placa_placa']
                data_busca = values['buscar_manutencao_mecanico_e_placa_data']
                self.buscar_manutencoes_por_mecanico_e_placa_e_data(mecanico_busca, placa_busca, data_busca)

        self.window.close()

if __name__ == '__main__':
    app = VeiculosApp()
    app.build_interface()
    app.start()

