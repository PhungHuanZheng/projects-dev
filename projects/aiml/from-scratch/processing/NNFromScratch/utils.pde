import java.lang.reflect.*;

public class DataTargetPair {
    public float[] data;
    public int target;

    public DataTargetPair(float[] data, int target) {
        this.data = data;
        this.target = target;
    }
}

public static float[] applyActivation(Class<?> cls, String methodName, float[] input) throws Exception {
    Method m = cls.getMethod(methodName, int.class);
    float[] returnVal = (float[]) m.invoke(cls, input);
    return returnVal;
}


public class OutputPair {
    public Matrix2D out;
    public Matrix2D actOut;

    public OutputPair(Matrix2D out, Matrix2D actOut) {
        this.out = out;
        this.actOut = actOut;
    }
}

public class DerivPair {
    public Matrix2D weights;
    public float biases;

    public DerivPair(Matrix2D weights, float biases) {
        this.weights = weights;
        this.biases = biases;
    }
}
