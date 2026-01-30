// ERP Basico - Cloudflare Worker com D1
// Todas as rotas da API REST do sistema ERP

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    },
  });
}

function notFound(msg = 'Recurso não encontrado') {
  return json({ error: msg }, 404);
}

function badRequest(msg) {
  return json({ error: msg }, 400);
}

// ============= CLIENTES =============
async function handleClientes(request, db, id) {
  const method = request.method;

  if (id) {
    const cliente = await db.prepare('SELECT * FROM clientes WHERE id = ?').bind(id).first();
    if (!cliente) return notFound('Cliente não encontrado');

    if (method === 'GET') {
      return json(cliente);
    }
    if (method === 'PUT') {
      const data = await request.json();
      await db.prepare(`
        UPDATE clientes SET nome=?, cpf_cnpj=?, email=?, telefone=?, endereco=?, cidade=?, estado=?, cep=?, updated_at=datetime('now')
        WHERE id=?
      `).bind(
        data.nome ?? cliente.nome, data.cpf_cnpj ?? cliente.cpf_cnpj,
        data.email ?? cliente.email, data.telefone ?? cliente.telefone,
        data.endereco ?? cliente.endereco, data.cidade ?? cliente.cidade,
        data.estado ?? cliente.estado, data.cep ?? cliente.cep, id
      ).run();
      const updated = await db.prepare('SELECT * FROM clientes WHERE id = ?').bind(id).first();
      return json(updated);
    }
    if (method === 'DELETE') {
      await db.prepare('UPDATE clientes SET ativo = 0 WHERE id = ?').bind(id).run();
      return new Response(null, { status: 204, headers: { 'Access-Control-Allow-Origin': '*' } });
    }
  }

  if (method === 'GET') {
    const { results } = await db.prepare('SELECT * FROM clientes WHERE ativo = 1').all();
    return json(results);
  }
  if (method === 'POST') {
    const data = await request.json();
    if (!data.nome || !data.cpf_cnpj) return badRequest('Nome e CPF/CNPJ são obrigatórios');
    const result = await db.prepare(`
      INSERT INTO clientes (nome, cpf_cnpj, email, telefone, endereco, cidade, estado, cep)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    `).bind(data.nome, data.cpf_cnpj, data.email || null, data.telefone || null,
      data.endereco || null, data.cidade || null, data.estado || null, data.cep || null
    ).run();
    const created = await db.prepare('SELECT * FROM clientes WHERE id = ?').bind(result.meta.last_row_id).first();
    return json(created, 201);
  }
  return notFound();
}

// ============= FORNECEDORES =============
async function handleFornecedores(request, db, id) {
  const method = request.method;

  if (id) {
    const fornecedor = await db.prepare('SELECT * FROM fornecedores WHERE id = ?').bind(id).first();
    if (!fornecedor) return notFound('Fornecedor não encontrado');

    if (method === 'GET') return json(fornecedor);
    if (method === 'PUT') {
      const data = await request.json();
      await db.prepare(`
        UPDATE fornecedores SET nome=?, cnpj=?, email=?, telefone=?, endereco=?, cidade=?, estado=?, cep=?, updated_at=datetime('now')
        WHERE id=?
      `).bind(
        data.nome ?? fornecedor.nome, data.cnpj ?? fornecedor.cnpj,
        data.email ?? fornecedor.email, data.telefone ?? fornecedor.telefone,
        data.endereco ?? fornecedor.endereco, data.cidade ?? fornecedor.cidade,
        data.estado ?? fornecedor.estado, data.cep ?? fornecedor.cep, id
      ).run();
      const updated = await db.prepare('SELECT * FROM fornecedores WHERE id = ?').bind(id).first();
      return json(updated);
    }
    if (method === 'DELETE') {
      await db.prepare('UPDATE fornecedores SET ativo = 0 WHERE id = ?').bind(id).run();
      return new Response(null, { status: 204, headers: { 'Access-Control-Allow-Origin': '*' } });
    }
  }

  if (method === 'GET') {
    const { results } = await db.prepare('SELECT * FROM fornecedores WHERE ativo = 1').all();
    return json(results);
  }
  if (method === 'POST') {
    const data = await request.json();
    if (!data.nome || !data.cnpj) return badRequest('Nome e CNPJ são obrigatórios');
    const result = await db.prepare(`
      INSERT INTO fornecedores (nome, cnpj, email, telefone, endereco, cidade, estado, cep)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    `).bind(data.nome, data.cnpj, data.email || null, data.telefone || null,
      data.endereco || null, data.cidade || null, data.estado || null, data.cep || null
    ).run();
    const created = await db.prepare('SELECT * FROM fornecedores WHERE id = ?').bind(result.meta.last_row_id).first();
    return json(created, 201);
  }
  return notFound();
}

