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

The python equivalent to this code is [here](codes\SIERPINSKI_GASKET.py). The image after running the puthon file will look like, <img title="a title" style="float: center;" alt="Alt text" src="assets\SIERPINSKI_GASKET.jpeg">

Any three non-colinear points will form a plane, to generate same as above result along that plane we will simply update the `vertices` to `vec3` something like,

```js
var vertices = [
    vec3(-1.0, -1.0, 0.0),
    vec3(0.0, 1.0, 0.0),
    vec3(1.0, -1.0, 0.0),
];
```

The python equivalent to this code is [here](codes\SIERPINSKI_GASKET_3d.py). The image after running the python file will look like, <img title="a title" style="float: center;" alt="Alt text" src="assets\SIERPINSKI_GASKET_3d.jpeg">

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

Consider the entire graphics system to be a state machine, a black box containing a finite-state machine. This state machine receives inputs from the application software, which may cause the machine's state to change or it to create an output. Graphics functions in WebGL are classified into two types: those that cause primitives to flow through a pipeline and those that change the state of the pipeline. Most define the state by activating various WebGL capabilities or by configuring rendering settings. In WebGL, there are just two functions that may generate output.

WebGL, the most recent version of the graphics programming language, now allows developers to design and utilise their own state variables rather than depending on third-party tools.

### OpenGL AND WebGL

The essential functions of WebGL are stored in a library called GL (or OpenGL in Windows). Shaders are authored in the OpenGL Shading Language (GLSL), however libraries exist to offer a basic common interface. Applications that use OpenGL and various window systems must be recompiled for each platform.

To improve code readability, desktop OpenGL and WebGL make extensive use of specified constants. We do not need to adjust to the local system because WebGL works within the browser. These constants will appear in all of our WebGL apps as strings such as gl.FILL and gl.POINTS, where gl is the name we provide to the WebGL context.

Neither OpenGL nor WebGL is object oriented. For many tasks, WebGL must offer a wide range of data types via different forms. WebGL and WebGL are not object oriented. Because JavaScript has only one numerical type, WebGL programmes may be simplified, and we only need to care about data types in activities involving data transfer between the CPU and the GPU. As a result, for many tasks, OpenGL and, to a lesser extent, WebGL must offer a range of data types via different forms.

### WebGL INTERFACE

<image src="assets\WebGL_organization.JPG" style='float :right;' width=300>
WebGL is compatible with a variety of different online apps, frameworks, and tools. WebGL web applications are developed in JavaScript, a language with syntax similar to high-level languages like C, C++, and Java. JavaScript, in particular, is object oriented in a totally different way than C++ or Java, with relatively few native types and functions as first-class objects.

The general procedure for starting a WebGL application is as follows. The programme is stored on a computer known as the server, and the computer on which we operate it is referred to as the client. The browser is a machine that can access the programme via its Uniform Resource Locator, or URL.

An HTML page is made up of tags and data at its core. Web pages adhere to the industry-standard Document Object Model (DOM). Every web page is a document object, and HTML is the standard description language for them. JavaScript code identified by a script element may be executed by all browsers. The HTML Canvas element offers a drawing canvas for browser-based applications.

### COORDINATE SYSTEM

Previously, computer graphics systems required the user to define all information, such as vertices and pixels, in display device units. If that were true for high-level application programmes, we'd have to talk about points in terms of screen locations measured in pixels or centimetres from a screen corner.

The advent of device-independent graphics liberated application programmers from having to worry about the specifics of input and output devices. In most applications, <b>vertex coordinates</b> are the same as object or world coordinates; but, depending on what we do or do not do in our shaders, vertex coordinates might be one of the various internal coordinate systems utilised in the pipeline.

At some point, the values in vertex coordinates must be mapped to window coordinates, and it is performed automatically as part of the rendering process.

## PRIMITIVES AND ATTRIBUTES

We can separate primitives into two classes: <b>geometric primitives</b> and <b>image</b>, or <b>raster, primitives</b>.

-   ### GEOMETRIC PRIMITIVES
    They contain points, lines, polygon, and sent seperatly to the geometric pipline in the graphical pipeline. In that pipeline they go through different geometric manipulation like, rotation, translation, clipping and rasterization.
    -   <b>Points</b> (`gl.POINTS`) Each vertex is displayed at a size of at least one pixel
    -   <b>Line segments</b> (`gl.LINES`) The line-segment type causes successive pairs of vertices to be interpreted as the endpoints of individual segments. Note that successive segments usually are disconnected because the vertices are processed on a pairwise basis.
    -   <b>POLYLINES</b> (`gl.LINE_STRIP`, `gl.LINE_LOOP`) If successive vertices (and line segments) are to be connected, we can use the line strip, or polyline form. Many curves can be approximated via a suitable polyline. If we wish the polyline to be closed, we can locate the final vertex in the same place as the first, or we can use the `gl.LINE_LOOP` type, which will draw a line segment from the final vertex to the first, thus creating a closed path.
-   ### POLYGON BASICS

    -   #### Definition
        Any object that has a border which can be described by a line loop.
    -   #### GOOD POLYGON
        -   <b>Simple</b> polygons which do not interset theirselves.
        -   <b>Convex</b> means any line segment that is formed by taking arbitary two unique points from interior or border of the polygon does not interset the polygon.
        -   <b>Flat</b> polygons lie in a unigue plan in $\mathbb{R}^3$.

    The performance of graphics systems is characterized by the number of polygons per second that can be rendered.

