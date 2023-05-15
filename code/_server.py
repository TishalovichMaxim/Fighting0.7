import pygame, threading, socket
from chars.character import SignalsSender, CharacterSignal, CharacterState
from chars.charater_type import CharacterType
from networking import ServerGame
from utils import get_addr_from_str

# if len(sys.argv) != 4:
#     sys.exit(11)
def aboba(server_addr_str, client1_addr_str, char_type_value_1, client2_addr_str, char_type_value_2):
    # SERVER_ADDRESS   = get_addr_from_str(sys.argv[1])
    # CLIENT_ADDRESS_1 = get_addr_from_str(sys.argv[2])
    # CLIENT_ADDRESS_2 = get_addr_from_str(sys.argv[3])
    SERVER_ADDRESS   = get_addr_from_str(server_addr_str)
    CLIENT_ADDRESS_1 = get_addr_from_str(client1_addr_str)
    CLIENT_ADDRESS_2 = get_addr_from_str(client2_addr_str)
    print(SERVER_ADDRESS, CLIENT_ADDRESS_1, CLIENT_ADDRESS_2)
    print(f"chtv1 = {char_type_value_1} chtv2 = {char_type_value_2}")
    # SERVER_ADDRESS   = ('192.168.1.7', 12000)
    # CLIENT_ADDRESS_1 = ('192.168.1.10', 20322z)
    # CLIENT_ADDRESS_2 = ('192.168.1.7', 20233)

    FPS = 60
    N_LAST_PACKETS = 50

    pygame.init()
    pygame.display.set_mode()

    game = ServerGame(CharacterType(char_type_value_1[0]), CharacterType(char_type_value_2[0]))
    game.char1.set_start_pos()
    game.char2.set_start_pos(False)
    def send_data(sock):
        clock = pygame.time.Clock()
        while not game.is_ended():
            sock.sendto(game.get_chars_info(), CLIENT_ADDRESS_1)
            sock.sendto(game.get_chars_info(True), CLIENT_ADDRESS_2)
            game.update()
            clock.tick(FPS)

        for _ in range(N_LAST_PACKETS):
            sock.sendto(game.get_chars_info(), CLIENT_ADDRESS_1)      
            sock.sendto(game.get_chars_info(True), CLIENT_ADDRESS_2)

    with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as sock:
        sock.bind(SERVER_ADDRESS)

        connected = [False, False]
        while (not connected[0]) or (not connected[1]):
            data, addr = sock.recvfrom(1024)
            if addr == CLIENT_ADDRESS_1:
                connected[0] = True
            else:
                connected[1] = True
            print(connected)
            print(not connected[0])
            print(not connected[1])
        
        sending_thread = threading.Thread(target=send_data, args=(sock,))
        sending_thread.start()
        clock = pygame.time.Clock()
        sig_sender = SignalsSender()
        while not game.is_ended():
            pygame.event.pump()
            data, addr = sock.recvfrom(1024)
            if addr == CLIENT_ADDRESS_1:
                game.char1.set_movs(data[0], data[1])
                for i in range(2, len(data)):
                    sig_sender.send_sig(game.char1, CharacterSignal(data[i]))
            else:
                game.char2.set_movs(data[0], data[1])
                for i in range(2, len(data)):
                    sig_sender.send_sig(game.char2, CharacterSignal(data[i]))
        print("The end...")
        sending_thread.join()