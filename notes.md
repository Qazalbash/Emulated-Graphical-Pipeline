# Graphics Programming

## Sierpinski Gasket

1. Pick an initial point $p = (x, y, 0)$ at random inside the triangle.
   <img title="a title" style="float: right;" alt="Alt text" src="assets\Sierpinski_Gasket.JPG">
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
