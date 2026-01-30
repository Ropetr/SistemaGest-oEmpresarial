# Sistema ERP - Guia de Início Rápido

## 🚀 Início Rápido (5 minutos)

### 1. Instalar e Executar

```bash
# Clonar repositório
git clone https://github.com/Ropetr/SistemaGest-oEmpresarial.git
cd SistemaGest-oEmpresarial

# Criar ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Executar sistema
python app.py
```

O sistema estará disponível em: http://localhost:5000

### 2. Testar o Sistema

```bash
# Executar suite de testes
python test_system.py
```

## 📱 Acessos

- **Interface Web**: http://localhost:5000
- **API REST**: http://localhost:5000/api
- **Documentação**: Ver API_DOCUMENTATION.md

## 🎯 Fluxo de Uso Típico

### Cenário 1: Comprar Produtos

```bash
# 1. Cadastrar fornecedor
curl -X POST http://localhost:5000/api/fornecedores \
  -H "Content-Type: application/json" \
  -d '{"nome": "Fornecedor ABC", "cnpj": "12.345.678/0001-90"}'

# 2. Cadastrar produto
curl -X POST http://localhost:5000/api/produtos \
  -H "Content-Type: application/json" \
  -d '{"codigo": "P001", "nome": "Notebook", "preco_custo": 2000, "preco_venda": 3000}'

# 3. Registrar entrada (nota fiscal)
curl -X POST http://localhost:5000/api/notas-entrada \
  -H "Content-Type: application/json" \
  -d '{
    "numero": "NE-001",
    "fornecedor_id": 1,
    "itens": [{"produto_id": 1, "quantidade": 10, "preco_unitario": 2000}]
  }'
```

**Resultado**: 
- ✅ Estoque aumenta automaticamente
- ✅ Lançamento de despesa criado
- ✅ Movimento de estoque registrado

### Cenário 2: Vender Produtos

```bash
# 1. Cadastrar cliente
curl -X POST http://localhost:5000/api/clientes \
  -H "Content-Type: application/json" \
  -d '{"nome": "Cliente XYZ", "cpf_cnpj": "123.456.789-00"}'

# 2. Criar pedido de venda
curl -X POST http://localhost:5000/api/pedidos-venda \
  -H "Content-Type: application/json" \
  -d '{
    "numero": "PV-001",
    "cliente_id": 1,
    "itens": [{"produto_id": 1, "quantidade": 2, "preco_unitario": 3000}]
  }'

# 3. Emitir nota de saída
curl -X POST http://localhost:5000/api/notas-saida \
  -H "Content-Type: application/json" \
  -d '{
    "numero": "NS-001",
    "cliente_id": 1,
    "pedido_venda_id": 1,
    "itens": [{"produto_id": 1, "quantidade": 2, "preco_unitario": 3000}]
  }'
```

**Resultado**:
- ✅ Estoque diminui automaticamente
- ✅ Lançamento de receita criado
- ✅ Pedido marcado como FATURADO
- ✅ Movimento de estoque registrado

### Cenário 3: Fazer Orçamento

```bash
curl -X POST http://localhost:5000/api/orcamentos \
  -H "Content-Type: application/json" \
  -d '{
    "numero": "ORC-001",
    "cliente_id": 1,
    "data_validade": "2024-12-31T23:59:59",
    "itens": [{"produto_id": 1, "quantidade": 5, "preco_unitario": 3000}]
  }'
```

### Cenário 4: Consultar Financeiro

```bash
# Ver resumo
curl http://localhost:5000/api/financeiro/resumo

# Ver receitas pendentes
curl http://localhost:5000/api/financeiro/lancamentos?tipo=RECEITA&status=PENDENTE

# Ver despesas pagas
curl http://localhost:5000/api/financeiro/lancamentos?tipo=DESPESA&status=PAGO
```

### Cenário 5: Verificar Estoque

```bash
# Ver todos os produtos em estoque
curl http://localhost:5000/api/estoque

# Ver movimentos de um produto
curl http://localhost:5000/api/estoque/movimentos?produto_id=1

# Fazer ajuste de estoque
curl -X POST http://localhost:5000/api/estoque/ajuste \
  -H "Content-Type: application/json" \
  -d '{"produto_id": 1, "quantidade": 15, "observacoes": "Inventário"}'
```

## 📊 Dados de Exemplo

Execute este script para popular o sistema com dados de exemplo:

```python
import requests

base = "http://localhost:5000/api"

# Cliente
requests.post(f"{base}/clientes", json={
    "nome": "Empresa Demo Ltda",
    "cpf_cnpj": "11.222.333/0001-44",
    "email": "demo@empresa.com"
})

# Fornecedor
requests.post(f"{base}/fornecedores", json={
    "nome": "Fornecedor Demo",
    "cnpj": "44.333.222/0001-11"
})

# Produto
requests.post(f"{base}/produtos", json={
    "codigo": "DEMO001",
    "nome": "Produto Demo",
    "preco_custo": 100,
    "preco_venda": 150
})
```

## 🔧 Configuração Avançada

### Usar outro banco de dados

Edite o arquivo `.env`:

```env
DATABASE_URL=postgresql://user:pass@localhost/erp_db
# ou
DATABASE_URL=mysql://user:pass@localhost/erp_db
```

### Executar em produção

```bash
# Usar servidor WSGI como Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📚 Recursos Adicionais

- **README.md**: Documentação completa
- **API_DOCUMENTATION.md**: Referência da API
- **test_system.py**: Exemplos de uso

## 🆘 Solução de Problemas

### Erro: "Address already in use"
```bash
# Encontrar processo na porta 5000
lsof -ti:5000 | xargs kill -9
```

### Erro: "No module named 'flask'"
```bash
# Verificar ambiente virtual ativo
which python
pip install -r requirements.txt
```

### Banco de dados corrompido
```bash
# Remover e recriar
rm instance/erp.db
python app.py
```

## 💡 Dicas

1. **Use a interface web** para ver todos os endpoints disponíveis
2. **Execute os testes** para entender o fluxo do sistema
3. **Consulte a API_DOCUMENTATION.md** para detalhes dos endpoints
4. **Estoque mínimo** aparece com status "CRÍTICO" quando abaixo do mínimo
5. **Lançamentos financeiros** são criados automaticamente em vendas e compras

## 🎓 Próximos Passos

1. ✅ Sistema básico implementado
2. 🔜 Adicionar autenticação (JWT)
3. 🔜 Adicionar relatórios (PDF)
4. 🔜 Implementar dashboard com gráficos
5. 🔜 Adicionar controle de usuários e permissões
6. 🔜 Implementar envio de e-mails
7. 🔜 Adicionar notificações em tempo real

## 📞 Suporte

Para dúvidas e sugestões, abra uma issue no GitHub.
