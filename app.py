import sqlite3

# CONEXÃO COM O BANCO DE DADOS

# Conecta (ou cria, se não existir) o arquivo clinica.db
conexao = sqlite3.connect("clinica.db")
cursor = conexao.cursor()

# Cria a tabela de pacientes, caso ainda não exista
cursor.execute("""
    CREATE TABLE IF NOT EXISTS pacientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        idade INTEGER NOT NULL,
        telefone TEXT NOT NULL
    )
""")

# Cria a tabela de médicos, caso ainda não exista
cursor.execute("""
    CREATE TABLE IF NOT EXISTS medicos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        especialidade TEXT NOT NULL,
        crm TEXT NOT NULL UNIQUE
    )
""")

conexao.commit()

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
    print("6. Cadastrar médico")
    print("7. Listar médicos")
    print("8. Sair")
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

        # Verifica se o paciente já está cadastrado (comparação sem diferenciar maiúsculas/minúsculas)
        cursor.execute(
            "SELECT id FROM pacientes WHERE LOWER(nome) = LOWER(?)",
            (nome,)
        )
        paciente_existe = cursor.fetchone()

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

        # Insere o paciente no banco de dados
        cursor.execute(
            "INSERT INTO pacientes (nome, idade, telefone) VALUES (?, ?, ?)",
            (nome, idade, telefone)
        )
        conexao.commit()

        print("\nPaciente cadastrado com sucesso!")

    # OPÇÃO 2 - VER ESTATÍSTICAS
 
    elif opcao == "2":

        print("\n--- ESTATÍSTICAS ---")

        cursor.execute("SELECT nome, idade FROM pacientes")
        pacientes = cursor.fetchall()

        if not pacientes:
            print("Nenhum paciente cadastrado.")

        else:
            total = len(pacientes)

            soma_idades = sum(idade for nome, idade in pacientes)
            media_idades = soma_idades / total

            paciente_mais_novo = min(pacientes, key=lambda p: p[1])
            paciente_mais_velho = max(pacientes, key=lambda p: p[1])

            print(f"Total de pacientes: {total}")

            print(
                f"Idade média dos pacientes: "
                f"{media_idades:.1f} anos"
            )

            print(
                f"Paciente mais novo: "
                f"{paciente_mais_novo[0]} - "
                f"{paciente_mais_novo[1]} anos"
            )

            print(
                f"Paciente mais velho: "
                f"{paciente_mais_velho[0]} - "
                f"{paciente_mais_velho[1]} anos"
            )

    # OPÇÃO 3 - BUSCAR PACIENTE

    elif opcao == "3":

        print("\n--- BUSCAR PACIENTE ---")

        cursor.execute("SELECT COUNT(*) FROM pacientes")
        total_pacientes = cursor.fetchone()[0]

        if total_pacientes == 0:
            print("Nenhum paciente cadastrado.")

        else:
            nome_busca = input(
                "Digite o nome do paciente: "
            ).strip()

            cursor.execute(
                "SELECT nome, idade, telefone FROM pacientes "
                "WHERE LOWER(nome) LIKE LOWER(?)",
                (f"%{nome_busca}%",)
            )
            encontrados = cursor.fetchall()

            if encontrados:

                print("\nPaciente(s) encontrado(s):")

                for nome, idade, telefone in encontrados:

                    print("-" * 30)
                    print(f"Nome: {nome}")
                    print(f"Idade: {idade} anos")
                    print(f"Telefone: {telefone}")

            else:
                print("Nenhum paciente encontrado.")


    # OPÇÃO 4 - LISTAR TODOS OS PACIENTES


    elif opcao == "4":

        print("\n--- PACIENTES CADASTRADOS ---")

        cursor.execute("SELECT nome, idade, telefone FROM pacientes ORDER BY id")
        pacientes = cursor.fetchall()

        if not pacientes:
            print("Nenhum paciente cadastrado.")

        else:

            for numero, (nome, idade, telefone) in enumerate(pacientes, 1):

                print("-" * 40)
                print(f"Paciente {numero}")
                print(f"Nome: {nome}")
                print(f"Idade: {idade} anos")
                print(f"Telefone: {telefone}")

            print("-" * 40)
            print(f"Total: {len(pacientes)} paciente(s)")


    # OPÇÃO 5 - VERIFICAR ATENDIMENTO
                
    elif opcao == "5":

        print("\n--- VERIFICAR ATENDIMENTO ---")

        # Solicita o nome do paciente
        nome_busca = input("Digite o nome do paciente: ").strip()

        # Procura o paciente no banco de dados
        cursor.execute(
            "SELECT nome FROM pacientes WHERE LOWER(nome) = LOWER(?)",
            (nome_busca,)
        )
        paciente = cursor.fetchone()

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
            continue


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


    # OPÇÃO 6 - CADASTRAR MÉDICO
   
    elif opcao == "6":

        print("\n--- CADASTRAR MÉDICO ---")

        nome = input("Nome do médico: ").strip()

        if nome == "":
            print("Erro: o nome não pode ficar vazio.")
            continue

        especialidade = input("Especialidade: ").strip()

        if especialidade == "":
            print("Erro: a especialidade não pode ficar vazia.")
            continue

        crm = input("CRM: ").strip()

        if crm == "":
            print("Erro: o CRM não pode ficar vazio.")
            continue

        # Verifica se já existe médico com esse CRM
        cursor.execute(
            "SELECT id FROM medicos WHERE LOWER(crm) = LOWER(?)",
            (crm,)
        )
        medico_existe = cursor.fetchone()

        if medico_existe:
            print("Erro: já existe um médico cadastrado com esse CRM.")
            continue

        cursor.execute(
            "INSERT INTO medicos (nome, especialidade, crm) VALUES (?, ?, ?)",
            (nome, especialidade, crm)
        )
        conexao.commit()

        print("\nMédico cadastrado com sucesso!")


    # OPÇÃO 7 - LISTAR MÉDICOS
 

    elif opcao == "7":

        print("\n--- MÉDICOS CADASTRADOS ---")

        cursor.execute("SELECT nome, especialidade, crm FROM medicos ORDER BY id")
        medicos = cursor.fetchall()

        if not medicos:
            print("Nenhum médico cadastrado.")

        else:

            for numero, (nome, especialidade, crm) in enumerate(medicos, 1):

                print("-" * 40)
                print(f"Médico {numero}")
                print(f"Nome: {nome}")
                print(f"Especialidade: {especialidade}")
                print(f"CRM: {crm}")

            print("-" * 40)
            print(f"Total: {len(medicos)} médico(s)")

  
    # OPÇÃO 8 - SAIR


    elif opcao == "8":

        print(
            "\nObrigado por utilizar o sistema Clínica Vida+!"
        )

        print("Sistema encerrado.")

        conexao.close()
        break

    # OPÇÃO INVÁLIDA

    else:

        print(
            "\nOpção inválida! Escolha uma opção entre 1 e 8."
        )
