import copy
import itertools


class Node:
    def __init__(self, data, positive_child=None, negative_child=None):
        self.data = data
        self.positive_child = positive_child
        self.negative_child = negative_child


class Record:
    def __init__(self, illness, symptoms):
        self.illness = illness
        self.symptoms = symptoms


def parse_data(filepath):
    with open(filepath) as data_file:
        records = []
        for line in data_file:
            words = line.strip().split()
            records.append(Record(words[0], words[1:]))
        return records


class Diagnoser:
    def __init__(self, root: Node):
        self.root = root

    def __goto_leaf(self, tree, remove_empty=False):

        if tree.positive_child is None or tree.negative_child is None:
            return

        if tree.positive_child.positive_child is not None:
            self.__goto_leaf(tree.positive_child, remove_empty)

        if tree.negative_child.positive_child is not None:
            self.__goto_leaf(tree.negative_child, remove_empty)

        if Diagnoser(tree.positive_child).inorderTraversal() == Diagnoser(
                tree.negative_child).inorderTraversal() or remove_empty and tree.negative_child.data == None or remove_empty and tree.positive_child.data == None:
            if tree.negative_child.data != None:
                tmp = tree.negative_child.data
            elif tree.positive_child.data != None:
                tmp = tree.positive_child.data
            else:
                tmp = tree.positive_child.data
            tree.negative_child = None
            tree.positive_child = None
            tree.data = tmp
            return

        if remove_empty and (tree.negative_child.data is None or tree.positive_child.data is None):
            if tree.negative_child.data != None:
                tmp = tree.negative_child.data
            elif tree.positive_child.data != None:
                tmp = tree.positive_child.data
            else:
                tmp = tree.positive_child.data
            tree.negative_child = None
            tree.positive_child = None
            tree.data = tmp
            return



    def minimize(self, remove_empty=False):
        if self.root is not None:
            if self.root.negative_child is not None and self.root.negative_child is not None:
                if self.root.negative_child.positive_child is not None and self.root.negative_child.positive_child is not None:
                    if Diagnoser(self.root.positive_child).inorderTraversal() == Diagnoser(
                            self.root.negative_child).inorderTraversal():

                        self.root.data = self.root.negative_child.data
                        self.root.positive_child = self.root.negative_child.positive_child
                        self.root.negative_child = self.root.negative_child.negative_child
                        self.minimize(remove_empty)
        self.__goto_leaf(self.root, remove_empty)

    def set_new_tree(self, tree, data, left, right):
        tree.data = data
        tree.positive_child = left
        tree.positive_child = right

    def diagnose(self, symptoms):
        if self.root.positive_child is None and self.root.negative_child is None:
            return self.root.data
        if self.root.data in symptoms:
            return Diagnoser(self.root.positive_child).diagnose(symptoms)
        return Diagnoser(self.root.negative_child).diagnose(symptoms)

    def calculate_success_rate(self, records):
        count = 0
        if len(records) < 1:
            raise ValueError('A very specific bad thing happened.')
        for record in records:
            iillness = record.illness
            symptoms = record.symptoms
            if Diagnoser(self.root).diagnose(symptoms) == iillness:
                count += 1
        return count / len(records)

    def all_illnesses(self):
        all_values = self.__go_over_tree_values()
        arr = []
        rng = len(all_values)
        for il in range(rng):
            max = self.__find_max(all_values)
            if max != '':
                arr.append(max)
            while max in all_values:
                all_values.remove(max)
        return arr

    def __find_max(self, arr):
        x = 0
        value = ''
        for j in arr:
            if arr.count(j) > x:
                x = arr.count(j)
                value = j
        return value

    def inorderTraversal(self):
        answer = []

        self.go_over_tree(self.root, answer)
        return answer

    def go_over_tree(self, root, arr=[]):
        if root == None:
            return
        Diagnoser(root.positive_child).go_over_tree(root.positive_child, arr)
        arr.append(root.data)
        Diagnoser(root.negative_child).go_over_tree(root.negative_child, arr)
        return

    def __go_over_tree_values(self, arr=[]):
        if self.root.data is not None and self.root.data != '' and self.root.positive_child is None and self.root.negative_child is None:
            arr.append(self.root.data)
        if self.root.positive_child is not None:
            Diagnoser(self.root.positive_child).__go_over_tree_values(arr)
        if self.root.negative_child is not None:
            Diagnoser(self.root.negative_child).__go_over_tree_values(arr)
        return arr

    def __go_over_tree_path(self, arr=[], path=[]):
        arr.append([self.root.data, copy.deepcopy(path)])
        if self.root.positive_child is None and self.root.negative_child is None:
            return arr
        if self.root.positive_child is not None:
            Diagnoser(self.root.positive_child).__go_over_tree_path(arr, path + [True])
        if self.root.negative_child is not None:
            Diagnoser(self.root.negative_child).__go_over_tree_path(arr, path + [False])
        return arr

    def paths_to_illness(self, illness):
        all_paths = self.__go_over_tree_path([], [])
        lst = []
        for i in all_paths:
            if i[0] == illness and i[1] not in lst:
                lst.append(i[1])

        return lst