-   ### POLYGONs IN WebGL

    <image src="assets\Triangle.png" style="float :right;" width=350>
    WebGL only supports traingles.

    -   <b>Triangle</b> (`gl.TRIANGLES`) The edges are the same as they would be if we used line loops. Each successive group of three vertices specifies a new triangle.
    -   <b>Strips and fans</b> (`gl.TRIANGLE_STRIP` , `gl.TRIANGLE_FAN`) These objects are based on groups of triangles that share vertices and edges. In the triangle strip, for example, each additional vertex is combined with the previous two vertices to define a new triangle (Figure 2.14). A triangle fan is based on one fixed point. The next two points determine the first triangle, and subsequent triangles are formed from one new point, the previous point, and the first (fixed) point.

-   ### TRIANGULATION
    Triangulation is a special case of the more general problem of tessellation. The usual strategy is to start with a list of vertices and generate a set of triangles consistent with the polygon defined by the list, a process known as <b>triangulation</b>. Every traingle is a good polygon (see above for reference). <b>Delaunay triangulation</b> algorithm finds a best triangulation.
-   ### TEXT

    <b>Stroke text</b> is constructed like other geometric objects. We use vertices to define line segments or curves that outline each character. If the characters are defined by closed boundaries, we can fill them. The advantage of stroke text is that it can be defined to have all the detail of any other object, and because it is defined in the same way as other graphical objects are, it can be manipulated by our standard transformations and viewed like any other graphical primitive.

    <b>Raster text</b> is simple and fast. Characters are defined as rectangles of bits called <b>bit blocks</b>. Each block defines a single character by the pattern of 0 and 1 bits in the block. A raster character can be placed in the framebuffer rapidly by a <b>bit-block-transfer (bitblt)</b> operation, which moves the block of bits using a single function call.

-   ### CURVEY OBJECTS

    Bazier Curves and other techniques are used for it.

-   ### ATTRIBUTES
    Properties that describe how an object should be rendered are called <b>attributes</b>.

## COLOR

It is an interesting part of graphics and animation and also very crucial to human understanding and psychie. Visible color is characterized by a function $C(\lambda)\in [350 \text{ nm}, 780 \text{ nm}]$, where $\lambda$ is the wave-length of the light. Human brain does not percieve the complete visible light range, but it is sensitive to three colors (as our retina have color cones which are sensitive to three colors) - the <b>tristimulus values</b>.

<b>Additive colors</b> are produced by varing the intensity of primary colors of additive system that are RGB (Red Green Blue). <b>Subtractive color models</b> are produced by varing the intensity of complementary colors that are CMY (Cyan Magenta Yellow).

-   ### RGB COLOR

    They follow index color model. A natural technique is to use the color cube and to specify color components as numbers between 0.0 and 1.0, where 1.0 denotes the maximum of the corresponding primary, and 0.0 denotes a zero value of that primary. We can assign colot to each vertex as a seperate color object, such as

    ```js
    var colors = [
        vec3(1.0, 0.0, 0.0),
        vec3(0.0, 1.0, 0.0),
        vec3(0.0, 0.0, 1.0),
    ];
    ```

    We can use 4-dimensional vectors to make this RGBA color system. When A = 0.0 the object is fully transparent and when A = 1.0 the object is fully opace. We can also use, `gl.clearColor(1.0, 1.0, 1.0, 1.0);` to make screen solid color. RGB values are maximum and because $\alpha$-channel is also high this means we will get a solid white color.

-   ### INDEXED COLOR
    We have $2^m$ bits for each Red, Green and Blue color. The framebuffer can specify only $2^k$ for them. $k=m=8$ is a common practice, where user can choose 256 colors.

## VIEWING

-   ### ORTHOGRAPHIC VIEW
    All light rays coming from scene are parallel and hit perpendicular to the camera. It is formed when our camera is at infinity (considerably large distance) or the scene is at infinity. Rather than worrying about cameras an infinite distance away, suppose that we start with projectors that are parallel to the positive $z$-axis and the projection plane at $z=0$. It takes a point $(x, y, z)$ and projects it into the point $(x, y, 0)$. In WebGL the volume cube has ranges $-1\le x,y,z\le 1$.

## CONTROL FUNCTIONS

-   ### ASPECT RATIO AND VIEWPORT
    The aspect ratio of a rectangle is the ratio of the rectangle’s width to its height. A viewport is a rectangular area of the display window. By default, it is the entire window, but it can be set to any smaller size in pixels via the function `gl.viewport(x, y, w, h);` where `(x,y)` is the lower-left corner of the viewport, and `w` and `h` give the width and height, respectively.

<!-- ## THE GASKET PROGRAM -->

## POLYGONS AND RECURSION

Similar python code is [here](codes\divide_triangle.py).

```js
var vertices = [vec2(-1.0, -1.0), vec2(0.0, 1.0), vec2(1.0, -1.0)];

function triangle(a, b, c) {
    points.push(a);
    points.push(b);
    points.push(c);
}

function divideTriangle(a, b, c, count) {
    if (count == 0) {
        triangle(a, b, c);
    } else {
        var ab = scale(0.5, add(a, b));
        var bc = scale(0.5, add(b, c));
        var ac = scale(0.5, add(a, c));

        --count;
        divideTriangle(a, ab, ac, count);
        divideTriangle(c, ac, bc, count);
        divideTriangle(b, bc, ab, count);
    }
}

divideTriangle(vertices[0], vertices[1], vertices[2], numTimesToSubdivide);
```

## THE THREE-DIMENSIONAL GASKET
