import sys
from itertools import combinations


def load_data(file_path):
    data = []
    with open(file_path, 'r') as f:
        for row in f:
            data.append(set(row.strip().split(",")))
    return data


def sort_dict(d):
    return dict(sorted(d.items(), key = lambda x: x[1]))


class Apriori:
    def __init__(self, file_path, min_support, min_confidence):
        self.min_support = min_support # 最小支持度
        self.min_confidence = min_confidence # 最小置信度
        self.data = load_data(file_path)
        self.num = len(self.data)
        self.frequency_list = None
        self.rules = None

    def large_1_items(self):
        items = dict()
        for row in self.data:
            for i in row:
                if i in items:
                    items[i] += 1
                else:
                    items[i] = 1
        items = {(i,): j / self.num for i, j in items.items() if j / self.num > self.min_support}
        return sort_dict(items)

    def compute_support(self, item_list):
        count = 0
        for row in self.data:
            if all(item in row for item in item_list):
                count += 1
        return count / self.num

    def generate_c(self, l):
        c = set()
        for p, q in combinations(l, 2):
            if p[:-2] == q[:-2]:
                c.add(p + (q[-1],))
        for candidate_set in set(c):
            k = len(candidate_set)
            for subset in combinations(candidate_set, k - 1):
                if subset not in l:
                    c.remove(candidate_set)
        return c

    def apriori(self):
        lk = self.large_1_items()
        self.frequency_list = []
        while lk:
            self.frequency_list.append(lk)
            c = self.generate_c(lk)
            lk = dict()
            for candidate_set in c:
                sup = self.compute_support(candidate_set)
                if sup >= self.min_support:
                    lk[candidate_set] = sup
            lk = sort_dict(lk)

    def generate_rule(self):
        self.rules = {}
        for k, items_set in enumerate(self.frequency_list[1:]):
            for items, sup in items_set.items():
                for i in range(len(items)):
                    x = items[:i] + items[i + 1:]
                    confidence = sup / self.frequency_list[k][x]
                    if confidence > self.min_confidence:
                        self.rules[x + (items[i],)] = (confidence, sup)

    def output_rule(self):
        with open("./output.txt", 'w') as f:
            f.write("==Frequent itemsets (min_sup=%s" % (self.min_support * 100) + "%)\n")
            for item_set in self.frequency_list:
                for items in item_set:
                    f.write("[%s], %s" % (",".join(items), int(item_set[items] * 100)) + "%\n")
            f.write("==High-confidence association rules (min_conf=%s" % (self.min_confidence * 100) + "%)\n")
            for rule in self.rules:
                l = "[%s]" % ",".join(rule[:-1])
                r = "[%s]" % rule[-1]
                c = "Conf: %.1f" % (self.rules[rule][0] * 100) + "%"
                s = "Supp: %.1f" % (self.rules[rule][1] * 100) + "%"
                f.write("%s => %s (%s, %s)\n" % (l, r, c, s))


if __name__ == '__main__':
    # if len(sys.argv) != 7:
    #    print("main <data path> <minimum support> <minimum confidence>")
    #    exit(1)
    # f = sys.argv[1]
    # s = float(sys.argv[2])
    # c = float(sys.argv[3])
    f = "./test.csv"
    s = 0.7
    c = 0.8

    a = Apriori(f, s, c)
    a.apriori()
    a.generate_rule()
    a.output_rule()


