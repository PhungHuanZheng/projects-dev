import java.util.ArrayList;
import java.lang.reflect.Method;

public class NeuralNetwork {
    private Class<Activations> act = NeuralNetwork.Activations.class;
    public ArrayList<Layer> layers = new ArrayList<Layer>();

    int inputNeuronCount;
    String[] activations;
    Method[] actMethods;


    public static class Activations {
        public static Matrix2D sigmoid(Matrix2D M) {
            Matrix2D copyM = M.copy();
            for (int y = 0; y < copyM.shape[0]; y++) {
                for (int x = 0; x < copyM.shape[1]; x++) {
                    copyM.data[y][x] = (float) (1 / (1 + Math.exp(-1)));
                }
            }
            return copyM;
        }

        // public static Matrix2D dsigmoid(Matrix2D M) {

        // }

        public static Matrix2D relu(Matrix2D M) {
            Matrix2D copyM = M.copy();
            for (int y = 0; y < copyM.shape[0]; y++) {
                for (int x = 0; x < copyM.shape[1]; x++) {
                    copyM.data[y][x] = copyM.data[y][x] > 0 ? copyM.data[y][x] : 0;
                }
            }
            return copyM;
        }

        public static Matrix2D softmax(Matrix2D M) {
            Matrix2D copyM = M.copy();
            copyM.mapLambda(x -> (float) Math.exp(x));
            float expSum = copyM.sum();

            for (int y = 0; y < copyM.shape[0]; y++) {
                for (int x = 0; x < copyM.shape[1]; x++) {
                    copyM.data[y][x] = copyM.data[y][x] / expSum;
                }
            }
            return copyM;
        }
    }

    public NeuralNetwork(int inputNeuronCount, int[] layerNeuronCounts, String[] activations) {
        this.inputNeuronCount = inputNeuronCount;
        this.activations = activations;

        // init activations from str to methods
       this.actMethods = new Method[activations.length];
        for (int i = 0; i < activations.length; i++) {
            try {
                this.actMethods[i] = this.act.getMethod(activations[i].toLowerCase(), Matrix2D.class);
            } catch (NoSuchMethodException e) {
                e.printStackTrace();
            }
        }

        // init weights and biases for input to first hidden layer
        Layer firstLayer = new Layer(inputNeuronCount);
        firstLayer.weights = new Matrix2D(layerNeuronCounts[0], inputNeuronCount).randomize(-1, 1);
        firstLayer.biases = new Matrix2D(layerNeuronCounts[0], 1).randomize(-1, 1);
        this.layers.add(firstLayer);

        for (int i = 0; i < layerNeuronCounts.length - 1; i++) {
            Layer layer = new Layer(layerNeuronCounts[i]);
            layer.weights = new Matrix2D(layerNeuronCounts[i + 1], layerNeuronCounts[i]).randomize(-1, 1);
            layer.biases = new Matrix2D(layerNeuronCounts[i + 1], 1).randomize(-1, 1);
            this.layers.add(layer);
        }
    }

    public void fit(Matrix2D X, Matrix2D y, int batchSize) {
        // check input shape
        if (X.shape[0] != this.inputNeuronCount) {
            throw new RuntimeException(String.format(
                    "Input array of length %d is incompatible with NeuralNetwork instance with input shape %d.",
                    X.shape[0], this.inputNeuronCount));
        }

        // iterate over datapoints
        for (int i = 0; i < this.inputNeuronCount; i++) {
            Matrix2D datapoint = Matrix2D.fromArray(X.getCol(i), 1);
            Matrix2D target = Matrix2D.fromArray(y.getRow(i), 1);

            Matrix2D output = this.feedforward(datapoint);
            Matrix2D error = Matrix2D.sub(target, output);

            error.print();
            return;
        }
    }

    public Matrix2D feedforward(Matrix2D datapoint) {
        Matrix2D layerInput = datapoint.copy();

        // feedforward datapoint
        for (int i = 0; i < this.layers.size(); i++) {
            Layer layer = this.layers.get(i);

            try {
                // this layer's weights * layer inputs + next layer's bias
                layerInput = Matrix2D.matmul(layer.weights, layerInput);
                layerInput.add(this.layers.get(i).biases);
                layerInput.mapMethod(
                        new NeuralNetwork.Activations(),
                        this.actMethods[i]);

            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        return layerInput;
    }

    public void print() {
        for (int i = 0; i < this.layers.size(); i++) {
            Layer layer = this.layers.get(i);

            System.out.println(
                    "Layer " + (i) + " -> " + (i + 1) + ": (" + layer.weights.shape[0] + ", " + layer.weights.shape[1] +
                            ") * (" + layer.weights.shape[1] + ", 1) + (" + layer.biases.shape[0] +
                            ", 1)");
        }
    }
}
