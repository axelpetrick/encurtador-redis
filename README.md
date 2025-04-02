# 🔗 Encurtador de URLs com Flask, Tkinter e Redis

Este projeto é um **encurtador de URLs** com interface gráfica e servidor web, desenvolvido com **Flask**, **Tkinter** e **Redis**. Ele oferece dois modos de operação:
- **Modo Local**: Para testes sem necessidade de um banco de dados externo.
- **Modo Redis**: Para armazenamento persistente das URLs e estatísticas de acessos.

## 🚀 Funcionalidades
✅ Interface gráfica com **Tkinter** para facilitar a criação de URLs encurtadas.

✅ Integração com **Redis** para armazenamento persistente e rastreamento de estatísticas.

✅ Servidor **Flask** para redirecionamento automático das URLs encurtadas.

✅ Suporte a **tempo de expiração** para URLs armazenadas no Redis.

✅ Geração de **códigos curtos aleatórios** para cada URL encurtada.

✅ **Ranking** das URLs mais acessadas (somente no modo Redis).

---
## 🖥️ Estrutura do Projeto

📂 **/encurtador** (pasta principal)
- 📄 `main.py` → Interface gráfica do encurtador.
- 📄 `server.py` → Servidor Flask para redirecionamento de URLs.

---
## 🎨 Interface Gráfica (Tkinter)
A interface gráfica foi desenvolvida com **Tkinter**, permitindo a criação e gerenciamento de URLs encurtadas de forma intuitiva. Ela possui duas abas:
1. **Redis Shortener** → Utiliza Redis para armazenamento.
2. **Local Shortener** → Usa um dicionário local para testes.

Cada aba contém:
- Campo de entrada para a URL original.
- Botão para gerar a URL encurtada.
- Campo para exibir o link encurtado.
- (No modo Redis) Opção para definir tempo de expiração.
- (No modo Redis) Exibição de estatísticas da URL.

---
## 🛠️ Modos de Operação

### 🔍 Modo Local – Testes sem Redis
Este modo permite encurtar URLs sem a necessidade de um banco de dados externo. As URLs são armazenadas **temporariamente** em um dicionário dentro da aplicação e são perdidas ao fechar o programa.

#### Como funciona?
1. O usuário insere a URL e clica em "Encurtar".
2. O programa gera um **código curto aleatório**.
3. A URL e o código são armazenados em um **dicionário local**.
4. O usuário pode visualizar todas as URLs encurtadas e seus acessos.
5. O redirecionamento é gerenciado pelo **Flask**.

📌 **Código principal (main.py):**
```python
self.local_urls[code] = {
    'url': original_url,
    'created_at': datetime.now(),
    'visits': 0
}
```

📌 **Redirecionamento via Flask (server.py):**
```python
@app.route('/local/<code>')
def redirect_local_url(code):
    if code in local_urls:
        local_urls[code]['visits'] += 1
        return redirect(local_urls[code]['url'])
    return "URL local não encontrada", 404
```

---
### 🚀 Modo Redis – URLs Persistentes e Estatísticas
Neste modo, as URLs encurtadas são **armazenadas no Redis**, garantindo persistência e rastreamento de estatísticas de acesso.

#### Como funciona?
1. O usuário insere a URL e define um **tempo de expiração** (padrão: 24h).
2. O programa gera um **código curto aleatório**.
3. A URL e o código são armazenados no **Redis** com um TTL (tempo de expiração).
4. Cada acesso à URL curta **incrementa um contador de acessos**.
5. O ranking das URLs mais acessadas é atualizado automaticamente.
6. As estatísticas são exibidas na interface gráfica.

📌 **Código principal (main.py):**
```python
# Armazena a URL no Redis com tempo de expiração
duration = expiration_hours * 3600
self.redis_client.setex(f"url:{code}", duration, original_url)

# Inicializa o contador de acessos
self.redis_client.set(f"stats:{code}", 0)
```

📌 **Redirecionamento via Flask (server.py):**
```python
@app.route('/<code>')
def redirect_url(code):
    original_url = redis_client.get(f"url:{code}")
    if original_url:
        redis_client.incr(f"stats:{code}")
        redis_client.zincrby("popular_urls", 1, code)
        return redirect(original_url.decode())
    return "URL não encontrada ou expirada", 404
```

---
## ⚡ Diferenças entre os Modos

| Modo | Armazenamento | Persistência | Estatísticas | Expiração |
|------|--------------|--------------|--------------|-----------|
| **Redis** | Redis | Sim | Sim | Sim |
| **Local** | Dicionário em memória | Não | Sim | Não |

📌 **O modo Redis é ideal para produção, pois mantém as URLs ativas e fornece estatísticas detalhadas.** 🚀

---
## 🏗️ Como Executar o Projeto

### 🔹 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 🔹 2. Executar o servidor Flask
```bash
python server.py
```

### 🔹 3. Executar a interface gráfica
```bash
python main.py
```

---
## 🛠️ Tecnologias Utilizadas
- **Python** – Linguagem principal do projeto.
- **Flask** – Servidor para redirecionamento de URLs.
- **Tkinter** – Interface gráfica para interação do usuário.
- **Redis** – Armazenamento persistente de URLs e estatísticas.

📌 **Este projeto é ideal para quem deseja aprender sobre integração entre interface gráfica, banco de dados em memória e servidores web!** 🔥

