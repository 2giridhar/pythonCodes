import math


class SinglyLinkedNode(object):
    def __init__(self, item=None, next_link=None):
        super(SinglyLinkedNode, self).__init__()
        self._item = item
        self._next = next_link

    @property
    def item(self):
        return self._item

    @item.setter
    def item(self, item):
        self._item = item

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, next):
        self._next = next

    def __repr__(self):
        return repr(self.item)


class SinglyLinkedList(object):
    def __init__(self):
        super(SinglyLinkedList, self).__init__()
        self._head = None
        self._length = 0

    def __len__(self):
        print "length: " + str(self._length)
        return self._length

    def __iter__(self):
        curr_node = self._head
        print "\n Linked List Iteration:"
        st = ""
        while curr_node:
            st += "-->"
            st += str(curr_node.item)
            curr_node = curr_node.next
        print st[3:]
        return True

    def __contains__(self, item):
        print "\n\n Searching for " + str(item)
        curr_node = self._head
        while curr_node:
            if curr_node.item == item:
                print "Node ", item, " found"
                return curr_node
            curr_node = curr_node.next
        print "Not found"
        return None

    def remove(self, item):
        print "\n\n Deletion of " + str(item)
        curr_node = self._head
        prev_node = None
        while curr_node:
            if curr_node.item is item:
                if prev_node is None:
                    self._head = curr_node
                else:
                    prev_node.next = curr_node.next
                self._length -= 1
                print "Item Deleted"
                return curr_node
            prev_node = curr_node
            curr_node = curr_node.next
        print "Item not Found"
        return None

    def prepend(self, item):
        print "\n\n Adding item %d :" % item
        if self._head is not None:
            new_node = SinglyLinkedNode(item, self._head)
        else:
            new_node = SinglyLinkedNode(item)
        self._head = new_node
        self._length += 1
        print "Node ", item, " is added at the start"
        return True

    def __repr__(self):
        s = "List:" + "->".join([item for item in self])
        return s


class KeyValuePair(object):
    def __init__(self, key=None, value=None):
        super(KeyValuePair, self).__init__()
        self._key = key
        self._value = value

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        self._key = key

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


def chain_hash(key=7, bin_count=10):
    # Hashing using division method
    return int(key % bin_count)


def oad_hash(key=7, i=0, bin_count=10):
    # Hashing using division method
    return int((key + i) % bin_count)


class ChainedHashDict(object):
    def __init__(self, bin_count=10, max_load=0.7, hashfunc=hash):
        super(ChainedHashDict, self).__init__()
        self._bincount = bin_count
        self._maxload = max_load
        self._hashtable = [None] * bin_count
        self._maxkeys = math.floor(bin_count * max_load)
        self._length = 0

    @property
    def load_factor(self):
        return self._maxkeys / self._bincount

    @property
    def bincount(self):
        return self._bincount

    @bincount.setter
    def bincount(self, count):
        self._bincount = count

    def rebuild(self, bincount):
        old_table = [None] * self.bincount
        index = 0
        while index < self.bincount:
            old_table[index] = self._hashtable[index]
            index += 1
        self._hashtable = [None] * bincount
        self.bincount = bincount
        self._length = 0
        self._maxkeys = math.floor(bincount * self._maxload)
        print "Rebuilt Tree:"
        for node in old_table:
            if node is not None:
                self. __setitem__(node.item.key, node.item.value)
                next_node = node.next
                while next_node:
                    self. __setitem__(next_node.item.key, next_node.item.value)
                    next_node = next_node.next

    def __getitem__(self, key):
        index = chain_hash(key, self.bincount)
        curr_node = self._hashtable[index]
        while curr_node:
            if key == curr_node.item.key:
                return curr_node.item
            else:
                curr_node = curr_node.next

    def __setitem__(self, key, value):
        if self._length == self._maxkeys:
            return "Error: List is full"
        obj = KeyValuePair(key, value)
        new_node = SinglyLinkedNode(obj)
        index = chain_hash(key, self.bincount)
        if self._hashtable[index] is None:
            self._hashtable[index] = new_node
        else:
            new_node.next = self._hashtable[index]
            self._hashtable[index] = new_node
        self._length += 1
        print "node (" + str(key) + "," + str(value) + ") inserted"

    def __delitem__(self, key):
        index = chain_hash(key, self.bincount)
        if self._hashtable[index] is not None:
            curr_node = self._hashtable[index]
            prev_node = None
            while curr_node:
                if curr_node.item.key == key:
                    if prev_node is None:
                        self._hashtable[index] = curr_node.next
                    else:
                        prev_node.next = curr_node.next
                    print "node (" + str(key) + "," + str(curr_node.item.value) + ") deleted"
                    return curr_node.item
                curr_node = curr_node.next
            print "Key" + str(key) + "not found in the list"
            return False

    def __contains__(self, key):
        index = chain_hash(key, self.bincount)
        if self._hashtable[index] is not None:
            curr_node = self._hashtable[index]
            while curr_node:
                if curr_node.item.key == key:
                    return curr_node.item
                curr_node = curr_node.next
            return False

    def __len__(self):
        print self._length
        return self._length

    def display(self):
        index = 0
        while index < self.bincount:
            print "-------------"
            if self._hashtable[index] is None:
                print "None"
            else:
                curr_node = self._hashtable[index]
                str1 = "head"
                while curr_node:
                    str1 = str1 + "-->(" + str(curr_node.item.key) + "," + str(curr_node.item.value) + ")"
                    curr_node = curr_node.next
                print str1
            index += 1
        print "--------------"


