# ==================== IMPORTS ====================
from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest
import mongomock
import json

import main

# ==================== TEST SETUP ====================
client = TestClient(main.app)
fake_mongo_client = mongomock.MongoClient()
database = fake_mongo_client.practica1
collection_historial = database.historial

# ==================== SUM OPERATION TESTS ====================

@pytest.mark.parametrize(
    "numbers, expected_result",
    [
        # Two numbers tests
        ([11, 29], 40),
        ([0, 0], 0),
        ([11.11, 29.29], 40.40),
        # Multiple numbers tests
        ([1, 2, 3], 6),
        ([10, 20, 30, 40], 100),
        ([0, 0, 0], 0),
        ([1.5, 2.5, 3.0], 7.0),
    ]
)
def test_sum_numbers(numbers, expected_result, monkeypatch):
    """Tests for sum operations with 2 or more numbers"""
    monkeypatch.setattr(main, "collection_historial", collection_historial)
    
    query_params = "&".join([f"numbers={num}" for num in numbers])
    response = client.get(f"/calculator/sum?{query_params}")
    
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["numbers"] == numbers
    assert abs(response_data["result"] - expected_result) < 0.01  # Tolerance for decimals

# ==================== SUBTRACTION OPERATION TESTS ====================

@pytest.mark.parametrize(
    "numbers, expected_result",
    [
        ([10, 3, 2], 5),  # 10 - 3 - 2 = 5
        ([100, 20, 30], 50),  # 100 - 20 - 30 = 50
        ([0, 5, 3], -8),  # 0 - 5 - 3 = -8
    ]
)
def test_subtract_multiple_numbers(numbers, expected_result, monkeypatch):
    """Tests for subtraction with multiple numbers"""
    monkeypatch.setattr(main, "collection_historial", collection_historial)
    
    query_params = "&".join([f"numbers={num}" for num in numbers])
    response = client.get(f"/calculator/substract?{query_params}")
    
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["numbers"] == numbers
    assert abs(response_data["result"] - expected_result) < 0.01

# ==================== MULTIPLICATION OPERATION TESTS ====================

@pytest.mark.parametrize(
    "numbers, expected_result",
    [
        ([2, 3, 4], 24),  # 2 * 3 * 4 = 24
        ([5, 2, 3], 30),  # 5 * 2 * 3 = 30
        ([1, 1, 1, 1], 1),  # 1 * 1 * 1 * 1 = 1
        ([0, 5, 10], 0),  # 0 * 5 * 10 = 0
        ([2.5, 4, 2], 20.0),  # 2.5 * 4 * 2 = 20
    ]
)
def test_multiply_multiple_numbers(numbers, expected_result, monkeypatch):
    """Tests for multiplication with multiple numbers"""
    monkeypatch.setattr(main, "collection_historial", collection_historial)
    
    query_params = "&".join([f"numbers={num}" for num in numbers])
    response = client.get(f"/calculator/multiply?{query_params}")
    
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["numbers"] == numbers
    assert abs(response_data["result"] - expected_result) < 0.01

# ==================== DIVISION OPERATION TESTS ====================

@pytest.mark.parametrize(
    "numbers, expected_result",
    [
        ([100, 2, 5], 10.0),  # 100 / 2 / 5 = 10
        ([120, 3, 4], 10.0),  # 120 / 3 / 4 = 10
        ([50, 2, 5], 5.0),  # 50 / 2 / 5 = 5
        ([100.0, 4.0, 5.0], 5.0),  # 100 / 4 / 5 = 5
    ]
)
def test_divide_multiple_numbers(numbers, expected_result, monkeypatch):
    """Tests for division with multiple numbers"""
    monkeypatch.setattr(main, "collection_historial", collection_historial)
    
    query_params = "&".join([f"numbers={num}" for num in numbers])
    response = client.get(f"/calculator/divide?{query_params}")
    
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["numbers"] == numbers
    assert response_data["result"] == expected_result

# ==================== VALIDATION TESTS ====================

# Insufficient numbers tests
def test_sum_insufficient_numbers(monkeypatch):
    """Test validation for insufficient numbers - Sum"""
    monkeypatch.setattr(main, "collection_historial", collection_historial)
    
    response = client.get("/calculator/sum?numbers=5")
    
    assert response.status_code == 400
    response_data = response.json()
    assert "At least 2 numbers are required" in response_data["error"]
    assert response_data["operation"] == "sum"
    assert response_data["operands"] == [5.0]

