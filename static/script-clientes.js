
//== Clientes ==

// cadastro de clientes
async function cadastrar() {
    const cpf = document.getElementById("cpf").value;
    const nome = document.getElementById("nome").value;
    const email = document.getElementById("email").value;

    const res = await fetch("/api/clientes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ cpf, nome, email })
    });

    const data = await res.json();
    if (res.ok) {
        alert("Cliente cadastrado com sucesso!");
        document.getElementById("cpf").value = "";
        document.getElementById("nome").value = "";
        document.getElementById("email").value = "";
    } else {
        alert("Erro: " + data.error);
    }
}

//listagem de clientes
async function carregarClientes() {
    const res = await fetch("/api/clientes");
    const clientes = await res.json();
    const tbody = document.getElementById("tabela-clientes");
    tbody.innerHTML = "";
    clientes.forEach(c => {
        tbody.innerHTML += `
        <tr>
            <td>${c.id}</td>
            <td>${c.nome}</td>
            <td>${c.email}</td>
            <td>
                <button class="btn btn-outline-primary btn-sm" onclick="window.location.href='/cliente/editar/${c.id}'">
                    Editar
                </button>
            </td>
        </tr>`;
    });
}

//informações do cliente para edição
async function carregarCliente() {
    const res = await fetch(`/api/clientes/${id}`);
    const c = await res.json();
    document.getElementById("display-id").textContent = c.id;
    document.getElementById("display-cpf").textContent = c.cpf;
    document.getElementById("nome").value = c.nome;
    document.getElementById("email").value = c.email;
}

//edição de cliente
async function editar() {
    const nome = document.getElementById("nome").value;
    const email = document.getElementById("email").value;

    const res = await fetch(`/api/clientes/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nome, email })
    });

    const data = await res.json();
    if (res.ok) {
        alert("Cliente atualizado!");
        window.location.href = "/cliente/lista";
    } else {
        alert("Erro: " + data.error);
    }
}

//deleção de cliente
async function deletar() {
    if (!confirm("Deseja excluir este cliente?")) return;

    const res = await fetch(`/api/clientes/${id}`, { method: "DELETE" });
    const data = await res.json();
    if (res.ok) {
        alert(data.message);
        window.location.href = "/cliente/lista";
    } else {
        alert("Erro ao deletar");
    }
}