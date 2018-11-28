import pygame, psutil, socket, os, pickle
import time

def uso_cpu_mem_disc_ip(cpu, disco, memo, netip, interf ):

    pygame.init()

    preto = (0, 0, 0)
    branco = (255, 255, 255)
    azul = (0, 0, 255)
    vermelho = (255, 0, 0)

    largura_tela = 1000
    altura_tela = 430
    tela = pygame.display.set_mode((largura_tela, altura_tela))
    pygame.display.set_caption('Informações sobre RAM - DISCO - CPU - IP')
    pygame.display.init()

    pygame.font.init()

    fonte = pygame.font.Font(None, 26)

    clock = pygame.time.Clock()

    def uso_cpu():
        tela.fill(preto)
        usocpu = cpu
        larguracpu = largura_tela - 2*20
        pygame.draw.rect(tela, azul, (10, 60, larguracpu, 70))
        larguracpu = larguracpu * (usocpu/100)
        pygame.draw.rect(tela, vermelho,(10, 60, larguracpu, 70))
        text_mem = (f'Uso de CPU é de {usocpu} %) ')
        text = fonte.render(text_mem, 1, preto)
        tela.blit(text, (10, 35))
        text = fonte.render(text_mem, 1, branco)
        tela.blit(text, (10, 35))


    def uso_disco():

        usomemoria = disco
        larguramem = largura_tela - 2*20
        pygame.draw.rect(tela, azul, (10, 260, larguramem, 70))
        larguramem = larguramem * (usomemoria.percent/100)
        pygame.draw.rect(tela, vermelho,(10, 260, larguramem, 70))
        totalmemgb = round((usomemoria.total / (1024 * 1024 * 1024)), 2)
        usada = round(usomemoria.used / (1024 * 1024 * 1024), 2 )
        text_mem = (f'Uso de memória secundária - Total:  {totalmemgb} GB | Em uso: {usada} GB ({usomemoria.percent} %) ')
        text = fonte.render(text_mem, 1, preto)
        tela.blit(text, (10, 240))
        text = fonte.render(text_mem, 1, branco)
        tela.blit(text, (10, 240))

    def mostra_memoria():
        mem = memo
        largura = largura_tela - 2*20
        pygame.draw.rect(tela, azul, (10, 160, largura, 70))
        largura = largura * (mem.percent/100)
        pygame.draw.rect(tela, vermelho, (10, 160, largura, 70))
        total = round(mem.total / (1024 * 1024 * 1024), 2)
        usada = round(mem.used / (1024 * 1024 * 1024), 2 )
        texto_barra = (f'Uso de Memória RAM- Total: {total}GB | Em uso: {usada}GB ({mem.percent})%')
        text = fonte.render(texto_barra, 1, branco)
        tela.blit(text, (10, 140))


    def ipmachine():
        network = netip
        net_interface = interf
        networks = list()
        for k, v in net_interface.items():
            mac = v[0].address
            ip = v[1].address
            data = network[k]
            net = dict()
            net['mac'] = mac
            net['Interface'] = k
            env = round((data.bytes_sent / (1024 * 1024)), 2)
            networks.append(net)
            if env != 0:
                return (ip)

    def ipdisplay():

        text_ip = (f'O IP em uso é {ipmachine()}')
        text = fonte.render(text_ip, 1, branco)
        tela.blit(text, (350, 360))

    cont = 60
    terminou = False

    while not terminou:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminou = True
        if cont == 60:
            uso_cpu()
            uso_disco()
            mostra_memoria()
            ipdisplay()
            cont = 0

        pygame.display.update()

        clock.tick(60)
        cont += 1

    pygame.display.quit()
    pygame.quit()



