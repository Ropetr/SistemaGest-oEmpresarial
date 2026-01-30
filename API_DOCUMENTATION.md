# API Documentation - Sistema ERP

## Base URL
```
http://localhost:5000/api
```

## Autenticação
Atualmente não há autenticação. Em produção, deve-se implementar JWT ou OAuth2.

---

## Clientes

### Listar Clientes
```http
GET /api/clientes
```

**Resposta:**
```json
[
  {
    "id": 1,
    "nome": "Empresa ABC Ltda",
    "cpf_cnpj": "12.345.678/0001-90",
    "email": "contato@abc.com",
    "telefone": "(11) 98765-4321",
    "endereco": "Rua ABC, 123",
    "cidade": "São Paulo",
    "estado": "SP",
    "cep": "01234-567",
    "ativo": true,
    "created_at": "2024-01-30T13:00:00",
    "updated_at": "2024-01-30T13:00:00"
  }
]
```

### Criar Cliente
```http
POST /api/clientes
```

**Body:**
```json
{
  "nome": "Empresa XYZ Ltda",
  "cpf_cnpj": "12.345.678/0001-90",
  "email": "contato@xyz.com",
  "telefone": "(11) 98765-4321",
  "endereco": "Rua ABC, 123",
  "cidade": "São Paulo",
  "estado": "SP",
  "cep": "01234-567"
}
```

### Buscar Cliente
```http
GET /api/clientes/{id}
```

### Atualizar Cliente
```http
PUT /api/clientes/{id}
```

**Body:** (todos os campos são opcionais)
```json
{
  "nome": "Novo Nome",
  "email": "novo@email.com",
  "telefone": "(11) 99999-9999"
}
```

### Desativar Cliente
```http
DELETE /api/clientes/{id}
```

---

## Fornecedores

### Listar Fornecedores
```http
GET /api/fornecedores
```

### Criar Fornecedor
```http
POST /api/fornecedores
```

**Body:**
```json
{
  "nome": "Fornecedor XYZ Ltda",
  "cnpj": "98.765.432/0001-10",
  "email": "vendas@xyz.com",
  "telefone": "(11) 3333-4444",
  "endereco": "Av. Principal, 456",
  "cidade": "São Paulo",
  "estado": "SP",
  "cep": "01234-890"
}
```

### Buscar Fornecedor
```http
GET /api/fornecedores/{id}
```

### Atualizar Fornecedor
```http
PUT /api/fornecedores/{id}
```

### Desativar Fornecedor
```http
DELETE /api/fornecedores/{id}
```

---

## Produtos

### Listar Produtos
```http
GET /api/produtos
```

### Criar Produto
```http
POST /api/produtos
```

**Body:**
```json
{
  "codigo": "PROD001",
  "nome": "Notebook Dell",
  "descricao": "Notebook Dell Inspiron 15",
  "unidade": "UN",
  "preco_custo": 2500.00,
  "preco_venda": 3500.00,
  "estoque_minimo": 5.0,
  "estoque_atual": 0.0
}
```

### Buscar Produto
```http
GET /api/produtos/{id}
```

### Atualizar Produto
```http
PUT /api/produtos/{id}
```

### Desativar Produto
```http
DELETE /api/produtos/{id}
```

---

## Orçamentos

### Listar Orçamentos
```http
GET /api/orcamentos
```

### Criar Orçamento
```http
POST /api/orcamentos
```

**Body:**
```json
{
  "numero": "ORC-001",
  "cliente_id": 1,
  "data_validade": "2024-12-31T23:59:59",
  "observacoes": "Orçamento válido por 30 dias",
  "itens": [
    {
      "produto_id": 1,
      "quantidade": 2,
      "preco_unitario": 3500.00
    }
  ]
}
```

