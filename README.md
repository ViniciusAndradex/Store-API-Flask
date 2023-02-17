# API Store

API cria em flask que simula a criação de uma loja, podendo adicionar items a mesma.

Foram criados 10 endpoints para a execução correta:
  - Tipo de requisição | rota
  1. get_store
  2. get_store/{id}
  3. post_store<br>
    Json:
      ```
      {
        "name": "string"
      }
      ```
  4. delete_store/{id}
  5. put_store/{id}<br>
    Json:
      ```
      {
        "name": "string"
      }
      ```   
 ##
  
  1. get_item
  2. get_item/{id}
  3. post_item<br>
    Json:
      ```
      {
        "name": "stiring",
        "price": 0,
        "store_id": 0
      }
      ```
  4. delete_item/{id}
  5. put_item/{id}
    Json:
      ```
      {
        "name": "string",
        "price": 0
      }
      ```

Podendo assim executar a simulação corretamente, os endpoints foram testados através do insomnia.

## Passo a passo para rodar a API

#### 1. Entrar no terminal de comando, se direcionar para a pasta onde o repositório foi clonoado e rodar o comando:
```venv -m venv```
_Desta forma você está criando o seu ambiente virtual python._

#### 2. Ativar o seu ambiente python no terminal:
```. venv/bin/activate```

#### 3. Ligar a sua API com o comando:
```flask run```

### Observação

*A API possui uma documentação para ter acesso a mesma acesse no seu navegador:*
#### http://localhost:5000/store-api
