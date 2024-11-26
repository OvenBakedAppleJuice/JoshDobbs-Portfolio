Project 3 Report

Josh Dobbs

11/25/2024

When I first start I kept up with making the unittest file, but as I got into more problems of
find_path after just finishing find_shortest_path I started to not make many test cases for my
problems, simply because there was no way to check my problem besides just using the
debugger and print statements. For example, one of my first major problems I was stuck on was
getting an index error when grabbing the top item from the stack of spots to visit in solve. Which
was strange because before I add an item to that stack I check to see if it exists on the grid, or
at least I thought I was doing that correctly. There was no way to check the local variable stack
in solve (at least from my knowledge), so I couldn’t make a test case for this anyways. I do wish
I could’ve, I mean I could have with a new instance variable but prarielearn wouldn’t like that.
Right now, my stack for both find functions use a list as the path stack rather than the llstack. I
did this because the way I store the path to that current point was to take the previous path and
add the current position to it. Originally it sounded simple, use push to add that current spot to
the list, but for the previous spot storing that llstack would have that new spot added to its path.
Which isn’t correct. I would need a new llstack for each position, but we did not make a combine
method in llstack to combine 2 together. I would have to iterate through the previous positions
llstack and add all those values to the new llstack + the new position. So why not just use a list
where storing it in the visited dictionary creates a new list object. Even after finishing I still do not
know how to properly use llstack besides making a new method for this case or iterating and
adding all new values to the new object (which would be very annoying considering we are not
allowed to use loops). I would write an optional argument for LLStack() that takes in an already
existing LLStack to duplicate it. So I thought the more efficient way of going was to return a list
have find_path convert that list to the llstack with a helper_function that iterates until the list is
empty then returns that llstack object.
Many of my other problems were within just checking the positions next to the current
position before adding it to the stack. Considering that I’m in discrete 2 where we talk about
shortests paths for 70% of the course, I had already known the exact algorithms to use for each
function the moment you talked about them in class. Depth first search and a simple version of
Dijkstra's algorithm that is essentially just Breadth first search. These algorithms stop when the
end result is detected in the visited list and returns that path. Had a few other minor issues like
the grid checking, honestly should’ve just noticed that one myself. So the unittests I ran into are
really all the issues I can make into unittests. I had no other issues that just understanding how
to read self.grid[][] to check near by positions. I was mostly stuck on reading the grid like
self.grid[x][y] since thats how the last projects 2D list was interpreted (These projects made me
hate 2D lists), when in reality for this project the GUI displays the grid as self.grid[y][x] because
each row going down is x and the positions inside those rows are y. This is why you see the
comments incorrectly relating to how the map is on the GUI. Instead imagine the map rotated 90
degrees to the left and the x, y coordinates work. I also thought while coding the find_path that
all the maps would be square so it would be possible to do (x-1, y) or (x+1, y) but no. In
conclusion 2D lists suck.
This report is tough because I can’t say I had many problems with this project, besides
just understanding how the project interprets this 2D list. So I wrote what I could, tested the
sample, no path, and a random one given from the path_gui. As well as a few others like edge
cases and the only thing I could think of where my problem was unittestable.