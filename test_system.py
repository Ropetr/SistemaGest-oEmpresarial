#!/usr/bin/env python
"""
Script de teste para validar as funcionalidades do Sistema ERP
"""
import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_cliente():
    """Testa CRUD de clientes"""
    print("\n=== TESTE: Clientes ===")
    
    # Criar
    data = {
        "nome": "Teste Cliente Ltda",
        "cpf_cnpj": "11.222.333/0001-44",
        "email": "teste@cliente.com",
        "telefone": "(11) 99999-9999"
    }
    response = requests.post(f"{BASE_URL}/clientes", json=data)
    assert response.status_code == 201
    cliente = response.json()
    print(f"✓ Cliente criado: {cliente['nome']}")
    
    # Listar
    response = requests.get(f"{BASE_URL}/clientes")
    assert response.status_code == 200
    print(f"✓ Total de clientes: {len(response.json())}")
    
    # Buscar
    response = requests.get(f"{BASE_URL}/clientes/{cliente['id']}")
    assert response.status_code == 200
    print(f"✓ Cliente encontrado: {response.json()['nome']}")
    
    # Atualizar
    response = requests.put(f"{BASE_URL}/clientes/{cliente['id']}", json={"telefone": "(11) 88888-8888"})
    assert response.status_code == 200
    print(f"✓ Cliente atualizado")
    
    return cliente['id']

def test_fornecedor():
    """Testa CRUD de fornecedores"""
    print("\n=== TESTE: Fornecedores ===")
    
    data = {
        "nome": "Teste Fornecedor S.A.",
        "cnpj": "44.333.222/0001-11",
        "email": "contato@fornecedor.com",
        "telefone": "(11) 3333-3333"
    }
    response = requests.post(f"{BASE_URL}/fornecedores", json=data)
    assert response.status_code == 201
    print(f"✓ Fornecedor criado: {response.json()['nome']}")
    
    return response.json()['id']

def test_produto():
    """Testa CRUD de produtos"""
    print("\n=== TESTE: Produtos ===")
    
    data = {
        "codigo": "TEST001",
        "nome": "Produto de Teste",
        "unidade": "UN",
        "preco_custo": 100.00,
        "preco_venda": 150.00,
        "estoque_minimo": 10.0
    }
    response = requests.post(f"{BASE_URL}/produtos", json=data)
    assert response.status_code == 201
    print(f"✓ Produto criado: {response.json()['nome']}")
    
    return response.json()['id']

def test_estoque(fornecedor_id, produto_id):
    """Testa operações de estoque"""
    print("\n=== TESTE: Estoque ===")
    
    # Criar nota de entrada
    data = {
        "numero": "NE-TEST-001",
        "fornecedor_id": fornecedor_id,
        "itens": [{"produto_id": produto_id, "quantidade": 50, "preco_unitario": 100.00}]
    }
    response = requests.post(f"{BASE_URL}/notas-entrada", json=data)
    assert response.status_code == 201
    print(f"✓ Nota de entrada criada")
    
    # Verificar estoque
    response = requests.get(f"{BASE_URL}/estoque")
    assert response.status_code == 200
    estoque = [e for e in response.json() if e['produto_id'] == produto_id][0]
    assert estoque['estoque_atual'] == 50.0
    print(f"✓ Estoque atualizado: {estoque['estoque_atual']}")
    
    # Ver movimentos
    response = requests.get(f"{BASE_URL}/estoque/movimentos?produto_id={produto_id}")
    assert response.status_code == 200
    print(f"✓ Movimentos registrados: {len(response.json())}")

def test_vendas(cliente_id, produto_id):
    """Testa fluxo de vendas"""
    print("\n=== TESTE: Vendas ===")
    
    # Criar orçamento
    data = {
        "numero": "ORC-TEST-001",
        "cliente_id": cliente_id,
        "data_validade": "2024-12-31T23:59:59",
        "itens": [{"produto_id": produto_id, "quantidade": 5, "preco_unitario": 150.00}]
    }
    response = requests.post(f"{BASE_URL}/orcamentos", json=data)
    assert response.status_code == 201
    print(f"✓ Orçamento criado: R$ {response.json()['valor_total']:.2f}")
    
    # Criar pedido
    data = {
        "numero": "PV-TEST-001",
        "cliente_id": cliente_id,
        "itens": [{"produto_id": produto_id, "quantidade": 10, "preco_unitario": 150.00}]
    }
    response = requests.post(f"{BASE_URL}/pedidos-venda", json=data)
    assert response.status_code == 201
    pedido = response.json()
    print(f"✓ Pedido criado: R$ {pedido['valor_total']:.2f}")
    
    # Criar nota de saída
    data = {
        "numero": "NS-TEST-001",
        "cliente_id": cliente_id,
        "pedido_venda_id": pedido['id'],
        "itens": [{"produto_id": produto_id, "quantidade": 10, "preco_unitario": 150.00}]
    }
    response = requests.post(f"{BASE_URL}/notas-saida", json=data)
    assert response.status_code == 201
    print(f"✓ Nota de saída criada: R$ {response.json()['valor_total']:.2f}")
    
    # Verificar status do pedido
    response = requests.get(f"{BASE_URL}/pedidos-venda/{pedido['id']}")
    assert response.json()['status'] == 'FATURADO'
    print(f"✓ Pedido atualizado para FATURADO")

def test_financeiro():
    """Testa módulo financeiro"""
    print("\n=== TESTE: Financeiro ===")
    
    # Listar lançamentos
    response = requests.get(f"{BASE_URL}/financeiro/lancamentos")
    assert response.status_code == 200
    print(f"✓ Lançamentos encontrados: {len(response.json())}")
    
    # Ver resumo
    response = requests.get(f"{BASE_URL}/financeiro/resumo")
    assert response.status_code == 200
    resumo = response.json()
    print(f"✓ Resumo financeiro:")
    print(f"  - Receitas: R$ {resumo['receitas']['total']:.2f}")
    print(f"  - Despesas: R$ {resumo['despesas']['total']:.2f}")
    print(f"  - Saldo: R$ {resumo['saldo']:.2f}")

def main():
    print("="*60)
    print("TESTE DO SISTEMA ERP")
    print("="*60)
    
    try:
        cliente_id = test_cliente()
        fornecedor_id = test_fornecedor()
        produto_id = test_produto()
        test_estoque(fornecedor_id, produto_id)
        test_vendas(cliente_id, produto_id)
        test_financeiro()
        
        print("\n" + "="*60)
        print("✅ TODOS OS TESTES PASSARAM!")
        print("="*60)
    except AssertionError as e:
        print(f"\n❌ TESTE FALHOU: {e}")
    except Exception as e:
        print(f"\n❌ ERRO: {e}")

if __name__ == "__main__":
    main()
