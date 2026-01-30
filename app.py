import os
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from models import (
    db, Cliente, Fornecedor, Produto, Orcamento, ItemOrcamento,
    PedidoVenda, ItemPedidoVenda, NotaEntrada, ItemNotaEntrada,
    NotaSaida, ItemNotaSaida, MovimentoEstoque, LancamentoFinanceiro
)

app = Flask(__name__)
CORS(app)

# Configuração
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///erp.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Criar tabelas
with app.app_context():
    db.create_all()

# Rota principal
@app.route('/')
def index():
    return render_template('index.html')

# ============= CLIENTES =============
@app.route('/api/clientes', methods=['GET', 'POST'])
def clientes():
    if request.method == 'GET':
        clientes = Cliente.query.filter_by(ativo=True).all()
        return jsonify([c.to_dict() for c in clientes])
    
    elif request.method == 'POST':
        data = request.json
        cliente = Cliente(
            nome=data['nome'],
            cpf_cnpj=data['cpf_cnpj'],
            email=data.get('email'),
            telefone=data.get('telefone'),
            endereco=data.get('endereco'),
            cidade=data.get('cidade'),
            estado=data.get('estado'),
            cep=data.get('cep')
        )
        db.session.add(cliente)
        db.session.commit()
        return jsonify(cliente.to_dict()), 201

