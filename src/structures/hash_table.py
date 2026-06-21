class _Node:
    __slots__ = ("key", "value", "next")

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    """
    Tabela hash própria com tratamento de colisão por encadeamento.

    Complexidade média: inserir/buscar/remover -> O(1)
    Pior caso (muitas colisões no mesmo bucket): O(n)
    Resize automático mantém fator de carga <= 0.75 -> O(1) amortizado.
    """

    def __init__(self, capacidade_inicial: int = 16, fator_carga_max: float = 0.75):
        self._capacidade = capacidade_inicial
        self._buckets = [None] * self._capacidade
        self._tamanho = 0
        self._fator_carga_max = fator_carga_max

    def _hash(self, key) -> int:
        return hash(key) % self._capacidade

    def inserir(self, key, value):
        idx = self._hash(key)
        node = self._buckets[idx]
        while node:
            if node.key == key:
                node.value = value
                return
            node = node.next
        novo = _Node(key, value)
        novo.next = self._buckets[idx]
        self._buckets[idx] = novo
        self._tamanho += 1
        if self._tamanho / self._capacidade > self._fator_carga_max:
            self._resize()

    def buscar(self, key):
        idx = self._hash(key)
        node = self._buckets[idx]
        while node:
            if node.key == key:
                return node.value
            node = node.next
        return None

    def contem(self, key) -> bool:
        return self.buscar(key) is not None

    def remover(self, key) -> bool:
        idx = self._hash(key)
        node = self._buckets[idx]
        anterior = None
        while node:
            if node.key == key:
                if anterior:
                    anterior.next = node.next
                else:
                    self._buckets[idx] = node.next
                self._tamanho -= 1
                return True
            anterior = node
            node = node.next
        return False

    def chaves(self):
        for bucket in self._buckets:
            node = bucket
            while node:
                yield node.key
                node = node.next

    def valores(self):
        for bucket in self._buckets:
            node = bucket
            while node:
                yield node.value
                node = node.next

    def itens(self):
        for bucket in self._buckets:
            node = bucket
            while node:
                yield (node.key, node.value)
                node = node.next

    def _resize(self):
        antigos = list(self.itens())
        self._capacidade *= 2
        self._buckets = [None] * self._capacidade
        self._tamanho = 0
        for k, v in antigos:
            self.inserir(k, v)

    def __len__(self):
        return self._tamanho

    def __repr__(self):
        return f"HashTable(tamanho={self._tamanho}, capacidade={self._capacidade})"