"""
A cultura da cana-de-açúcar se adapta muito bem às regiões de clima tropical,
quente e úmido, cuja temperatura predominante seja entre 19 e 32º C
e onde as chuvas sejam bem distribuídas,

As necessidades hídricas da cana-de-açúcar vão de 1.500 a 2.500 milímetros
aproximadamente 4000 a 6000 litros de água por hectare por dia - media 5000

O valor do pH em cloreto de cálcio deve ser de aproximadamente 6

Tipo de cana               duração dos ciclos
Cana de ano e meio         14 a 22 meses -> media 18 meses
cana de ano                12 meses
cana soca                  12 meses
cana de inverno            12 a 16 meses media -> 15 meses
"""
from random import uniform, randint
import os
import oracledb
import pandas as pd

tipoCana = ["Cana_de_ano_e_meio", "Cana_de_Ano", "Cana_Soca", "Cana_de_Inverno"]


def bancodedados():
    # Try para tentativa de Conexão com o Banco de Dados
    try:
        # Efetua a conexão com o Usuário no servidor
        conn = oracledb.connect(user='rm560575', password="fiap24", dsn='oracle.fiap.com.br:1521/ORCL')
        # Cria as instruções para cada módulo
        inst_cadastro = conn.cursor()
        inst_consulta = conn.cursor()
        inst_exclusao = conn.cursor()

    except Exception as e:
        # Informa o erro
        print("Erro: ", e)
        # Flag para não executar a Aplicação
        conexao = False
    else:
        # Flag para executar a Aplicação
        conexao = True
    while conexao:


        """
    BATCH_SIZE = 10000

    with conn.cursor() as cursor:

        # Predefine the memory areas to match the table definition.
        # This can improve performance by avoiding memory reallocations.
        # Here, one parameter is passed for each of the columns.
        # "None" is used for the ID column, since the size of NUMBER isn't
        # variable.  The "25" matches the maximum expected data size for the
        # NAME column
        cursor.setinputsizes(None, 25,255,255,255,255)

        with open(FILE_NAME, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            sql = "insert into test (tipoc_cana, mes,ano,temperatura,agua,indice_maturacao,valor_ph) values (:1, :2, :4, :5, :6, :7)"
            data = []
            for line in csv_reader:
                data.append((line[0], line[1]))
                if len(data) % BATCH_SIZE == 0:
                    cursor.executemany(sql, data)
                    data = []
            if data:
                cursor.executemany(sql, data)
            connection.commit()
        """

        os.system('cls')
        print("---MENU DO BANCO DE DADOS---\n")
        while True:
            try:
                print("Digite a oppção desejada:\n"
                      "1) Adcionar registro\n"
                      "2) listar registro\n"
                      "3) excluir registro\n"
                      "4) excluir tudo\n"
                      "0) Sair do progrma\n")
                opcao2 = int(input("Digite a opção escolhida: "))
            except ValueError:
                print("Digite um valor valido")
            else:
                if opcao2 == 1:
                    try:
                        print("----- GERAR ALEATORIO -----\n")
                        # gera os valores para cadastro
                        randomtemp = uniform(19.0, 32.0)
                        randommaturacao = uniform(0.01, 1.00)
                        randomagua = randint(15000, 20000)
                        randomph = randint(0, 14)
                        randommes = randint(1, 12)
                        randomano = randint(2024, 2050)
                        cana = randint(0, 3)
                        # Monta a instrução SQL de cadastro em uma string
                        cadastro = f""" INSERT INTO agro (tipo_cana, mes, ano, temperatura, agua, indice_maturacao, valor_ph)
                        VALUES ('{tipoCana[cana]}', {randommes}, {randomano}, {randomtemp:.3f
                        f"{randomagua},"
                        f"{randommaturacao:.3f},"
                        f"{randomph}\n")}) """
                        print(randomtemp, randommaturacao, randomagua, randomph, randommes, randomano, cana)
                        # Executa e grava o Registro na Tabela
                        inst_cadastro.execute(cadastro)
                        conn.commit()
                    except:
                        print("Erro na transação do BD")
                    else:
                        print("\nDados gravados")
                    input("Presione ENTER")

                elif opcao2 == 2:
                    lista_dados = []
                    inst_consulta.execute('SELECT * FROM agro')
                    data = inst_consulta.fetchall()
                    for dt in data:
                        lista_dados.append(dt)
                    lista_dados = sorted(lista_dados)
                    dados_df = pd.DataFrame.from_records(lista_dados,
                                                         columns=['id', 'tipo_cana', 'mes', 'Ano', 'Temperatura',
                                                                  'Agua',
                                                                  'Indice_Maturacao', 'Valor_PH'])
                    if dados_df.empty:
                        print(f"Não há dados no banco")
                    else:
                        print(dados_df)

                elif opcao2 == 3:
                    # EXCLUIR UM REGISTRO
                    lista_dados = []  # Lista para captura de dados da tabela
                    registro_id = input("Escolha um Id: ")  # Permite o usuário escolher um Pet pelo ID
                    if registro_id.isdigit():
                        pet_id = int(registro_id)
                        consulta = f""" SELECT * FROM agro WHERE id = {registro_id}"""
                        inst_consulta.execute(consulta)
                        data = inst_consulta.fetchall()

                        # Insere os valores da tabela na lista
                        for dt in data:
                            lista_dados.append(dt)

                        # Verifica se o registro está cadastrado
                        if len(lista_dados) == 0:
                            print(f"Não há um registro com o ID = {registro_id}")
                        else:
                            # Cria a instrução SQL de exclusão pelo ID
                            exclusao = f"DELETE FROM agro WHERE id={registro_id}"
                            # Executa a instrução e atualiza a tabela
                            inst_exclusao.execute(exclusao)
                            conn.commit()
                            print("\nregistro apagado")  # Exibe mensagem caso haja sucesso
                    else:
                        print("O Id não é numérico!")
                    input("Pressione ENTER")  # Pausa o loop para a leitura da mensagem

                elif opcao2 == 4:
                    # EXCLUIR TODOS OS REGISTROS

                    print("\nExlcuir todos os registros?\n")
                    confirma = input("CONFIRMA A EXCLUSÃO DE TODOS OS REGISTROS?[S]im ou [N]ÃO?")
                    if confirma.upper() == "S":
                        # Apaga todos os registros
                        exclusao = "DELETE FROM agro"
                        inst_exclusao.execute(exclusao)
                        conn.commit()

                        # Depois de excluir todos os registros ele zera o ID
                        data_reset_ids = """ ALTER TABLE agro MODIFY(ID GENERATED AS IDENTITY (START WITH 1)) """
                        inst_exclusao.execute(data_reset_ids)
                        conn.commit()

                        print("\nTodos os registros foram excluídos!")
                    else:
                        print("Operação cancelada pelo usuário!")
                    input("Pressione ENTER")  # Pausa o loop para a leitura da men

                elif opcao2 == 0:
                    sair_programa()
                else:
                    print("Digite um valor valido ")


