// == Produtos ==

//cadastro de produtos
async function cadastrar() {
    const nome = document.getElementById("nome").value;
    const preco = parseFloat(document.getElementById("preco").value);
    const quantidade = parseInt(document.getElementById("quantidade").value);

    const res = await fetch("/api/produtos", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nome, preco, quantidade })
    });

    const data = await res.json();
    if (res.ok) {
        alert("Produto cadastrado com sucesso!");
        document.getElementById("nome").value = "";
        document.getElementById("preco").value = "";
        document.getElementById("quantidade").value = "";
    } else {
        alert("Erro: " + data.error);
    }
}


//informações do produto para edição
async function carregarProduto() {
    const res = await fetch(`/api/produtos/${id}`);
    const p = await res.json();
    document.getElementById("nome").value = p.nome;
    document.getElementById("preco").value = p.preco;
    document.getElementById("quantidade").value = p.quantidade;
}

//edição de produto
async function editar() {
    const nome = document.getElementById("nome").value;
    const preco = parseFloat(document.getElementById("preco").value);
    const quantidade = parseInt(document.getElementById("quantidade").value);

    const res = await fetch(`/api/produtos/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nome, preco, quantidade })
    });

    const data = await res.json();
    if (res.ok) {
        alert("Produto atualizado!");
        window.location.href = "/produtos/lista";
    } else {
        alert("Erro: " + data.error);
    }
}

//deleção de produto
async function deletar() {

    if (!confirm("Deseja excluir este produto?")) return;

    const res = await fetch(`/api/produtos/${id}`, { method: "DELETE" });
    const data = await res.json();
    if (res.ok) {
        alert(data.message);
        window.location.href = "/produtos/lista";
    } else {
        alert("Erro ao deletar");
    }
}


//listagem de produtos
async function carregarProdutos() {
    const res = await fetch("/api/produtos");
    const produtos = await res.json();
    const tbody = document.getElementById("tabela-produtos");
    tbody.innerHTML = "";
    produtos.forEach(p => {
        tbody.innerHTML += `
        <tr>
            <td>${p.id}</td>
            <td>${p.nome}</td>
            <td>R$ ${p.preco.toFixed(2)}</td>
            <td>${p.quantidade}</td>
            <td>
                <button class="btn btn-outline-info btn-sm"
                    onclick="window.location.href='/produtos/editar/${p.id}'">
                    Editar
                </button>
            </td>
        </tr>`;
    });
}
