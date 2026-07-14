import sys

def make_list(first, second):
    set_first = set(first)
    set_second = set(second)

    return list(set_first.difference(set_second))

def marketing():
    #почты клиентов
    clients = ['andrew@gmail.com', 'jessica@gmail.com', 'ted@mosby.com',
    'john@snow.is', 'bill_gates@live.com', 'mark@facebook.com',
    'elon@paypal.com', 'jessica@gmail.com']
    #участники мероприятий
    participants = ['walter@heisenberg.com', 'vasily@mail.ru',
    'pinkman@yo.org', 'jessica@gmail.com', 'elon@paypal.com',
    'pinkman@yo.org', 'mr@robot.gov', 'eleven@yahoo.com']
    #клиенты, посмотревшие писмо
    recipients = ['andrew@gmail.com', 'jessica@gmail.com', 'john@snow.is']

    arguments = sys.argv

    if (len(arguments) == 2):
        if (arguments[1] == 'call_center'):
            answer = make_list(clients, recipients)
        elif(arguments[1] == 'potential_clients'):
            answer = make_list(participants, clients)
        elif(arguments[1] == 'loly_program'):
            answer = make_list(clients, participants)
        else:
            raise ValueError(f"Have not parameter - {arguments[1]}")
        print(answer)


if __name__ == '__main__':
    marketing()