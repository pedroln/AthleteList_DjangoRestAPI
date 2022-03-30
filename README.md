<h2> DESAFIO - REST API - PYTHON/DJANGO REST FRAMEWORK </h2>

<h3>Requisitos que foram feitos com sucesso: </h3>

- Upload do CSV para popular a base de dados da aplicação, sem repetições.

- Criação dos modelos que guardam as informações do CSV na base de dados.

- Listagem Geral e Filtrada(GET - Paginada), Criação(POST), Atualização(PUT), Deleção(PUT) de um Atleta.

- Filtragem de Atleta (Paginada) por todos os seus campos ('id', 'Name', 'Sex', 'Age', 'Height', 'Weight', 'Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal')

- Validaçoes adicionais ao adicionar ou atualizar um atleta.

<h3> INFORMAÇÕES IMPORTANTES </h3>

<h5> 

- Foi se utilizado a database SQLIte (já contida em projetos Django) para guardar os modelos Atletas e Regiões (E populado com os dois CSV que constavam nos links).

- Todos os testes de rotas foram feitos usando as rotas especificadas via postman, também se pode testar as rotas a partir do seu navegador, abaixo estará informado em qual link estará rodando o servidor.

- As exceções e validações construídas foram feitas a partir de um estudo de cada campo do CSV. </h5>

<h3> COMO RODAR O PROGRAMA </h3>

<h5>

- Para iniciar a API, basta abrir o terminal na pasta raiz da API e rodar o comando. </h5>
<blockquote> "python manage.py runserver" </blockquote>

<h5>
  
- Após este comando, o servidor estará rodando em: </h5>
<blockquote> "localhost:8000" </blockquote>

<h5> 
  
- Abaixo está listado as rotas e os bodys em JSON (para as requisições que exigem uma inserção do mesmo) de modo que a requisição seja feita com sucesso para cada requisito (e também para dar trigger em cada exceção/validação que foi criada)</h5>

<h3> ATENÇÃO - PRIMEIRAMENTE É NECESSÁRIO POVOAR A BASE DE DADOS A PARTIR DOS CSV OFERECIDOS, LOGO, ANTES DE QUALQUER TESTE DAS OUTRAS ROTAS, FAZER ESTAS REQUISIÇÕES AO SERVIDOR </h3>

  - Já que havia muitas informações no CSV utilizado, foi se utilizada a estratégia de Bulk-Loading para carregar o CSV, para otimizar a velocidade de povoamento no banco de dados.
  
  - <strong>POVOAR A BASE DE DADOS DOS ATLETAS - ROTA - POST</strong>
    <blockquote> "localhost:8000/athletes/uploadAthletes" </blockquote>
    
    Se estiver utilizando um navegador, vá a 
    <blockquote> "localhost:8000/athletes/uploadAthletes" </blockquote>
    no campo File, clique em escolher arquivo e selecione o arquivo CSV que se encontra na pasta raiz
    <blockquote> "athlete_events.csv" </blockquote>
    após isso, clicar no botão inferior direito POST, após alguns segundos (pois o CSV é extenso) a base de dados de atletas estará povoada e retornará o status
    <blockquote> {
    "status": "Atletas adicionados ao banco de dados com sucesso"
    } </blockquote>
    
  - <strong>POVOAR A BASE DE DADOS DAS REGIÕES DOS ATLETAS - ROTA - POST</strong>
    <blockquote> "localhost:8000/athletes/uploadRegions" </blockquote>
    
    Se estiver utilizando um navegador, vá a 
    <blockquote> "localhost:8000/athletes/uploadRegions" </blockquote>
    no campo File, clique em escolher arquivo e selecione o arquivo CSV que se encontra na pasta raiz
    <blockquote> "noc_regions.csv" </blockquote>
    após isso, clicar no botão inferior direito POST, após alguns segundos a base de dados das regiões dos atletas estará povoada.
    <blockquote> {
    "status": "Regiões adicionadas ao banco de dados com sucesso"
    } </blockquote>
  

