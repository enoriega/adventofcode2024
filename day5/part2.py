import itertools as it
from collections import defaultdict, deque

from typing import Optional

def main():
    # Read the data
    with open("day5/input.txt") as f:
        # Read rules
        rules = [[int(n) for n in l.split('|')] for l in it.takewhile(lambda line: line.strip(), f)]
        # Read the updates
        updates = [[int(n) for n in l.split(',')] for l in f]

    # Build lists of predecessors
    predecessors = defaultdict(set)

    for h, t in rules:
        # Add the predecessor to the corresponding list
        predecessors[t].add(h)

    
    def validate_update(update:list[int]) -> bool:
        """ Check if any element to the right doesn't occur to the left """
        invalid = False
        ix = len(update)-1
        while ix > 0:
            swapped = False
            jx = ix-1
            while jx >= 0:
                if update[jx] not in predecessors[update[ix]]:
                    hold = update[ix]
                    update[ix] = update[jx]
                    update[jx] = hold
                    invalid = True
                    swapped = True
                    break
                jx -= 1
            if not swapped:
                ix -= 1

        return invalid
                
                
    # Now check the updates to see if they are invalid
    total = 0 # Accumulate the middle elements here
    for update in updates:
        is_invalid = validate_update(update)
        if is_invalid:
            total += update[len(update)//2]

    print(total)




        


if __name__ == "__main__":
    main()