// ============= PRODUTOS =============
async function handleProdutos(request, db, id) {
  const method = request.method;

  if (id) {
    const produto = await db.prepare('SELECT * FROM produtos WHERE id = ?').bind(id).first();
    if (!produto) return notFound('Produto não encontrado');

    if (method === 'GET') return json(produto);
    if (method === 'PUT') {
      const data = await request.json();
      await db.prepare(`
        UPDATE produtos SET codigo=?, nome=?, descricao=?, unidade=?, preco_custo=?, preco_venda=?, estoque_minimo=?, updated_at=datetime('now')
        WHERE id=?
      `).bind(
        data.codigo ?? produto.codigo, data.nome ?? produto.nome,
        data.descricao ?? produto.descricao, data.unidade ?? produto.unidade,
        data.preco_custo ?? produto.preco_custo, data.preco_venda ?? produto.preco_venda,
        data.estoque_minimo ?? produto.estoque_minimo, id
      ).run();
      const updated = await db.prepare('SELECT * FROM produtos WHERE id = ?').bind(id).first();
      return json(updated);
    }
    if (method === 'DELETE') {
      await db.prepare('UPDATE produtos SET ativo = 0 WHERE id = ?').bind(id).run();
      return new Response(null, { status: 204, headers: { 'Access-Control-Allow-Origin': '*' } });
    }
  }

  if (method === 'GET') {
    const { results } = await db.prepare('SELECT * FROM produtos WHERE ativo = 1').all();
    return json(results);
  }
  if (method === 'POST') {
    const data = await request.json();
    if (!data.codigo || !data.nome) return badRequest('Código e Nome são obrigatórios');
    const result = await db.prepare(`
      INSERT INTO produtos (codigo, nome, descricao, unidade, preco_custo, preco_venda, estoque_minimo, estoque_atual)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    `).bind(data.codigo, data.nome, data.descricao || null, data.unidade || 'UN',
      data.preco_custo || 0, data.preco_venda || 0, data.estoque_minimo || 0, data.estoque_atual || 0
    ).run();
    const created = await db.prepare('SELECT * FROM produtos WHERE id = ?').bind(result.meta.last_row_id).first();
    return json(created, 201);
  }
  return notFound();
}

