from collections import deque


class LinkedList:
    def __init__(self):
        self.head = None

    def __repr__(self):
        node = self.head
        nodes = []
        while node is not None:
            nodes.append(str(node.value))
            node = node.next
        nodes.append("None")
        return " -> ".join(nodes)


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

    def __repr__(self):
        return str(self.value)

    def find_node(self, search_value):
        node = self
        while True:
            if node.value == search_value:
                return node
            else:
                node = node.next


def crabby_game(rounds, cup_grab_count, cups_length):
    cups = deque([5, 2, 3, 7, 6, 4, 8, 1, 9])

    # cups = deque([3, 8, 9, 1, 2, 5, 4, 6, 7])
    extended = [x for x in range(10, cups_length + 1)]
    cups.extend(extended)

    node_dict = {}
    linked_list = LinkedList()
    linked_list.head = Node(cups.popleft())

    cup_node = linked_list.head
    node_dict[cup_node.value] = cup_node
    for cup in cups:
        cup_node.next = Node(cup)
        cup_node = cup_node.next
        node_dict[cup] = cup_node

    node_dict[cups_length].next = linked_list.head

    lowest_cup = min(cups)
    highest_cup = max(cups)
    loop_node = linked_list.head
    for y in range(rounds):
        # Only the current node and the last node of 3 need updating
        # current node -> node after 3
        # third node -> target_node
        grabbed_cups = []
        end_node = loop_node.next
        grabbed_cups.append(end_node.value)
        for x in range(cup_grab_count - 1):
            end_node = end_node.next
            grabbed_cups.append(end_node.value)

        destination_cup = loop_node.value - 1 if loop_node.value != lowest_cup else highest_cup
        while True:
            if destination_cup in grabbed_cups:
                if destination_cup <= lowest_cup:
                    destination_cup = highest_cup
                else:
                    destination_cup -= 1
            else:
                break

        # destination_node = linked_list.head.find_node(destination_cup)
        destination_node = node_dict.get(destination_cup)

        after_3_node = end_node.next
        new_after_3_node = destination_node.next
        curr_1st_of_3_node = loop_node.next

        loop_node.next = after_3_node
        end_node.next = new_after_3_node
        destination_node.next = curr_1st_of_3_node

        # go to the next one
        loop_node = loop_node.next
        if y % 100000 == 0:
            print(y)

    one_node = node_dict.get(1)
    print(one_node.value)
    print(one_node.next.value)
    print(one_node.next.next.value)
    return one_node.next.value * one_node.next.next.value


print(crabby_game(int(1e7), 3, int(1e6)))
