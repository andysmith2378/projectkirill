To install, pip the requirements with:

pip install -r requirements.txt

Run from the command line with:

python main.py


Click to zoom in at the position of the mouse pointer.


Finds the number of times one must apply the function,
f(a, b) = a * a + b, to each point before the result exceeds
Grid.threshold.

If Grid.elementwise equals True, Grid.fill() uses a straight-forward,
ineffecient method, one element at a time:
    for every point, x, on the horizontal axis
        for every point, y, on the vertical axis
            find the number of times one must apply the function

If Grid.elementwise equals False, Grid.fill() uses a faster array
method instead


To set Grid.elementwise to True or False, change ELEMENTWISE in
main.py here:

if __name__ == '__main__':
    ELEMENTWISE = True