// ============= ORCAMENTOS =============
async function handleOrcamentos(request, db, id) {
  const method = request.method;

  if (id) {
    const orcamento = await db.prepare(`
      SELECT o.*, c.nome as cliente_nome FROM orcamentos o
      LEFT JOIN clientes c ON o.cliente_id = c.id WHERE o.id = ?
    `).bind(id).first();
    if (!orcamento) return notFound('Orçamento não encontrado');

    if (method === 'GET') {
      const { results: itens } = await db.prepare(`
        SELECT io.*, p.nome as produto_nome FROM itens_orcamento io
        LEFT JOIN produtos p ON io.produto_id = p.id WHERE io.orcamento_id = ?
      `).bind(id).all();
      orcamento.itens = itens;
      return json(orcamento);
    }
    if (method === 'PUT') {
      const data = await request.json();
      await db.prepare(`UPDATE orcamentos SET status=?, observacoes=?, updated_at=datetime('now') WHERE id=?`)
        .bind(data.status ?? orcamento.status, data.observacoes ?? orcamento.observacoes, id).run();
      const updated = await db.prepare('SELECT * FROM orcamentos WHERE id = ?').bind(id).first();
      return json(updated);
    }
    if (method === 'DELETE') {
      await db.prepare('DELETE FROM itens_orcamento WHERE orcamento_id = ?').bind(id).run();
      await db.prepare('DELETE FROM orcamentos WHERE id = ?').bind(id).run();
      return new Response(null, { status: 204, headers: { 'Access-Control-Allow-Origin': '*' } });
    }
  }

  if (method === 'GET') {
    const { results } = await db.prepare(`
      SELECT o.*, c.nome as cliente_nome FROM orcamentos o
      LEFT JOIN clientes c ON o.cliente_id = c.id ORDER BY o.created_at DESC
    `).all();
    return json(results);
  }
  if (method === 'POST') {
    const data = await request.json();
    if (!data.numero || !data.cliente_id) return badRequest('Número e cliente são obrigatórios');

    let valor_total = 0;
    const itens = data.itens || [];

    for (const item of itens) {
      const produto = await db.prepare('SELECT * FROM produtos WHERE id = ?').bind(item.produto_id).first();
      if (!produto) return notFound(`Produto ${item.produto_id} não encontrado`);
      const preco = item.preco_unitario ?? produto.preco_venda;
      item._preco = preco;
      item._subtotal = item.quantidade * preco;
      valor_total += item._subtotal;
    }

    const result = await db.prepare(`
      INSERT INTO orcamentos (numero, cliente_id, data_validade, valor_total, observacoes, status)
      VALUES (?, ?, ?, ?, ?, ?)
    `).bind(data.numero, data.cliente_id, data.data_validade || null, valor_total,
      data.observacoes || null, data.status || 'PENDENTE'
    ).run();
    const orcamentoId = result.meta.last_row_id;

    for (const item of itens) {
      await db.prepare(`
        INSERT INTO itens_orcamento (orcamento_id, produto_id, quantidade, preco_unitario, subtotal)
        VALUES (?, ?, ?, ?, ?)
      `).bind(orcamentoId, item.produto_id, item.quantidade, item._preco, item._subtotal).run();
    }

    const created = await db.prepare(`
      SELECT o.*, c.nome as cliente_nome FROM orcamentos o
      LEFT JOIN clientes c ON o.cliente_id = c.id WHERE o.id = ?
    `).bind(orcamentoId).first();
    const { results: createdItens } = await db.prepare(`
      SELECT io.*, p.nome as produto_nome FROM itens_orcamento io
      LEFT JOIN produtos p ON io.produto_id = p.id WHERE io.orcamento_id = ?
    `).bind(orcamentoId).all();
    created.itens = createdItens;
    return json(created, 201);
  }
  return notFound();
}