def imprimir(canatupla,  listavariaveis):
    global tipoCana
    with open("arquivo.csv", "w") as arq:
        # imprime na primeira linha o que o usuario digitou no .txt
        arq.write(f"tipo_cana, mes, ano, temperatura, agua, indice_maturacao, valor_ph\n"
                  f"{tipoCana[canatupla]},"
                  f"{listavariaveis[0]},"
                  f"{listavariaveis[1]},"
                  f"{listavariaveis[2]},"
                  f"{listavariaveis[3]},"
                  f"0,"
                  f"0\n")
        # variaveis auxiliares pra ajudar a arrumar o numero do mes durante o for
        aux = listavariaveis[0]+1
        mes = listavariaveis[0]+12
        imprimeano = listavariaveis[1]
        umaVez = 0
        for x in range(aux, mes):
            # gerar valores aleatorios para a temp, indice de maturacao, agua e PH
            randomtemp = uniform(19.0, 32.0)
            randommaturacao = uniform(0.01, 1.00)
            randomagua = randint(15000, 20000)
            randomph = randint(0, 14)

            # auxiliares para arrumar o mes e o ano durante o for
            auxiliar = x
            imprimeMes = x
            if auxiliar > 12:
                imprimeMes = imprimeMes - 12
                if auxiliar > 12 and umaVez == 0:
                    umaVez = 1
                    imprimeano = imprimeano + 1
            # escreve no arquivo com os valores aleatorios
            arq.write(f"{tipoCana[canatupla]},"
                      f"{imprimeMes},"
                      f"{imprimeano},"
                      f"{randomtemp:.3f},"
                      f"{randomagua},"
                      f"{randommaturacao:.3f},"
                      f"{randomph}\n")


    print("Imprimindo em arquvio de nome arquivo.csv\n")
    bancodedados()


