import java.text.DecimalFormat;
import java.util.function.Function;

import errors.IncompatibleShapeException;

public class Matrix2D {
    public int[] shape;
    public int size;
    public float[][] data;

    public Matrix2D(int rows, int columns) {
        // init shape and data as 0s
        this.shape = new int[] { rows, columns };
        this.size = rows * columns;
        this.data = new float[rows][columns];
        for (int y = 0; y < rows; y++) {
            for (int x = 0; x < columns; x++) {
                this.data[y][x] = 0;
            }
        }
    }

    private static void checkEWCompatibility(Matrix2D M1, Matrix2D M2, String op) throws IncompatibleShapeException {
        if (M1.shape[0] != M2.shape[0] || M1.shape[1] != M2.shape[1]) {
            throw new IncompatibleShapeException(String.format(
                    "Matrices of shape (%d, %d) and shape (%d, %d) are incompatible for operation \"%s\".",
                    M1.shape[0], M1.shape[1], M2.shape[0], M2.shape[1], op));
        }
    }

    private static void checkMMCompatibility(Matrix2D M1, Matrix2D M2, String op) throws IncompatibleShapeException {
        if (M1.shape[1] != M2.shape[0]) {
            throw new IncompatibleShapeException(String.format(
                    "Matrices of shape (%d, %d) and shape (%d, %d) are incompatible for operation \"%s\".",
                    M1.shape[0], M1.shape[1], M2.shape[0], M2.shape[1], op));
        }
    }

    /*
     * Indexing methods to get row (axis 0) or column (axis 1) of matrix
     */
    public float[] getRow(int index) {
        return this.data[index];
    }

    public float[] getCol(int index) {
        float[] colValues = new float[this.shape[0]];
        for (int i = 0; i < colValues.length; i++) {
            colValues[i] = this.data[i][index];
        }
        return colValues;
    }

    /*
     * Utility methods
     */
    public Matrix2D randomize(float min, float max) {
        // iterate over matrix data
        for (int y = 0; y < this.shape[0]; y++) {
            for (int x = 0; x < this.shape[1]; x++) {
                this.data[y][x] = (float) (Math.random() * (max - min) + min);
            }
        }

        // return self for method chaining
        return this;
    }

    public Matrix2D copy() {
        // copy over data to new instance and return
        Matrix2D copyM = new Matrix2D(this.shape[0], this.shape[1]);
        for (int y = 0; y < this.shape[0]; y++) {
            for (int x = 0; x < this.shape[1]; x++) {
                copyM.data[y][x] = this.data[y][x];
            }
        }
        return copyM;
    }

    public float min() {
        float minValue = (float) Double.POSITIVE_INFINITY;
        for (int y = 0; y < this.shape[0]; y++) {
            for (int x = 0; x < this.shape[1]; x++) {
                // check against current min value
                if (this.data[y][x] < minValue) {
                    minValue = this.data[y][x];
                }
            }
        }
        return minValue;
    }

    public float max() {
        float maxValue = (float) Double.NEGATIVE_INFINITY;
        for (int y = 0; y < this.shape[0]; y++) {
            for (int x = 0; x < this.shape[1]; x++) {
                // check against current min value
                if (this.data[y][x] > maxValue) {
                    maxValue = this.data[y][x];
                }
            }
        }
        return maxValue;
    }

    public void transpose() {
        float[][] newData = new float[this.shape[1]][this.shape[0]];
        for (int i = 0; i < this.shape[1]; i++) {
            newData[i] = this.getCol(i);
        }

        this.shape = new int[] { this.shape[1], this.shape[0] };
        this.data = newData;
    }

    public static Matrix2D transpose(Matrix2D M) {
        Matrix2D copyM = M.copy();
        copyM.transpose();
        return copyM;
    }

