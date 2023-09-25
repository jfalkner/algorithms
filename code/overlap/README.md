# Overlapping Segments

Consider that you are working with digital video that you are annotating in
real-time. Certain segments of the video end up with annotations, but not all
of the video may be annotated. Additionally, multiple annotations may exist for
either the same segment or an overlapping segement. All of this data is logged
and later summarized. The task at hand is to summarize per video what total time
range covers all annotations and also a summary of the unique portions of the
video that are annotated.

For example, here are several segments in a format `[video_id, start_time, end_time]`:

```
[1, 2, 3], [1, 3, 4], [1, 6, 9], [1, 5, 6], [2, 0, 1]
```

The total annotated time per video is the lowest start time through highest end
time. e.g.

```
# Total Annotated Time
[1, 2, 9]
[2, 0, 1]
```

The set of unique segements (accounting for overlaps) is the following.

```
[1, 2, 4], [1, 5, 9]
[2, 0, 1]
```

This is a popular code challenge that I've had asked several times. It is a
straight-forward questions that could easily be done suboptimally with a brute
force approach. I think it is popular because it lacks any sort of big computer
science trick for the solution. Anyone should be able to do this. Experienced
programmers will likely give an optimal solution with the first go.

---

Let's break this in to two sections since as presented, you'd likely solve the
first total annotation time question then do the unique segment one. In one
interview the second ask for a list of unique segments was only given after the
first question was solved, which was almost certainly done to avoid letting me
solve the second (harder) question first and using the same solution to solve
both problems.


#### Total Segment Length

Solving total segment length is done by considering that we want to loop through
this data, ideally once, and know the answer. Only the min and the max value
per segment is needed. This can be stored in a dict that is keyed by the video's
id. That'll allow for tracking any number of videos quickly.

Below assumes that input data is alawys correctly formatted and we always have
integer values that can be correctly represented by Python. Start time is always
less or equal to end. These assumptions should be directly noted during the
interview since they save a bunch of time and are almost certainly valid.

'''
segments = [
    [1, 2, 3], [1, 3, 4], [1, 6, 9], [1, 5, 6],
    [2, 0, 1]
]

# dict to track min/max values
total_lengths = {}

# Tuple unpack to get the expected format
for video_id, start_time, end_time in segments:
    min_start, max_end = total_lengths.get(video_id, [start_time, end_time])
    total_lengths[video_id] = [
        min(min_start, start_time),
	max(max_end, end_time)
    ]

# Display the results
for video_id, [start_time, end_time] in total_lengths.items():
    print([video_id, start_time, end_time])
'''

This will print out the expected result from the introduction.

```
# Total Annotated Time
[1, 2, 9]
[2, 0, 1]
```

Performance of the above code is straight-forward. There is just one loop and a
dict being used.

* O(n) for the loop tha iterates once through each segment. 
* O(1) for each dictionary lookup

Total time should be on the order of O(n) where n is the number of segments
considered. If someone is being a stickler, dict usage isn't strictly O(n) and
could be more like O(log(n)), depending on how the hashtable is implemented and
if keys collide; however, for screening challenges like this, it should be fair
to say O(n) and assume key collisions aren't a substantial perf issue.

Memory used is minimal since the dict has just one entry per video and keeps
only two values. In theory, you could process many, many segments wihtout really
worrying about memory use. You'd say this is O(v) for memory use where v is the
unique number of video ids.


##### Overlapping Segments

This is the real, harder part of this question. Instead of tracking the total
span of time that annotations exist per video, track the list of unique segments
that have annotations. This requires reducing overlaps and potentially tracking
more than one segment per video.

The so