def calculodoindicematuracao(brixTopo, brixBase):
    indice = brixTopo/(brixBase*100)
    return indice


def perguntaindicematuracao():
    opcao2 = input("Deseja saber o indice de maturação da cana? S/N: ")
    if opcao2 == "s" or opcao2 == "S":
        brixTopo = int(input("Digite o brix do topo do colmo: "))
        brixBase = int(input("Digite o brix da base do colmo: "))
        return calculodoindicematuracao(brixTopo, brixBase)
    elif opcao2 == "n" or opcao2 == "N":
        return 0
    else:
        return 0


def canameioano():
    variaveiscana = []
    print("Digite a data do plantio das sementes da Cana de ano e meio ")
    mes, ano = pegardata()
    mesNovo = mes + 18
    while mesNovo > 12:
        mesNovo = mesNovo - 12
        anoNovo = ano + 1
    print(f"A data da proxima colheita será aproximadamente no: mes {mesNovo} e no ano: {anoNovo} ")
    aguaplantacao = 5000 * (18*30)
    print(f"Ira gastar aproximadamente {aguaplantacao} "
          f"litros de agua ao todo durante a plantação, sendo 5000 litros diarios em media ")
    indice = perguntaindicematuracao()
    print(f"A colheita deve ocorrer quando o indice de maturacao for igual a 1, o indice da plantaçao atual é: {indice}")
    # faz uma lista com as variaveis da cana para pode enviar para a funcao imprimir
    variaveiscana.append(mes)
    variaveiscana.append(ano)
    variaveiscana.append(float(input("Qual foi a temperatura durante o platio? ")))
    variaveiscana.append(int(input("Quanto de agua foi utilizado durante o plantio? Gasto mensal ")))
    print(variaveiscana)
    imprimir(0, variaveiscana)


def canaano():
    variaveiscana = []
    print("Digite o dia e o mes do plantio das sementes da Cana de ano\n")
    mes, ano = pegardata()
    # checa se o mes for passar de dezembro e arruma para o ano seguinte enquanto aumenta o ano em 1
    mesNovo = mes + 12
    while mesNovo > 12:
        mesNovo = mesNovo - 12
        anoNovo = ano + 1
    print(f"A data da proxima colheita será aproximadamente no: mes {mesNovo} e no ano: {anoNovo} ")
    aguaplantacao = 5000 * (12 * 30)
    print(f"Ira gastar aproximadamente {aguaplantacao} "
          f"litros de agua ao todo durante a plantação, sendo 5000 litros diarios")
    indice = perguntaindicematuracao()
    print(f"A colheita deve ocorrer quando o indice de maturacao for igual a 1, o indice da plantaçao atual é: {indice}")
    # faz uma lista com as variaveis da cana para pode enviar para a funcao imprimir
    variaveiscana.append(mes)
    variaveiscana.append(ano)
    variaveiscana.append(float(input("Qual foi a temperatura durante o platio? ")))
    variaveiscana.append(int(input("Quanto de agua foi utilizado durante o plantio? Gasto mensal ")))
    imprimir(1, variaveiscana)


