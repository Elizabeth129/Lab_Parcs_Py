from Pyro4 import expose
import math


class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.workers = workers
        if workers is not None:
            self.workers_cnt = len(workers)
        else:
            self.workers_cnt = 0
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.text = None
        self.pattern = None

    def solve(self):
        # print("Job started")
        # print(f"Starting with {self.workers_cnt} workers")
        self.read_input()
        n = len(self.text)
        m = len(self.pattern)
        text_chunks = []
        for i in range(self.workers_cnt):
            left_bound = int(math.ceil(n / self.workers_cnt)) * i
            right_bound = int(math.ceil(n / self.workers_cnt)) * (i + 1) + (m - 1)
            right_bound = min(right_bound, n)
            text_chunks.append(self.text[left_bound:right_bound])

        reduced = None
        for run in range(10):
            mapped = []
            for i in range(self.workers_cnt):
                mapped.append(self.workers[i].worker_solve(text_chunks[i], self.pattern))
            if reduced is None:
                reduced = self.reduce(mapped)

        self.write_output(reduced)

    def read_input(self):
        f = open(self.input_file_name, "r")
        self.text = f.readline().rstrip('\r\n')
        self.pattern = f.readline().rstrip('\r\n')
        f.close()

    def write_output(self, answer):
        f = open(self.output_file_name, "w")
        f.write(str(int(answer)))
        f.close()

    @staticmethod
    @expose
    def worker_solve(text, pattern):
        result = 0
        combined = pattern + '#' + text
        pi = [0]
        for i in range(1, len(combined)):
            j = pi[i - 1]
            while j > 0 and combined[i] != combined[j]:
                j = pi[j - 1]
            if combined[i] == combined[j]:
                j += 1
            pi.append(j)
        for i in range(len(pattern), len(combined)):
            if pi[i] == len(pattern):
                result += 1
        return [result]

    @staticmethod
    @expose
    def reduce(mapped):
        res = []
        for item in mapped:
            res.extend(item.value)
        return sum(res)


# if __name__ == '__main__':
#     master = Solver(workers=[Solver(), Solver()], input_file_name="input1000000.txt", output_file_name="output.txt")
#     master.solve()
