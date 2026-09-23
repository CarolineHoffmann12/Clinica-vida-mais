# Lista que armazenará todos os pacientes cadastrados
pacientes = []

while True:

    # MENU PRINCIPAL
    print("\n" + "=" * 40)
    print("       SISTEMA CLÍNICA VIDA+")
    print("=" * 40)
    print("1. Cadastrar paciente")
    print("2. Ver estatísticas")
    print("3. Buscar paciente")
    print("4. Listar todos os pacientes")
    print("5. Verificar atendimento")
    print("6. Sair")
    print("=" * 40)

    opcao = input("Escolha uma opção: ")

    # OPÇÃO 1 - CADASTRAR PACIENTE

    if opcao == "1":

        print("\n--- CADASTRAR PACIENTE ---")

        nome = input("Nome do paciente: ").strip()

        # Verifica se o nome foi preenchido
        if nome == "":
            print("Erro: o nome não pode ficar vazio.")
            continue

        # Verifica se o paciente já está cadastrado
        paciente_existe = False

        for paciente in pacientes:
            if paciente["nome"].lower() == nome.lower():
                paciente_existe = True
                break

        if paciente_existe:
            print("Erro: este paciente já está cadastrado.")
            continue

        # Tratamento de erro para a idade
        try:
            idade = int(input("Idade: "))

            if idade < 0:
                print("Erro: a idade não pode ser negativa.")
                continue

        except ValueError:
            print("Erro: digite uma idade válida.")
            continue

        telefone = input("Telefone: ").strip()

        if telefone == "":
            print("Erro: o telefone não pode ficar vazio.")
            continue

        # Cria um dicionário com os dados do paciente
        paciente = {
            "nome": nome,
            "idade": idade,
            "telefone": telefone
        }

        # Adiciona o dicionário à lista
        pacientes.append(paciente)

        print("\nPaciente cadastrado com sucesso!")


    # OPÇÃO 2 - VER ESTATÍSTICAS

    elif opcao == "2":

        print("\n--- ESTATÍSTICAS ---")

        if not pacientes:
            print("Nenhum paciente cadastrado.")

        else:
            total = len(pacientes)

            soma_idades = sum(
                paciente["idade"] for paciente in pacientes
            )

            media_idades = soma_idades / total

            paciente_mais_novo = min(
                pacientes,
                key=lambda paciente: paciente["idade"]
            )

            paciente_mais_velho = max(
                pacientes,
                key=lambda paciente: paciente["idade"]
            )

            print(f"Total de pacientes: {total}")

            print(
                f"Idade média dos pacientes: "
                f"{media_idades:.1f} anos"
            )

            print(
                f"Paciente mais novo: "
                f"{paciente_mais_novo['nome']} - "
                f"{paciente_mais_novo['idade']} anos"
            )

            print(
                f"Paciente mais velho: "
                f"{paciente_mais_velho['nome']} - "
                f"{paciente_mais_velho['idade']} anos"
            )

    # OPÇÃO 3 - BUSCAR PACIENTE


    elif opcao == "3":

        print("\n--- BUSCAR PACIENTE ---")

        if not pacientes:
            print("Nenhum paciente cadastrado.")

        else:
            nome_busca = input(
                "Digite o nome do paciente: "
            ).strip()

            encontrados = []

            for paciente in pacientes:

                if nome_busca.lower() in paciente["nome"].lower():
                    encontrados.append(paciente)

            if encontrados:

                print("\nPaciente(s) encontrado(s):")

                for paciente in encontrados:

                    print("-" * 30)
                    print(f"Nome: {paciente['nome']}")
                    print(f"Idade: {paciente['idade']} anos")
                    print(f"Telefone: {paciente['telefone']}")

            else:
                print("Nenhum paciente encontrado.")


    # OPÇÃO 4 - LISTAR TODOS OS PACIENTES

    elif opcao == "4":

        print("\n--- PACIENTES CADASTRADOS ---")

        if not pacientes:
            print("Nenhum paciente cadastrado.")

        else:

            for numero, paciente in enumerate(pacientes, 1):

                print("-" * 40)
                print(f"Paciente {numero}")
                print(f"Nome: {paciente['nome']}")
                print(f"Idade: {paciente['idade']} anos")
                print(f"Telefone: {paciente['telefone']}")

            print("-" * 40)
            print(f"Total: {len(pacientes)} paciente(s)")

  
    # OPÇÃO 5 - VERIFICAR ATENDIMENTO

    elif opcao == "5":
    
        print("\n--- VERIFICAR ATENDIMENTO ---")

        # Solicita o nome do paciente
        nome_busca = input("Digite o nome do paciente: ").strip()

        paciente = None

        # Procura o paciente na lista de cadastrados
        for p in pacientes:
            if p["nome"].lower() == nome_busca.lower():
                paciente = p
                break
        # Verifica se o paciente foi encontrado
        if paciente:

            emergencia = input(
                "É uma emergência? (s/n): "
            ).lower() == "s"

            agendamento = input(
                "Paciente tem agendamento? (s/n): "
            ).lower() == "s"

            documentos = input(
                "Documentos estão em dia? (s/n): "
            ).lower() == "s"

            medico_disponivel = input(
                "Há médico disponível? (s/n): "
            ).lower() == "s"

            pagamentos = input(
                "Pagamentos estão em dia? (s/n): "
            ).lower() == "s"
        else: 
            print("\nPaciente não encontrado. Cadastre-o antes de verificar o atendimento.")
            continue  # volta pro menu principal sem tentar avaliar as regras)

        
        # EMERGÊNCIA
        # Regra: C E (B OU D)

        if emergencia:

            atendimento_liberado = (
                medico_disponivel
                and (documentos or pagamentos)
            )

            if atendimento_liberado:
                print(
                    "\nAtendimento LIBERADO para emergência!"
                )

            else:
                print(
                    "\nAtendimento NEGADO para emergência!"
                )

 
        # CONSULTA NORMAL
        # Regra: (A E B E C) OU (B E C E D)

        else:

            atendimento_liberado = (
                agendamento
                and documentos
                and medico_disponivel
            ) or (
                documentos
                and medico_disponivel
                and pagamentos
            )

            if atendimento_liberado:
                print(
                    "\nAtendimento LIBERADO para consulta normal!"
                )

            else:
                print(
                    "\nAtendimento NEGADO para consulta normal!"
                )


    # OPÇÃO 6 - SAIR

    elif opcao == "6":

        print(
            "\nObrigado por utilizar o sistema Clínica Vida+!"
        )

        print("Sistema encerrado.")

        break


  
    # OPÇÃO INVÁLIDA

    else:

        print(
            "\nOpção inválida! Escolha uma opção entre 1 e 6."
        )           