**Resposta:**
```json
{
  "id": 1,
  "numero": "ORC-001",
  "cliente_id": 1,
  "cliente_nome": "Empresa ABC Ltda",
  "data_orcamento": "2024-01-30T13:00:00",
  "data_validade": "2024-12-31T23:59:59",
  "valor_total": 7000.00,
  "status": "PENDENTE",
  "itens": [
    {
      "id": 1,
      "produto_id": 1,
      "produto_nome": "Notebook Dell",
      "quantidade": 2,
      "preco_unitario": 3500.00,
      "subtotal": 7000.00
    }
  ]
}
```

### Buscar Orçamento
```http
GET /api/orcamentos/{id}
```

### Atualizar Status do Orçamento
```http
PUT /api/orcamentos/{id}
```

**Body:**
```json
{
  "status": "APROVADO"
}
```

**Status possíveis:** `PENDENTE`, `APROVADO`, `REJEITADO`

---

## Pedidos de Venda

### Listar Pedidos
```http
GET /api/pedidos-venda
```

### Criar Pedido
```http
POST /api/pedidos-venda
```

**Body:**
```json
{
  "numero": "PV-001",
  "cliente_id": 1,
  "data_entrega": "2024-02-15T00:00:00",
  "observacoes": "Entregar pela manhã",
  "itens": [
    {
      "produto_id": 1,
      "quantidade": 3,
      "preco_unitario": 3500.00
    }
  ]
}
```

**Nota:** Ao criar um pedido, automaticamente é criado um lançamento financeiro de receita.

### Buscar Pedido
```http
GET /api/pedidos-venda/{id}
```

### Atualizar Pedido
```http
PUT /api/pedidos-venda/{id}
```

**Status possíveis:** `ABERTO`, `FATURADO`, `CANCELADO`

---

## Notas de Entrada

### Listar Notas de Entrada
```http
GET /api/notas-entrada
```

### Criar Nota de Entrada
```http
POST /api/notas-entrada
```

**Body:**
```json
{
  "numero": "NE-001",
  "fornecedor_id": 1,
  "observacoes": "Compra à vista",
  "itens": [
    {
      "produto_id": 1,
      "quantidade": 10,
      "preco_unitario": 2500.00
    }
  ]
}
```

**Nota:** Ao criar uma nota de entrada:
- O estoque do produto é aumentado
- O preço de custo do produto é atualizado
- Um movimento de estoque é registrado
- Um lançamento financeiro de despesa é criado

### Buscar Nota de Entrada
```http
GET /api/notas-entrada/{id}
```

---

## Notas de Saída

### Listar Notas de Saída
```http
GET /api/notas-saida
```

### Criar Nota de Saída
```http
POST /api/notas-saida
```

**Body:**
```json
{
  "numero": "NS-001",
  "cliente_id": 1,
  "pedido_venda_id": 1,
  "observacoes": "Entrega realizada",
  "itens": [
    {
      "produto_id": 1,
      "quantidade": 3,
      "preco_unitario": 3500.00
    }
  ]
}
```

**Nota:** Ao criar uma nota de saída:
- O estoque do produto é diminuído
- Um movimento de estoque é registrado
- Se houver `pedido_venda_id`, o status do pedido é atualizado para `FATURADO`
- Valida se há estoque suficiente antes de processar

**Validações:**
- Retorna erro 400 se não houver estoque suficiente

### Buscar Nota de Saída
```http
GET /api/notas-saida/{id}
```

---

## Estoque

### Ver Status do Estoque
```http
GET /api/estoque
```

**Resposta:**
```json
[
  {
    "produto_id": 1,
    "codigo": "PROD001",
    "nome": "Notebook Dell",
    "unidade": "UN",
    "estoque_atual": 7.0,
    "estoque_minimo": 5.0,
    "status": "OK"
  }
]
```

**Status possíveis:**
- `OK`: Estoque acima do mínimo
- `CRÍTICO`: Estoque abaixo do mínimo

### Listar Movimentos de Estoque
```http
GET /api/estoque/movimentos?produto_id={id}
```

**Parâmetros de Query:**
- `produto_id` (opcional): Filtrar movimentos por produto

