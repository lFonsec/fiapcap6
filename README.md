
# Cap 6 - Python e além

Um sistema para uma empresa agro com um databse oracle

## Ideia
a ideia inicial era criar um sistema em que a maior parte do seu funcionamento era automatizado, o usuario só adcionaria a primeira inserção nos registros, após essa inserção o sistema iria se auto preencher utilizando os sensores, tanto que eu não fiz a parte de alteração de dados para o banco de dados
por que o usuario apenas checaria ou deletaria os registros, por que a parte de inserção seria automatizada, para isso eu fiz os valores serem gerado aleatoriamente

O programa começa perguntando ao usuario qual tipo de cana que ele está cultivando, após isso é perguntado  sobre o mes e o ano do plantio, que o sistema da uma estimativa para a colheita dependendo da especie da cana, pergunta o quanto de agua que que foi gasto durante o mes do plantio, a temperatura média do mes do plantio, pergunta se ele quer medir o indice de maturação, eo valor do ph, depois dessas perguntas o sistema gera um arquivo .csv com os  valores de cada mes até o mes da colheita estipulada com os valores gerados aleatoriamente, após o arquivo ser gerado ele, uma outra função iria carregar eeste arquivo no banco de dados(Arrumar), após esta incerção viria a pergunta sobre o banco de dados, se o usuario queria adcionar um novo registro que seria uma simulação do sistema adcionando os valroes pego pelos sensores, visulizar todos os registros ou excluindo 1 ou todos os registros