def canasoca():
    variaveiscana = []
    print("Digite o dia e o mes do plantio das sementes da Cana soca\n")
    mes, ano = pegardata()
    mesNovo = mes + 12
    while mesNovo > 12:
        mesNovo = mesNovo - 12
        anoNovo = ano + 1
    print(f"A data da proxima colheita será aproximadamente no: mes {mesNovo} e no ano: {anoNovo} ")
    aguaplantacao = 5000 * (15 * 30)
    print(f"Ira gastar aproximadamente {aguaplantacao} "
          f"litros de agua ao todo durante a plantação, sendo 5000 litros diarios")
    indice = perguntaindicematuracao()
    print(f"A colheita deve ocorrer quando o indice de maturacao for igual a 1, o indice da plantaçao atual é: {indice}")
    # faz uma lista com as variaveis da cana para pode enviar para a funcao imprimir
    variaveiscana.append(mes)
    variaveiscana.append(ano)
    variaveiscana.append(float(input("Qual foi a temperatura durante o platio? ")))
    variaveiscana.append(int(input("Quanto de agua foi utilizado durante o plantio? Gasto mensal ")))
    imprimir(2, variaveiscana)


def canainverno():
    variaveiscana = []
    print("Digite o dia e o mes do plantio das sementes da Cana de inverno\n")
    mes, ano = pegardata()
    mesNovo = mes + 15
    while mesNovo > 12:
        mesNovo = mesNovo - 12
        anoNovo = ano + 1
    print(f"A data da proxima colheita será aproximadamente no: mes {mesNovo} e no ano: {anoNovo} ")
    aguaplantacao = 5000 * (15 * 30)
    print(f"Ira gastar aproximadamente {aguaplantacao} "
          f"litros de agua ao todo durante a plantação, sendo 5000 litros diarios")
    indice = perguntaindicematuracao()
    print(f"A colheita deve ocorrer quando o indice de maturacao for igual a 1, o indice da plantaçao atual é: {indice}")
    # faz uma lista com as variaveis da cana para pode enviar para a funcao imprimir
    variaveiscana.append(mes)
    variaveiscana.append(ano)
    variaveiscana.append(float(input("Qual foi a temperatura durante o platio? ")))
    variaveiscana.append(int(input("Quanto de agua foi utilizado durante o plantio? Gasto mensal ")))
    imprimir(3, variaveiscana)


def sair_programa():
    print("Fechando o programa...")
    exit()


def pegardata():
    while True:
        try:
            mes = int(input("Mes em numeros: "))
        except ValueError:
            print("Digite um mes valido")
        else:
            if mes < 1 or mes > 12:
                print("Digite um mes valido")
        try:
            ano = int(input("Ano em numeros: "))
        except ValueError:
            print("Digite um ano valido")
        return mes, ano


while True:
    try:
        print("Digite a cana que está sendo cultivada:\n"
              "1) Cana de ano e meio\n"
              "2) cana de ano\n"
              "3) cana soca\n"
              "4) cana de inverno\n"
              "5) direto pro Banco\n"
              "0) Sair do progrma\n")
        opcao1 = int(input("Digite a opção escolhida: "))
    except ValueError:
        print("Digite um valor valido")
    else:
        if opcao1 == 1:
            canameioano()
        elif opcao1 == 2:
            canaano()
        elif opcao1 == 3:
            canasoca()
        elif opcao1 == 4:
            canainverno()
        elif opcao1 == 5:
            bancodedados()
        elif opcao1 == 0:
            sair_programa()
        else:
            print("Digite um valor valido ")
