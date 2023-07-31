package interfaces;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.function.Function;

public abstract class IMatrix {
	public int[] shape;
	public int size;
	public float[][] data;
	
//	matrix value operations
	public abstract float min();
	public abstract float max();
	public abstract float sum();
	public abstract float mean();
	
//	matrix indexing and slicing
	public abstract <T extends IMatrix> T rowAt(int index);
	public abstract <T extends IMatrix> T colAt(int index);
	public abstract <T extends IMatrix> T rowsAt(int[] indexes);
	public abstract <T extends IMatrix> T colsAt(int[] indexes);
	
//	basic matrix-matrix element-wise operations
	public abstract <T extends IMatrix> T add(T M);
	public abstract <T extends IMatrix> T sub(T M);
	public abstract <T extends IMatrix> T mul(T M);
	public abstract <T extends IMatrix> T div(T M);
	
//	basic matrix-number element-wise operations
	public abstract <T extends IMatrix> T add(float num);
	public abstract <T extends IMatrix> T sub(float num);
	public abstract <T extends IMatrix> T mul(float num);
	public abstract <T extends IMatrix> T div(float num);
	
//	matrix-matrix non-element-wise operations
	public abstract <T extends IMatrix> T matmul(T M);
	public abstract <T extends IMatrix> T concat(T M, int axis);
	
//	matrix utility methods
	public abstract <T extends IMatrix> T copy();
	public abstract <T extends IMatrix> T fromArray(float[] arr, int[] shape);
	public abstract float[] flatten();
	public abstract <T extends IMatrix> T T();
	public abstract float[] unique();
	
	public abstract <T extends IMatrix> T mapLambda(Function<Float, Float> lambda);
	public abstract <T extends IMatrix> T mapMethod(Object obj, Method method) throws IllegalAccessException, IllegalArgumentException, InvocationTargetException;
	
//	matrix post-creation methods
	public abstract <T extends IMatrix> T randomize(float min, float max);
	public abstract <T extends IMatrix> T scaleTo(float min, float max);
	
//	display methods
	public abstract void print();
}
