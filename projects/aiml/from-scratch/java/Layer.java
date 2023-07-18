import java.util.function.Function;

public class Layer {
    int neuronCount;

    public Matrix2D weights;
    public Matrix2D biases;
    public Function<Float, Float> activation;

    public Layer(int neuronCount) {
        this.neuronCount = neuronCount;
    }
}