    /*
     * Basic matrix-matrix operations
     */
    public void matmul(Matrix2D M2) {
        Matrix2D.checkMMCompatibility(this, M2, "matmul");

        // get new matrix with resulting shape
        Matrix2D resultM = new Matrix2D(this.shape[0], M2.shape[1]);
        for (int y = 0; y < resultM.shape[0]; y++) {
            for (int x = 0; x < resultM.shape[1]; x++) {
                // do row * column and get sum
                float[] rowData = this.getRow(y);
                float[] colData = M2.getCol(x);

                float sum = 0;
                for (int i = 0; i < rowData.length; i++) {
                    sum += rowData[i] * colData[i];
                }

                resultM.data[y][x] = sum;
            }
        }

        // set attributes to new matrix's
        this.shape = resultM.shape;
        this.data = resultM.data;
    }

    public static Matrix2D matmul(Matrix2D M1, Matrix2D M2) {
        Matrix2D copyM = M1.copy();
        copyM.matmul(M2);
        return copyM;
    }

    public void add(Matrix2D M2) {
        Matrix2D.checkEWCompatibility(this, M2, "add");

        // iterate over matrix data
        for (int y = 0; y < this.shape[0]; y++) {
            for (int x = 0; x < this.shape[1]; x++) {
                // add values element wise in place
                this.data[y][x] += M2.data[y][x];
            }
        }
    }

    public static Matrix2D add(Matrix2D M1, Matrix2D M2) {
        Matrix2D copyM = M1.copy();
        copyM.add(M2);
        return copyM;
    }

    public void sub(Matrix2D M2) {
        Matrix2D.checkEWCompatibility(this, M2, "add");

        // iterate over matrix data
        for (int y = 0; y < this.shape[0]; y++) {
            for (int x = 0; x < this.shape[1]; x++) {
                // add values element wise in place
                this.data[y][x] -= M2.data[y][x];
            }
        }
    }

    public static Matrix2D sub(Matrix2D M1, Matrix2D M2) {
        Matrix2D copyM = M1.copy();
        copyM.sub(M2);
        return copyM;
    }

    public void mult(Matrix2D M2) {
        Matrix2D.checkEWCompatibility(this, M2, "add");

        // iterate over matrix data
        for (int y = 0; y < this.shape[0]; y++) {
            for (int x = 0; x < this.shape[1]; x++) {
                // add values element wise in place
                this.data[y][x] *= M2.data[y][x];
            }
        }
    }

    public static Matrix2D mult(Matrix2D M1, Matrix2D M2) {
        Matrix2D copyM = M1.copy();
        copyM.mult(M2);
        return copyM;
    }

    public void div(Matrix2D M2) {
        Matrix2D.checkEWCompatibility(this, M2, "add");

        // iterate over matrix data
        for (int y = 0; y < this.shape[0]; y++) {
            for (int x = 0; x < this.shape[1]; x++) {
                // add values element wise in place
                this.data[y][x] /= M2.data[y][x];
            }
        }
    }

    public static Matrix2D div(Matrix2D M1, Matrix2D M2) {
        Matrix2D copyM = M1.copy();
        copyM.div(M2);
        return copyM;
    }

    /*
     * Basic matrix-value operations
     */
    public void map(Function<Float, Float> lambda) {
        for (int y = 0; y < this.shape[0]; y++) {
            for (int x = 0; x < this.shape[1]; x++) {
                this.data[y][x] = lambda.apply(this.data[y][x]);
            }
        }
    }

    /*
     * Display methods
     */
    public void print() {
        String matrixStr = "[[";
        DecimalFormat df = new DecimalFormat("+#,##0.0000;-#");

        for (int y = 0; y < this.shape[0]; y++) {
            for (int x = 0; x < this.shape[1]; x++) {
                if (x == 0 && y > 0) {
                    matrixStr += " [";
                }
                matrixStr += df.format(this.data[y][x]);
                if (x < this.shape[1] - 1) {
                    matrixStr += ", ";
                    continue;
                }
                if (x == this.shape[1] - 1 && y == this.shape[0] - 1) {
                    matrixStr += "]";
                }
                matrixStr += "]\n";
            }
        }
        System.out.println(matrixStr);
    }
}