// ============= PEDIDOS DE VENDA =============
async function handlePedidosVenda(request, db, id) {
  const method = request.method;

  if (id) {
    const pedido = await db.prepare(`
      SELECT p.*, c.nome as cliente_nome FROM pedidos_venda p
      LEFT JOIN clientes c ON p.cliente_id = c.id WHERE p.id = ?
    `).bind(id).first();
    if (!pedido) return notFound('Pedido não encontrado');

    if (method === 'GET') {
      const { results: itens } = await db.prepare(`
        SELECT ipv.*, pr.nome as produto_nome FROM itens_pedido_venda ipv
        LEFT JOIN produtos pr ON ipv.produto_id = pr.id WHERE ipv.pedido_id = ?
      `).bind(id).all();
      pedido.itens = itens;
      return json(pedido);
    }
    if (method === 'PUT') {
      const data = await request.json();
      await db.prepare(`UPDATE pedidos_venda SET status=?, observacoes=?, updated_at=datetime('now') WHERE id=?`)
        .bind(data.status ?? pedido.status, data.observacoes ?? pedido.observacoes, id).run();
      const updated = await db.prepare('SELECT * FROM pedidos_venda WHERE id = ?').bind(id).first();
      return json(updated);
    }
    if (method === 'DELETE') {
      await db.prepare('DELETE FROM itens_pedido_venda WHERE pedido_id = ?').bind(id).run();
      await db.prepare('DELETE FROM pedidos_venda WHERE id = ?').bind(id).run();
      return new Response(null, { status: 204, headers: { 'Access-Control-Allow-Origin': '*' } });
    }
  }

  if (method === 'GET') {
    const { results } = await db.prepare(`
      SELECT p.*, c.nome as cliente_nome FROM pedidos_venda p
      LEFT JOIN clientes c ON p.cliente_id = c.id ORDER BY p.created_at DESC
    `).all();
    return json(results);
  }
  if (method === 'POST') {
    const data = await request.json();
    if (!data.numero || !data.cliente_id) return badRequest('Número e cliente são obrigatórios');

    let valor_total = 0;
    const itens = data.itens || [];

    for (const item of itens) {
      const produto = await db.prepare('SELECT * FROM produtos WHERE id = ?').bind(item.produto_id).first();
      if (!produto) return notFound(`Produto ${item.produto_id} não encontrado`);
      const preco = item.preco_unitario ?? produto.preco_venda;
      item._preco = preco;
      item._subtotal = item.quantidade * preco;
      valor_total += item._subtotal;
    }

    const result = await db.prepare(`
      INSERT INTO pedidos_venda (numero, cliente_id, data_entrega, valor_total, observacoes, status)
      VALUES (?, ?, ?, ?, ?, ?)
    `).bind(data.numero, data.cliente_id, data.data_entrega || null, valor_total,
      data.observacoes || null, data.status || 'ABERTO'
    ).run();
    const pedidoId = result.meta.last_row_id;

    for (const item of itens) {
      await db.prepare(`
        INSERT INTO itens_pedido_venda (pedido_id, produto_id, quantidade, preco_unitario, subtotal)
        VALUES (?, ?, ?, ?, ?)
      `).bind(pedidoId, item.produto_id, item.quantidade, item._preco, item._subtotal).run();
    }

    // Criar lançamento financeiro
    await db.prepare(`
      INSERT INTO lancamentos_financeiros (tipo, descricao, valor, cliente_id, status, categoria)
      VALUES ('RECEITA', ?, ?, ?, 'PENDENTE', 'VENDAS')
    `).bind(`Pedido de Venda #${data.numero}`, valor_total, data.cliente_id).run();

    const created = await db.prepare(`
      SELECT p.*, c.nome as cliente_nome FROM pedidos_venda p
      LEFT JOIN clientes c ON p.cliente_id = c.id WHERE p.id = ?
    `).bind(pedidoId).first();
    const { results: createdItens } = await db.prepare(`
      SELECT ipv.*, pr.nome as produto_nome FROM itens_pedido_venda ipv
      LEFT JOIN produtos pr ON ipv.produto_id = pr.id WHERE ipv.pedido_id = ?
    `).bind(pedidoId).all();
    created.itens = createdItens;
    return json(created, 201);
  }
  return notFound();
}

