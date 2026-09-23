from flask import Flask, render_template, request, redirect, url_for, flash

from database import get_conexao, inicializar_banco

app = Flask(__name__)
app.secret_key = "clinica-vida-mais-chave-de-desenvolvimento"  # troque em produção

inicializar_banco()


@app.route("/")
def index():
    return render_template("index.html")


# ==========================================
# PACIENTES
# ==========================================

@app.route("/pacientes")
def pacientes_listar():
    termo = request.args.get("q", "").strip()

    conexao = get_conexao()
    cursor = conexao.cursor()

    if termo:
        cursor.execute(
            "SELECT * FROM pacientes WHERE LOWER(nome) LIKE LOWER(?) ORDER BY id",
            (f"%{termo}%",)
        )
    else:
        cursor.execute("SELECT * FROM pacientes ORDER BY id")

    pacientes = cursor.fetchall()
    conexao.close()

    return render_template("pacientes_listar.html", pacientes=pacientes, termo=termo)


@app.route("/pacientes/cadastrar", methods=["GET", "POST"])
def pacientes_cadastrar():
    valores = {"nome": "", "idade": "", "telefone": ""}

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        idade_raw = request.form.get("idade", "").strip()
        telefone = request.form.get("telefone", "").strip()

        valores = {"nome": nome, "idade": idade_raw, "telefone": telefone}

        erro = None
        idade = None

        if not nome:
            erro = "O nome não pode ficar vazio."
        elif not telefone:
            erro = "O telefone não pode ficar vazio."
        else:
            try:
                idade = int(idade_raw)
                if idade < 0:
                    erro = "A idade não pode ser negativa."
            except ValueError:
                erro = "Digite uma idade válida."

        if not erro:
            conexao = get_conexao()
            cursor = conexao.cursor()

            cursor.execute(
                "SELECT id FROM pacientes WHERE LOWER(nome) = LOWER(?)", (nome,)
            )
            if cursor.fetchone():
                erro = "Este paciente já está cadastrado."
            else:
                cursor.execute(
                    "INSERT INTO pacientes (nome, idade, telefone) VALUES (?, ?, ?)",
                    (nome, idade, telefone)
                )
                conexao.commit()

            conexao.close()

        if erro:
            flash(erro, "erro")
            return render_template("pacientes_cadastrar.html", valores=valores)

        flash("Paciente cadastrado com sucesso!", "sucesso")
        return redirect(url_for("pacientes_listar"))

    return render_template("pacientes_cadastrar.html", valores=valores)


@app.route("/pacientes/estatisticas")
def pacientes_estatisticas():
    conexao = get_conexao()
    cursor = conexao.cursor()
    cursor.execute("SELECT nome, idade FROM pacientes")
    pacientes = cursor.fetchall()
    conexao.close()

    stats = None

    if pacientes:
        total = len(pacientes)
        soma_idades = sum(p["idade"] for p in pacientes)
        media_idades = soma_idades / total
        mais_novo = min(pacientes, key=lambda p: p["idade"])
        mais_velho = max(pacientes, key=lambda p: p["idade"])

        stats = {
            "total": total,
            "media": media_idades,
            "mais_novo": mais_novo,
            "mais_velho": mais_velho,
        }

    return render_template("pacientes_estatisticas.html", stats=stats)


if __name__ == "__main__":
    app.run(debug=True)
