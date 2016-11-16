import json


# describes a pair of (input_data, label)
class InputLabelPair:
    def __init__(self, input_data, label):
        self.input_data = input_data
        self.label = label


# takes in a raw .hlt file, parses out the useful information for ML, and writes
# back to ./parsed. Each move is parsed into two lines, the first the input data and
# the second the label (move)
# input data is comma seperated integers
class HLTMapper:
    LOOK_AREA = 3  # size of the square area to inspect for each move. Should be odd

    # frames are [framenum][height][width][ID, strength]

    # Tiles are described as [strength, production, isOurs]
    # This pattern is repeated LOOK_AREA^2 times in sequence


    # generator that creates a range that wraps map bounderies
    # EX wrap_range (47, 53, 50) will iterate over [47, 48, 49, 0, 1, 2]
    @staticmethod
    def wrap_range(lower_, upper_, limit):
        lower = lower_
        upper = upper_

        if lower < 0:
            lower = limit + lower
        if upper > limit:
            upper = upper - limit

        val = lower
        while val is not upper:
            if val == limit:
                val = 0

            yield val
            val += 1


    # given a frame and location, returns the input_data for that frame and location
    @staticmethod
    def _get_input_data(frames, productions, width, height, frame_num, y_, x_):
        diff = int(HLTMapper.LOOK_AREA / 2)

        our_id = frames[frame_num][y_][x_][0]
        input_data = []
        for y in HLTMapper.wrap_range(y_-diff, y_+diff+1, height):
            for x in HLTMapper.wrap_range(x_-diff, x_+diff+1, width):
                input_data.append(frames[frame_num][y][x][1])  # strength
                input_data.append(productions[y][x])  # production
                input_data.append(1 if frames[frame_num][y][x][0] is our_id else 0)  # owner

        return input_data

    # entry point. reads in from input_filename, outputs to output_filename
    @staticmethod
    def parse(input_filename, output_filename):
        assert(HLTMapper.LOOK_AREA % 2 != 0) # sanity check

        # read file. assuming they wont be larger than system memory
        with open('dataset/%s' % input_filename, 'r') as f_in:
            data = f_in.read()

        # parse into json
        j_data = json.loads(data)

        # get the useful data
        width = j_data['width']
        height = j_data['height']
        num_players = j_data['num_players']
        num_frames = j_data['num_frames']
        productions = j_data['productions']
        frames = j_data['frames']
        moves = j_data['moves']

        # initialize input-label-pairs list
        input_output_pairs = []

        # iterate all frames (except the last)
        for frame_num in range(num_frames-1):

            print('%s of %s...' % (frame_num, num_frames-1))

            # iterate grid
            for y in range(height):
                for x in range(width):

                    # only tiles with an owner
                    if frames[frame_num][y][x][0]:

                        # get input data as list
                        input_data = HLTMapper._get_input_data(frames, productions, width, height, frame_num, y, x)

                        # get correct label
                        label = moves[frame_num][y][x]

                        # append to list
                        input_output_pairs.append(InputLabelPair(input_data, label))

        # prepare lines
        lines = []
        for pair in input_output_pairs:
            lines.append(str(pair.input_data)[1:-1] + '\n')
            lines.append(str(pair.label) + '\n')

        # writeout
        with open('parsed/%s' % output_filename, 'w') as f_out:
            f_out.writelines(lines)


if __name__ == '__main__':
    f_in = '1479101235-398560114.hlt'
    f_out = 'test.txt'

    HLTMapper.parse(f_in, f_out)

    print('done')