@app.route('/api/clientes/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def cliente(id):
    cliente = Cliente.query.get_or_404(id)
    
    if request.method == 'GET':
        return jsonify(cliente.to_dict())
    
    elif request.method == 'PUT':
        data = request.json
        cliente.nome = data.get('nome', cliente.nome)
        cliente.cpf_cnpj = data.get('cpf_cnpj', cliente.cpf_cnpj)
        cliente.email = data.get('email', cliente.email)
        cliente.telefone = data.get('telefone', cliente.telefone)
        cliente.endereco = data.get('endereco', cliente.endereco)
        cliente.cidade = data.get('cidade', cliente.cidade)
        cliente.estado = data.get('estado', cliente.estado)
        cliente.cep = data.get('cep', cliente.cep)
        cliente.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify(cliente.to_dict())
    
    elif request.method == 'DELETE':
        cliente.ativo = False
        db.session.commit()
        return '', 204

# ============= FORNECEDORES =============
@app.route('/api/fornecedores', methods=['GET', 'POST'])
def fornecedores():
    if request.method == 'GET':
        fornecedores = Fornecedor.query.filter_by(ativo=True).all()
        return jsonify([f.to_dict() for f in fornecedores])
    
    elif request.method == 'POST':
        data = request.json
        fornecedor = Fornecedor(
            nome=data['nome'],
            cnpj=data['cnpj'],
            email=data.get('email'),
            telefone=data.get('telefone'),
            endereco=data.get('endereco'),
            cidade=data.get('cidade'),
            estado=data.get('estado'),
            cep=data.get('cep')
        )
        db.session.add(fornecedor)
        db.session.commit()
        return jsonify(fornecedor.to_dict()), 201

@app.route('/api/fornecedores/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def fornecedor(id):
    fornecedor = Fornecedor.query.get_or_404(id)
    
    if request.method == 'GET':
        return jsonify(fornecedor.to_dict())
    
    elif request.method == 'PUT':
        data = request.json
        fornecedor.nome = data.get('nome', fornecedor.nome)
        fornecedor.cnpj = data.get('cnpj', fornecedor.cnpj)
        fornecedor.email = data.get('email', fornecedor.email)
        fornecedor.telefone = data.get('telefone', fornecedor.telefone)
        fornecedor.endereco = data.get('endereco', fornecedor.endereco)
        fornecedor.cidade = data.get('cidade', fornecedor.cidade)
        fornecedor.estado = data.get('estado', fornecedor.estado)
        fornecedor.cep = data.get('cep', fornecedor.cep)
        fornecedor.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify(fornecedor.to_dict())
    
    elif request.method == 'DELETE':
        fornecedor.ativo = False
        db.session.commit()
        return '', 204

# ============= PRODUTOS =============
@app.route('/api/produtos', methods=['GET', 'POST'])
def produtos():
    if request.method == 'GET':
        produtos = Produto.query.filter_by(ativo=True).all()
        return jsonify([p.to_dict() for p in produtos])
    
    elif request.method == 'POST':
        data = request.json
        produto = Produto(
            codigo=data['codigo'],
            nome=data['nome'],
            descricao=data.get('descricao'),
            unidade=data.get('unidade', 'UN'),
            preco_custo=data.get('preco_custo', 0.0),
            preco_venda=data.get('preco_venda', 0.0),
            estoque_minimo=data.get('estoque_minimo', 0.0),
            estoque_atual=data.get('estoque_atual', 0.0)
        )
        db.session.add(produto)
        db.session.commit()
        return jsonify(produto.to_dict()), 201

@app.route('/api/produtos/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def produto(id):
    produto = Produto.query.get_or_404(id)
    
    if request.method == 'GET':
        return jsonify(produto.to_dict())
    
    elif request.method == 'PUT':
        data = request.json
        produto.codigo = data.get('codigo', produto.codigo)
        produto.nome = data.get('nome', produto.nome)
        produto.descricao = data.get('descricao', produto.descricao)
        produto.unidade = data.get('unidade', produto.unidade)
        produto.preco_custo = data.get('preco_custo', produto.preco_custo)
        produto.preco_venda = data.get('preco_venda', produto.preco_venda)
        produto.estoque_minimo = data.get('estoque_minimo', produto.estoque_minimo)
        produto.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify(produto.to_dict())
    
    elif request.method == 'DELETE':
        produto.ativo = False
        db.session.commit()
        return '', 204

# ============= ORÇAMENTOS =============
@app.route('/api/orcamentos', methods=['GET', 'POST'])
def orcamentos():
    if request.method == 'GET':
        orcamentos = Orcamento.query.all()
        return jsonify([o.to_dict() for o in orcamentos])
    
    elif request.method == 'POST':
        data = request.json
        orcamento = Orcamento(
            numero=data['numero'],
            cliente_id=data['cliente_id'],
            data_validade=datetime.fromisoformat(data['data_validade']) if data.get('data_validade') else None,
            observacoes=data.get('observacoes'),
            status=data.get('status', 'PENDENTE')
        )
        
        valor_total = 0.0
        for item_data in data.get('itens', []):
            produto = Produto.query.get(item_data['produto_id'])
            if not produto:
                return jsonify({'error': 'Produto não encontrado'}), 404
            
            quantidade = float(item_data['quantidade'])
            preco_unitario = float(item_data.get('preco_unitario', produto.preco_venda))
            subtotal = quantidade * preco_unitario
            
            item = ItemOrcamento(
                produto_id=item_data['produto_id'],
                quantidade=quantidade,
                preco_unitario=preco_unitario,
                subtotal=subtotal
            )
            orcamento.itens.append(item)
            valor_total += subtotal
        
        orcamento.valor_total = valor_total
        db.session.add(orcamento)
        db.session.commit()
        return jsonify(orcamento.to_dict()), 201

@app.route('/api/orcamentos/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def orcamento(id):
    orcamento = Orcamento.query.get_or_404(id)
    
    if request.method == 'GET':
        return jsonify(orcamento.to_dict())
    
    elif request.method == 'PUT':
        data = request.json
        orcamento.status = data.get('status', orcamento.status)
        orcamento.observacoes = data.get('observacoes', orcamento.observacoes)
        orcamento.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify(orcamento.to_dict())
    
    elif request.method == 'DELETE':
        db.session.delete(orcamento)
        db.session.commit()
        return '', 204

# ============= PEDIDOS DE VENDA =============
@app.route('/api/pedidos-venda', methods=['GET', 'POST'])
def pedidos_venda():
    if request.method == 'GET':
        pedidos = PedidoVenda.query.all()
        return jsonify([p.to_dict() for p in pedidos])
    
    elif request.method == 'POST':
        data = request.json
        pedido = PedidoVenda(
            numero=data['numero'],
            cliente_id=data['cliente_id'],
            data_entrega=datetime.fromisoformat(data['data_entrega']) if data.get('data_entrega') else None,
            observacoes=data.get('observacoes'),
            status=data.get('status', 'ABERTO')
        )
        
        valor_total = 0.0
        for item_data in data.get('itens', []):
            produto = Produto.query.get(item_data['produto_id'])
            if not produto:
                return jsonify({'error': 'Produto não encontrado'}), 404
            
            quantidade = float(item_data['quantidade'])
            preco_unitario = float(item_data.get('preco_unitario', produto.preco_venda))
            subtotal = quantidade * preco_unitario
            
            item = ItemPedidoVenda(
                produto_id=item_data['produto_id'],
                quantidade=quantidade,
                preco_unitario=preco_unitario,
                subtotal=subtotal
            )
            pedido.itens.append(item)
            valor_total += subtotal
        
        pedido.valor_total = valor_total
        db.session.add(pedido)
        db.session.commit()
        
        # Criar lançamento financeiro
        lancamento = LancamentoFinanceiro(
            tipo='RECEITA',
            descricao=f'Pedido de Venda #{pedido.numero}',
            valor=valor_total,
            cliente_id=pedido.cliente_id,
            status='PENDENTE',
            categoria='VENDAS'
        )
        db.session.add(lancamento)
        db.session.commit()
        
        return jsonify(pedido.to_dict()), 201

@app.route('/api/pedidos-venda/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def pedido_venda(id):
    pedido = PedidoVenda.query.get_or_404(id)
    
    if request.method == 'GET':
        return jsonify(pedido.to_dict())
    
    elif request.method == 'PUT':
        data = request.json
        pedido.status = data.get('status', pedido.status)
        pedido.observacoes = data.get('observacoes', pedido.observacoes)
        pedido.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify(pedido.to_dict())
    
    elif request.method == 'DELETE':
        db.session.delete(pedido)
        db.session.commit()
        return '', 204

# ============= NOTAS DE ENTRADA =============
@app.route('/api/notas-entrada', methods=['GET', 'POST'])
def notas_entrada():
    if request.method == 'GET':
        notas = NotaEntrada.query.all()
        return jsonify([n.to_dict() for n in notas])
    
    elif request.method == 'POST':
        data = request.json
        nota = NotaEntrada(
            numero=data['numero'],
            fornecedor_id=data['fornecedor_id'],
            observacoes=data.get('observacoes')
        )
        
        valor_total = 0.0
        for item_data in data.get('itens', []):
            produto = Produto.query.get(item_data['produto_id'])
            if not produto:
                return jsonify({'error': 'Produto não encontrado'}), 404
            
            quantidade = float(item_data['quantidade'])
            preco_unitario = float(item_data['preco_unitario'])
            subtotal = quantidade * preco_unitario
            
            item = ItemNotaEntrada(
                produto_id=item_data['produto_id'],
                quantidade=quantidade,
                preco_unitario=preco_unitario,
                subtotal=subtotal
            )
            nota.itens.append(item)
            valor_total += subtotal
            
            # Atualizar estoque
            estoque_anterior = produto.estoque_atual
            produto.estoque_atual += quantidade
            produto.preco_custo = preco_unitario
            
            # Registrar movimento de estoque
            movimento = MovimentoEstoque(
                produto_id=produto.id,
                tipo='ENTRADA',
                quantidade=quantidade,
                estoque_anterior=estoque_anterior,
                estoque_atual=produto.estoque_atual,
                referencia=data['numero'],
                observacoes=f'Nota de Entrada #{data["numero"]}'
            )
            db.session.add(movimento)
        
        nota.valor_total = valor_total
        db.session.add(nota)
        db.session.commit()
        
        # Criar lançamento financeiro
        lancamento = LancamentoFinanceiro(
            tipo='DESPESA',
            descricao=f'Nota de Entrada #{nota.numero}',
            valor=valor_total,
            fornecedor_id=nota.fornecedor_id,
            status='PENDENTE',
            categoria='COMPRAS'
        )
        db.session.add(lancamento)
        db.session.commit()
        
        return jsonify(nota.to_dict()), 201

@app.route('/api/notas-entrada/<int:id>', methods=['GET', 'DELETE'])
def nota_entrada(id):
    nota = NotaEntrada.query.get_or_404(id)
    
    if request.method == 'GET':
        return jsonify(nota.to_dict())
    
    elif request.method == 'DELETE':
        db.session.delete(nota)
        db.session.commit()
        return '', 204

# ============= NOTAS DE SAÍDA =============
@app.route('/api/notas-saida', methods=['GET', 'POST'])
def notas_saida():
    if request.method == 'GET':
        notas = NotaSaida.query.all()
        return jsonify([n.to_dict() for n in notas])
    
    elif request.method == 'POST':
        data = request.json
        nota = NotaSaida(
            numero=data['numero'],
            cliente_id=data['cliente_id'],
            pedido_venda_id=data.get('pedido_venda_id'),
            observacoes=data.get('observacoes')
        )
        
        valor_total = 0.0
        for item_data in data.get('itens', []):
            produto = Produto.query.get(item_data['produto_id'])
            if not produto:
                return jsonify({'error': 'Produto não encontrado'}), 404
            
            quantidade = float(item_data['quantidade'])
            
            # Verificar estoque
            if produto.estoque_atual < quantidade:
                return jsonify({'error': f'Estoque insuficiente para o produto {produto.nome}'}), 400
            
            preco_unitario = float(item_data.get('preco_unitario', produto.preco_venda))
            subtotal = quantidade * preco_unitario
            
            item = ItemNotaSaida(
                produto_id=item_data['produto_id'],
                quantidade=quantidade,
                preco_unitario=preco_unitario,
                subtotal=subtotal
            )
            nota.itens.append(item)
            valor_total += subtotal
            
            # Atualizar estoque
            estoque_anterior = produto.estoque_atual
            produto.estoque_atual -= quantidade
            
            # Registrar movimento de estoque
            movimento = MovimentoEstoque(
                produto_id=produto.id,
                tipo='SAIDA',
                quantidade=quantidade,
                estoque_anterior=estoque_anterior,
                estoque_atual=produto.estoque_atual,
                referencia=data['numero'],
                observacoes=f'Nota de Saída #{data["numero"]}'
            )
            db.session.add(movimento)
        
        nota.valor_total = valor_total
        db.session.add(nota)
        
        # Atualizar status do pedido se vinculado
        if nota.pedido_venda_id:
            pedido = PedidoVenda.query.get(nota.pedido_venda_id)
            if pedido:
                pedido.status = 'FATURADO'
        
        db.session.commit()
        return jsonify(nota.to_dict()), 201

@app.route('/api/notas-saida/<int:id>', methods=['GET', 'DELETE'])
def nota_saida(id):
    nota = NotaSaida.query.get_or_404(id)
    
    if request.method == 'GET':
        return jsonify(nota.to_dict())
    
    elif request.method == 'DELETE':
        db.session.delete(nota)
        db.session.commit()
        return '', 204

# ============= ESTOQUE =============
@app.route('/api/estoque', methods=['GET'])
def estoque():
    produtos = Produto.query.filter_by(ativo=True).all()
    estoque_data = []
    for produto in produtos:
        estoque_data.append({
            'produto_id': produto.id,
            'codigo': produto.codigo,
            'nome': produto.nome,
            'unidade': produto.unidade,
            'estoque_atual': produto.estoque_atual,
            'estoque_minimo': produto.estoque_minimo,
            'status': 'CRÍTICO' if produto.estoque_atual < produto.estoque_minimo else 'OK'
        })
    return jsonify(estoque_data)

@app.route('/api/estoque/movimentos', methods=['GET'])
def movimentos_estoque():
    produto_id = request.args.get('produto_id')
    if produto_id:
        movimentos = MovimentoEstoque.query.filter_by(produto_id=produto_id).order_by(MovimentoEstoque.data_movimento.desc()).all()
    else:
        movimentos = MovimentoEstoque.query.order_by(MovimentoEstoque.data_movimento.desc()).limit(100).all()
    return jsonify([m.to_dict() for m in movimentos])

@app.route('/api/estoque/ajuste', methods=['POST'])
def ajuste_estoque():
    data = request.json
    produto = Produto.query.get_or_404(data['produto_id'])
    
    quantidade = float(data['quantidade'])
    estoque_anterior = produto.estoque_atual
    produto.estoque_atual = quantidade
    
    movimento = MovimentoEstoque(
        produto_id=produto.id,
        tipo='AJUSTE',
        quantidade=quantidade - estoque_anterior,
        estoque_anterior=estoque_anterior,
        estoque_atual=quantidade,
        observacoes=data.get('observacoes', 'Ajuste manual de estoque')
    )
    db.session.add(movimento)
    db.session.commit()
    
    return jsonify(movimento.to_dict()), 201

# ============= FINANCEIRO =============
@app.route('/api/financeiro/lancamentos', methods=['GET', 'POST'])
def lancamentos_financeiros():
    if request.method == 'GET':
        tipo = request.args.get('tipo')
        status = request.args.get('status')
        
        query = LancamentoFinanceiro.query
        if tipo:
            query = query.filter_by(tipo=tipo)
        if status:
            query = query.filter_by(status=status)
        
        lancamentos = query.order_by(LancamentoFinanceiro.data_vencimento.desc()).all()
        return jsonify([l.to_dict() for l in lancamentos])
    
    elif request.method == 'POST':
        data = request.json
        lancamento = LancamentoFinanceiro(
            tipo=data['tipo'],
            descricao=data['descricao'],
            valor=float(data['valor']),
            data_vencimento=datetime.fromisoformat(data['data_vencimento']) if data.get('data_vencimento') else None,
            status=data.get('status', 'PENDENTE'),
            categoria=data.get('categoria'),
            cliente_id=data.get('cliente_id'),
            fornecedor_id=data.get('fornecedor_id'),
            observacoes=data.get('observacoes')
        )
        db.session.add(lancamento)
        db.session.commit()
        return jsonify(lancamento.to_dict()), 201

@app.route('/api/financeiro/lancamentos/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def lancamento_financeiro(id):
    lancamento = LancamentoFinanceiro.query.get_or_404(id)
    
    if request.method == 'GET':
        return jsonify(lancamento.to_dict())
    
    elif request.method == 'PUT':
        data = request.json
        lancamento.status = data.get('status', lancamento.status)
        if data.get('status') == 'PAGO' and not lancamento.data_pagamento:
            lancamento.data_pagamento = datetime.utcnow()
        lancamento.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify(lancamento.to_dict())
    
    elif request.method == 'DELETE':
        db.session.delete(lancamento)
        db.session.commit()
        return '', 204

@app.route('/api/financeiro/resumo', methods=['GET'])
def resumo_financeiro():
    # Calcular totais
    receitas_pendentes = db.session.query(db.func.sum(LancamentoFinanceiro.valor)).filter_by(
        tipo='RECEITA', status='PENDENTE'
    ).scalar() or 0.0
    
    receitas_pagas = db.session.query(db.func.sum(LancamentoFinanceiro.valor)).filter_by(
        tipo='RECEITA', status='PAGO'
    ).scalar() or 0.0
    
    despesas_pendentes = db.session.query(db.func.sum(LancamentoFinanceiro.valor)).filter_by(
        tipo='DESPESA', status='PENDENTE'
    ).scalar() or 0.0
    
    despesas_pagas = db.session.query(db.func.sum(LancamentoFinanceiro.valor)).filter_by(
        tipo='DESPESA', status='PAGO'
    ).scalar() or 0.0
    
    return jsonify({
        'receitas': {
            'pendentes': receitas_pendentes,
            'pagas': receitas_pagas,
            'total': receitas_pendentes + receitas_pagas
        },
        'despesas': {
            'pendentes': despesas_pendentes,
            'pagas': despesas_pagas,
            'total': despesas_pendentes + despesas_pagas
        },
        'saldo': (receitas_pagas - despesas_pagas),
        'saldo_previsto': (receitas_pendentes + receitas_pagas) - (despesas_pendentes + despesas_pagas)
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
