All experiments are run from the command line from within the ai-assignment-1-search/ root directory. The script requires two arguments: --domain and --algo.

Here are the commands to run the four experiments:
1. Classic WGC with Breadth-First Search

python -m run --domain wgc --algo bfs

2. Classic WGC with Iterative-Deepening Search

python -m run --domain wgc --algo ids

3. WGC with Sheep using Breadth-First Search

python -m run --domain wgc-sheep --algo bfs

4. WGC with Sheep using Iterative-Deepening Search

python -m run --domain wgc-sheep --algo ids