def cpu_info(cpuinf, cpu_percent, cpufreqcurrent, cpufreqmax, cpucountf, cpucount, cpuper):
    pygame.init()

    info_cpu = cpuinf
    inf = cpu_percent

    preto = (0, 0, 0)
    branco = (255, 255, 255)
    azul = (0, 0, 255)
    vermelho = (255, 0, 0)
    cinza = (100, 100, 100)

    largura_tela = 1000
    altura_tela = 400
    tela = pygame.display.set_mode((largura_tela, altura_tela))
    pygame.display.set_caption('Informações da CPU')
    pygame.display.init()

    s1 = pygame.Surface((largura_tela, altura_tela))
    s2 = pygame.Surface((largura_tela, altura_tela/2))

    pygame.font.init()

    fonte = pygame.font.Font(None, 26)

    clock = pygame.time.Clock()


    def mostra_texto(s1, nome, chave,pos_x, pos_y):
        text = fonte.render(nome, True, preto)
        s1.blit(text, (10, pos_y))
        if chave == 'freq':
            s = (f'{round(cpufreqcurrent, 2)}')
        elif chave == 'nucleos':
            s = (f'Físicos: {cpucountf} | Lógicos: {cpucount}')
        elif chave == 'freqmax':
            s = (f'{cpufreqmax}')
        else:
            s = (f'{(info_cpu[chave])}')
        text = fonte.render(s, True, cinza)
        s1.blit(text, (pos_x, pos_y))


    def informacao_cpu():
        s1.fill(branco)
        mostra_texto(s1, "Nome:", "brand", 225,  10)
        mostra_texto(s1, "Arquitetura:", "arch", 225,  30)
        mostra_texto(s1, "Palavra (bits):", "bits", 225,  50)
        mostra_texto(s1, "Frequência (MHz):", "freq",225, 70)
        mostra_texto(s1, 'Frequência Max (Mhz):', 'freqmax', 225, 90)
        mostra_texto(s1, "Núcleos(físicos | lógicos):", "nucleos",225,  110)
        tela.blit(s1, (0, 0))

    def grafico_nucleos(s, l_cpu_percent):
      s.fill(cinza)
      num_cpu = len(l_cpu_percent)
      alt = s.get_height() - 20
      larg = ((s.get_width()-20) - ((num_cpu+1)*10))/num_cpu
      d = 20
      for i in l_cpu_percent:
          pygame.draw.rect(s, vermelho, (d, 10, larg, alt))
          pygame.draw.rect(s, azul, (d, 10, larg, (1-(i/100))*alt))
          d = d + larg + 10
      # parte mais abaixo da tela e à esquerda
      tela.blit(s, (0, altura_tela/2))


    def texto_cores():
        cpu = cpuper
        texto = (f'* Gráfico de uso de cada core do CPU (físico e lógico) em ordem sequencial. Uso total da CPU em : {cpu} %')
        text = fonte.render(texto, 1, preto)
        tela.blit(text, (0, 155))

    cont = 60
    terminou = False

    while not terminou:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminou = True
        if cont == 60:
            informacao_cpu()
            grafico_nucleos(s2, inf)
            texto_cores()
            cont = 0

        pygame.display.update()

        clock.tick(60)
        cont += 1

    pygame.display.quit()
    pygame.quit()



def checagem_dados(x):

    listadir = x
    dicionario = {}
    for l in listadir:
        if os.path.isfile(l):
            dicionario[l] = []
            dicionario[l].append(os.stat(l).st_size) # Tamanho do arquivo
            dicionario[l].append(os.stat(l).st_atime) # data de criação do arquivo
            dicionario[l].append(os.stat(l).st_mtime) # Data de Modificação do arquivo
            dicionario[l].append(f'Arquivo') #tipo arquivo
            dicionario[l].append(os.path.abspath(l)) # caminho absoluto do arquivo


        else:
            dicionario[l] = []
            dicionario[l].append(os.stat(l).st_size) # Tamanho da pasta
            dicionario[l].append(os.stat(l).st_atime) # data de criação da pasta
            dicionario[l].append(os.stat(l).st_mtime) # Data de Modificação da pasta
            dicionario[l].append(f'Pasta') # Tipo Pasta
            dicionario[l].append(os.path.abspath(l)) # caminho absoluto da pasta

# O código abaixo imprime o título das colunas
    titulo = '{:31}'.format("Nome")
    titulo = titulo + '{:11}'.format("Tamanho")
    titulo = titulo + '{:27}'.format("Data de Modificação")
    titulo = titulo + '{:27}'.format("Data de Criação")
    titulo = titulo + '{:10}'.format('Tipo')
    titulo = titulo + '{:50}'.format('Caminho')
    print(titulo)