class OpenAddressHashDict(object):
    def __init__(self, bin_count=10, max_load=0.7, hashfunc=hash):
        super(OpenAddressHashDict, self).__init__()
        self._bincount = bin_count
        self._maxload = max_load
        self._hashtable = [None] * bin_count
        self._maxkeys = math.floor(bin_count * max_load)
        self._length = 0

    @property
    def load_factor(self):
        return self._maxkeys / self.bincount

    @property
    def bincount(self):
        return self._bincount

    @bincount.setter
    def bincount(self, count):
        self._bincount = count

    def rebuild(self, bincount):
        old_table = [None] * self.bincount
        index = 0
        while index < self.bincount:
            old_table[index] = self._hashtable[index]
            index += 1
        self._hashtable = [None] * bincount
        self.bincount = bincount
        self._length = 0
        print "\n\n Open Address hash tree rebuilt:"
        for node in old_table:
            if node is not None:
                self. __setitem__(node.key, node.value)

    def __getitem__(self, key):
        print "Getting the value:"
        for i in range(0, self.bincount - 1):
            if self._hashtable[i] is not None:
                if self._hashtable[i].key == key:
                    print self._hashtable[i].value
                    return self._hashtable[i].value

    def __setitem__(self, key, value):
        if self._bincount == self._length:
            return "Error: Bin Full"
        index = oad_hash(key, 0, self.bincount)
        kvpair = KeyValuePair(key, value)
        if self._hashtable[index] is None:
            self._hashtable[index] = kvpair
        else:
            i = 0
            while self._hashtable[index] is not None:
                i += 1
                index = oad_hash(key, i, self.bincount)
            self._hashtable[index] = kvpair
        print "(" + str(key) + "," + str(value) + ") inserted"

    def __delitem__(self, key):
        for i in range(0, self.bincount):
            if self._hashtable[i] is not None:
                if self._hashtable[i].key == key:
                    print "value", self._hashtable[i].value, "deleted at key ", key
                    self._hashtable[i] = None
                    self._length -= 1

    def __contains__(self, key):
        for i in range(0, self.bincount):
            if self._hashtable[i] is not None:
                if self._hashtable[i].key == key:
                    print "Hash table contains the value " + str(self._hashtable[i].value) + "at key" + str(key)

    def __len__(self):
        return self._length

    def display(self):
        for i in range(0, self.bincount):
            print " _______"
            if self._hashtable[i] is None:
                print "| None |"
            else:
                print "| (" + str(self._hashtable[i].key) + "," + \
                      str(self._hashtable[i].value) + ") |"
        print " _______"


class BinaryTreeNode(object):
    def __init__(self, data=None, left=None, right=None, parent=None):
        super(BinaryTreeNode, self).__init__()
        self.data = data
        self.left = left
        self.right = right
        self.parent = parent


class BinaryTreeNode(object):
    def __init__(self, data=None, left=None, right=None, parent=None):
        """
        >>> Binary_Node = BinaryTreeNode(4, None, None, None)
        """
        super(BinaryTreeNode, self).__init__()
        self.data = data
        self.left = left
        self.right = right
        self.parent = parent