// ============= NOTAS DE ENTRADA =============
async function handleNotasEntrada(request, db, id) {
  const method = request.method;

  if (id) {
    const nota = await db.prepare(`
      SELECT n.*, f.nome as fornecedor_nome FROM notas_entrada n
      LEFT JOIN fornecedores f ON n.fornecedor_id = f.id WHERE n.id = ?
    `).bind(id).first();
    if (!nota) return notFound('Nota de entrada não encontrada');

    if (method === 'GET') {
      const { results: itens } = await db.prepare(`
        SELECT ine.*, p.nome as produto_nome FROM itens_nota_entrada ine
        LEFT JOIN produtos p ON ine.produto_id = p.id WHERE ine.nota_id = ?
      `).bind(id).all();
      nota.itens = itens;
      return json(nota);
    }
    if (method === 'DELETE') {
      await db.prepare('DELETE FROM itens_nota_entrada WHERE nota_id = ?').bind(id).run();
      await db.prepare('DELETE FROM notas_entrada WHERE id = ?').bind(id).run();
      return new Response(null, { status: 204, headers: { 'Access-Control-Allow-Origin': '*' } });
    }
  }

  if (method === 'GET') {
    const { results } = await db.prepare(`
      SELECT n.*, f.nome as fornecedor_nome FROM notas_entrada n
      LEFT JOIN fornecedores f ON n.fornecedor_id = f.id ORDER BY n.created_at DESC
    `).all();
    return json(results);
  }
  if (method === 'POST') {
    const data = await request.json();
    if (!data.numero || !data.fornecedor_id) return badRequest('Número e fornecedor são obrigatórios');

    let valor_total = 0;
    const itens = data.itens || [];

    for (const item of itens) {
      const produto = await db.prepare('SELECT * FROM produtos WHERE id = ?').bind(item.produto_id).first();
      if (!produto) return notFound(`Produto ${item.produto_id} não encontrado`);
      const subtotal = item.quantidade * item.preco_unitario;
      item._subtotal = subtotal;
      item._produto = produto;
      valor_total += subtotal;
    }

    const result = await db.prepare(`
      INSERT INTO notas_entrada (numero, fornecedor_id, valor_total, observacoes)
      VALUES (?, ?, ?, ?)
    `).bind(data.numero, data.fornecedor_id, valor_total, data.observacoes || null).run();
    const notaId = result.meta.last_row_id;

    for (const item of itens) {
      await db.prepare(`
        INSERT INTO itens_nota_entrada (nota_id, produto_id, quantidade, preco_unitario, subtotal)
        VALUES (?, ?, ?, ?, ?)
      `).bind(notaId, item.produto_id, item.quantidade, item.preco_unitario, item._subtotal).run();

      // Atualizar estoque
      const estoque_anterior = item._produto.estoque_atual;
      const estoque_novo = estoque_anterior + item.quantidade;
      await db.prepare('UPDATE produtos SET estoque_atual = ?, preco_custo = ?, updated_at = datetime(\'now\') WHERE id = ?')
        .bind(estoque_novo, item.preco_unitario, item.produto_id).run();

      // Registrar movimento
      await db.prepare(`
        INSERT INTO movimentos_estoque (produto_id, tipo, quantidade, estoque_anterior, estoque_atual, referencia, observacoes)
        VALUES (?, 'ENTRADA', ?, ?, ?, ?, ?)
      `).bind(item.produto_id, item.quantidade, estoque_anterior, estoque_novo,
        data.numero, `Nota de Entrada #${data.numero}`).run();
    }

    // Lançamento financeiro
    await db.prepare(`
      INSERT INTO lancamentos_financeiros (tipo, descricao, valor, fornecedor_id, status, categoria)
      VALUES ('DESPESA', ?, ?, ?, 'PENDENTE', 'COMPRAS')
    `).bind(`Nota de Entrada #${data.numero}`, valor_total, data.fornecedor_id).run();

    const created = await db.prepare(`
      SELECT n.*, f.nome as fornecedor_nome FROM notas_entrada n
      LEFT JOIN fornecedores f ON n.fornecedor_id = f.id WHERE n.id = ?
    `).bind(notaId).first();
    const { results: createdItens } = await db.prepare(`
      SELECT ine.*, p.nome as produto_nome FROM itens_nota_entrada ine
      LEFT JOIN produtos p ON ine.produto_id = p.id WHERE ine.nota_id = ?
    `).bind(notaId).all();
    created.itens = createdItens;
    return json(created, 201);
  }
  return notFound();
}

