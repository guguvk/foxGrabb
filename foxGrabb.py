#!/usr/share/python3

# foxgrabb v1.0, Author @guguvk (Axel González)

import socket, signal, argparse

signal.signal(signal.SIGINT, signal.SIG_DFL)

parser = argparse.ArgumentParser()
parser.add_argument("-t","--target",help="target",required=True)
parser.add_argument("-p","--ports",help="puerto o puertos",required=True)
args = parser.parse_args()

ports = list(map(int,args.ports.split(",")))


for port in ports:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            response = s.connect_ex((args.target, port))
            if response == 0:
                if port == 80:
                    rsp = "HEAD / HTTP/1.1\r\nHost: %s\r\n\r\n" % args.target
                    s.send(rsp.encode())
                banner = s.recv(4096)
                message = "\n[*] Port: %s Open\n\n" % port
                try:
                    message += banner.strip().decode()
                except UnicodeDecodeError:
                    message += "Respuesta en binario, no se puede leer"
                print("%s\n" % message)
            else:
                print("\n[*] Port: %s Closed" % port)
    except socket.gaierror:
        print("Error: No se pudo resolver el nombre del host.")
    except ConnectionRefusedError:
        print("Error: La conexión fue rechazada.")
    except TimeoutError:
        print("Error: Se alcanzó el tiempo de espera.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")