class BinarySearchTreeDict(object):

    def __init__(self):
        """
        >>> bst = BinarySearchTreeDict()
        """
        super(BinarySearchTreeDict, self).__init__()
        # TODO initialize
        self.root = None

    @property
    def height(self):
        """
        >>> bst = BinarySearchTreeDict()
        >>> bst.__setitem__(1, "one")
        >>> bst.height
        0
        """

        return self.get_height(self.root)

    def get_height(self, current_root):
        tree_height = -1
        if (current_root is not None):
            left_height = self.get_height(current_root.left)
            right_height = self.get_height(current_root.right)

            if(left_height > right_height):
                tree_height = left_height + 1
            else:
                tree_height = right_height + 1

        return tree_height

    def transplant(self, u, v):
        """
        Auxillary Function
        """
        if(u.parent is None):
            self.root = v
        elif(u.data.keys()[0] is u.parent.left.data.keys()[0]):
            u.parent.left = v
        else:
            u.parent.right = v
        if(v is not None):
            v.parent = u.parent

    def treeMinimum(temproot):
        """
        Auxillary Function
        """
        while temproot.left is not None:
            temproot = temproot.left
        return temproot

    def get_inorder(self, current_root):
        """
        Auxillary Function
        """
        if current_root is not None:
            for i in self.get_inorder(current_root.left):
                yield i
            yield current_root.data.keys()[0]
            for i in self.get_inorder(current_root.right):
                yield i
        else:
            StopIteration()

    def inorder_keys(self):
        """
        >>> bst = BinarySearchTreeDict()
        >>> bst.__setitem__(5, "five")
        >>> bst.__setitem__(3, "three")
        >>> bst.__setitem__(7, "seven")
        >>> bst.inorder_keys()
        In order tree traversal:3->5->7
        """
        print "In order tree traversal:" + "->".join([str(i) for i in self.get_inorder(self.root)])

    #########################

    def get_postorder(self, current_root):
        """
        Auxillary Function
        """
        if current_root is not None:
            for i in self.get_postorder(current_root.left):
                yield i
            for i in self.get_postorder(current_root.right):
                yield i
            yield current_root.data.keys()[0]
        else:
                StopIteration()

    def postorder_keys(self):
        """
        >>> bst = BinarySearchTreeDict()
        >>> bst.__setitem__(5, "five")
        >>> bst.__setitem__(3, "three")
        >>> bst.__setitem__(7, "seven")
        >>> bst.postorder_keys()
        Post order tree traversal:3->7->5
        """
        print "Post order tree traversal:" + "->".join([str(i) for i in self.get_postorder(self.root)])

    ##########################

    def get_preorder(self, current_root):
        """
        Auxillary Function
        """
        if current_root is not None:
            yield current_root.data.keys()[0]
            for i in self.get_preorder(current_root.left):
                yield i
            for i in self.get_preorder(current_root.right):
                yield i
        else:
                StopIteration()

    def preorder_keys(self):
        """
        >>> bst = BinarySearchTreeDict()
        >>> bst.__setitem__(5, "five")
        >>> bst.__setitem__(3, "three")
        >>> bst.__setitem__(7, "seven")
        >>> bst.preorder_keys()
        Pre order tree traversal: 5->3->7
        """
        print "Pre order tree traversal: " + "->".join([str(i) for i in self.get_preorder(self.root)])

    def items(self):
        """
        >>> bst = BinarySearchTreeDict()
        >>> bst.__setitem__(5, "five")
        >>> bst.__setitem__(3, "three")
        >>> bst.__setitem__(7, "seven")
        >>> bst.inorder_keys()
        In order tree traversal:3->5->7
        """
        self.inorder_keys()

    def __getitem__(self, key):
        """
        >>> bst = BinarySearchTreeDict()
        >>> bst.__setitem__(1, "one")
        >>> bst.__getitem__(2)
        'Key not found'
        """

        message = "Key not found"
        current_node = self.search_key(self.root, key)
        if current_node is not None:
            message = str(current_node.data.get(current_node.data.keys()[0]))
        return message

    def search_key(self, current_root, key):
        """
        Auxillary Function
        """
        node = None
        while(current_root is not None):
            keys = current_root.data.keys()[0]

            if keys == key:
                node = current_root
                break
            elif key < keys:
                current_root = current_root.left
            elif key > keys:
                current_root = current_root.right
        return node

    def __setitem__(self, key, value):
        """
        >>> bst = BinarySearchTreeDict()
        >>> bst.__setitem__(1, "one")
        """
        new_data = {key: value}
        new_node = BinaryTreeNode(data=new_data)

        if(self.root is None):
            self.root = new_node
        else:
            self.insert(self.root, new_node)

    def insert(self, current_root, new_node):
        new_key = new_node.data.keys()[0]
        current_root_key = current_root.data.keys()[0]

        if(new_key < current_root_key):
            if(current_root.left is None):
                new_node.parent = current_root
                current_root.left = new_node

            else:
                self.insert(current_root.left, new_node)

        else:
            if(current_root.right is None):
                new_node.parent = current_root
                current_root.right = new_node

            else:
                self.insert(current_root.right, new_node)

    def __delitem__(self, key):
        """
        >>> bst = BinarySearchTreeDict()
        >>> bst.__setitem__(1, "one")
        >>> bst.__delitem__(1)
        Trying to delete: 1
        """
        print "Trying to delete: " + str(key)
        node = self.search_key(self.root, key)
        if(node is not None):
            if(node.left is None):
                self.transplant(node, node.right)
            elif(node.right is None):
                self.transplant(node, node.left)
            else:
                successor = self.treeMinimum(node.right)
                if(successor.parent.data.keys()[0] is not node.data.keys()[0]):
                    self.transplant(successor, successor.right)
                    successor.right = node.right
                    successor.right.parent = successor
                self.transplant(node, successor)
                successor.left = node.left
                successor.left.parent = successor

    def __contains__(self, key):
        """
        >>> bst = BinarySearchTreeDict()
        >>> bst.__setitem__(2, "Two")
        >>> bst.__contains__(2)
        'Found 2: Two'
        """

        msg = "Key not found"
        curr_node = self.search_key(self.root, key)
        if curr_node is not None:
            msg = "Found " + str(key) + ": " + str(curr_node.data.get(curr_node.data.keys()[0]))
        return msg

    def __len__(self):
        """
        >>> bst = BinarySearchTreeDict()
        >>> bst.__setitem__(2, "two")
        >>> bst.__setitem__(3, "three")
        >>> bst.__setitem__(4, "four")
        >>> bst.__len__()
        3
        """
        return self.get_length(self.root)

    def get_length(self, current_root):
        length = 0

        if(current_root is not None):
            len_left = self.get_length(current_root.left)
            len_right = self.get_length(current_root.right)
            length = len_left + len_right + 1

        return length

    def display(self):
        """
        >>> bst = BinarySearchTreeDict()
        >>> bst.__setitem__(2, "two")
        >>> bst.__setitem__(3, "three")
        >>> bst.__setitem__(8, "eight")
        >>> bst.display()
        In order tree traversal:2->3->8
        Pre order tree traversal: 3->2->8
        """
        self.inorder_keys()
        self.preorder_keys()


