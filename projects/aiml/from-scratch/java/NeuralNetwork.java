import java.util.ArrayList;
import java.lang.reflect.Method;

public class NeuralNetwork {
    private Class<Activations> act = NeuralNetwork.Activations.class;
    public ArrayList<Layer> layers = new ArrayList<Layer>();

    int inputNeuronCount;

    public NeuralNetwork(int inputNeuronCount, int[] layerNeuronCounts, String[] activations) {
        this.inputNeuronCount = inputNeuronCount;

        // init activations from str to methods
        Method[] actMethods = new Method[activations.length];
        for (int i = 0; i < activations.length; i++) {
            try {
                actMethods[i] = act.getMethod(activations[0].toLowerCase(), float.class);
            } catch (NoSuchMethodException e) {
                e.printStackTrace();
            }
        }

        // init weight and bias matrices for layers
        for (int i = 0; i < layerNeuronCounts.length - 1; i++) {
            Layer layer = new Layer(layerNeuronCounts[i]);
            layer.weights = new Matrix2D(layerNeuronCounts[i + 1], layerNeuronCounts[i]);
            layer.biases = new Matrix2D(layerNeuronCounts[i], 1);
        }
    }

    public static class Activations {
        public static float sigmoid(float num) {
            return (float) (1 / 1 + Math.exp(-num));
        }

        public static float relu(float num) {
            return num > 0 ? num : 0;
        }
    }

    public void feedforward(Matrix2D inputs) {
        // check input shape
        if (inputs.shape[0] != this.inputNeuronCount) {
            throw new RuntimeException(String.format(
                "Input array of length %d is incompatible with NeuralNetwork instance with input shape %d.", 
                inputs.shape[0], this.inputNeuronCount
                ));
        }
    }
}
