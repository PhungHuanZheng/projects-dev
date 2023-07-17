/**
 * √(-1) = imaginary number i
 * 3 + i = complex number whereby '3' is the real part and 'i' is the imaginary part
 *
 * For this visual, we take the asxes of the canvas, a 2-Dimensional
 * plane, to be x -> real and y -> imaginary. The Mandelbrot set follows
 * the equation:
 *                f(z) = z² + c
 *                f(0) = 0² + c
 *                f(c) = c² + c
 *                f(c² + c) = (c² + c)² + c
 *
 * whereby input 'z' is a complex number, a number with a real and an imaginary part.
 *
 *                (a + bi) * (a + bi)
 *              = a² + abi + abi + b²i²
 *              = a² + 2abi - b²
 *              = (a² - b²) + 2abi (real + imaginary)
 *
 * The Mandelbrot set is the set of numbers for which the function above remains bounded
 * and does not tend towards infinity.
 */

final int MAX_ITERATIONS = 75;
final float scale = 2;

float ca = 0;
float cb = 0;


void setup() {
    size(800, 800);
    pixelDensity(1);
    loadPixels();
    colorMode(RGB);
    for (int x = 0; x < width; x++) {
        for (int y = 0; y < height; y++) {

            // scale numbers down (-2 - 2i to 2 + 2i)
            float a = map(x, 0, width, -scale, scale) - scale / 10;
            float b = map(y, 0, height, -scale, scale);

            // in the equations, c is the ORIGINAL value, store it before iterating
            float ca = a;
            float cb = b;

            int counter = 0;
            boolean towardsInfinity = false;

            for (; counter < MAX_ITERATIONS; counter++) {
                // calculate real and imaginary parts for next generation
                float aa = a * a - b * b;
                float bb = 2 * a * b;

                // equation f(z) = z² + c
                a = aa + ca;
                b = bb + cb;

                // if greater than "infinity"
                if (abs(a + b) > 16) {
                    break;
                }
            }

            float brightness = map(counter, 0, MAX_ITERATIONS, 0, 255);
            if (counter == MAX_ITERATIONS) brightness = 0;

            pixels[y * width + x] = color(brightness, brightness, brightness, 255);
        }
    }
    updatePixels();
}

void draw() {
    background(0);
    loadPixels();
    for (int x = 0; x < width; x++) {
        for (int y = 0; y < height; y++) {

            // scale numbers down (-2 - 2i to 2 + 2i)
            float a = map(x, 0, width, -scale, scale) - scale / 10;
            float b = map(y, 0, height, -scale, scale);

            // in the equations, c is the ORIGINAL value, store it before iterating
            float ca = a;
            float cb = b;

            int counter = 0;
            boolean towardsInfinity = false;

            for (; counter < MAX_ITERATIONS; counter++) {
                // calculate real and imaginary parts for next generation
                float aa = a * a - b * b;
                float bb = 2 * a * b;

                // equation f(z) = z² + c
                a = aa + ca;
                b = bb + cb;

                // if greater than "infinity"
                if (abs(a + b) > 16) {
                    break;
                }
            }

            float brightness = map(counter, 0, MAX_ITERATIONS, 0, 255);
            if (counter == MAX_ITERATIONS) brightness = 0;

            pixels[y * width + x] = color(brightness, brightness, brightness, 255);
        }
    }
    updatePixels();
}
