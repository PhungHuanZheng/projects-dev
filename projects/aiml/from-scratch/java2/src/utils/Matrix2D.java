package utils;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.function.Function;

import errors.IncompatibleShapeException;
import interfaces.IMatrix;

public class Matrix2D extends IMatrix {

	public Matrix2D(int rows, int columns) {
//		basic init
		this.shape = new int[] { rows, columns };
		this.size = rows * columns;

//		init 2d array of 0s as data
		this.data = new float[rows][columns];
		for (int y = 0; y < rows; y++) {
			for (int x = 0; x < columns; x++) {
				this.data[y][x] = 0;
			}
		}
	}

//	matrix compatibility checking
	private static void checkEWCompatibility(IMatrix M1, IMatrix M2, String op) throws IncompatibleShapeException {
		if (M1.shape[0] != M2.shape[0] || M1.shape[1] != M2.shape[1]) {
			throw new IncompatibleShapeException(String.format(
					"Matrices of shape (%d, %d) and shape (%d, %d) are incompatible for operation \"%s\".", M1.shape[0],
					M1.shape[1], M2.shape[0], M2.shape[1], op));
		}
	}

	private static void checkMMCompatibility(IMatrix M1, IMatrix M2, String op) throws IncompatibleShapeException {
		if (M1.shape[1] != M2.shape[0]) {
			throw new IncompatibleShapeException(String.format(
					"Matrices of shape (%d, %d) and shape (%d, %d) are incompatible for operation \"%s\".", M1.shape[0],
					M1.shape[1], M2.shape[0], M2.shape[1], op));
		}
	}

//	matrix value operations
	@Override
	public float min() {
		float minValue = (float) Double.POSITIVE_INFINITY;
		for (int y = 0; y < this.shape[0]; y++) {
			for (int x = 0; x < this.shape[1]; x++) {
				float value = this.data[y][x];

				if (value < minValue) {
					minValue = value;
				}
			}
		}
		return minValue;
	}

	@Override
	public float max() {
		float maxValue = (float) Double.NEGATIVE_INFINITY;
		for (int y = 0; y < this.shape[0]; y++) {
			for (int x = 0; x < this.shape[1]; x++) {
				float value = this.data[y][x];

				if (value > maxValue) {
					maxValue = value;
				}
			}
		}
		return maxValue;
	}

	@Override
	public float sum() {
		float sum = 0;
		for (int y = 0; y < this.shape[0]; y++) {
			for (int x = 0; x < this.shape[1]; x++) {
				sum += this.data[y][x];
			}
		}
		return sum;
	}

	@Override
	public float mean() {
		return this.sum() / this.size;
	}

//	matrix indexing and slicing
	@SuppressWarnings("unchecked")
	@Override
	public <T extends IMatrix> T rowAt(int index) {
//		create and return a matrix with a single row
		Matrix2D M = new Matrix2D(1, this.shape[1]);
		M.data[0] = this.data[index];
		return (T) M;
	}

	@SuppressWarnings("unchecked")
	@Override
	public <T extends IMatrix> T colAt(int index) {
//		create and return a matrix with a single column
		Matrix2D M = new Matrix2D(this.shape[0], 1);
		for (int i = 0; i < this.shape[0]; i++) {
			M.data[i][0] = this.data[i][index];
		}
		return (T) M;
	}

	@SuppressWarnings("unchecked")
	@Override
	public <T extends IMatrix> T rowsAt(int[] indexes) {
//		get initial matrix and concat rows to it
		Matrix2D rows = this.rowAt(indexes[0]);
		for (int i = 1; i < indexes.length; i++) {
			rows.concat(this.rowAt(i), 0);
		}
		return (T) rows;
	}

	@SuppressWarnings("unchecked")
	@Override
	public <T extends IMatrix> T colsAt(int[] indexes) {
//		get initial matrix and concat cols to it
		Matrix2D cols = this.colAt(indexes[0]);
		for (int i = 1; i < indexes.length; i++) {
			cols.concat(this.colAt(i), 1);
		}
		return (T) cols;
	}

//	basic matrix-matrix element-wise operations
	@SuppressWarnings("unchecked")
	@Override
	public <T extends IMatrix> T add(T M) {
//		add elements in 2 matrices
		Matrix2D.checkEWCompatibility(this, M, "add");

//		iterate over and add elements
		for (int y = 0; y < this.shape[0]; y++) {
			for (int x = 0; x < this.shape[1]; x++) {
				this.data[y][x] += M.data[y][x];
			}
		}

		return (T) this;
	}

	@SuppressWarnings("unchecked")
	@Override
	public <T extends IMatrix> T sub(T M) {
//		add elements in 2 matrices
		Matrix2D.checkEWCompatibility(this, M, "sub");

//		iterate over and add elements
		for (int y = 0; y < this.shape[0]; y++) {
			for (int x = 0; x < this.shape[1]; x++) {
				this.data[y][x] -= M.data[y][x];
			}
		}

		return (T) this;
	}

