import textwrap

# Função auxiliar para validar CPF
def validar_cpf(cpf):
    # Remove qualquer caractere que não seja dígito
    cpf = ''.join(filter(str.isdigit, cpf))
    
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    # Cálculo do primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = (soma * 10 % 11) if (soma * 10 % 11) < 10 else 0

    # Cálculo do segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = (soma * 10 % 11) if (soma * 10 % 11) < 10 else 0

    return cpf[-2:] == f'{digito1}{digito2}'

# Função auxiliar para gerar um novo número de conta
def gerar_numero_conta(contas):
    if contas:
        return max(conta['numero_conta'] for conta in contas) + 1
    return 1

# Função para exibir o menu
def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [ec]\tExcluir conta
    [eu]\tExcluir usuário
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

# Função para depositar valor
def depositar(saldo, valor, extrato):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    return saldo, extrato

# Função para sacar valor
def sacar(saldo, valor, extrato, limite, numero_saques, limite_saques):
    if valor <= 0:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        return saldo, extrato

    if valor > saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
    elif valor > limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
    elif numero_saques >= limite_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
    else:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")

    return saldo, extrato

# Função para exibir extrato
def exibir_extrato(contas):
    numero_conta = int(input("Informe o número da conta: "))
    conta = next((c for c in contas if c["numero_conta"] == numero_conta), None)

    if not conta:
        print("\n@@@ Conta não encontrada! @@@")
        return

    extrato = conta.get('extrato', 'Não foram realizadas movimentações.')
    saldo = conta.get('saldo', 0)
    
    print(f"\n================ EXTRATO ================\n{extrato}\nSaldo:\t\tR$ {saldo:.2f}\n==========================================")

# Função para criar um novo usuário
def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    
    if not validar_cpf(cpf):
        print("\n@@@ CPF inválido! @@@")
        return
    
    usuario = next((u for u in usuarios if u["cpf"] == cpf), None)

    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("=== Usuário criado com sucesso! ===")

# Função para criar uma nova conta
def criar_conta(agencia, usuarios, contas):
    cpf = input("Informe o CPF do usuário: ")

    if not validar_cpf(cpf):
        print("\n@@@ CPF inválido! @@@")
        return

    usuario = next((u for u in usuarios if u["cpf"] == cpf), None)

    if usuario:
        numero_conta = gerar_numero_conta(contas)
        contas.append({"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario, "saldo": 0, "extrato": "", "numero_saques": 0})
        print(f"\n=== Conta criada com sucesso! Número da conta: {numero_conta} ===")
    else:
        print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")


# Função para listar contas
def listar_contas(contas, usuarios):
    opcao = input("Deseja listar todas as contas ou contas de um usuário específico? (todas/usuario): ").lower()

    if opcao == 'usuario':
        cpf = input("Informe o CPF do usuário: ")
        
        if not validar_cpf(cpf):
            print("\n@@@ CPF inválido! @@@")
            return

        usuario = next((u for u in usuarios if u["cpf"] == cpf), None)

        if usuario:
            contas_usuario = [conta for conta in contas if conta['usuario'] == usuario]
            if contas_usuario:
                for conta in contas_usuario:
                    print(f"Agência: {conta['agencia']} | Conta: {conta['numero_conta']} | Titular: {conta['usuario']['nome']}")
            else:
                print("\n@@@ Usuário não possui contas. @@@")
        else:
            print("\n@@@ Usuário não encontrado! @@@")
    else:
        for conta in contas:
            print(f"Agência: {conta['agencia']} | Conta: {conta['numero_conta']} | Titular: {conta['usuario']['nome']}")

# Função para excluir conta
def excluir_conta(contas):
    numero_conta = int(input("Informe o número da conta a ser excluída: "))
    conta = next((c for c in contas if c["numero_conta"] == numero_conta), None)

    if conta:
        contas.remove(conta)
        print("\n=== Conta excluída com sucesso! ===")
    else:
        print("\n@@@ Conta não encontrada! @@@")

# Função para excluir usuário
def excluir_usuario(usuarios, contas):
    cpf = input("Informe o CPF do usuário a ser excluído: ")
    
    if not validar_cpf(cpf):
        print("\n@@@ CPF inválido! @@@")
        return

    usuario = next((u for u in usuarios if u["cpf"] == cpf), None)

    if usuario:
        contas_usuario = [c for c in contas if c["usuario"] == usuario]

        if contas_usuario:
            print("\n@@@ O usuário possui contas ativas. Exclua as contas primeiro! @@@")
        else:
            usuarios.remove(usuario)
            print("\n=== Usuário excluído com sucesso! ===")
    else:
        print("\n@@@ Usuário não encontrado! @@@")

# Função principal
def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            numero_conta = int(input("Informe o número da conta: "))
            conta = next((c for c in contas if c["numero_conta"] == numero_conta), None)

            if conta:
                valor = float(input("Informe o valor do depósito: "))
                conta['saldo'], conta['extrato'] = depositar(conta['saldo'], valor, conta['extrato'])
            else:
                print("\n@@@ Conta não encontrada! @@@")

        elif opcao == "s":
            numero_conta = int(input("Informe o número da conta: "))
            conta = next((c for c in contas if c["numero_conta"] == numero_conta), None)

            if conta:
                valor = float(input("Informe o valor do saque: "))
                conta['saldo'], conta['extrato'] = sacar(
                    saldo=conta['saldo'],
                    valor=valor,
                    extrato=conta['extrato'],
                    limite=500,
                    numero_saques=conta['numero_saques'],
                    limite_saques=LIMITE_SAQUES,
                )
            else:
                print("\n@@@ Conta não encontrada! @@@")

        elif opcao == "e":
            exibir_extrato(contas)

        elif opcao == "nc":
            criar_conta(AGENCIA, usuarios, contas)

        elif opcao == "lc":
            listar_contas(contas, usuarios)

        elif opcao == "ec":
            excluir_conta(contas)

        elif opcao == "eu":
            excluir_usuario(usuarios, contas)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()
