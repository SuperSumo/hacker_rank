from collections import defaultdict
import bisect
import itertools


def mocked_raw_input(fname):
    def set_raw_input_string(fname):
        for line in open(fname):
            yield line
    yield_func = set_raw_input_string(fname)

    def z():
        return next(yield_func)
    return z


# The function to add a track to a row
def add_mask(tracks, row, start, end):

    print ''
    print tracks
    print 'INSERTING ROW', row, (start, end)

    # If no tracks, insert and go away
    if len(tracks[row]) == 0:
        bisect.insort(tracks[row], (start, end))
        print 'tracks:', tracks
        return

    # Figure out if the start or end is within a track
    startIndex = 0
    startInTrack = None
    endIndex = len(tracks[row])
    endInTrack = None
    # Figure out the start position
    for i in xrange(len(tracks[row])):
        tStart, tEnd = tracks[row][i]
        print 'testing start', i, tStart, tEnd
        if start >= tStart:
            print 'startIndex is now', i
            startIndex = i
            if start < tEnd:
                print "Staring in track!", i
                startInTrack = i
        else:
            print 'found startIndex', startIndex
            break
    # Figure out the end position
    for i in xrange(len(tracks[row]) - 1, -1, -1):
        tStart, tEnd = tracks[row][i]
        print 'testing end', i, tStart, tEnd
        if end <= tEnd:
            print 'endIndex is now', i
            endIndex = i
            if end > tStart:
                print "Ending in track!", i
                endInTrack = i
        else:
            print 'found endIndex', endIndex
            break

    print 'startInTrack', startInTrack
    print 'endInTrack', endInTrack
    print 'startIndex', startIndex
    print 'endIndex', endIndex

    # If the inserted track is completely in another
    # track, bail out.
    if startInTrack is not None and startInTrack == endInTrack:
        print "Track was engulfed"
        return

    # Fix the start and end if they were in a track
    if startInTrack is not None:
        start = tracks[row][startInTrack][1]
        print "Start is now", start
    if endInTrack is not None:
        end = tracks[row][endInTrack][0]
        print "End is now", end

    # Remove any tracks being completely overlapped
    if endIndex - startIndex > 1:
        for _ in range(startIndex, endIndex):
            print "Removing overlapped track", tracks[row][startIndex]
            del tracks[row][startIndex]

    # Get the position of an inserted track
    trackPos = bisect.bisect(tracks[row], (start, end))
    print 'trackPos', trackPos

    # Check the neighbors for touching tracks and merge
    print 'neighbors', tracks[row][trackPos - 1:trackPos + 1]

    # Check the right track first because of del index
    if trackPos != len(tracks[row]):
        rStart, rEnd = tracks[row][trackPos]
        print 'right', tracks[row][trackPos], trackPos
        if rStart - end == 0:
            print "Deleting right neighbor", tracks[row][trackPos]
            end = rEnd
            del(tracks[row][trackPos])

    # Now check the left track
    if trackPos != 0:
        lStart, lEnd = tracks[row][trackPos - 1]
        print 'left', tracks[row][trackPos - 1], trackPos - 1, start, lEnd
        if start - lEnd == 0:
            print "Deleting left neighbor", tracks[row][trackPos - 1]
            start = lStart
            del(tracks[row][trackPos - 1])

    # Insert the track
    bisect.insort(tracks[row], (start, end))
    print 'tracks:', tracks


# Mock out raw_input
raw_input = mocked_raw_input('gridland_unit_tests.txt')

numRows, numCols, numTracks = map(int, raw_input().split())

# Make a default dictionary of tracks
tracks = defaultdict(list)

# Add the tracks
for _ in xrange(numTracks):
    row, start, end = map(int, raw_input().split())
    add_mask(tracks, row - 1, start - 1, end)

print '\ntracks:', tracks


def sum_tracks(tracks):
    def diff(x):
        return x[1] - x[0]
    trackFlatIterator = itertools.chain.from_iterable(tracks.values())
    return sum(map(diff, trackFlatIterator))


print 'Sum of tracks = ', sum_tracks(tracks)
print 'Open spots = ', numRows * numCols - sum_tracks(tracks)