# O loop abaixo serve para imprimir na tela os dados referentes as colunas, já formatadas
    for i in dicionario:
        kb = dicionario[i][0]/1000
        tamanho = '{:10}'.format(str('{:.2f}'.format(kb)+' KB'))
        nome = '{:30}'.format(i)
        tipo = '{:9}'.format(dicionario[i][3])
        caminho = '{:50}'.format(dicionario[i][4])
        print(nome, tamanho, time.ctime(dicionario[i][2]), " ", time.ctime(dicionario[i][1]), " ", tipo, caminho)


def mostra_info_system(x):
    try:
        # A variável titulo acumula os valores de string que formarão os titulos das colunas
        titulo = '{:37}'.format('PID - Nome do processo')
        titulo = titulo + '{:22}'.format('Número do Processo')
        titulo = titulo + '{:31}'.format('Data de criação')
        titulo = titulo + '{:20}'.format('Uso % da CPU')
        titulo = titulo + '{:20}'.format('Uso de memória')
        print(titulo) # imprime os valores acumulados em titulo
        processo = x # armazena na var processo todos os valores de processo adquiridos por pids
        for proc in processo: # Realiza a leitura individual de cada item armazenado na var processo
            p = psutil.Process(proc) # Aplica o método Process a cada item dentro da var processo
            texto = '{:40}'.format(str(p.name())) # Armazena na var texto o nome do processo
            texto = texto + '{:15}'.format(p.pid) +"    " # Armazena na var texto o número do processo
            texto = texto + time.ctime(p.create_time()) + " " # Armazena na var texto a data de criação do processo
            texto = texto + '{:10.2f}'.format(p.memory_percent()) +'%' # Armazena na var texto o percentual de uso da CPU pelo processo
            rss = p.memory_info().rss / (1024 * 1024) # Armazena na var texto o valor da parcela de memória principal usada pelo processo em MB
            texto = texto + '{:26.2f}'.format(rss) + " MB"
            print(texto)# imprime todas as informações acima de forma concatenada ( em linha )
    except:
        pass



def dados_redes(x):
    redes = x # adquirindo dados das redes disponíveis
    nomes = [] # Criando recipiente de armazenagem dos dados

    #Imprimindo linearmente os títulos das colunas
    titulo ='{:30}'.format('Nome da rede') + " "
    titulo = titulo + '{:19}'.format('Physical Address') + " "
    titulo = titulo + '{:19}'.format('IPV4') + " "
    titulo = titulo + '{:39}'.format('IPV6') + " "
    titulo = titulo + 'Netmask'
    print(titulo)

    for i in redes:
        if i != 'Loopback Pseudo-Interface 1': #Separando redes que não quero que apareçam
            nomes.append(i)
    for i in nomes: # Cotando os dados que creio serem relevantes ao desenvolvimento do trabalho.
        texto ='{:30}'.format(i) + " " #Nome da rede
        texto = texto + '{:20}'.format(redes[i][0].address)#Endereço físico MAC Address
        texto = texto + '{:20}'.format(redes[i][1].address)# IPV4
        texto = texto + '{:40}'.format(redes[i][2].address)# IPV6
        texto = texto + '{:25}'.format(redes[i][1].netmask)# Netmask
        print(texto) # Impressão linear dos dados de preenchimento das colunas, já formatados


#Manipulação de listas de seleção. Código mais limpo.

def opcao(opcao):


    if opcao == "1":
        return 'memoria'
    elif opcao == "2":
        return 'cpu'
    elif opcao == "3":
        return 'arquivos'
    elif opcao == "4":
        return 'processos'
    elif opcao == "5":
        return 'redes'
    elif opcao == "6":
        return 'sair'
    else:
        print(f'Opção inválida. Escolha uma das opções válidas.\n')
        main()