	@SuppressWarnings("unchecked")
	@Override
	public <T extends IMatrix> T mul(T M) {
//		add elements in 2 matrices
		Matrix2D.checkEWCompatibility(this, M, "mul");

//		iterate over and add elements
		for (int y = 0; y < this.shape[0]; y++) {
			for (int x = 0; x < this.shape[1]; x++) {
				this.data[y][x] *= M.data[y][x];
			}
		}

		return (T) this;
	}

	@SuppressWarnings("unchecked")
	@Override
	public <T extends IMatrix> T div(T M) {
//		add elements in 2 matrices
		Matrix2D.checkEWCompatibility(this, M, "div");

//		iterate over and add elements
		for (int y = 0; y < this.shape[0]; y++) {
			for (int x = 0; x < this.shape[1]; x++) {
				this.data[y][x] /= M.data[y][x];
			}
		}

		return (T) this;
	}

//	basic matrix-number element-wise operations
	@SuppressWarnings("unchecked")
	@Override
	public <T extends IMatrix> T add(float num) {
//		iterate over and add elements
		for (int y = 0; y < this.shape[0]; y++) {
			for (int x = 0; x < this.shape[1]; x++) {
				this.data[y][x] += num;
			}
		}

		return (T) this;
	}

	@SuppressWarnings("unchecked")
	@Override
	public <T extends IMatrix> T sub(float num) {
//		iterate over and add elements
		for (int y = 0; y < this.shape[0]; y++) {
			for (int x = 0; x < this.shape[1]; x++) {
				this.data[y][x] -= num;
			}
		}

		return (T) this;
	}

	@SuppressWarnings("unchecked")
	@Override
	public <T extends IMatrix> T mul(float num) {
//		iterate over and add elements
		for (int y = 0; y < this.shape[0]; y++) {
			for (int x = 0; x < this.shape[1]; x++) {
				this.data[y][x] *= num;
			}
		}

		return (T) this;
	}

	@SuppressWarnings("unchecked")
	@Override
	public <T extends IMatrix> T div(float num) {
//		iterate over and add elements
		for (int y = 0; y < this.shape[0]; y++) {
			for (int x = 0; x < this.shape[1]; x++) {
				this.data[y][x] /= num;
			}
		}

		return (T) this;
	}

//	matrix-matrix non-element-wise operations
	@SuppressWarnings("unchecked")
	@Override
	public <T extends IMatrix> T matmul(T M) {
//		matrix multiplication: A * B, column * row
		Matrix2D.checkMMCompatibility(this, M, "matmul");

//		create new matrix with new shape
		Matrix2D matrix = new Matrix2D(this.shape[0], M.shape[1]);

//		populate matrix elements
		for (int y = 0; y < matrix.shape[0]; y++) {
//			get row
			float[] row = this.rowAt(y).flatten();
			for (int x = 0; x < matrix.shape[1]; x++) {
//				get column
				float[] column = M.colAt(x).flatten();

//				element-wise multiplication and sum
				float sum = 0;
				for (int i = 0; i < row.length; i++) {
					sum += row[i] * column[i];
				}
				matrix.data[y][x] = sum;
			}
		}

		this.shape = matrix.shape;
		this.size = matrix.size;
		this.data = matrix.data;

		return (T) this;
	}

	@SuppressWarnings("unchecked")
	@Override
	public <T extends IMatrix> T concat(T M, int axis) throws RuntimeException {
//		init variables
		int[] tempShape;
		int tempSize;
		float[][] tempData;

		switch (axis) {
//		concat to the bottom
		case 0:
			tempShape = new int[] { this.shape[0] + M.shape[0], this.shape[1] };
			tempSize = this.shape[0] * this.shape[1];
			tempData = new float[this.shape[0] + M.shape[0]][this.shape[1]];

			for (int i = 0; i < this.shape[0]; i++) {
				tempData[i] = this.data[i];
			}
			for (int i = 0; i < M.shape[0]; i++) {
				tempData[this.shape[0] + i] = M.data[i];
			}

			this.data = tempData;
			this.shape = tempShape;
			this.size = tempSize;

			return (T) this;

//		concat to the right
		case 1:
			tempShape = new int[] { this.shape[0], this.shape[1] + M.shape[1] };
			tempSize = this.shape[0] * this.shape[1];
			tempData = new float[this.shape[0]][this.shape[1] + M.shape[1]];

			for (int y = 0; y < tempShape[0]; y++) {
				for (int x = 0; x < this.shape[1]; x++) {
					tempData[y][x] = this.data[y][x];
				}
				for (int x = 0; x < M.shape[1]; x++) {
					tempData[y][this.shape[1] + x] = M.data[y][x];
				}
			}

			this.data = tempData;
			this.shape = tempShape;
			this.size = tempSize;

			return (T) this;

		default:
			throw new RuntimeException(String.format("Axis %d is invalid for %s instance with 2 dimensions.", axis,
					this.getClass().getName()));
		}
	}

//	matrix utility methods
	@SuppressWarnings("unchecked")
	@Override
	public <T extends IMatrix> T copy() {
//		create new matrix and give it this matrix's data
		Matrix2D M = new Matrix2D(this.shape[0], this.shape[1]);
		for (int y = 0; y < M.shape[0]; y++) {
			for (int x = 0; x < M.shape[1]; x++) {
				M.data[y][x] = this.data[y][x];
			}
		}
		return (T) M;
	}