// ============= NOTAS DE SAIDA =============
async function handleNotasSaida(request, db, id) {
  const method = request.method;

  if (id) {
    const nota = await db.prepare(`
      SELECT n.*, c.nome as cliente_nome FROM notas_saida n
      LEFT JOIN clientes c ON n.cliente_id = c.id WHERE n.id = ?
    `).bind(id).first();
    if (!nota) return notFound('Nota de saída não encontrada');

    if (method === 'GET') {
      const { results: itens } = await db.prepare(`
        SELECT ins.*, p.nome as produto_nome FROM itens_nota_saida ins
        LEFT JOIN produtos p ON ins.produto_id = p.id WHERE ins.nota_id = ?
      `).bind(id).all();
      nota.itens = itens;
      return json(nota);
    }
    if (method === 'DELETE') {
      await db.prepare('DELETE FROM itens_nota_saida WHERE nota_id = ?').bind(id).run();
      await db.prepare('DELETE FROM notas_saida WHERE id = ?').bind(id).run();
      return new Response(null, { status: 204, headers: { 'Access-Control-Allow-Origin': '*' } });
    }
  }

  if (method === 'GET') {
    const { results } = await db.prepare(`
      SELECT n.*, c.nome as cliente_nome FROM notas_saida n
      LEFT JOIN clientes c ON n.cliente_id = c.id ORDER BY n.created_at DESC
    `).all();
    return json(results);
  }
  if (method === 'POST') {
    const data = await request.json();
    if (!data.numero || !data.cliente_id) return badRequest('Número e cliente são obrigatórios');

    let valor_total = 0;
    const itens = data.itens || [];

    // Validar estoque antes de processar
    for (const item of itens) {
      const produto = await db.prepare('SELECT * FROM produtos WHERE id = ?').bind(item.produto_id).first();
      if (!produto) return notFound(`Produto ${item.produto_id} não encontrado`);
      if (produto.estoque_atual < item.quantidade) {
        return badRequest(`Estoque insuficiente para o produto ${produto.nome}. Disponível: ${produto.estoque_atual}`);
      }
      const preco = item.preco_unitario ?? produto.preco_venda;
      item._preco = preco;
      item._subtotal = item.quantidade * preco;
      item._produto = produto;
      valor_total += item._subtotal;
    }

    const result = await db.prepare(`
      INSERT INTO notas_saida (numero, cliente_id, pedido_venda_id, valor_total, observacoes)
      VALUES (?, ?, ?, ?, ?)
    `).bind(data.numero, data.cliente_id, data.pedido_venda_id || null, valor_total,
      data.observacoes || null).run();
    const notaId = result.meta.last_row_id;

    for (const item of itens) {
      await db.prepare(`
        INSERT INTO itens_nota_saida (nota_id, produto_id, quantidade, preco_unitario, subtotal)
        VALUES (?, ?, ?, ?, ?)
      `).bind(notaId, item.produto_id, item.quantidade, item._preco, item._subtotal).run();

      // Atualizar estoque
      const estoque_anterior = item._produto.estoque_atual;
      const estoque_novo = estoque_anterior - item.quantidade;
      await db.prepare('UPDATE produtos SET estoque_atual = ?, updated_at = datetime(\'now\') WHERE id = ?')
        .bind(estoque_novo, item.produto_id).run();

      // Registrar movimento
      await db.prepare(`
        INSERT INTO movimentos_estoque (produto_id, tipo, quantidade, estoque_anterior, estoque_atual, referencia, observacoes)
        VALUES (?, 'SAIDA', ?, ?, ?, ?, ?)
      `).bind(item.produto_id, item.quantidade, estoque_anterior, estoque_novo,
        data.numero, `Nota de Saída #${data.numero}`).run();
    }

    // Atualizar pedido de venda se vinculado
    if (data.pedido_venda_id) {
      await db.prepare("UPDATE pedidos_venda SET status = 'FATURADO', updated_at = datetime('now') WHERE id = ?")
        .bind(data.pedido_venda_id).run();
    }

    const created = await db.prepare(`
      SELECT n.*, c.nome as cliente_nome FROM notas_saida n
      LEFT JOIN clientes c ON n.cliente_id = c.id WHERE n.id = ?
    `).bind(notaId).first();
    const { results: createdItens } = await db.prepare(`
      SELECT ins.*, p.nome as produto_nome FROM itens_nota_saida ins
      LEFT JOIN produtos p ON ins.produto_id = p.id WHERE ins.nota_id = ?
    `).bind(notaId).all();
    created.itens = createdItens;
    return json(created, 201);
  }
  return notFound();
}