def requisicao(entrada, cliente):

    if entrada == "memoria":
        solicitacao = pickle.dumps(entrada)
        cliente.send(solicitacao)
        time.sleep(3)
        resposta = cliente.recv(100000000)
        retorno = pickle.loads(resposta)
        cpu = retorno[0]
        disco = retorno[1]
        memo = retorno[2]
        netip = retorno[3]
        interf = retorno[4]
        uso_cpu_mem_disc_ip(cpu, disco, memo, netip, interf )
        return print(f'Finalizando a aplicação gráfica.\nObrigado por utilizar nosso sistema.')

    elif entrada == "cpu":
        solicitacao = pickle.dumps(entrada)
        cliente.send(solicitacao)
        time.sleep(3)
        resposta = cliente.recv(100000000)
        retorno = pickle.loads(resposta)
        cpuinf = retorno[0]
        cpu_percent = retorno[1]
        cpufreqcurrent = retorno[2]
        cpufreqmax = retorno[3]
        cpucountf = retorno[4]
        cpucount = retorno[5]
        cpuper = retorno[6]
        cpu_info(cpuinf, cpu_percent, cpufreqcurrent, cpufreqmax, cpucountf, cpucount, cpuper)
        return print(f'Finalizando a aplicação gráfica.\nObrigado por utilizar nosso sistema.')

    elif entrada == "arquivos":
        solicitacao = pickle.dumps(entrada)
        cliente.send(solicitacao)
        time.sleep(3)
        resposta = cliente.recv(10000000)
        retorno = pickle.loads(resposta)
        return retorno

    elif entrada == "processos":
        solicitacao = pickle.dumps(entrada)
        cliente.send(solicitacao)
        time.sleep(3)
        resposta = cliente.recv(10000000)
        retorno = pickle.loads(resposta)
        return retorno

    elif entrada == "redes":
        solicitacao = pickle.dumps(entrada)
        cliente.send(solicitacao)
        time.sleep(3)
        resposta = cliente.recv(10000000)
        retorno = pickle.loads(resposta)
        return retorno

    elif entrada == "sair":
        print(f'\nObrigado por utilizar nosso sistema.')
        return cliente.close()

    else:
        main()





def main():
    #gera Socket
    host = socket.gethostname()
    porta = 8881
    endereco = (host, porta)
    cliente_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    #Conexão com o servidor
    cliente_tcp.connect(endereco)
    solicitacao = pickle.dumps('Cliente solicitando conexão para transfeência de arquivos')
    cliente_tcp.send(solicitacao)
    time.sleep(2)
    conn_ans = cliente_tcp.recv(1024)
    conn_accept = pickle.loads(conn_ans)
    print(conn_accept)
    # input do operador para seleção de arquivo)

    print("\nBem vindo, escolha uma das opções. Selecione o número correspontente: ")
    print("1 - Memória") # retorna 'memoria'
    print("2 - CPU e sistema")# retorna 'cpu'
    print("3 - Arquivos locais ")# retorna 'arquivo'
    print("4 - Processos")# retorna 'processo'
    print("5 - Redes")# retorna 'redes'
    print("6 - Sair")# retorna 'sair'
    entrada = input(f'\nEscolha uma das opções. Selecione o número correspontente --> ')
    if entrada != '1' and  entrada != '2' and  entrada != '3' and  entrada != '4' and entrada != '5' and entrada != '6':
        print(f'Valor de entrada errado. Por favor digite uma das opções abaixo: ')
        cliente_tcp.close()
        main()
    else:
        escolha = opcao(entrada)

    #conexão e troca de dados
    try:
        if escolha != 'cpu' and escolha != 'memoria':
            x = requisicao(escolha, cliente_tcp)
            time.sleep(2)
            if escolha == 'arquivos':
                print('')
                checagem_dados(x)
                main()
            if escolha == 'redes':
                print('')
                dados_redes(x)
                main()
            if escolha == 'processos':
                print('')
                mostra_info_system(x)
                main()

        elif escolha == 'cpu':
            print(f'Iniciando a aplicação gráfica\n')
            requisicao(escolha, cliente_tcp)
            main()

        elif  escolha == 'memoria':
            print(f'Iniciando a aplicação gráfica\n')
            requisicao(escolha, cliente_tcp)
            main()
        else:
            cliente_tcp.close()
            main()

            
    except Exception as err:
        print(f'Erro: {str(err)} ')
        cliente_tcp.close() #fecha conexão com o servidor
        main()



if __name__=="__main__":
    main()
