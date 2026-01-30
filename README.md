# Sistema de Gestão Empresarial (ERP Básico)

Sistema ERP completo desenvolvido em Python/Flask para gerenciamento empresarial com os seguintes módulos:

## 🚀 Funcionalidades

### 1. **Clientes e Fornecedores**
- Cadastro completo de clientes (CPF/CNPJ, contatos, endereço)
- Cadastro de fornecedores com informações detalhadas
- Controle de status ativo/inativo
- Histórico de relacionamentos

### 2. **Orçamentos e Pedidos de Venda**
- Criação de orçamentos com múltiplos itens
- Controle de validade e status (Pendente, Aprovado, Rejeitado)
- Gerenciamento de pedidos de venda
- Cálculo automático de valores totais
- Status de pedidos (Aberto, Faturado, Cancelado)

### 3. **Notas de Entrada e Saída**
- Registro de notas de entrada de mercadorias
- Emissão de notas de saída
- Atualização automática de estoque
- Vínculo com pedidos de venda

### 4. **Estoque**
- Controle em tempo real do estoque
- Alertas de estoque mínimo
- Histórico completo de movimentações
- Tipos de movimento: Entrada, Saída e Ajuste
- Rastreabilidade de produtos

### 5. **Financeiro**
- Controle de contas a pagar e receber
- Lançamentos de receitas e despesas
- Status de pagamento (Pendente, Pago, Cancelado)
- Resumo financeiro com saldos
- Categorização de lançamentos
- Integração automática com vendas e compras

## 📋 Requisitos

- Python 3.8+
- Flask 3.0.0
- SQLAlchemy
- SQLite (ou outro banco de dados compatível)

## 🛠️ Instalação

1. Clone o repositório:
```bash
git clone https://github.com/Ropetr/SistemaGest-oEmpresarial.git
cd SistemaGest-oEmpresarial
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. Execute o sistema:
```bash
python app.py
```

O sistema estará disponível em `http://localhost:5000`

## 📡 API REST

### Clientes
- `GET /api/clientes` - Listar clientes
- `POST /api/clientes` - Criar cliente
- `GET /api/clientes/{id}` - Buscar cliente
- `PUT /api/clientes/{id}` - Atualizar cliente
- `DELETE /api/clientes/{id}` - Desativar cliente

### Fornecedores
- `GET /api/fornecedores` - Listar fornecedores
- `POST /api/fornecedores` - Criar fornecedor
- `GET /api/fornecedores/{id}` - Buscar fornecedor
- `PUT /api/fornecedores/{id}` - Atualizar fornecedor
- `DELETE /api/fornecedores/{id}` - Desativar fornecedor

### Produtos
- `GET /api/produtos` - Listar produtos
- `POST /api/produtos` - Criar produto
- `GET /api/produtos/{id}` - Buscar produto
- `PUT /api/produtos/{id}` - Atualizar produto
- `DELETE /api/produtos/{id}` - Desativar produto

### Orçamentos
- `GET /api/orcamentos` - Listar orçamentos
- `POST /api/orcamentos` - Criar orçamento
- `GET /api/orcamentos/{id}` - Buscar orçamento
- `PUT /api/orcamentos/{id}` - Atualizar status
- `DELETE /api/orcamentos/{id}` - Excluir orçamento

### Pedidos de Venda
- `GET /api/pedidos-venda` - Listar pedidos
- `POST /api/pedidos-venda` - Criar pedido
- `GET /api/pedidos-venda/{id}` - Buscar pedido
- `PUT /api/pedidos-venda/{id}` - Atualizar status
- `DELETE /api/pedidos-venda/{id}` - Excluir pedido

### Notas de Entrada
- `GET /api/notas-entrada` - Listar notas
- `POST /api/notas-entrada` - Criar nota (atualiza estoque)
- `GET /api/notas-entrada/{id}` - Buscar nota
- `DELETE /api/notas-entrada/{id}` - Excluir nota

### Notas de Saída
- `GET /api/notas-saida` - Listar notas
- `POST /api/notas-saida` - Criar nota (baixa estoque)
- `GET /api/notas-saida/{id}` - Buscar nota
- `DELETE /api/notas-saida/{id}` - Excluir nota

