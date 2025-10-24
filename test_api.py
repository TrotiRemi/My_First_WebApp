"""
Script de test complet pour l'API School Organizer
Teste : Signup → Login → Logout → Login → Créer Cours → Ajouter Document
"""

import requests
import json
from datetime import date

API_BASE = "http://localhost:8000/api/v1"

# Couleurs pour l'affichage
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

def print_test(name):
    print(f"\n{BLUE}{'='*60}")
    print(f"TEST: {name}")
    print(f"{'='*60}{RESET}")

def print_success(msg):
    print(f"{GREEN}✓ {msg}{RESET}")

def print_error(msg):
    print(f"{RED}✗ {msg}{RESET}")

def print_response(data):
    print(f"{json.dumps(data, indent=2)}")

# === TEST 1: SIGNUP ===
print_test("1. SIGNUP - Créer un compte")

signup_data = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
}

try:
    response = requests.post(f"{API_BASE}/auth/signup", json=signup_data)
    if response.status_code == 201:
        print_success(f"Account créé (status: {response.status_code})")
        print_response(response.json())
    else:
        print_error(f"Erreur: {response.status_code}")
        print_response(response.json())
except Exception as e:
    print_error(f"Exception: {e}")

# === TEST 2: LOGIN (1ère fois) ===
print_test("2. LOGIN - Se connecter (1ère fois)")

login_data = {
    "username": "testuser",
    "password": "password123"
}

token = None
try:
    response = requests.post(
        f"{API_BASE}/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    if response.status_code == 200:
        data = response.json()
        token = data.get("access_token")
        print_success(f"Login réussi (status: {response.status_code})")
        print(f"Token reçu: {token[:50]}...")
        print_response(data)
    else:
        print_error(f"Erreur: {response.status_code}")
        print_response(response.json())
except Exception as e:
    print_error(f"Exception: {e}")

if not token:
    print_error("Pas de token, arrêt du script")
    exit(1)

# === TEST 3: LOGOUT ===
print_test("3. LOGOUT - Se déconnecter")

try:
    response = requests.post(
        f"{API_BASE}/auth/logout",
        headers={"Authorization": f"Bearer {token}"}
    )
    if response.status_code == 200:
        print_success(f"Logout réussi (status: {response.status_code})")
        print_response(response.json())
    else:
        print_error(f"Erreur: {response.status_code}")
        print_response(response.json())
except Exception as e:
    print_error(f"Exception: {e}")

# === TEST 4: LOGIN (2e fois) ===
print_test("4. LOGIN - Se reconnecter (2e fois)")

token = None
try:
    response = requests.post(
        f"{API_BASE}/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    if response.status_code == 200:
        data = response.json()
        token = data.get("access_token")
        print_success(f"Login réussi (status: {response.status_code})")
        print(f"Nouveau token reçu: {token[:50]}...")
        print_response(data)
    else:
        print_error(f"Erreur: {response.status_code}")
        print_response(response.json())
except Exception as e:
    print_error(f"Exception: {e}")

if not token:
    print_error("Pas de token, arrêt du script")
    exit(1)

# === TEST 5: CRÉER UN COURS ===
print_test("5. CRÉER UN COURS")

course_data = {
    "title": "Mathématiques",
    "description": "Cours de maths niveau L1",
    "start_date": str(date(2025, 1, 15)),
    "end_date": str(date(2025, 5, 30))
}

course_id = None
try:
    response = requests.post(
        f"{API_BASE}/courses/",
        json=course_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    if response.status_code == 201:
        data = response.json()
        course_id = data.get("id")
        print_success(f"Cours créé (status: {response.status_code})")
        print(f"Course ID: {course_id}")
        print_response(data)
    else:
        print_error(f"Erreur: {response.status_code}")
        print_response(response.json())
except Exception as e:
    print_error(f"Exception: {e}")

if not course_id:
    print_error("Pas de course_id, arrêt du script")
    exit(1)

# === TEST 6: AJOUTER UN DOCUMENT ===
print_test("6. AJOUTER UN DOCUMENT")

document_data = {
    "title": "Cours de Maths - Chapitre 1",
    "url": "https://example.com/maths-ch1.pdf",
    "type": "lecture",
    "course_id": course_id
}

try:
    response = requests.post(
        f"{API_BASE}/documents/",
        json=document_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    if response.status_code == 201:
        data = response.json()
        print_success(f"Document créé (status: {response.status_code})")
        print(f"Document ID: {data.get('id')}")
        print_response(data)
    else:
        print_error(f"Erreur: {response.status_code}")
        print_response(response.json())
except Exception as e:
    print_error(f"Exception: {e}")

# === TEST 7: RÉCUPÉRER TOUS LES DOCUMENTS ===
print_test("7. RÉCUPÉRER TOUS LES DOCUMENTS")

try:
    response = requests.get(
        f"{API_BASE}/documents/",
        headers={"Authorization": f"Bearer {token}"}
    )
    if response.status_code == 200:
        data = response.json()
        print_success(f"Documents récupérés (status: {response.status_code})")
        print(f"Nombre de documents: {len(data)}")
        print_response(data)
    else:
        print_error(f"Erreur: {response.status_code}")
        print_response(response.json())
except Exception as e:
    print_error(f"Exception: {e}")

print(f"\n{GREEN}{'='*60}")
print("✓ TOUS LES TESTS COMPLÉTÉS")
print(f"{'='*60}{RESET}\n")