def test_multiply_insufficient_numbers(monkeypatch):
    """Test validation for insufficient numbers - Multiplication"""
    monkeypatch.setattr(main, "collection_historial", collection_historial)
    
    response = client.get("/calculator/multiply?numbers=10")
    
    assert response.status_code == 400
    response_data = response.json()
    assert "At least 2 numbers are required" in response_data["error"]
    assert response_data["operation"] == "multiplication"
    assert response_data["operands"] == [10.0]

# Division by zero tests
def test_divide_by_zero_multiple_numbers(monkeypatch):
    """Test validation for division by zero - Multiple numbers"""
    monkeypatch.setattr(main, "collection_historial", collection_historial)
    
    response = client.get("/calculator/divide?numbers=10&numbers=0&numbers=5")
    
    assert response.status_code == 403
    response_data = response.json()
    assert "Division by zero" in response_data["error"]
    assert response_data["operation"] == "division"
    assert response_data["operands"] == [10.0, 0.0, 5.0]

def test_divide_by_zero_last_number(monkeypatch):
    """Test validation for division by zero - Last number"""
    monkeypatch.setattr(main, "collection_historial", collection_historial)
    
    response = client.get("/calculator/divide?numbers=100&numbers=2&numbers=0")
    
    assert response.status_code == 403
    response_data = response.json()
    assert "Division by zero" in response_data["error"]
    assert response_data["operation"] == "division"
    assert response_data["operands"] == [100.0, 2.0, 0.0]

# Negative numbers tests
def test_sum_negative_numbers_error(monkeypatch):
    """Test validation for negative numbers - Sum"""
    monkeypatch.setattr(main, "collection_historial", collection_historial)
    
    response = client.get("/calculator/sum?numbers=-5&numbers=10&numbers=15")
    
    assert response.status_code == 400
    response_data = response.json()
    assert "Negative numbers are not allowed" in response_data["error"]
    assert response_data["operation"] == "sum"
    assert response_data["operands"] == [-5.0, 10.0, 15.0]

def test_multiply_negative_numbers_error(monkeypatch):
    """Test validation for negative numbers - Multiplication"""
    monkeypatch.setattr(main, "collection_historial", collection_historial)
    
    response = client.get("/calculator/multiply?numbers=5&numbers=-3&numbers=2")
    
    assert response.status_code == 400
    response_data = response.json()
    assert "Negative numbers are not allowed" in response_data["error"]
    assert response_data["operation"] == "multiplication"
    assert response_data["operands"] == [5.0, -3.0, 2.0]

# ==================== EDGE CASES AND SPECIAL TESTS ====================

def test_large_numbers(monkeypatch):
    """Test for extreme cases - Large numbers"""
    monkeypatch.setattr(main, "collection_historial", collection_historial)
    
    large_numbers = [1000000, 2000000, 3000000]
    query_params = "&".join([f"numbers={num}" for num in large_numbers])
    response = client.get(f"/calculator/sum?{query_params}")
    
    assert response.status_code == 200
    assert response.json()["result"] == 6000000

def test_many_numbers(monkeypatch):
    """Test for extreme cases - Many numbers"""
    monkeypatch.setattr(main, "collection_historial", collection_historial)
    
    many_numbers = [1] * 10  # 10 numbers equal to 1
    query_params = "&".join([f"numbers={num}" for num in many_numbers])
    response = client.get(f"/calculator/sum?{query_params}")
    
    assert response.status_code == 200
    assert response.json()["result"] == 10

def test_decimal_precision(monkeypatch):
    """Test for decimal precision"""
    monkeypatch.setattr(main, "collection_historial", collection_historial)
    
    response = client.get("/calculator/divide?numbers=10&numbers=3")
    
    assert response.status_code == 200
    result = response.json()["result"]
    # 10/3 = 3.333...
    assert abs(result - 3.3333333333333335) < 0.0001

# ==================== HISTORY TESTS ====================

def test_history(monkeypatch):
    """Test for history endpoint"""
    monkeypatch.setattr(main, "collection_historial", collection_historial)

    response = client.get("/calculator/history")
    assert response.status_code == 200