<h3> AGORA QUE A BASE DE DADOS JÁ ESTÁ POVOADA POR COMPLETO, AS SEGUINTES ROTAS PODEM SER TESTADAS </h3>

  - <strong>LISTAGEM DE ATLETAS COM FILTRO - ROTA - GET</strong> 
    <blockquote>localhost:8080/athletes/getAthletes</blockquote>
  
    Se estiver utilizando um navegador, vá a 
    <blockquote> localhost:8000/athletes/getAthletes </blockquote>
    Caso a base de dados dos atletas já esteja povoada, será listado todos os atletas de forma paginada (de 50 em 50), há também o botão Filters, permitindo filtrar a     lista de atletas de diversos modos, retornando atletas apenas com as informações inseridas.

  - <strong> ADIÇÃO DE ATLETA - ROTA - POST</strong> 
    <blockquote>localhost:8080/athletes/postAthlete</blockquote>
  
    Se estiver utilizando um navegador, vá a 
    <blockquote> localhost:8000/athletes/postAthlete </blockquote>
    no espaço Content, adicione o seguinte exemplo de requisição em JSON para adicionar um Atleta com sucesso
    <blockquote> 
           
            {
            "Name": "Atleta Teste",
  
            "Sex": "M",
  
            "Age": "24",
  
            "Height": "180",
  
            "Weight": "80",
  
            "Team": "Brazil",
  
            "NOC": "BRA",
  
            "Games": "1992 Summer",
  
            "Year": 1992,
  
            "Season": "Summer",
  
            "City": "Barcelona",
  
            "Sport": "Basketball",
  
            "Event": "Basketball Men's Basketball",
  
            "Medal": "Gold" 
            }
      </blockquote>
 
      Se nenhum atleta já tiver as exatas informações inseridas na requisição, um novo atleta será inserido com estas informações na base de dados, junto com um ID           único
      
      <strong>POSSÍVEIS EXCEÇÕES:</strong>
      - Se já possuir um atleta com as exatas informações inseridas na requisição, irá retornar erro com 400 com a seguinte mensagem: "Atleta com estas informações já      está inserido na base de dados"
      - Se o campo "Sex" tiver o valor diferente de "M" ou "F", irá retornar erro 400 com a seguinte mensagem: "Sexo inserido inválido, necessário que o sexo inserido       seja Masculino (M) ou Feminino(F)"
      - Se o campo "Medalha" tiver o valor diferente de "Gold","Silver","Bronze" ou "nan", irá retornar erro 400 com a seguinte mensagem: "Tipo de Medalha inserida           inválida, necessário que a medalha inserida seja Ouro(Gold), Prata(Silver) ou Bronze(Bronze) ou Nenhuma Medalha(nan)"
      - Se o campo "Year" tiver o valor maior do que o ano atual (2022), irá retornar o erro 400 com a seguinte mensagem: "Ano inserido inválido, necessário que o ano       inserido seja menor ou igual ao ano atual (2022)"
      - Se o campo "Season" tiver o valor diferente de "Summer" ou "Winter", irá retornar o erro 400 com a seguinte mensagem: "Estação dos Jogos inserida inválida,           necessário que seja Verão(Summer) ou Inverno(Winter)"
      - Se a sigla da nacionalidade "NOC" não constar no campo "NOC" do CSV de regiões (noc_regions.csv), irá retornar o erro 400 com a seguinte mensagem: "Sigla da         nacionalidade inserida inválida, para saber qual siglas são aceitas na nacionalidade, checar o arquivo noc_regions.csv (campo NOC)"
      - Se a região do time "Team" não constar no campo "Region" do CSV de regiões (noc_regions.csv), irá retornar o erro 400 com a seguinte mensagem: "Região inserida       inválida, para saber qual siglas são aceitas na nacionalidade, checar o arquivo noc_regions.csv (campo Region)"
     
  - <strong> UPDATE DE ATLETA - ROTA - PUT</strong> 
    <blockquote>localhost:8080/athletes/updateAthlete/"idDoAtleta"</blockquote>
  
    Se estiver utilizando um navegador, vá a 
    <blockquote> localhost:8000/athletes/updateAthlete/"idDoAtleta" </blockquote>
    sendo o campo "idDoAtleta" um ID válido de um atleta que consta na base de dados (pode se usar o ID de numero 1 para dar um caso de sucesso).
    
    No espaço Content, adicione o seguinte exemplo de requisição em JSON para atualizar um Atleta com sucesso
    <blockquote> 
           
            {
            "Name": "Atleta Teste Update",
  
            "Sex": "M",
  
            "Age": "25",
  
            "Height": "180",
  
            "Weight": "80",
  
            "Team": "Brazil",
  
            "NOC": "BRA",
  
            "Games": "1992 Summer",
  
            "Year": 1992,
  
            "Season": "Summer",
  
            "City": "Barcelona",
  
            "Sport": "Basketball",
  
            "Event": "Basketball Men's Basketball",
  
            "Medal": "Gold" 
            }
      </blockquote>
 
      Se nenhum atleta já tiver as exatas informações inseridas na requisição, o atleta do ID correspondente ao inserido na requisição terá suas informações                 atualizadas no banco de dados
      
      <strong>POSSÍVEIS EXCEÇÕES:</strong>
      - Se já possuir um atleta com as exatas informações inseridas na requisição, irá retornar erro com 400 com a seguinte mensagem: "Atleta com estas informações já       está inserido na base de dados"
      - Se o campo "Sex" tiver o valor diferente de "M" ou "F", irá retornar erro 400 com a seguinte mensagem: "Sexo inserido inválido, necessário que o sexo inserido       seja Masculino (M) ou Feminino(F)"
      - Se o campo "Medalha" tiver o valor diferente de "Gold","Silver","Bronze" ou "nan", irá retornar erro 400 com a seguinte mensagem: "Tipo de Medalha inserida           inválida, necessário que a medalha inserida seja Ouro(Gold), Prata(Silver) ou Bronze(Bronze) ou Nenhuma Medalha(nan)"
      - Se o campo "Year" tiver o valor maior do que o ano atual (2022), irá retornar o erro 400 com a seguinte mensagem: "Ano inserido inválido, necessário que o ano       inserido seja menor ou igual ao ano atual (2022)"
      - Se o campo "Season" tiver o valor diferente de "Summer" ou "Winter", irá retornar o erro 400 com a seguinte mensagem: "Estação dos Jogos inserida inválida,           necessário que seja Verão(Summer) ou Inverno(Winter)"
      - Se a sigla da nacionalidade "NOC" não constar no campo "NOC" do CSV de regiões (noc_regions.csv), irá retornar o erro 400 com a seguinte mensagem: "Sigla da         nacionalidade inserida inválida, para saber qual siglas são aceitas na nacionalidade, checar o arquivo noc_regions.csv (campo NOC)"
      - Se a região do time "Team" não constar no campo "Region" do CSV de regiões (noc_regions.csv), irá retornar o erro 400 com a seguinte mensagem: "Região inserida       inválida, para saber qual siglas são aceitas na nacionalidade, checar o arquivo noc_regions.csv (campo Region)"

  - <strong> DELEÇÃO DE ATLETA - ROTA - DELETE</strong> 
    <blockquote>localhost:8080/athletes/deleteAthlete/"idDoAtleta"</blockquote>
    
    Se estiver utilizando um navegador, vá a 
    <blockquote> localhost:8000/athletes/deleteAthlete/"idDoAtleta" </blockquote>
    sendo o campo "idDoAtleta" um ID válido de um atleta que consta na base de dados (pode se usar o ID de numero 1 para dar um caso de sucesso).
    
    Na tela que aparecer, basta clicar no botão Delete, no canto superior direito e confirmar a deleção, se o ID do atleta for correspondente a algum inserido na base     de dados, o atleta será deletado e retornará a mensagem "Apagado".
    
    <strong>POSSÍVEIS EXCEÇÕES:</strong>
    - ValueError: Caso o "idDoAtleta" inserido na requisição não for do tipo inteiro.
    - DoesNotExist: Caso o "idDoAtleta" inserido na requisição não existir correspondente na base de dados.
    
    
    
