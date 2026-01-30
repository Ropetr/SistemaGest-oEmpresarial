from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Clientes
class Cliente(db.Model):
    __tablename__ = 'clientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf_cnpj = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.String(200))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(2))
    cep = db.Column(db.String(10))
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    orcamentos = db.relationship('Orcamento', backref='cliente', lazy=True)
    pedidos = db.relationship('PedidoVenda', backref='cliente', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cpf_cnpj': self.cpf_cnpj,
            'email': self.email,
            'telefone': self.telefone,
            'endereco': self.endereco,
            'cidade': self.cidade,
            'estado': self.estado,
            'cep': self.cep,
            'ativo': self.ativo,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

# Fornecedores
class Fornecedor(db.Model):
    __tablename__ = 'fornecedores'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.String(200))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(2))
    cep = db.Column(db.String(10))
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    notas_entrada = db.relationship('NotaEntrada', backref='fornecedor', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cnpj': self.cnpj,
            'email': self.email,
            'telefone': self.telefone,
            'endereco': self.endereco,
            'cidade': self.cidade,
            'estado': self.estado,
            'cep': self.cep,
            'ativo': self.ativo,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

# Produtos
class Produto(db.Model):
    __tablename__ = 'produtos'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    unidade = db.Column(db.String(10), default='UN')
    preco_custo = db.Column(db.Float, default=0.0)
    preco_venda = db.Column(db.Float, default=0.0)
    estoque_minimo = db.Column(db.Float, default=0.0)
    estoque_atual = db.Column(db.Float, default=0.0)
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    movimentos_estoque = db.relationship('MovimentoEstoque', backref='produto', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'nome': self.nome,
            'descricao': self.descricao,
            'unidade': self.unidade,
            'preco_custo': self.preco_custo,
            'preco_venda': self.preco_venda,
            'estoque_minimo': self.estoque_minimo,
            'estoque_atual': self.estoque_atual,
            'ativo': self.ativo,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

# Orçamentos
class Orcamento(db.Model):
    __tablename__ = 'orcamentos'
    
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(50), unique=True, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    data_orcamento = db.Column(db.DateTime, default=datetime.utcnow)
    data_validade = db.Column(db.DateTime)
    valor_total = db.Column(db.Float, default=0.0)
    observacoes = db.Column(db.Text)
    status = db.Column(db.String(20), default='PENDENTE')  # PENDENTE, APROVADO, REJEITADO
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    itens = db.relationship('ItemOrcamento', backref='orcamento', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'numero': self.numero,
            'cliente_id': self.cliente_id,
            'cliente_nome': self.cliente.nome if self.cliente else None,
            'data_orcamento': self.data_orcamento.isoformat() if self.data_orcamento else None,
            'data_validade': self.data_validade.isoformat() if self.data_validade else None,
            'valor_total': self.valor_total,
            'observacoes': self.observacoes,
            'status': self.status,
            'itens': [item.to_dict() for item in self.itens],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class ItemOrcamento(db.Model):
    __tablename__ = 'itens_orcamento'
    
    id = db.Column(db.Integer, primary_key=True)
    orcamento_id = db.Column(db.Integer, db.ForeignKey('orcamentos.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Float, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    
    produto = db.relationship('Produto')
    
    def to_dict(self):
        return {
            'id': self.id,
            'produto_id': self.produto_id,
            'produto_nome': self.produto.nome if self.produto else None,
            'quantidade': self.quantidade,
            'preco_unitario': self.preco_unitario,
            'subtotal': self.subtotal
        }

# Pedidos de Venda
class PedidoVenda(db.Model):
    __tablename__ = 'pedidos_venda'
    
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(50), unique=True, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    data_pedido = db.Column(db.DateTime, default=datetime.utcnow)
    data_entrega = db.Column(db.DateTime)
    valor_total = db.Column(db.Float, default=0.0)
    observacoes = db.Column(db.Text)
    status = db.Column(db.String(20), default='ABERTO')  # ABERTO, FATURADO, CANCELADO
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    itens = db.relationship('ItemPedidoVenda', backref='pedido', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'numero': self.numero,
            'cliente_id': self.cliente_id,
            'cliente_nome': self.cliente.nome if self.cliente else None,
            'data_pedido': self.data_pedido.isoformat() if self.data_pedido else None,
            'data_entrega': self.data_entrega.isoformat() if self.data_entrega else None,
            'valor_total': self.valor_total,
            'observacoes': self.observacoes,
            'status': self.status,
            'itens': [item.to_dict() for item in self.itens],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class ItemPedidoVenda(db.Model):
    __tablename__ = 'itens_pedido_venda'
    
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos_venda.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Float, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    
    produto = db.relationship('Produto')
    
    def to_dict(self):
        return {
            'id': self.id,
            'produto_id': self.produto_id,
            'produto_nome': self.produto.nome if self.produto else None,
            'quantidade': self.quantidade,
            'preco_unitario': self.preco_unitario,
            'subtotal': self.subtotal
        }

# Notas de Entrada
class NotaEntrada(db.Model):
    __tablename__ = 'notas_entrada'
    
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(50), unique=True, nullable=False)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedores.id'), nullable=False)
    data_entrada = db.Column(db.DateTime, default=datetime.utcnow)
    valor_total = db.Column(db.Float, default=0.0)
    observacoes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    itens = db.relationship('ItemNotaEntrada', backref='nota', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'numero': self.numero,
            'fornecedor_id': self.fornecedor_id,
            'fornecedor_nome': self.fornecedor.nome if self.fornecedor else None,
            'data_entrada': self.data_entrada.isoformat() if self.data_entrada else None,
            'valor_total': self.valor_total,
            'observacoes': self.observacoes,
            'itens': [item.to_dict() for item in self.itens],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class ItemNotaEntrada(db.Model):
    __tablename__ = 'itens_nota_entrada'
    
    id = db.Column(db.Integer, primary_key=True)
    nota_id = db.Column(db.Integer, db.ForeignKey('notas_entrada.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Float, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    
    produto = db.relationship('Produto')
    
    def to_dict(self):
        return {
            'id': self.id,
            'produto_id': self.produto_id,
            'produto_nome': self.produto.nome if self.produto else None,
            'quantidade': self.quantidade,
            'preco_unitario': self.preco_unitario,
            'subtotal': self.subtotal
        }

# Notas de Saída
class NotaSaida(db.Model):
    __tablename__ = 'notas_saida'
    
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(50), unique=True, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    pedido_venda_id = db.Column(db.Integer, db.ForeignKey('pedidos_venda.id'))
    data_saida = db.Column(db.DateTime, default=datetime.utcnow)
    valor_total = db.Column(db.Float, default=0.0)
    observacoes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    cliente = db.relationship('Cliente')
    itens = db.relationship('ItemNotaSaida', backref='nota', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'numero': self.numero,
            'cliente_id': self.cliente_id,
            'cliente_nome': self.cliente.nome if self.cliente else None,
            'pedido_venda_id': self.pedido_venda_id,
            'data_saida': self.data_saida.isoformat() if self.data_saida else None,
            'valor_total': self.valor_total,
            'observacoes': self.observacoes,
            'itens': [item.to_dict() for item in self.itens],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class ItemNotaSaida(db.Model):
    __tablename__ = 'itens_nota_saida'
    
    id = db.Column(db.Integer, primary_key=True)
    nota_id = db.Column(db.Integer, db.ForeignKey('notas_saida.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Float, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    
    produto = db.relationship('Produto')
    
    def to_dict(self):
        return {
            'id': self.id,
            'produto_id': self.produto_id,
            'produto_nome': self.produto.nome if self.produto else None,
            'quantidade': self.quantidade,
            'preco_unitario': self.preco_unitario,
            'subtotal': self.subtotal
        }

# Movimentos de Estoque
class MovimentoEstoque(db.Model):
    __tablename__ = 'movimentos_estoque'
    
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # ENTRADA, SAIDA, AJUSTE
    quantidade = db.Column(db.Float, nullable=False)
    estoque_anterior = db.Column(db.Float, nullable=False)
    estoque_atual = db.Column(db.Float, nullable=False)
    referencia = db.Column(db.String(100))  # Número da nota ou pedido
    observacoes = db.Column(db.Text)
    data_movimento = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'produto_id': self.produto_id,
            'produto_nome': self.produto.nome if self.produto else None,
            'tipo': self.tipo,
            'quantidade': self.quantidade,
            'estoque_anterior': self.estoque_anterior,
            'estoque_atual': self.estoque_atual,
            'referencia': self.referencia,
            'observacoes': self.observacoes,
            'data_movimento': self.data_movimento.isoformat() if self.data_movimento else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# Lançamentos Financeiros
class LancamentoFinanceiro(db.Model):
    __tablename__ = 'lancamentos_financeiros'
    
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), nullable=False)  # RECEITA, DESPESA
    descricao = db.Column(db.String(200), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data_lancamento = db.Column(db.DateTime, default=datetime.utcnow)
    data_vencimento = db.Column(db.DateTime)
    data_pagamento = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='PENDENTE')  # PENDENTE, PAGO, CANCELADO
    categoria = db.Column(db.String(50))
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedores.id'))
    observacoes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    cliente = db.relationship('Cliente')
    fornecedor = db.relationship('Fornecedor')
    
    def to_dict(self):
        return {
            'id': self.id,
            'tipo': self.tipo,
            'descricao': self.descricao,
            'valor': self.valor,
            'data_lancamento': self.data_lancamento.isoformat() if self.data_lancamento else None,
            'data_vencimento': self.data_vencimento.isoformat() if self.data_vencimento else None,
            'data_pagamento': self.data_pagamento.isoformat() if self.data_pagamento else None,
            'status': self.status,
            'categoria': self.categoria,
            'cliente_id': self.cliente_id,
            'cliente_nome': self.cliente.nome if self.cliente else None,
            'fornecedor_id': self.fornecedor_id,
            'fornecedor_nome': self.fornecedor.nome if self.fornecedor else None,
            'observacoes': self.observacoes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
