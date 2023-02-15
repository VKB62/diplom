import hashlib
import json
from .set import *
from time import time


class Blockchain(object):
    def __init__(self):
        """
        Инициализируем свой блокчейн
        """
        self.current_transactions = []
        self.chain = []

        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Создаем новый блок в нашем Блокчейне

        :параметр proof: <int> proof полученный после использования алгоритма «Доказательство выполнения работы»
        :параметр previous_hash: (Опциональный) <str> Хэш предыдущего Блока
        :return: <dict> Новый блок
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Сбрасываем текущий список транзакций
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, user, choice):
        """
        Создает новую транзакцию для перехода к следующему замайненному Блоку

        :param user: <str> Пользователь
        :param choice: <str> Выбор пользователя
        :return: <int> Индекс блока который будет хранить в себе эту транзакцию
        """

        self.current_transactions.append({
            'user': user,
            'choice': choice,
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        Создает a SHA-256 хэш блока

        :параметр block: <dict> Блок
        :return: <str>
        """

        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        """
        Простой алгоритм Proof of Work:
         - Ищем число p' такое, чтобы hash(pp') содержал в себе 4 лидирующих нуля, где p это предыдущий proof, а p' это новый proof

        :параметр last_proof: <int>
        :return: <int>
        """

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Проверяем Proof: Содержит ли hash(last_proof, proof) 4 лидирующих нуля?

        :параметр last_proof: <int> предыдущий Proof
        :параметр proof: <int> Тукущий Proof
        :return: <bool> True если все верно, иначе False.
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


def main():
    f = open('block.txt', 'w')

    # Создаем экземпляр Blockchain
    blockchain = Blockchain()
    for count, user in enumerate(userss):
        blockchain.new_transaction(user, count + 1)
        blockchain.new_block(blockchain.proof_of_work(blockchain.chain[count]['proof']))
    for chain in blockchain.chain:
        f.write(f'{chain}\n')
    f.close()
