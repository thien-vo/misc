#!/usr/bin/env python2

import time
from collections import deque


def compute_triangular(n):
    """
    Compute the triangular sequence given integer n
    https://www.mathsisfun.com/algebra/triangular-numbers.html
    """
    return n * (n+1) / 2


def adjust_label(increase, decrease, new_num, old_num):
    """
    Given increase and decrease consecutive chains, adjust the data as follow:
    - If the new number start/continue an increasing subrange:
        - increase the already existing increasing consecutive subrange count by 1 OR
        - start a new increasing consecutive subrange count of 1
    - The opposite for negative chain
    - Do nothing if it is an equal subrange
    """
    compare = cmp(new_num, old_num)
    # Increasing subrange
    if compare == 1:
        # Interupt negative consecutive
        if decrease[-1] > 0:
            decrease.append(0)
        increase[-1] += 1
    # Decreasing subrange
    elif compare == -1:
        # Interupt positive consecutive
        if increase[-1] > 0:
            increase.append(0)
        decrease[-1] += 1
    # Equal subrange
    else:
        # Interupt any consecutive going on
        if decrease[-1] > 0:
            decrease.append(0)
        if increase[-1] > 0:
            increase.append(0)


def print_ranges(arr, k):
    """
    Mimicking a do-while loop.
    Get the initial valid subrange, calculating the consecutive labels and sum,
    then within a for loop skipping over the initial range, add the next element
    to the subrange after the removal of the first element in the range is processed.

    During the removal of the leading element, we adjust the consecutive labels.
    By comparing the first 2 leading elements, we can find out whether it came from either
    of the positive or negative chain or neither. If it comes from either chain, we adjust
    the sum by that label before decreasing or removing it (if decreasing it make it 0).

    During adding the next element, we also adjust the consecutive labels.
    If it is an increment, we simply add the newly updated increase chain label,
    otherwise if it is a decrement, we simply take away the newly updated decrease chain label.
    If it is an equal, then we do nothing

    We store each of the number in the out_array to print all at once at the end to avoid
    I/O overhead cost.
    :param arr - the given array of number
    :param k - the given window to slide
    """
    if k > len(arr):
        print 'Given a bigger window than the available numbers/data points.'
        return

    # Output array to print all at once at the end
    out_array = []

    # Store the initial subrange
    cur_deque = deque(arr[0:k])

    # Making the initial label
    # Start out with 0 for the first element
    increase = deque([0])
    decrease = deque([0])

    # Skip over the first elem evaluation
    for i in range(1, len(cur_deque)):
        cur_num = cur_deque[i]
        prev_num = cur_deque[i-1]
        adjust_label(increase, decrease, cur_num, prev_num)

    # Making initial sum
    cur_sum = 0

    for num in increase:
        cur_sum += compute_triangular(num)
    for num in decrease:
        cur_sum -= compute_triangular(num)

    # Result of the first subrange
    out_array.append(str(cur_sum))

    for i in range(k, len(arr)):
        # remove the first item
        removed_num = cur_deque.popleft()

        # Check to see if it interupts positive or negative consecutive chain
        if removed_num < cur_deque[0]:
            assert increase[0] != 0 # should never be 0 if it came from positive chain
            cur_sum -= increase[0]
            # Decrease consecutive chain if possible, otherwise remove the consecutive
            if (increase[0] - 1) > 0:
                increase[0] -= 1
            else:
                increase.popleft()
        elif removed_num > cur_deque[0]:
            assert decrease[0] != 0 # should never be 0 if it came from negative chain
            cur_sum += decrease[0]
            # Decrease consecutive chain if possible, otherwise remove the consecutive
            if (decrease[0] - 1) > 0:
                decrease[0] -= 1
            else:
                decrease.popleft()

        # add new item (store the last current element before doing so)
        new_num = arr[i]
        old_num = cur_deque[-1]
        cur_deque.append(new_num)

        # adjust consecutive chain
        adjust_label(increase, decrease, new_num, old_num)
        # Increasing subrange
        if new_num > old_num:
            cur_sum += increase[-1]
        # Decreasing subrange
        elif new_num < old_num:
            cur_sum -= decrease[-1]

        out_array.append(str(cur_sum))
    print '\n'.join(out_array)


if __name__ == '__main__':
    # Open the file
    f = open('input.txt')

    # Strip away new line and leading/trailing whitespace
    lines = [line.strip() for line in f.readlines()]

    # Cast the first input of n and k to int
    n, k = [int(num) for num in lines[0].split(' ')]
    nums = [int(num) for num in lines[1].split(' ')]
    # Unused variable n
    print_ranges(nums, k)