// ============= ESTOQUE =============
async function handleEstoque(request, db, subpath) {
  if (subpath === 'movimentos') {
    const url = new URL(request.url);
    const produto_id = url.searchParams.get('produto_id');
    let results;
    if (produto_id) {
      ({ results } = await db.prepare(`
        SELECT me.*, p.nome as produto_nome FROM movimentos_estoque me
        LEFT JOIN produtos p ON me.produto_id = p.id
        WHERE me.produto_id = ? ORDER BY me.data_movimento DESC
      `).bind(produto_id).all());
    } else {
      ({ results } = await db.prepare(`
        SELECT me.*, p.nome as produto_nome FROM movimentos_estoque me
        LEFT JOIN produtos p ON me.produto_id = p.id
        ORDER BY me.data_movimento DESC LIMIT 100
      `).all());
    }
    return json(results);
  }

  if (subpath === 'ajuste' && request.method === 'POST') {
    const data = await request.json();
    const produto = await db.prepare('SELECT * FROM produtos WHERE id = ?').bind(data.produto_id).first();
    if (!produto) return notFound('Produto não encontrado');

    const quantidade = parseFloat(data.quantidade);
    const estoque_anterior = produto.estoque_atual;

    await db.prepare('UPDATE produtos SET estoque_atual = ?, updated_at = datetime(\'now\') WHERE id = ?')
      .bind(quantidade, data.produto_id).run();

    const result = await db.prepare(`
      INSERT INTO movimentos_estoque (produto_id, tipo, quantidade, estoque_anterior, estoque_atual, observacoes)
      VALUES (?, 'AJUSTE', ?, ?, ?, ?)
    `).bind(data.produto_id, quantidade - estoque_anterior, estoque_anterior, quantidade,
      data.observacoes || 'Ajuste manual de estoque').run();

    const movimento = await db.prepare(`
      SELECT me.*, p.nome as produto_nome FROM movimentos_estoque me
      LEFT JOIN produtos p ON me.produto_id = p.id WHERE me.id = ?
    `).bind(result.meta.last_row_id).first();
    return json(movimento, 201);
  }

  // GET /api/estoque - Lista posição de estoque
  const { results } = await db.prepare('SELECT * FROM produtos WHERE ativo = 1').all();
  const estoque = results.map(p => ({
    produto_id: p.id,
    codigo: p.codigo,
    nome: p.nome,
    unidade: p.unidade,
    estoque_atual: p.estoque_atual,
    estoque_minimo: p.estoque_minimo,
    status: p.estoque_atual < p.estoque_minimo ? 'CRÍTICO' : 'OK'
  }));
  return json(estoque);
}

// ============= FINANCEIRO =============
async function handleFinanceiro(request, db, subpath, id) {
  if (subpath === 'resumo') {
    const recPend = await db.prepare("SELECT COALESCE(SUM(valor),0) as total FROM lancamentos_financeiros WHERE tipo='RECEITA' AND status='PENDENTE'").first();
    const recPago = await db.prepare("SELECT COALESCE(SUM(valor),0) as total FROM lancamentos_financeiros WHERE tipo='RECEITA' AND status='PAGO'").first();
    const desPend = await db.prepare("SELECT COALESCE(SUM(valor),0) as total FROM lancamentos_financeiros WHERE tipo='DESPESA' AND status='PENDENTE'").first();
    const desPago = await db.prepare("SELECT COALESCE(SUM(valor),0) as total FROM lancamentos_financeiros WHERE tipo='DESPESA' AND status='PAGO'").first();

    return json({
      receitas: { pendentes: recPend.total, pagas: recPago.total, total: recPend.total + recPago.total },
      despesas: { pendentes: desPend.total, pagas: desPago.total, total: desPend.total + desPago.total },
      saldo: recPago.total - desPago.total,
      saldo_previsto: (recPend.total + recPago.total) - (desPend.total + desPago.total)
    });
  }

  if (subpath === 'lancamentos') {
    if (id) {
      const lancamento = await db.prepare(`
        SELECT lf.*, c.nome as cliente_nome, f.nome as fornecedor_nome
        FROM lancamentos_financeiros lf
        LEFT JOIN clientes c ON lf.cliente_id = c.id
        LEFT JOIN fornecedores f ON lf.fornecedor_id = f.id
        WHERE lf.id = ?
      `).bind(id).first();
      if (!lancamento) return notFound('Lançamento não encontrado');

      if (request.method === 'GET') return json(lancamento);
      if (request.method === 'PUT') {
        const data = await request.json();
        let pagamento = lancamento.data_pagamento;
        if (data.status === 'PAGO' && !pagamento) {
          pagamento = new Date().toISOString();
        }
        await db.prepare(`UPDATE lancamentos_financeiros SET status=?, data_pagamento=?, updated_at=datetime('now') WHERE id=?`)
          .bind(data.status ?? lancamento.status, pagamento, id).run();
        const updated = await db.prepare('SELECT * FROM lancamentos_financeiros WHERE id = ?').bind(id).first();
        return json(updated);
      }
      if (request.method === 'DELETE') {
        await db.prepare('DELETE FROM lancamentos_financeiros WHERE id = ?').bind(id).run();
        return new Response(null, { status: 204, headers: { 'Access-Control-Allow-Origin': '*' } });
      }
    }

    if (request.method === 'GET') {
      const url = new URL(request.url);
      const tipo = url.searchParams.get('tipo');
      const status = url.searchParams.get('status');
      let query = `SELECT lf.*, c.nome as cliente_nome, f.nome as fornecedor_nome
        FROM lancamentos_financeiros lf
        LEFT JOIN clientes c ON lf.cliente_id = c.id
        LEFT JOIN fornecedores f ON lf.fornecedor_id = f.id WHERE 1=1`;
      const binds = [];
      if (tipo) { query += ' AND lf.tipo = ?'; binds.push(tipo); }
      if (status) { query += ' AND lf.status = ?'; binds.push(status); }
      query += ' ORDER BY lf.data_vencimento DESC';

      let stmt = db.prepare(query);
      if (binds.length > 0) stmt = stmt.bind(...binds);
      const { results } = await stmt.all();
      return json(results);
    }
    if (request.method === 'POST') {
      const data = await request.json();
      if (!data.tipo || !data.descricao || data.valor === undefined) {
        return badRequest('Tipo, descrição e valor são obrigatórios');
      }
      const result = await db.prepare(`
        INSERT INTO lancamentos_financeiros (tipo, descricao, valor, data_vencimento, status, categoria, cliente_id, fornecedor_id, observacoes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
      `).bind(data.tipo, data.descricao, parseFloat(data.valor), data.data_vencimento || null,
        data.status || 'PENDENTE', data.categoria || null, data.cliente_id || null,
        data.fornecedor_id || null, data.observacoes || null).run();
      const created = await db.prepare('SELECT * FROM lancamentos_financeiros WHERE id = ?').bind(result.meta.last_row_id).first();
      return json(created, 201);
    }
  }
  return notFound();
}