**Resposta:**
```json
[
  {
    "id": 1,
    "produto_id": 1,
    "produto_nome": "Notebook Dell",
    "tipo": "ENTRADA",
    "quantidade": 10.0,
    "estoque_anterior": 0.0,
    "estoque_atual": 10.0,
    "referencia": "NE-001",
    "observacoes": "Nota de Entrada #NE-001",
    "data_movimento": "2024-01-30T13:00:00"
  }
]
```

**Tipos de movimento:** `ENTRADA`, `SAIDA`, `AJUSTE`

### Fazer Ajuste de Estoque
```http
POST /api/estoque/ajuste
```

**Body:**
```json
{
  "produto_id": 1,
  "quantidade": 15.0,
  "observacoes": "Ajuste de inventário"
}
```

---

## Financeiro

### Listar Lançamentos Financeiros
```http
GET /api/financeiro/lancamentos?tipo={tipo}&status={status}
```

**Parâmetros de Query:**
- `tipo` (opcional): `RECEITA` ou `DESPESA`
- `status` (opcional): `PENDENTE`, `PAGO`, `CANCELADO`

**Resposta:**
```json
[
  {
    "id": 1,
    "tipo": "RECEITA",
    "descricao": "Pedido de Venda #PV-001",
    "valor": 10500.00,
    "data_lancamento": "2024-01-30T13:00:00",
    "data_vencimento": null,
    "data_pagamento": null,
    "status": "PENDENTE",
    "categoria": "VENDAS",
    "cliente_id": 1,
    "cliente_nome": "Empresa ABC Ltda",
    "fornecedor_id": null,
    "observacoes": null
  }
]
```

### Criar Lançamento Financeiro
```http
POST /api/financeiro/lancamentos
```

**Body:**
```json
{
  "tipo": "RECEITA",
  "descricao": "Serviço de consultoria",
  "valor": 5000.00,
  "data_vencimento": "2024-02-28T00:00:00",
  "status": "PENDENTE",
  "categoria": "SERVICOS",
  "cliente_id": 1,
  "observacoes": "Pagamento em 30 dias"
}
```

### Buscar Lançamento
```http
GET /api/financeiro/lancamentos/{id}
```

### Atualizar Lançamento
```http
PUT /api/financeiro/lancamentos/{id}
```

**Body:**
```json
{
  "status": "PAGO"
}
```

**Nota:** Ao atualizar o status para `PAGO`, a data de pagamento é automaticamente preenchida.

### Resumo Financeiro
```http
GET /api/financeiro/resumo
```

**Resposta:**
```json
{
  "receitas": {
    "pendentes": 12000.00,
    "pagas": 5000.00,
    "total": 17000.00
  },
  "despesas": {
    "pendentes": 30000.00,
    "pagas": 10000.00,
    "total": 40000.00
  },
  "saldo": -5000.00,
  "saldo_previsto": -23000.00
}
```

**Cálculos:**
- `saldo`: Receitas pagas - Despesas pagas
- `saldo_previsto`: Total de receitas - Total de despesas

---

## Códigos de Status HTTP

- `200 OK`: Operação bem-sucedida
- `201 Created`: Recurso criado com sucesso
- `204 No Content`: Recurso deletado com sucesso
- `400 Bad Request`: Erro de validação (ex: estoque insuficiente)
- `404 Not Found`: Recurso não encontrado

---

## Exemplos de Uso com cURL

### Criar Cliente
```bash
curl -X POST http://localhost:5000/api/clientes \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Minha Empresa",
    "cpf_cnpj": "12.345.678/0001-90",
    "email": "contato@minhaempresa.com"
  }'
```

### Criar Produto
```bash
curl -X POST http://localhost:5000/api/produtos \
  -H "Content-Type: application/json" \
  -d '{
    "codigo": "PROD001",
    "nome": "Produto Teste",
    "preco_custo": 100.00,
    "preco_venda": 150.00
  }'
```

### Ver Estoque
```bash
curl http://localhost:5000/api/estoque
```

### Ver Resumo Financeiro
```bash
curl http://localhost:5000/api/financeiro/resumo
```
