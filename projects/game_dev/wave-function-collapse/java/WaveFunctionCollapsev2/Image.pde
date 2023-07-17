public class Image {
    public int width;
    public int height;
    public int[] pixels;
    public int[][] pixelMatrix;

    public Image(PImage image) {
        width = image.width;
        height = image.height;

        // split pixels into RGB values
        pixels = new int[image.pixels.length * 3];
        for (int i = 0, j = 0; i < image.pixels.length; i++) {
            // derive rgb from color int value
            pixels[j++] = image.pixels[i] >> 16 & 0xFF; // R
            pixels[j++] = image.pixels[i] >> 8 & 0xFF;  // G
            pixels[j++] = image.pixels[i] & 0xFF;       // B
        }

        // get 2D array of pixels
        pixelMatrix = new int[height][width * 3];
        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width * 3; x++) {
                pixelMatrix[y][x] = pixels[y * (width * 3) + x];
            }
        }
    }

    public int[] getRow(int rowIndex) {
        return pixelMatrix[rowIndex];
    }

    public int[] getCol(int colIndex) {
        int[] colValues = new int[height * 3];
        for (int i = 0, j = 0; i < height; i++) {
            colValues[j++] = pixelMatrix[i][colIndex * 3];
            colValues[j++] = pixelMatrix[i][colIndex * 3 + 1];
            colValues[j++] = pixelMatrix[i][colIndex * 3 + 2];
        }
        return colValues;
    }

    public PImage asPImage() {
        // create empty image with fresh pixel buffer
        PImage img = createImage(width, height, RGB);
        img.loadPixels();

        // populate created pixel buffer
        for (int i = 0, j = 0; i < img.pixels.length; i++) {
            img.pixels[i] = color(pixels[j++], pixels[j++], pixels[j++]);
        }
        return img;
    }
}