	@SuppressWarnings("unchecked")
	@Override
	public <T extends IMatrix> T fromArray(float[] arr, int[] shape) {
//		check if array can be reshaped to shape passed
		if (arr.length != shape[0] * shape[1]) {
			throw new RuntimeException(
					String.format("Array of length %d cannot be transformed into matrix of shape (%d, %d).", arr.length,
							shape[0], shape[1]));
		}

//		create new empty matrix
		Matrix2D M = new Matrix2D(shape[0], shape[1]);

//		iterate over dimensions and populate
		for (int y = 0; y < M.shape[0]; y++) {
			for (int x = 0; x < M.shape[1]; x++) {
				M.data[y][x] = arr[y * M.shape[1] + x];
			}
		}
		return (T) M;
	}

	@Override
	public float[] flatten() {
		float[] flatArr = new float[this.size];
		for (int y = 0; y < this.shape[0]; y++) {
			for (int x = 0; x < this.shape[1]; x++) {
				flatArr[y * this.shape[1] + x] = this.data[y][x];
			}
		}
		return flatArr;
	}

	@SuppressWarnings("unchecked")
	@Override
	public <T extends IMatrix> T T() {
//		build new matrix with opposite shape
		Matrix2D M = new Matrix2D(this.shape[1], this.shape[0]);
		for (int i = 0; i < M.shape[0]; i++) {
			M.data[i] = this.colAt(i).flatten();
		}

		this.shape = M.shape;
		this.size = M.size;
		this.data = M.data;

		return (T) this;
	}

	@Override
	public float[] unique() {
//		get ArrayList of unique values
		ArrayList<Float> uniqueValues = new ArrayList<Float>();
		for (int y = 0; y < this.shape[0]; y++) {
			for (int x = 0; x < this.shape[1]; x++) {
				if (!uniqueValues.contains(this.data[y][x])) {
					uniqueValues.add(this.data[y][x]);
				}
			}
		}

//		convert to array
		float[] unique = new float[uniqueValues.size()];
		for (int i = 0; i < unique.length; i++) {
			unique[i] = uniqueValues.get(i);
		}
		return unique;
	}

	@SuppressWarnings("unchecked")
	@Override
	public <T extends IMatrix> T mapLambda(Function<Float, Float> lambda) {
		for (int y = 0; y < this.shape[0]; y++) {
			for (int x = 0; x < this.shape[1]; x++) {
				this.data[y][x] = lambda.apply(this.data[y][x]);
			}
		}
		return (T) this;
	}
	
	@SuppressWarnings("unchecked")
	@Override
	public <T extends IMatrix> T mapMethod(Object obj, Method method) throws IllegalAccessException, IllegalArgumentException, InvocationTargetException {
		Matrix2D M = (Matrix2D)method.invoke(obj, this);
        this.shape = new int[]{M.shape[0], M.shape[1]};
        this.data = M.data;
        
        return (T) this;
	}

//	matrix post-creation methods
	@SuppressWarnings({ "unchecked" })
	@Override
	public <T extends IMatrix> T randomize(float min, float max) {
		for (int y = 0; y < this.shape[0]; y++) {
			for (int x = 0; x < this.shape[1]; x++) {
				float randFloat = (float) Math.random() * (max - min) + min;
				this.data[y][x] = randFloat;
			}
		}
		return (T) this;
	}

	@SuppressWarnings({ "unchecked" })
	@Override
	public <T extends IMatrix> T scaleTo(float min, float max) {
//		get min and max values
		float minValue = this.min();
		float maxValue = this.max();

//		iterate over and scale values between min and max to args passed
		for (int y = 0; y < this.shape[0]; y++) {
			for (int x = 0; x < this.shape[1]; x++) {
//				calculate ratio to scale data
				float value = this.data[y][x];
				float ratio = (value - minValue) / (maxValue - minValue);

//				scale value in matrix
				this.data[y][x] = min + ((max - min) * ratio);
			}
		}
		return (T) this;
	}

//	display methods
	@Override
	public void print() {
		String matrixStr = "[[";
		DecimalFormat df = new DecimalFormat("+#,##0.000;-#");

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
