import json

class VeiculosApp:
    def __init__(self):
        self.clientes = self.carregar_clientes()
        self.veiculos = self.carregar_veiculos()
        self.manutencoes = self.carregar_manutencoes()

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
        nome = input("Nome do Cliente: ")
        rg = input("RG: ")
        endereco = input("Endereço: ")
        telefone = input("Telefone: ")
        whatsapp = input("WhatsApp: ")

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
            print("Cliente adicionado com sucesso!")
            self.listar_clientes()
        else:
            print("Preencha todos os campos!")

    def buscar_clientes_por_nome(self, nome_busca):
        clientes_encontrados = [c for c in self.clientes if nome_busca.lower() in c['nome'].lower()]
        for cliente in clientes_encontrados:
            print(f"Nome: {cliente['nome']} - RG: {cliente['rg']} - Endereço: {cliente['endereco']} - Telefone: {cliente['telefone']} - WhatsApp: {cliente['whatsapp']}")

    def editar_cliente(self):
        self.listar_clientes()
        indice = int(input("Selecione o índice do cliente para editar: "))
        cliente = self.clientes[indice]
        novo_nome = input(f'Novo Nome [{cliente["nome"]}]: ') or cliente['nome']
        novo_rg = input(f'Novo RG [{cliente["rg"]}]: ') or cliente['rg']
        novo_endereco = input(f'Novo Endereço [{cliente["endereco"]}]: ') or cliente['endereco']
        novo_telefone = input(f'Novo Telefone [{cliente["telefone"]}]: ') or cliente['telefone']
        novo_whatsapp = input(f'Novo WhatsApp [{cliente["whatsapp"]}]: ') or cliente['whatsapp']

        if novo_nome and novo_rg and novo_endereco and novo_telefone:
            cliente['nome'] = novo_nome
            cliente['rg'] = novo_rg
            cliente['endereco'] = novo_endereco
            cliente['telefone'] = novo_telefone
            cliente['whatsapp'] = novo_whatsapp
            self.salvar_clientes()
            print("Cliente editado com sucesso!")
            self.listar_clientes()
        else:
            print("Preencha todos os campos!")

    def excluir_cliente(self):
        self.listar_clientes()
        indice = int(input("Selecione o índice do cliente para excluir: "))
        cliente = self.clientes.pop(indice)
        self.salvar_clientes()
        print(f"Cliente {cliente['nome']} excluído com sucesso!")
        self.listar_clientes()

    def listar_clientes(self):
        for i, cliente in enumerate(self.clientes):
            print(f"{i}: Nome: {cliente['nome']} - RG: {cliente['rg']} - Endereço: {cliente['endereco']} - Telefone: {cliente['telefone']} - WhatsApp: {cliente['whatsapp']}")

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
        marca = input("Marca: ")
        modelo = input("Modelo: ")
        ano = input("Ano: ")
        placa = input("Placa: ")

        if marca and modelo and ano and placa:
            veiculo = {
                'marca': marca,
                'modelo': modelo,
                'ano': ano,
                'placa': placa
            }
            self.veiculos.append(veiculo)
            self.salvar_veiculos()
            print(f"Veículo {marca} {modelo} {ano} {placa} adicionado com sucesso!")
            self.listar_veiculos()
        else:
            print("Preencha todos os campos!")

    def editar_veiculo(self):
        self.listar_veiculos()
        indice = int(input("Selecione o índice do veículo para editar: "))
        veiculo = self.veiculos[indice]
        nova_marca = input(f'Nova Marca [{veiculo["marca"]}]: ') or veiculo['marca']
        novo_modelo = input(f'Novo Modelo [{veiculo["modelo"]}]: ') or veiculo['modelo']
        novo_ano = input(f'Novo Ano [{veiculo["ano"]}]: ') or veiculo['ano']
        nova_placa = input(f'Nova Placa [{veiculo["placa"]}]: ') or veiculo['placa']

        if nova_marca and novo_modelo and novo_ano and nova_placa:
            veiculo['marca'] = nova_marca
            veiculo['modelo'] = novo_modelo
            veiculo['ano'] = novo_ano
            veiculo['placa'] = nova_placa
            self.salvar_veiculos()
            print("Veículo editado com sucesso!")
            self.listar_veiculos()
        else:
            print("Preencha todos os campos!")

    def excluir_veiculo(self):
        self.listar_veiculos()
        indice = int(input("Selecione o índice do veículo para excluir: "))
        veiculo = self.veiculos.pop(indice)
        self.salvar_veiculos()
        print(f"Veículo {veiculo['marca']} {veiculo['modelo']} {veiculo['ano']} {veiculo['placa']} excluído com sucesso!")
        self.listar_veiculos()

    def listar_veiculos(self):
        for i, veiculo in enumerate(self.veiculos):
            print(f"{i}: Marca: {veiculo['marca']} - Modelo: {veiculo['modelo']} - Ano: {veiculo['ano']} - Placa: {veiculo['placa']}")

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
        placa = input("Placa do Veículo: ")
        data = input("Data: ")
        informacoes = input("Informações: ")
        valor = input("Valor (R$): ")
        mecanico = input("Mecânico: ")

        if placa and data and informacoes and valor:
            if not any(v['placa'] == placa for v in self.veiculos):
                print("Placa não cadastrada! Cadastre o veículo primeiro.")
                return

            valor_tratado = valor.replace('R$', '').replace(',', '').strip()
            try:
                valor_float = float(valor_tratado)
            except ValueError:
                print("Valor de manutenção inválido. Use o formato correto.")
                return

            manutencao = {
                'placa': placa,
                'data': data,
                'informacoes': informacoes,
                'valor': f"R${valor_float:.2f}",
                'mecanico': mecanico
            }
            self.manutencoes.append(manutencao)
            self.salvar_manutencoes()
            print("Manutenção adicionada com sucesso!")
            self.listar_manutencoes()
        else:
            print("Preencha todos os campos!")

    def editar_manutencao(self):
        self.listar_manutencoes()
        indice = int(input("Selecione o índice da manutenção para editar: "))
        manutencao = self.manutencoes[indice]
        nova_placa = input(f'Nova Placa [{manutencao["placa"]}]: ') or manutencao['placa']
        nova_data = input(f'Nova Data [{manutencao["data"]}]: ') or manutencao['data']
        novas_informacoes = input(f'Novas Informações [{manutencao["informacoes"]}]: ') or manutencao['informacoes']
        novo_valor = input(f'Novo Valor [{manutencao["valor"]}]: ') or manutencao['valor']
        novo_mecanico = input(f'Novo Mecânico [{manutencao["mecanico"]}]: ') or manutencao['mecanico']

        if nova_placa and nova_data and novas_informacoes and novo_valor:
            manutencao['placa'] = nova_placa
            manutencao['data'] = nova_data
            manutencao['informacoes'] = novas_informacoes
            manutencao['valor'] = novo_valor
            manutencao['mecanico'] = novo_mecanico
            self.salvar_manutencoes()
            print("Manutenção editada com sucesso!")
            self.listar_manutencoes()
        else:
            print("Preencha todos os campos!")

    def excluir_manutencao(self):
        self.listar_manutencoes()
        indice = int(input("Selecione o índice da manutenção para excluir: "))
        manutencao = self.manutencoes.pop(indice)
        self.salvar_manutencoes()
        print(f"Manutenção da placa {manutencao['placa']} excluída com sucesso!")
        self.listar_manutencoes()

    def listar_manutencoes(self):
        for i, manutencao in enumerate(self.manutencoes):
            print(f"{i}: Placa: {manutencao['placa']} - Data: {manutencao['data']} - Informações: {manutencao['informacoes']} - Valor: {manutencao['valor']} - Mecânico: {manutencao['mecanico']}")

    def menu_principal(self):
        while True:
            print("1. Adicionar Cliente")
            print("2. Listar Clientes")
            print("3. Editar Cliente")
            print("4. Excluir Cliente")
            print("5. Adicionar Veículo")
            print("6. Listar Veículos")
            print("7. Editar Veículo")
            print("8. Excluir Veículo")
            print("9. Adicionar Manutenção")
            print("10. Listar Manutenções")
            print("11. Editar Manutenção")
            print("12. Excluir Manutenção")
            print("0. Sair")
            escolha = input("Escolha uma opção: ")

            if escolha == '1':
                self.adicionar_cliente()
            elif escolha == '2':
                self.listar_clientes()
            elif escolha == '3':
                self.editar_cliente()
            elif escolha == '4':
                self.excluir_cliente()
            elif escolha == '5':
                self.adicionar_veiculo()
            elif escolha == '6':
                self.listar_veiculos()
            elif escolha == '7':
                self.editar_veiculo()
            elif escolha == '8':
                self.excluir_veiculo()
            elif escolha == '9':
                self.adicionar_manutencao()
            elif escolha == '10':
                self.listar_manutencoes()
            elif escolha == '11':
                self.editar_manutencao()
            elif escolha == '12':
                self.excluir_manutencao()
            elif escolha == '0':
                break
            else:
                print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    app = VeiculosApp()
    app.menu_principal()
