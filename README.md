Aqui está a descrição atualizada do repositório, incluindo a explicação sobre o modo local:  

---

# 🔗 URL Shortener – Flask, Tkinter & Redis  

Este repositório contém um **encurtador de URLs** desenvolvido com **Flask**, **Tkinter** e **Redis**, combinando uma API web para encurtamento de links com uma interface gráfica para fácil interação.  

## 🚀 Tecnologias Utilizadas  
- **Flask**: Framework web para criação da API REST para redirecionamento.  
- **Tkinter**: Interface gráfica para facilitar o uso do encurtador.  
- **Redis**: Banco de dados NoSQL utilizado para armazenar as URLs encurtadas e estatísticas de acesso.  

## 📌 Funcionalidades  
✅ **Encurtar URLs via interface gráfica** com Tkinter.  
✅ **Armazenamento em Redis** para URLs persistentes com tempo de expiração.  
✅ **Modo local (sem Redis)** para testes rápidos sem dependências externas.  
✅ **Redirecionamento automático** ao acessar uma URL encurtada.  
✅ **Exibição de estatísticas** como número de acessos e tempo de expiração da URL.  
✅ **Listagem das URLs encurtadas no modo local**.  

## 📂 Estrutura do Projeto  
```
📦 url-shortener  
 ┣ 📜 main.py      # Interface gráfica (Tkinter) para encurtar URLs  
 ┣ 📜 server.py    # Servidor Flask para redirecionamento  
 ┣ 📜 requirements.txt # Dependências do projeto  
 ┗ 📜 README.md    # Documentação do projeto  
```

## 🖥️ Como Executar  
### 1️⃣ Configurar o ambiente  
Certifique-se de ter o **Python 3** instalado. Em seguida, instale as dependências:  
```sh
pip install -r requirements.txt
```

Se for utilizar o Redis, certifique-se de que ele está instalado e rodando:  
```sh
docker run -d -p 6379:6379 redis
```

### 2️⃣ Iniciar o Servidor  
Para rodar o servidor Flask, execute:  
```sh
python server.py
```

### 3️⃣ Iniciar a Interface Gráfica  
Execute o seguinte comando para abrir a interface Tkinter:  
```sh
python main.py
```

---

## 🔍 Modo Local – Testes sem Redis  

O projeto inclui um **modo local** que permite encurtar URLs sem a necessidade do Redis, facilitando testes sem dependências externas. Esse modo armazena as URLs em um dicionário dentro do próprio programa, mantendo-as apenas durante a execução do software.  

### 📌 Como Funciona  

#### 🖥️ Armazenamento Local  
- No modo local, as URLs são armazenadas no dicionário `self.local_urls` dentro do **main.py**.  
- Cada URL encurtada recebe um **código único** gerado aleatoriamente.  
- Esse código é associado à URL original e armazenado junto com a data de criação e um contador de acessos.  

#### 🚀 Criação de URL Encurtada no Modo Local  
1. O usuário insere a URL na interface Tkinter.  
2. O programa gera um **código curto aleatório**.  
3. O código é armazenado no dicionário `self.local_urls`.  
4. A URL encurtada é exibida na interface e pode ser copiada.  
5. Todas as URLs encurtadas ficam listadas em um campo de texto.  

📌 **Exemplo de armazenamento local:**  
```python
self.local_urls[code] = {
    'url': original_url,
    'created_at': datetime.now(),
    'visits': 0
}
```

#### 🔄 Redirecionamento Local  
O servidor Flask (server.py) também suporta o modo local.  
Quando um usuário acessa uma URL encurtada localmente (`http://0.0.0.0:5000/local/<codigo>`), o Flask verifica o dicionário `local_urls` e faz o redirecionamento se a URL existir.  

📌 **Exemplo de redirecionamento local no Flask:**  
```python
@app.route('/local/<code>')
def redirect_local_url(code):
    if code in local_urls:
        local_urls[code]['visits'] += 1
        return redirect(local_urls[code]['url'])
    return "URL local não encontrada", 404
```

---

### 🔍 Diferenças entre os Modos  

| Modo | Armazenamento | Persistência | Estatísticas | Expiração |
|------|--------------|--------------|--------------|-----------|
| **Redis** | Redis | Sim | Sim | Sim |
| **Local** | Dicionário em memória | Não | Sim | Não |

📌 **O modo local é ideal para testes rápidos, mas não persiste URLs após o encerramento do programa.** Para URLs permanentes, utilize o Redis. 🚀  

---

## 📜 Licença  
Este projeto está sob a licença MIT.  

📌 **Contribuições são bem-vindas!** Sinta-se à vontade para abrir issues e pull requests. 🚀
