from flink.plan.Environment import get_environment
from flink.plan.Constants import INT, STRING, WriteMode
from flink.functions.GroupReduceFunction \
import GroupReduceFunction

class Adder(GroupReduceFunction):
    def reduce(self, iterator, collector):
        count, w = iterator.next()
        count += sum([element[0] for element in iterator])
        collector.collect((count, w))

if __name__ == "__main__":
    output_file = '/Users/li2he1/Google Drive/Laioffer/SDE/Full_stack_project/FlinkProcess/out.txt' 
    print('write output to: %s' % (output_file, ))
    env = get_environment()
    stream = env.from_elements("split the sentence into words")
    stream \
        .flat_map(lambda x, count: [(1, word) for word in \
         x.lower().split()]) \
        .group_by(1) \
        .reduce_group(Adder(), combinable=True) \
        .map(lambda cw: 'count is: %s word is: %s' % (cw[0], cw[1])) \
        .write_text(output_file, write_mode=WriteMode.OVERWRITE)

    env.execute(local=True)
