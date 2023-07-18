public class Matrix2D {
    public int[] shape;
    public float[][] data;

    public Matrix2D (int rows, int columns, boolean initRandom) {
        // init basic attributes
        this.shape = new int[]{rows, columns};

        // init matrix data
        this.data = new float[rows][columns];
        for (int y = 0; y < rows; y++) {
            for (int x = 0; x < columns; x++) {
                this.data[y][x] = initRandom ? random(2) - 1 : 0;
            }
        }
    }
    
    public float[] rowAt(int rowId) {
        return this.data[rowId];
    }
    
    public float[] colAt(int colId) {
        float[] colValues = new float[this.shape[0]];
        for (int i = 0; i < colValues.length; i++) {
            colValues[i] = this.data[i][colId];
        }
        return colValues;
    }
    
    public Matrix2D fromArray(float[] arr, int[] size) {
        // check if arr passed can be reshaped to size passed
        if (arr.length != (size[0] * size[1])) {
            throw new RuntimeException(String.format(
            "Array of length %d cannot be reshaped into a matrix of shape (%d, %d)",
            arr.length, size[0], size[1]
            ));
        }
        
        Matrix2D matrix = new Matrix2D(size[0], size[1], false);
        for (int y = 0, j = 0; y < size[0]; y++) {
            for (int x = 0; x < size[1]; x++, j++) {
                matrix.data[y][x] = arr[j];
            }
        }
        return matrix;
    }
    
    public float sum() {
        float sum_ = 0;
        for (int y = 0; y < this.shape[0]; y++) {
            for (int x = 0; x < this.shape[1]; x++) {
                sum_ += this.data[y][x];
            }
        }
        return sum_;
    }

    public Matrix2D add(Matrix2D M2) {
        // check that matrix shapes match
        if (this.shape[0] != M2.shape[0] || this.shape[1] != M2.shape[1]) {
            throw new RuntimeException(String.format(
                "Matrices of size (%d, %d) and size (%d, %d) are not compatible for operation \"add\".",
                this.shape[0], this.shape[1], M2.shape[0], M2.shape[1]
                ));
        }

        // adds the matrix passed to this matrix like: A + B
        Matrix2D M1 = this.copy();
        for (int y = 0; y < this.shape[0]; y++) {
            for (int x = 0; x < this.shape[1]; x++) {
                M1.data[y][x] += M2.data[y][x];
            }
        }
        return M1;
    }
    
    public Matrix2D sub(Matrix2D M2) {
        // check that matrix shapes match
        if (this.shape[0] != M2.shape[0] || this.shape[1] != M2.shape[1]) {
            throw new RuntimeException(String.format(
                "Matrices of size (%d, %d) and size (%d, %d) are not compatible for operation \"sub\".",
                this.shape[0], this.shape[1], M2.shape[0], M2.shape[1]
                ));
        }

        // adds the matrix passed to this matrix like: A - B
        Matrix2D M1 = this.copy();
        for (int y = 0; y < this.shape[0]; y++) {
            for (int x = 0; x < this.shape[1]; x++) {
                M1.data[y][x] -= M2.data[y][x];
            }
        }
        return M1;
    }
    
    public Matrix2D sub(float num) {
        // adds the matrix passed to this matrix like: A - B
        Matrix2D M1 = this.copy();
        for (int y = 0; y < this.shape[0]; y++) {
            for (int x = 0; x < this.shape[1]; x++) {
                M1.data[y][x] -= num;
            }
        }
        return M1;
    }
    
    public Matrix2D mult(Matrix2D M2) {
        // check that matrix shapes match
        if (this.shape[0] != M2.shape[0] || this.shape[1] != M2.shape[1]) {
            throw new RuntimeException(String.format(
                "Matrices of size (%d, %d) and size (%d, %d) are not compatible for operation \"sub\".",
                this.shape[0], this.shape[1], M2.shape[0], M2.shape[1]
                ));
        }

        // adds the matrix passed to this matrix like: A - B
        Matrix2D M1 = this.copy();
        for (int y = 0; y < this.shape[0]; y++) {
            for (int x = 0; x < this.shape[1]; x++) {
                M1.data[y][x] *= M2.data[y][x];
            }
        }
        return M1;
    }
    
    public Matrix2D mult(float num) {
        // adds the matrix passed to this matrix like: A - B
        Matrix2D M1 = this.copy();
        for (int y = 0; y < this.shape[0]; y++) {
            for (int x = 0; x < this.shape[1]; x++) {
                M1.data[y][x] *= num;
            }
        }
        return M1;
    }
    
    

    public Matrix2D matmul(Matrix2D M2) {
        // check that matrices are compatible
        if (this.shape[1] != M2.shape[0]) {
            throw new RuntimeException(String.format(
                "Matrices of size (%d, %d) and size (%d, %d) are not compatible for operation \"matmul\".",
                this.shape[0], this.shape[1], M2.shape[0], M2.shape[1]
                ));
        }
        
        // multiplies the matrix passed to this matrix like: A * B
        Matrix2D matrix = new Matrix2D(this.shape[0], M2.shape[1], false);
        for (int y = 0; y < matrix.shape[0]; y++) {
            float[] rowM1 = this.rowAt(y);
            for (int x = 0; x < matrix.shape[1]; x++) {
                float[] colM2 = M2.colAt(x);
                
                // do M1 row * M2 col to get single cell value
                for (int i = 0; i < rowM1.length; i++) {
                    matrix.data[y][x] += rowM1[i] * colM2[i];
                }
            }
        }
        return matrix;
    }
    
    public Matrix2D transpose() {
        Matrix2D matrix = new Matrix2D(this.shape[1], this.shape[0], false);
        for (int i = 0; i < this.shape[1]; i++) {
            matrix.data[i] = this.colAt(i);
        }
        return matrix;
    }

    public Matrix2D copy() {
        float[][] copiedData = new float[this.shape[0]][this.shape[1]];
        for (int y = 0; y < this.shape[0]; y++) {
            for (int x = 0; x < this.shape[1]; x++) {
                copiedData[y][x] = this.data[y][x];
            }
        }

        Matrix2D matrix = new Matrix2D(this.shape[0], this.shape[1], false);
        matrix.data = copiedData;
        return matrix;
    }
    
    public String toStr() {
        String matrixStr = "";
        for (int y = 0; y < this.shape[0]; y++) {
            for (int x = 0; x < this.shape[1]; x++) {
                matrixStr += this.data[y][x] + " ";
            }
            matrixStr += "\n";
        }
        return matrixStr;
    }
}
