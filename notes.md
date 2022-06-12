# Graphics Programming

## THE SIERPINSKI GASKET

   <img title="a title" style="float: right;" alt="Alt text" src="assets\Sierpinski_Gasket.JPG">

1. Pick an initial point $p = (x, y, 0)$ at random inside the triangle.
2. Select one of the three vertices at random.
3. Find the point $q$ halfway between $p$ and the randomly selected vertex.
4. Display $q$ by putting some sort of marker, such as a small circle, at the corresponding location on the display.
5. Replace $p$ with $q$.
6. Return to step 2.

The psuedo-code for this algorithim will be,

```
function sierpinski()
{
    initialize_the_system();
    p = find_initial_point();

    for (some_number_of_points)
    {
        q = generate_a_point(p);
        display_the_point(q);
        p = q;
    }

    cleanup();
}
```

The real code will look like

The strategy used in this algorithm is known as <b>immediate mode graphics</b> and, until recently, was the standard method for displaying graphics, especially where interactive performance was needed. One consequence of immediate mode is that there is no memory of the geometric data. With our first example, if we want to display the points again, we would have to go through the entire creation and display process a second time.

```js
function sierpinski()
{
    initialize_the_system();
    p = find_initial_point();

    for (some_number_of_points)
    {
        q = generate_a_point(p);
        store_the_point(q);
        p = q;
    }

    display_all_points();
    cleanup();
}
```

In our second algorithm, because the data are stored in a data structure, we can redisplay the data. The method of operation is known as <b>retained mode graphics</b> and goes back to some of the earliest special-purpose graphics display hardware. This approach has one major flaw. Suppose that we wish to redisplay the same objects in a different manner, as we might in an animation. The geometry of the objects is unchanged but the objects may be moving. Displaying all the points as we just outlined involves sending the data from the CPU to the GPU each time that we wish to display the objects in a new position. For large amounts of data, this data transfer is the major bottleneck in the display process. Consider the following alternative scheme:

```js
function sierpinski()
{
    initialize_the_system();
    p = find_initial_point();

    for (some_number_of_points)
    {
        q = generate_a_point(p);
        store_the_point(q);
        p = q;
    }

    send_all_points_to_GPU();
    display_data_on_GPU();
    cleanup();
}
```

As before, we place data in an array, but now we have broken the display process into two parts: storing the data on the GPU and displaying the data that have been stored. If we only have to display our data once, there is no advantage over our previous method; but if we want to animate the display, our data are already on the GPU and redisplay does not require any additional data transfer, only a simple function call that alters the location of some spatial data describing the objects that have moved.

## PROGRAMMING TWO-DIMENSIONAL APPLICATIONS

WebGL utlizes the three dimensional coordinate system. Although we can plot in two dimension setting the $z=0$. A coordinate is usually represented by a point $\textbf{p}=(x,y,z)$ or column vector $\textbf{p}=\begin{bmatrix} x & y & z\end{bmatrix}^\intercal$. We use the terms vertex and point in a somewhat different manner in WebGL. A vertex is a position in space; we use two-, three-, and four-dimensional spaces in computer graphics.

We want to start with as simple a program as possible by putting all the data we want to display inside a cube centered at the origin whose diagonal goes from $(−1, −1, −1)$ to $(1, 1, 1)$. This system, known as <b>clip coordinates</b>. Objects outside this cube will be eliminated or <b>clipped</b> and cannot appear on the display.

We could write the program using a simple array of two elements to hold the `x` and `y` values of each point. In JavaScript, we would construct such an array as follows:

```js
var p = new Float32Array([x, y]);
var n = p.length;
```

`p` is just a contiguous array of standard 32-bit floating-point numbers.