// ============= ROUTER PRINCIPAL =============
export default {
  async fetch(request, env) {
    // CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type',
        },
      });
    }

    const url = new URL(request.url);
    const path = url.pathname;
    const db = env.DB;

    try {
      // API Routes
      if (path.startsWith('/api/')) {
        const parts = path.replace('/api/', '').split('/').filter(Boolean);

        // /api/clientes[/id]
        if (parts[0] === 'clientes') {
          return handleClientes(request, db, parts[1] ? parseInt(parts[1]) : null);
        }

        // /api/fornecedores[/id]
        if (parts[0] === 'fornecedores') {
          return handleFornecedores(request, db, parts[1] ? parseInt(parts[1]) : null);
        }

        // /api/produtos[/id]
        if (parts[0] === 'produtos') {
          return handleProdutos(request, db, parts[1] ? parseInt(parts[1]) : null);
        }

        // /api/orcamentos[/id]
        if (parts[0] === 'orcamentos') {
          return handleOrcamentos(request, db, parts[1] ? parseInt(parts[1]) : null);
        }

        // /api/pedidos-venda[/id]
        if (parts[0] === 'pedidos-venda') {
          return handlePedidosVenda(request, db, parts[1] ? parseInt(parts[1]) : null);
        }

        // /api/notas-entrada[/id]
        if (parts[0] === 'notas-entrada') {
          return handleNotasEntrada(request, db, parts[1] ? parseInt(parts[1]) : null);
        }

        // /api/notas-saida[/id]
        if (parts[0] === 'notas-saida') {
          return handleNotasSaida(request, db, parts[1] ? parseInt(parts[1]) : null);
        }

        // /api/estoque[/movimentos|ajuste]
        if (parts[0] === 'estoque') {
          return handleEstoque(request, db, parts[1] || null);
        }

        // /api/financeiro/lancamentos[/id] | /api/financeiro/resumo
        if (parts[0] === 'financeiro') {
          return handleFinanceiro(request, db, parts[1], parts[2] ? parseInt(parts[2]) : null);
        }

        return notFound('Endpoint não encontrado');
      }

      // Serve static assets (handled by Cloudflare Workers Assets)
      return env.ASSETS.fetch(request);
    } catch (error) {
      return json({ error: error.message || 'Erro interno do servidor' }, 500);
    }
  },
};