def terrible_hash(bin):
    """A terrible hash function that can be used for testing.

    A hash function should produce unpredictable results,
    but it is useful to see what happens to a hash table when
    you use the worst-possible hash function.  The function
    returned from this factory function will always return
    the same number, regardless of the key.

    :param bin:
        The result of the hash function, regardless of which
        item is used.

    :return:
        A python function that can be passes into the constructor
        of a hash table to use for hashing objects.
    """

    def hashfunc(item):
        return bin

    return hashfunc


def main():
    # Thoroughly test your program and produce useful out.
    #
    # Do at least these kinds of tests:
    #  (1)  Check the boundary conditions (empty containers,
    #       full containers, etc)
    #  (2)  Test your hash tables for terrible hash functions
    #       that map to keys in the middle or ends of your
    #       table
    #  (3)  Check your table on 100s or randomly generated
    #       sets of keys to make sure they function
    #
    #  (4)  Make sure that no keys / items are lost, especially
    #       as a result of deleting another key

    print "\n\nLINKED LIST TESTING"
    sll = SinglyLinkedList()
    striker = 10
    coin = 3
    while striker < 40:
        sll.prepend(striker)
        striker += coin
        coin += 1
    sll.__len__()
    sll.__iter__()
    sll.__contains__(13)
    sll.remove(13)
    sll.__contains__(13)

    print "\n\nChained Hash Dictionary:"
    chd = ChainedHashDict()

    chd.__setitem__(13, 30)
    chd.__setitem__(3, 19)
    chd.__setitem__(45, 22)
    chd.__setitem__(36, 36)
    chd.__setitem__(73, 37)
    chd.__getitem__(3)
    chd.__delitem__(45)
    chd.__contains__(36)
    chd.__len__()
    chd.display()
    chd.rebuild(8)
    chd.display()


    print "\n\nOpen Address Hash Dictionary:"
    chd = OpenAddressHashDict()

    chd.__setitem__(13, 30)
    chd.__setitem__(3, 19)
    chd.__setitem__(45, 22)
    chd.__setitem__(36, 36)
    chd.__setitem__(73, 37)
    chd.__getitem__(3)
    chd.__delitem__(45)
    chd.__contains__(36)
    chd.__len__()
    chd.display()
    chd.rebuild(8)
    chd.display()


if __name__ == '__main__':
    main()
