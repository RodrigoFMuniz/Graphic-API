import socket,psutil, time,  pickle, os
import cpuinfo





#Função principal

def main():

    # gera Socket
    host = socket.gethostname()
    porta = 8881
    servidor_endereco = (host, porta)
    servidor_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_tcp.bind(servidor_endereco)

    try:
        while True:
            #Aguarda conexão
            servidor_tcp.listen()
            print(f'Aguardando conexão do cliente\n')

            #Aceita conexão
            (cliente_tcp, cliente_endereco) = servidor_tcp.accept()
            print(f'Conectado ao cliente {cliente_endereco[0]}\n')

            #Recebe requisição do servidor
            cliente_arq = cliente_tcp.recv(2000)
            cliente_msg = pickle.loads(cliente_arq)
            print(cliente_msg)
            time.sleep(2)
            msg = pickle.dumps(f'\nConectado ao servidor')
            cliente_tcp.send(msg)
            time.sleep(2)
            cliente_req = cliente_tcp.recv(2000)
            cliente_requisicao = pickle.loads(cliente_req)
            print(f'Arquivo solicitado pelo processo cliente ==> {cliente_requisicao}\n')

            if cliente_requisicao == "memoria":
                lista = []
                cpu = psutil.cpu_percent()
                disco = psutil.disk_usage('.')
                memo = psutil.virtual_memory()
                netip = psutil.net_io_counters(pernic=True)
                interf = psutil.net_if_addrs()

                lista.append(cpu)
                lista.append(disco)
                lista.append(memo)
                lista.append(netip)
                lista.append(interf)
                fil = pickle.dumps(lista)
                time.sleep(2)
                cliente_tcp.send(fil)
                time.sleep(2)

            elif cliente_requisicao == "cpu":
                lista = []
                cpuinf = cpuinfo.get_cpu_info()
                cpu_percent = psutil.cpu_percent(percpu=True)
                cpufreqcurrent = psutil.cpu_freq().current
                cpufreqmax = psutil.cpu_freq().max
                cpucountf = psutil.cpu_count(logical=False)
                cpucount = psutil.cpu_count(logical=True)
                cpuper = psutil.cpu_percent()
                lista.append(cpuinf)
                lista.append(cpu_percent)
                lista.append(cpufreqcurrent)
                lista.append(cpufreqmax)
                lista.append(cpucountf)
                lista.append(cpucount)
                lista.append(cpuper)
                fil = pickle.dumps(lista)
                time.sleep(2)
                cliente_tcp.send(fil)
                time.sleep(2)


            elif cliente_requisicao == "arquivos":
                f = os.listdir('.')
                fil = pickle.dumps(f)
                cliente_tcp.send(fil)
                time.sleep(2)

            elif cliente_requisicao == "processos":
                f = psutil.pids()
                fil = pickle.dumps(f)
                cliente_tcp.send(fil)
                time.sleep(2)

            elif cliente_requisicao == "redes":
                f = psutil.net_if_addrs()
                fil = pickle.dumps(f)
                cliente_tcp.send(fil)
                time.sleep(2)

            else:
                main()




    except Exception as err:
        print(f'Erro: {str(err)}')
        servidor_tcp.close()
        main()


if __name__ == "__main__":
    main()




