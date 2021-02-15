# Breadth First Search

This program tries to solve the Post Correspondence problem according to the following algorithm.

– In the first stage of search, use a breadth-first search through the state space
detailed in problem 4 from the written component until the queue of frontier
states has reached a specified maximum. You should use a HashMap or
Dictionary over strings to eliminate repeated states.

– In the second stage of search, use iterative deepening starting from the frontier
created in the first stage, until a specified limit has been reached.



## More Info!

• Input


– The maximum size of the queue (the frontier) used in the breadth-first search.
– The value of some kind of parameter (e.g. maximum depth; maximum number of states; maximum run time) that will to prevent the program from going
into an infinite loop. Note that the program can go into an infinite loop either in stage 2 or in stage 1, if the search can proceed without exhausting the
queue, so the limit must apply to both stages.

– The set of dominos.

– (*) A flag indicating the type of output, as described in the next section
(Output).
Use a simple format for inputting, but do not hard code any aspect of the input.


• Output
The program should always output one of the following three:

– A sequence of dominos that solve the problem.

– A flag indicating that no solution exists.

– A flag indicating that no solution was found within the limits of search.
In addition if the flag in (*) above is set, the program should output the sequence of states generated in searching for the solution.


```bash
Python 3.7
```

## Usage

```python
In command line 
cd #local file 
#change input.txt with files to run code
python dominos.py input.txt

```
