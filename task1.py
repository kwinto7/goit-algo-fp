class Node:
    """Клас для вузла однозв'язного списку"""
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    """Клас для однозв'язного списку"""
    def __init__(self):
        self.head = None

    def append(self, data):
        """Додає елемент у кінець списку"""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def print_list(self):
        """Друк списку"""
        current = self.head
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print("None")

    # 1. Реверсування списку
    def reverse(self):
        prev = None
        current = self.head
        while current:
            nxt = current.next
            current.next = prev
            prev = current
            current = nxt
        self.head = prev

    # 2. Сортування вставками
    def insertion_sort(self):
        sorted_head = None
        current = self.head
        while current:
            next_node = current.next
            sorted_head = self._sorted_insert(sorted_head, current)
            current = next_node
        self.head = sorted_head

    def _sorted_insert(self, head_ref, new_node):
        if head_ref is None or head_ref.data >= new_node.data:
            new_node.next = head_ref
            return new_node
        else:
            current = head_ref
            while current.next and current.next.data < new_node.data:
                current = current.next
            new_node.next = current.next
            current.next = new_node
            return head_ref

    # 3. Об’єднання двох відсортованих списків
    @staticmethod
    def merge_sorted(list1, list2):
        dummy = Node(0)
        tail = dummy
        a, b = list1.head, list2.head

        while a and b:
            if a.data < b.data:
                tail.next = a
                a = a.next
            else:
                tail.next = b
                b = b.next
            tail = tail.next

        if a:
            tail.next = a
        if b:
            tail.next = b

        merged = LinkedList()
        merged.head = dummy.next
        return merged

if __name__ == "__main__":
    # Створюємо список
    ll = LinkedList()
    ll.append(3)
    ll.append(1)
    ll.append(4)
    ll.append(2)

    print("Початковий список:")
    ll.print_list()

    # Реверсування
    ll.reverse()
    print("Після реверсу:")
    ll.print_list()

    # Сортування вставками
    ll.insertion_sort()
    print("Після сортування вставками:")
    ll.print_list()

    # Другий список
    ll2 = LinkedList()
    ll2.append(0)
    ll2.append(5)
    ll2.append(6)

    print("Другий список:")
    ll2.print_list()

    # Об’єднання
    merged = LinkedList.merge_sorted(ll, ll2)
    print("Об’єднаний відсортований список:")
    merged.print_list()
