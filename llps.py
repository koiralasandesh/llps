from matplotlib import pyplot as plt, rc
from matplotlib.animation import FuncAnimation
from copy import deepcopy
from enum import Enum

def init():
  global sequence
  global ax
  global lines

  #Set up the drawing area
  ax = plt.axes(xlim=(0, len(sequence)+1), ylim=(0, max(sequence)+1))
  ax.set_xlabel('Left-end of streak interval')
  ax.set_ylabel('Minival value in the streak')

  #Draw an empty line since the init() function must return some lines
  lines, = ax.plot([], [], lw=2)
  return lines,
 
def animate(i):
  global sequence
  global ax
  global lines
  global growing_streaks

  if i % 2 == 0:
    #Draw an horizontal line that represents the value at the [i//2 + 1]-th position in the sequence. 
    #If i equals 0, it is the 1st position in the sequence. 
    #If i equals 2, it is the 2nd position in the sequence.
    #And so on.
    ax.axhline(y=sequence[i//2], color='red', linestyle='-.')
    lines.set_data([], [])
    return lines, 
  else: 
    #Draw the markers that represent the growing streaks after the [i//2+1]-th value in the sequence.
    #If i equals 1, it is the 1st position in the sequence. 
    #If i equals 3, it is the 2nd position in the sequence.
    #And so on.
    ax.clear()
    ax.set_xlabel('Left-end of streak interval')
    ax.set_ylabel('Minival value in the streak')
    ax.set_xlim(0, len(sequence)+1)
    ax.set_ylim(0, max(sequence)+1)
    for gs in growing_streaks[i//2]:
      sc, = ax.plot(gs[0], gs[2], marker='s', markerfacecolor='none', markeredgecolor='green', markersize=12, ls='')
    return sc,

#main function to return the streaks
def llps(sequence):
    #creting empty list to append streaks after each iteration
    local_prominent_streaks=[]
    prominent_streaks=[]
    growing_streaks=[]

    #loop through each number in sequence
    for current_position in range(len(sequence)):
        #current number in sequence
        current_value=sequence[current_position]
        #exception for first number in sequence
        if current_position==0:
            #empty streaks to fill with streaks after this iteration
            current_lps=[]
            current_ps=[]
            current_gs=[]
            current_gs.append([1,1,current_value])
            local_prominent_streaks.append(current_lps)
            growing_streaks.append(current_gs)
            prominent_streaks.append(current_gs)
            continue

        #copying streaks from last iteration to modify for this iteration
        current_ps=[]
        current_lps=deepcopy(local_prominent_streaks[current_position-1])
        current_gs=deepcopy(growing_streaks[current_position-1])
        looping_gs=deepcopy(growing_streaks[current_position-1])

        #modifying previous growing streaks with respect to the current number in sequence
        for x in range(len(looping_gs)):
            this_gs=looping_gs[x]                    
            if this_gs[2]<=current_value:
                current_gs[x][1]=current_gs[x][1]+1

            if this_gs[2]>current_value:
                current_lps.append(this_gs)
                current_gs.remove(this_gs)

        #creating new streaks to append to growinf streaks of current iteration 
        left_end=find_left(sequence,current_position)
        right_end=current_position
        temp_gs=[left_end+1,right_end+1,current_value]
        if temp_gs not in current_gs:
            current_gs.append(temp_gs)
        
        #creating one list of all growing and lps for this iteration to find skyline
        all_current_streaks = []
        for x in current_gs:
            all_current_streaks.append(x)
        for x in current_lps:
            all_current_streaks.append(x)

        #skyline streaks among all streaks in this iteration
        current_ps =find_skyline(all_current_streaks)      
        
        #appending streaks in this iteration to larger list of all iterations
        local_prominent_streaks.append(current_lps)
        growing_streaks.append(current_gs)
        prominent_streaks.append(current_ps)
    return local_prominent_streaks, growing_streaks, prominent_streaks

#function to find the lest_end to create new streaks
def find_left(sequence,curr_position):
    if curr_position==0:
        return 0
    curr_value= sequence[curr_position]
    for x in range(curr_position,0,-1):
        if sequence[x]<curr_value:
            return x+1
    return 0

#function to find the skyline streaks among various sttreks passed as list
def find_skyline(streaks): 
    #creating empty skyline list 
    skyline = []
    #loop through all streaks
    for p in streaks:
        updated=[]
        outcome=None
        #loop through all skyline poins if any exists
        for q in skyline:
            #compare current streak with curent skyline streak
            outcome=compare(p,q)
            if outcome==Outcome.DOMINATED: break
            if outcome!= Outcome.DOMINATES: updated.append(q)
        if outcome!=Outcome.DOMINATED:
            skyline=updated
            skyline.append(p)
    return skyline

#function to compare streaks
def compare(p,q):
    if len(p)!=len(q): return Outcome.INCOMPARABLE
    p_greater=False
    q_greater=False
    #compare based on eiter length of streak or value of streak
    q_greater=((q[2]>=p[2]) and ((q[1]-q[0])>(p[1]-p[0]))) or ((q[2]>p[2]) and ((q[1]-q[0])>=(p[1]-p[0])))
    p_greater=((q[2]<=p[2]) and ((q[1]-q[0])<(p[1]-p[0]))) or ((q[2]<p[2]) and ((q[1]-q[0])<=(p[1]-p[0])))
    if p_greater and not q_greater: return Outcome.DOMINATES
    if not p_greater and q_greater: return Outcome.DOMINATED
    return Outcome.NO_DOMINANCE
   


#creating outcomes
class Outcome(Enum):
    DOMINATED=1
    DOMINATES=2
    INCOMPARABLE=3
    NO_DOMINANCE=4

#You should test your code using different sequences to make sure your code
#correctly consider all scenarios. We will test your code by using different 
#sequences.

sequence = [3, 1, 7, 7, 2, 5, 4, 6, 7, 3]
local_prominent_streaks, growing_streaks, prominent_streaks = llps(sequence)
print("lps:")
for x in local_prominent_streaks:
    print(x)
print("\ngs:")
for x in growing_streaks:
    print(x)
print("\nps:")
for x in prominent_streaks:
    print(x)

#You should comment out the following hard-coded values of local_prominent_streaks, 
#growing_streaks, and prominent_streaks. They are provided in this file to help 
#you see how the rest of the code works. 

# local_prominent_streaks = [
#   [], 
#   [[1, 1, 3]], 
#   [[1, 1, 3]], 
#   [[1, 1, 3]], 
#   [[1, 1, 3], [3, 4, 7]],
#   [[1, 1, 3], [3, 4, 7]],
#   [[1, 1, 3], [3, 4, 7], [6, 6, 5]],
#   [[1, 1, 3], [3, 4, 7], [6, 6, 5]],
#   [[1, 1, 3], [3, 4, 7], [6, 6, 5]],
#   [[1, 1, 3], [3, 4, 7], [6, 6, 5], [6, 9, 4], [8, 9, 6], [9, 9, 7]]
# ]
# growing_streaks = [
#   [[1, 1, 3]], 
#   [[1, 2, 1]], 
#   [[1, 3, 1], [3, 3, 7]], 
#   [[1, 4, 1], [3, 4, 7]], 
#   [[1, 5, 1], [3, 5, 2]], 
#   [[1, 6, 1], [3, 6, 2], [6, 6, 5]], 
#   [[1, 7, 1], [3, 7, 2], [6, 7, 4]], 
#   [[1, 8, 1], [3, 8, 2], [6, 8, 4], [8, 8, 6]], 
#   [[1, 9, 1], [3, 9, 2], [6, 9, 4], [8, 9, 6], [9, 9, 7]], 
#   [[1, 10, 1], [3, 10, 2], [6, 10, 3]]
# ]
# prominent_streaks = [
#   [[1, 1, 3]],
#   [[1, 2, 1], [1, 1, 3]],
#   [[1, 3, 1], [3, 3, 7]],  
#   [[1, 4, 1], [3, 4, 7]],  
#   [[1, 5, 1], [3, 5, 2], [3, 4, 7]],  
#   [[1, 6, 1], [3, 6, 2], [3, 4, 7]],  
#   [[1, 7, 1], [3, 7, 2], [3, 4, 7]],  
#   [[1, 8, 1], [3, 8, 2], [6, 8, 4], [3, 4, 7]],  
#   [[1, 9, 1], [3, 9, 2], [6, 9, 4], [3, 4, 7]], 
#   [[1, 10, 1], [3, 10, 2], [6, 10, 3], [6, 9, 4], [3, 4, 7]]
# ]

#You shouldn't change anything below. The code is for setting up the animation. 
fig = plt.figure(figsize=(8,8))
ax = None
lines = None

ani = FuncAnimation(fig, animate, init_func=init, frames=len(sequence*2), interval=1000, blit=True)
rc('animation', html='html5')
ani