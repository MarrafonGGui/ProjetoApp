function adicionarProduto() {
    const container = document.getElementById("produtos-container");

    const div = document.createElement("div");
    div.classList.add("produto-item");

    div.innerHTML = `
        <label>Produto:</label>
        <select name="id_produto[]" class="ipt-cadastro">
            ${produtos.map(p => `
                <option value="${p.id_produto}">
                    ${p.nome_produto} - R$ ${p.preco}
                </option>
            `).join("")}
        </select>

        <label>Quantidade:</label>
        <input type="number" class="ipt-cadastro" name="quantidade[]" min="1" value="1" required>

        <button type="button" class="btn btn-outline-danger btn-sm" onclick="removerProduto(this)">
            Remover Produto
        </button>
    `;

    container.appendChild(div);
}
function removerProduto(botao) {
    const container = document.getElementById("produtos-container");

    if (container.children.length > 1) {
        botao.closest(".produto-item").remove();
    } else {
        alert("A venda precisa ter pelo menos um produto.");
    }
}