### Estoque
- `GET /api/estoque` - Ver status do estoque
- `GET /api/estoque/movimentos` - Listar movimentos
- `POST /api/estoque/ajuste` - Fazer ajuste manual

### Financeiro
- `GET /api/financeiro/lancamentos` - Listar lançamentos
- `POST /api/financeiro/lancamentos` - Criar lançamento
- `GET /api/financeiro/lancamentos/{id}` - Buscar lançamento
- `PUT /api/financeiro/lancamentos/{id}` - Atualizar status
- `DELETE /api/financeiro/lancamentos/{id}` - Excluir lançamento
- `GET /api/financeiro/resumo` - Resumo financeiro

## 📊 Exemplos de Uso

### Criar um Cliente
```bash
curl -X POST http://localhost:5000/api/clientes \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Empresa XYZ Ltda",
    "cpf_cnpj": "12.345.678/0001-90",
    "email": "contato@xyz.com",
    "telefone": "(11) 98765-4321",
    "endereco": "Rua ABC, 123",
    "cidade": "São Paulo",
    "estado": "SP",
    "cep": "01234-567"
  }'
```

### Criar um Produto
```bash
curl -X POST http://localhost:5000/api/produtos \
  -H "Content-Type: application/json" \
  -d '{
    "codigo": "PROD001",
    "nome": "Notebook",
    "descricao": "Notebook 15 polegadas",
    "unidade": "UN",
    "preco_custo": 2000.00,
    "preco_venda": 3000.00,
    "estoque_minimo": 5.0,
    "estoque_atual": 10.0
  }'
```

### Criar uma Nota de Entrada
```bash
curl -X POST http://localhost:5000/api/notas-entrada \
  -H "Content-Type: application/json" \
  -d '{
    "numero": "NE-001",
    "fornecedor_id": 1,
    "itens": [
      {
        "produto_id": 1,
        "quantidade": 10,
        "preco_unitario": 2000.00
      }
    ]
  }'
```

### Criar um Pedido de Venda
```bash
curl -X POST http://localhost:5000/api/pedidos-venda \
  -H "Content-Type: application/json" \
  -d '{
    "numero": "PV-001",
    "cliente_id": 1,
    "data_entrega": "2024-02-01T00:00:00",
    "itens": [
      {
        "produto_id": 1,
        "quantidade": 2,
        "preco_unitario": 3000.00
      }
    ]
  }'
```

### Ver Resumo Financeiro
```bash
curl http://localhost:5000/api/financeiro/resumo
```

## 🗄️ Estrutura do Banco de Dados

O sistema utiliza SQLite por padrão e possui as seguintes tabelas:

- **clientes** - Cadastro de clientes
- **fornecedores** - Cadastro de fornecedores
- **produtos** - Catálogo de produtos
- **orcamentos** / **itens_orcamento** - Orçamentos e seus itens
- **pedidos_venda** / **itens_pedido_venda** - Pedidos e seus itens
- **notas_entrada** / **itens_nota_entrada** - Notas de entrada e itens
- **notas_saida** / **itens_nota_saida** - Notas de saída e itens
- **movimentos_estoque** - Histórico de movimentações
- **lancamentos_financeiros** - Lançamentos financeiros

## 🔒 Segurança

- Validação de estoque antes de emitir notas de saída
- Controle de status para prevenir duplicações
- Soft delete para clientes e fornecedores
- Timestamps automáticos em todos os registros

## 🚧 Regras de Negócio

1. **Estoque**: Notas de entrada aumentam o estoque, notas de saída diminuem
2. **Financeiro**: Pedidos de venda geram receitas, notas de entrada geram despesas
3. **Validações**: Não é possível fazer saída com estoque insuficiente
4. **Relacionamentos**: Notas de saída podem ser vinculadas a pedidos de venda
5. **Status**: Pedidos mudam para "FATURADO" quando há nota de saída vinculada

## 📝 Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

## 👥 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

## 📧 Contato

Para dúvidas e sugestões, abra uma issue no GitHub.