def count_max_in_records(records):
    lst = []
    lst2 = []
    for i in records:
        lst.append(i.illness)
    for j in lst:
        lst2.append(lst.count(j))
    max1 = lst[lst2.index(max(lst2))]
    try:
        return max1
    except:
        return None


def build_tree(records, symptoms):
    if len(symptoms) == 0 and len(records) == 0:
        return Diagnoser(Node(None, None, None))

    if len(symptoms) == 0:
        return Diagnoser(Node(count_max_in_records(records), None, None))

    for i in records:
        if not isinstance(i, Record):
            raise TypeError('not a record')
    for i in symptoms:
        if not isinstance(i, str):
            raise TypeError('not a string')
    tree = __bulid_tree_helper(symptoms, [], [], records)
    return Diagnoser(tree)


def __bulid_tree_helper(symptoms, yes_simp, no_simp, records):
    if len(symptoms) == 0:
        match = []
        help = []
        # check yes simp in record and add to help list
        for record in records:
            for elem in range(len(yes_simp)):
                if yes_simp[elem] in record.symptoms:
                    if elem == len(yes_simp) - 1:
                        help.append(record)
                else:
                    break
        # if no such thing in help,check on no list
        if len(help) == 0:
            for record in records:
                for elem in range(len(no_simp)):
                    if no_simp[elem] not in record.symptoms:
                        if elem == len(no_simp) - 1:
                            match.append(record.illness)
                    else:
                        break
            try:
                return Node(max(match, key=match.count), None, None)
            except:
                return Node(None, None, None)

        # if no list empty check only on yes
        if len(no_simp) == 0:
            for record in records:
                for elem in range(len(yes_simp)):
                    if yes_simp[elem] in record.symptoms:
                        if elem == len(yes_simp) - 1:
                            match.append(record.illness)
                    else:
                        break
            try:
                return Node(max(match, key=match.count), None, None)
            except:
                return Node(None, None, None)
        # if three mach in yes u need to check also match in no
        for i in help:
            for elem in range(len(no_simp)):
                if no_simp[elem] not in i.symptoms:
                    if elem == len(no_simp) - 1:
                        match.append(i.illness)
                else:
                    break
        try:
            return Node(max(match, key=match.count), None, None)
        except:
            return Node(None, None, None)

        return Node(None, None, None)

    return Node(symptoms[0], __bulid_tree_helper(symptoms[1:], yes_simp + [symptoms[0]], no_simp, records),
                __bulid_tree_helper(symptoms[1:], yes_simp, no_simp + [symptoms[0]], records))


def optimal_tree(records, symptoms, depth):
    if not 0 <= depth <= len(symptoms):
        raise ValueError('wrong deapth')
    if len(symptoms) != len(set(symptoms)):
        raise ValueError('double symptoms')
    combos = list(itertools.combinations(symptoms, depth))
    max_sus = 0
    best_tree = None
    for comb in combos:
        tree_rate = build_tree(records, list(comb)).calculate_success_rate(records)
        if tree_rate > max_sus:
            max_sus = tree_rate
            best_tree = build_tree(records, list(comb))
    return best_tree


if __name__ == "__main__":

    # Manually build a simple tree.
    #                cough
    #          Yes /       \ No
    #        fever           healthy
    #   Yes /     \ No
    # covid-19   cold

    flu_leaf = Node("covid-19", None, None)
    cold_leaf = Node("cold", None, None)
    inner_vertex = Node("fever", flu_leaf, cold_leaf)
    healthy_leaf = Node("healthy", None, None)
    root = Node("cough", inner_vertex, healthy_leaf)

    diagnoser = Diagnoser(root)
    print(diagnoser.go_over_tree())
    # Simple test
    diagnosis = diagnoser.diagnose(["cough"])
    if diagnosis == "cold":
        print("Test passed")
    else:
        print("Test failed. Should have printed cold, printed: ", diagnosis)

# # Add more tests for sections 2-7 here.
