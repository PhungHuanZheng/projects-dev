public class PixelMatrix {
    public int[] flatPixels;
    public Shape shape;
    public int[][] matrixPixels;

    public PixelMatrix(int[] pixels_, int width_, int height_) {
        flatPixels = pixels_;
        shape = new Shape(width_, height_);
        
        matrixPixels = new int[height_][width_];
        for (int y = 0; y < height_; y++) {
            for (int x = 0; x < width_; x++) {
                matrixPixels[y][x] = flatPixels[y * width_ + x];
            }
        }
    }

    public int[] getRow(int rowIndex) {
        return matrixPixels[rowIndex];
    }

    public int[] getCol(int colIndex) {
        int[] colValues = new int[matrixPixels.length];
        for (int i = 0; i < matrixPixels.length; i++) {
            colValues[i] = matrixPixels[i][colIndex];
        }
        return colValues;
    }
}
