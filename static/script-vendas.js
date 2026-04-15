//  == Vendas ==

//listagem de Vendas
async function carregarVendas() {
    const res = await fetch("/api/vendas");
    const vendas = await res.json();
    const tbody = document.getElementById("tabela-vendas");
    tbody.innerHTML = "";
    vendas.forEach(v => {
        tbody.innerHTML += `
        <tr>
            <td>${v.id}</td>
            <td>${v.data_venda}</td>
            <td>${v.cliente}</td>
            <td>R$ ${v.preco_total.toFixed(2)}</td>
            <td>
                <button class="btn btn-outline-info btn-sm"
                    onclick="window.location.href='/vendas/acessar/${v.id}'">
                    Acessar Venda
                </button>
            </td>
        </tr>`;
    });
}

//carrega dados para efetuar a venda
async function carregarDados() {
    const [resClientes, resProdutos] = await Promise.all([
        fetch("/api/clientes"),
        fetch("/api/produtos")
    ]);
    const clientes = await resClientes.json();
    produtos = await resProdutos.json();

    const selectCliente = document.getElementById("id_cliente");
    selectCliente.innerHTML = clientes.map(c =>
        `<option value="${c.id}">${c.nome}</option>`
    ).join("");

    adicionarProduto(); // Adiciona o primeiro item
}

// gera as opções de produtos
function opcoesprodutos() {
    return produtos.map(p =>
        `<option value="${p.id}">${p.nome} - R$ ${p.preco.toFixed(2)}</option>`
    ).join("");
}

//adiciona um novo produto na venda
function adicionarProduto() {
    const container = document.getElementById("produtos-container");
    const div = document.createElement("div");
    div.classList.add("produto-item");
    div.innerHTML = `
        <label>Produto:</label>
        <select class="ipt-cadastro produto-select">${opcoesprodutos()}</select>
        <label>Quantidade:</label>
        <input type="number" class="ipt-cadastro produto-qtd" min="1" value="1" required>
        <button type="button" class="btn btn-outline-danger btn-sm" onclick="removerProduto(this)">
            Remover Produto
        </button>
    `;
    container.appendChild(div);
}

//remove produto da venda
function removerProduto(botao) {
    const container = document.getElementById("produtos-container");
    if (container.children.length > 1) {
        botao.closest(".produto-item").remove();
    } else {
        alert("A venda precisa ter pelo menos um produto.");
    }
}

//Finaliza a venda
async function finalizarVenda() {
    const id_cliente = document.getElementById("id_cliente").value;
    const selects = document.querySelectorAll(".produto-select");
    const qtds = document.querySelectorAll(".produto-qtd");

    const itens = [];
    selects.forEach((sel, i) => {
        itens.push({
            id_produto: parseInt(sel.value),
            quantidade: parseInt(qtds[i].value)
        });
    });

    const res = await fetch("/api/vendas", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ id_cliente: parseInt(id_cliente), itens })
    });

    const data = await res.json();
    if (res.ok) {
        window.location.href = `/vendas/fim/${data.id}`;
    } else {
        alert("Erro: " + data.error);
    }
}

//carrega detalhes da venda
async function carregarVenda() {
    const res = await fetch(`/api/vendas/${id}`);
    const venda = await res.json();
    const tbody = document.getElementById("tabela-venda");
    tbody.innerHTML = "";
    venda.itens.forEach(item => {
        tbody.innerHTML += `
        <tr>
            <td>${venda.id}</td>
            <td>${venda.data_venda}</td>
            <td>${venda.cliente}</td>
            <td>${item.nome_produto}</td>
            <td>${item.quantidade}</td>
            <td>R$ ${item.preco_unitario.toFixed(2)}</td>
            <td>R$ ${venda.preco_total.toFixed(2)}</td>
        </tr>`;
    });
}

//deleta a venda
async function deletar() {
    if (!confirm("Deseja excluir esta venda?")) return;

    const res = await fetch(`/api/vendas/${id}`, { method: "DELETE" });
    const data = await res.json();
    if (res.ok) {
        alert(data.message);
        window.location.href = "/vendas/lista";
    } else {
        alert("Erro ao deletar");
    }
}
