# Optimization functionalities based on axis aligned bounding boxes and edges at the bounding box perimeter.

# line_segment: (origin_x, origin_y, end_x, end_y) all given in absolute coordinates
from operator import itemgetter

def split_lines(directives):
    for directive in directives:
        origin = directive["origin"]
        current_point = origin
        new_directives = []
        for element in directive["elements"]:
            if element["type"] is not "line":
                # Ignore other elements than lines.
                current_point = element["end_point"](element)
            else:
                (x, y) = element["end_point"](element)
                (curr_x, curr_y) = current_point
                new_directives.append( (curr_x, curr_y, curr_x + x, curr_y + y))
                current_point = (curr_x + x, curr_y + y)

# Get the bounding rectangle for all vertices in a single piece:
# from top left corner (min_x, min_y) to lower right (max_x, max_y)
def get_bounds(segments):
    min_x = min(segments[0][0], segments[0][2])
    max_x = min_x
    min_y = min(segments[0][1], segments[0][3])
    max_y = min_y

    for (ax, ay, bx, by) in segments:
        min_x = min(min_x, ax, bx)
        max_x = max(max_x, ax, bx)
        min_y = min(min_y, ay, by)
        max_y = max(max_y, ay, by)

    return (min_x, min_y, max_x, max_y)


def find_outermost_lines(segments, top_edge=True):
    def return_outer_line(a, b):
        if top_edge:
            if a[1] > b[1]:
                return b
            return a
        else:
            if a[1] < b[1]:
                return b
            return a

    def get_min_max(line):
        (a_x, _, b_x, _) = line
        if a_x < b_x:
            return a_x, b_x
        else:
            return b_x, a_x

    horizontal_segments = list(filter(lambda segment: segment[1] == segment[3], segments))

    s = sorted(horizontal_segments, key=(lambda seg: max(seg[0], seg[2])))
    horizontal_segments = sorted(s, key=(lambda seg: min(seg[0], seg[2])))

    print("Original segs: {}".format(horizontal_segments))

    (bound_min_x, _, bound_max_x, _) = get_bounds(horizontal_segments)

    def get_overlapping(start_x, end_x, ordered_segments):
        overlapping_segs = []
        for seg in ordered_segments:
            s_min_x, s_max_x = get_min_max(seg)
            if start_x >= s_max_x:
                continue
            if s_min_x >= end_x:
                break
            overlapping_segs.append(seg)
        return overlapping_segs

    def find_lines(start_x, end_x, segments):
        outest_segments = []
        overlapping_segs = get_overlapping(start_x, end_x, segments)

        outermost_segment = reduce(return_outer_line, overlapping_segs)
        o_min_x, o_max_x = get_min_max(outermost_segment)
        middle_segment_start = max(start_x, o_min_x)
        middle_segment_end = min(end_x, o_max_x)
        if o_min_x > start_x:
            outest_segments.extend(find_lines(start_x, o_min_x, overlapping_segs))
        outest_segments.append((middle_segment_start, outermost_segment[1], middle_segment_end, outermost_segment[1]))
        if o_max_x < end_x:
            outest_segments.extend(find_lines(o_max_x, end_x, overlapping_segs))
        return outest_segments

    outmost_segments = find_lines(bound_min_x, bound_max_x, horizontal_segments)
    print("Outermost segments: {}".format(outmost_segments))


if __name__ == "__main__":
    segments = [
        (0, 0, 10, 0),
        (0, 0, 10, 1),
        (1, 0, 9, 0),
        (0, 1, 10, 1),
        (8, 2, 10, 2),
        (0, -1, 5, -1),
        (5, -1, 10, -1),
        (3, -2, 6, -2)
    ]
    find_outermost_lines(segments, True)
    find_outermost_lines(segments, False)
