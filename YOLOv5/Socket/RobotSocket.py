import socket
from _thread import *

client_sockets = [] # ������ ������ Ŭ���̾�Ʈ ���

# ���� IP �� ������ ��Ʈ
HOST = '127.0.0.1'
PORT = 2524

# ���� ���� ����
print('>> Server Start')
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()



# �����忡�� ����Ǵ� �ڵ��Դϴ�.
# ������ Ŭ���̾�Ʈ���� ���ο� �����尡 �����Ǿ� ����� �ϰ� �˴ϴ�.
# �ش� �κп��� ���ǿ� �´� ���� �����ֵ��� �����ϱ�
def threaded(client_socket, addr):
    print('>> Connected by :', addr[0], ':', addr[1])

    # Ŭ���̾�Ʈ�� ������ ���� �� ���� �ݺ��մϴ�.
    while True:

        try:

            # �����Ͱ� ���ŵǸ� Ŭ���̾�Ʈ�� �ٽ� �����մϴ�.(����)
            data = client_socket.recv(1024)

            if not data:
                print('>> Disconnected by ' + addr[0], ':', addr[1])
                break

            print('>> Received from ' + addr[0], ':', addr[1], data.decode())

            # ������ ������ Ŭ���̾�Ʈ�鿡�� ä�� ������
            # �޼����� ���� ������ ������ ������ ������ Ŭ���̾�Ʈ���� �޼��� ������
            for client in client_sockets :
                if client != client_socket :
                    client.send(data)

        except ConnectionResetError as e:
            print('>> Disconnected by ' + addr[0], ':', addr[1])
            break
            
    if client_socket in client_sockets :
        client_sockets.remove(client_socket)
        print('remove client list : ',len(client_sockets))

    client_socket.close()


try:
    while True:
        print('>> Wait')

        client_socket, addr = server_socket.accept()
        client_sockets.append(client_socket)
        start_new_thread(threaded,(client_socket, addr))
        print("inner count : ", len(client_sockets))
        
except Exception as e :
    print ('what error? : ',e)

finally:
    server_socket.close()




