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

The three-dimensional coordinate system has been used by WebGL. Although, by setting the $z=0$. A coordinate is usually represented by a point $\textbf{p}=(x,y,z)$ or column vector $\textbf{p}=\begin{bmatrix} x & y & z\end{bmatrix}^\intercal$. In WebGL, the terms vertex and point are used in somewhat different ways. A vertex is a location in space; in computer graphics, we employ two-, three-, and four-dimensional spaces.

We want to start with a simple programme, so we'll place all of the data we want to show within a cube centred at the origin, with a diagonal running from $(1, 1, 1)$ to $(1, 1, 1)$. This is referred as as <b>clip coordinates</b>. Objects outside this cube will be removed or <b>clipped</b> and will not appear on the screen.

The programme might be written using a simple array of two items to hold the `x` and `y` values of each point. In JavaScript, we might create an array like this:

```js
var p = new Float32Array([x, y]);
var n = p.length;
```

`p` is just a contiguous array of standard 32-bit floating-point numbers. We can initialize an array component wise like,

```js
p[0] = x;
p[1] = y;
```

We can produce much cleaner code if we first define a two-dimensional point object and its actions. We developed such objects and methods and included them in the MV.js package. Numeric data is stored within these objects using JavaScript arrays.

The types in the OpenGL ES Shading Language (GLSL) that we use to construct our shaders correspond to the functions and three- and four-dimensional objects defined in MV.js. As a result, using MV.js should make all of our code examples clearer than if we had used regular JavaScript arrays. Although these functions were designed to be GLSL-compliant, because JavaScript does not provide operator overloading like C++ and GLSL, we wrote functions for arithmetic operations involving points, vectors, and other kinds. Nonetheless, code pieces written in MV.js, such as

```js
var a = vec2(1.0, 2.0);
var b = vec2(3.0, 4.0);
var c = add(a, b); // returns a new vec2
```

may be utilised in the programme and simply transformed into shader code. Individual components can be accessed via indexing, much like an array ( a[0] and a[1] ). The code below creates 5000 points by starting with the vertices of a triangle in the plane $z=0$:

```js
const numPoints = 5000;

var vertices = [vec2(-1.0, -1.0), vec2(0.0, 1.0), vec2(1.0, -1.0)];

var u = scale(0.5, add(vertices[0], vertices[1]));
var v = scale(0.5, add(vertices[0], vertices[2]));
var p = scale(0.5, add(u, v));

points = [p];

for (var i = 1; i < numPoints; ++i) {
    var j = Math.floor(Math.random() * 3);

    p = scale(0.5, add(points[i - 1], vertices[j]));
    points.push(p);
}
```

The python equivalent to this code is [here](SIERPINSKI_GASKET.py). The image after running the puthon file will look like, <img title="a title" style="float: center;" alt="Alt text" src="assets\SIERPINSKI_GASKET.jpeg">

Any three non-colinear points will form a plane, to generate same as above result along that plane we will simply update the `vertices` to `vec3` something like,

```js
var vertices = [
    vec3(-1.0, -1.0, 0.0),
    vec3(0.0, 1.0, 0.0),
    vec3(1.0, -1.0, 0.0),
];
```

The python equivalent to this code is [here](SIERPINSKI_GASKET_3d.py). The image after running the puthon file will look like, <img title="a title" style="float: center;" alt="Alt text" src="assets\SIERPINSKI_GASKET_3d.jpeg">

## THE WEBGL APPLICATION PROGRAMMING INTERFACE

### GRAPHICS FUNCTION

In essence, a graphics programme is a <b>black box</b>, a term used by engineers to describe a system whose attributes are defined solely by its inputs and outputs; we may know nothing about its fundamental workings. Consider the graphics system to be a box whose inputs include application programme function calls, measurements from input devices like the mouse and keyboard, and maybe extra input like operating system messages. The visuals sent to our output devices are the primary outputs.

<img title="a title" style="float: center;" alt="Alt text" src="assets\graphics_function.JPG">

A graphics system performs a number of tasks in order to create output and handle user input. An API for interfacing with this system may include hundreds of functions. These functions can be divided into seven categories:

1. #### <b>Primitive functions</b>
    Primitives are low-level objects or atomic entities that our system may display. Primitives can be points, line segments, polygons, pixels, text, and many types of curves and surfaces. WebGL natively offers a limited set of primitives, such as points, lines and triangles. Larger primitive sets are frequently supported with high efficiency using programmable shaders.
2. #### <b>Attribute functions</b>
    In WebGL, attributes are how of an API. Attributes control how a primitive looks on the screen. They can be as simple as selecting a colour to show a line segment or a pattern to fill a polygon, or selecting a typeface for the titles on a graph.
3. #### <b>Viewing functions</b>
    If we are to construct a picture, we must explain our synthetic camera's position and orientation in our environment. WebGL does not have any viewing functions and instead depends on transformations in the application or shaders to create the required view. This allows us to define numerous views, although degree of freedom provided by APIs varies.
4. #### <b>Transformation functions</b>
    WebGL allows us to perform complex transformations such as rotation, translation, and scaling. A good API offers the user with a collection of transformation functions that allow her to perform object transformations. Transformations are carried out in WebGL by creating them in our apps and then applying them either in the application or in the shaders.
5. #### <b>Input functions</b>
    An API for interactive applications must have a collection of input methods that allow us to deal with the many types of input that define current graphics systems. We require functionalities to interact with devices like keyboards, mouse, and data tablets.
6. #### <b>Control functions</b>
    Control functions let us to interface with the window system, configure our programmes, and handle any issues that occur during programme execution. In any actual programme, we must also consider the complications of working in a multiprocessing, multiwindow environment. Such an environment is typically one in which we are linked to a network and there are other users.
7. #### <b>Query functions</b>
    If we are to develop device-independent applications, we should expect the API implementation to account for changes across devices, such as the number of colours available or the size of the display. However, there are some cases where we need to know some features of the specific implementation. For example, if we knew ahead of time that we would be dealing with a display that could only handle two colours rather than millions, we would probably do things differently. In general, we may frequently use other information from the API within our apps, such as camera settings or framebuffer data. A good API delivers this information via a set of query functions.

### THE GRAPHICS PIPELINE AND STATE MACHINE
