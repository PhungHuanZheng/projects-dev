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

        public static Matrix2D dsigmoid(Matrix2D M) {
            Matrix2D copyM = M.copy();
            for (int y = 0; y < copyM.shape[0]; y++) {
                for (int x = 0; x < copyM.shape[1]; x++) {
                    copyM.data[y][x] = (float)((1 / (1 + Math.exp(-1))) * (1 - (1 / (1 + Math.exp(-1)))));
                }
            }
            return copyM;
        }

        public static Matrix2D relu(Matrix2D M) {
            Matrix2D copyM = M.copy();
            for (int y = 0; y < copyM.shape[0]; y++) {
                for (int x = 0; x < copyM.shape[1]; x++) {
                    copyM.data[y][x] = copyM.data[y][x] > 0 ? copyM.data[y][x] : 0;
                }
            }
            return copyM;
        }

        public static Matrix2D drelu(Matrix2D M) {
            Matrix2D copyM = M.copy();
            for (int y = 0; y < copyM.shape[0]; y++) {
                for (int x = 0; x < copyM.shape[1]; x++) {
                    copyM.data[y][x] = copyM.data[y][x] > 0 ? 1 : 0;
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
    
        public static Matrix2D dsoftmax(Matrix2D M) {
            float[] probM = Matrix2D.transpose(M).data[0];
            Matrix2D softmaxDeriv = new Matrix2D(M.size, M.size);

            // build nxn matrix where the diagonal -> i == j and the others -> i != j
            // https://www.youtube.com/watch?v=rf4WF-5y8uY 4:20
            for (int i = 0; i < probM.length; i++) {
                for (int j = 0; j < probM.length; j++) {
                    if (i == j) {
                        softmaxDeriv.data[i][j] = probM[i] * (1 - probM[i]);
                        continue;
                    }
                    softmaxDeriv.data[i][j] = -probM[i] * probM[j];
                }
            }
            return softmaxDeriv;
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

    public void fit(Matrix2D X, Matrix2D y, int batchSize, int epochs, float learningRate) {
        // check input shape
        if (X.shape[0] != this.inputNeuronCount) {
            throw new RuntimeException(String.format(
                    "Input array of length %d is incompatible with NeuralNetwork instance with input shape %d.",
                    X.shape[0], this.inputNeuronCount));
        }

        // iterate over epochs
        for (int i = 0; i < epochs; i++) {
            // track error for the current batch
            Matrix2D[] batchTargets = new Matrix2D[batchSize];
            Matrix2D[] batchOutputs = new Matrix2D[batchSize];

            // iterate over datapoints
            for (int j = 0, k = 0; j < this.inputNeuronCount; j++) {
                Matrix2D datapoint = Matrix2D.fromArray(X.getCol(j), 1);
                Matrix2D target = Matrix2D.fromArray(y.getRow(j), 1);
                Matrix2D output = this.feedforward(datapoint);

                // update batch index
                batchTargets[k] = target;
                batchOutputs[k] = output;
                k++;
                
                // update params by batch size
                if (j % batchSize == 0 || j == this.inputNeuronCount - 1) {
                    // send params to backpropagate and pray
                    this.backpropagate(X, batchOutputs, batchTargets, batchSize, learningRate);
                    k = 0;
                }
            }
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
                layerInput.mapMethod(new NeuralNetwork.Activations(), this.actMethods[i]);

            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        return layerInput;
    }

    public void backpropagate(Matrix2D X, Matrix2D[] outputs, Matrix2D[] targets, int batchSize, float learningRate) {
        // get mean output and error of batch passed, init output layer error for loop
        Matrix2D layerError = new Matrix2D(outputs[0].shape[0], outputs[0].shape[1]);
        Matrix2D layerOutputs = new Matrix2D(outputs[0].shape[0], outputs[0].shape[1]);
        Matrix2D layerTargets = new Matrix2D(targets[0].shape[0], targets[0].shape[1]);

        // get mean target and output for the batch
        for (int i = 0; i < outputs.length && outputs[i] != null; i++) {
            Matrix2D errorM = Matrix2D.sub(targets[i], outputs[i]);
            layerError.add(errorM);

            layerOutputs.add(outputs[i]);
            layerTargets.add(targets[i]);
        }
        layerError.mapLambda((x) -> x / batchSize);
        layerOutputs.mapLambda((x) -> x / batchSize);
        layerTargets.mapLambda((x) -> x / batchSize);

        for (int i = this.layers.size() - 1; i >= 1; i--) {
            try {
                Layer layer = this.layers.get(i);
                Method actFunctionDeriv = this.act.getMethod("d" + activations[i].toLowerCase(), Matrix2D.class);
                System.out.println(i);

                // get previous layer errors
                Matrix2D layerWeightsT = Matrix2D.transpose(layer.weights);
                layerError = Matrix2D.matmul(layerWeightsT, layerError);
                
                // calculate gradients from deriv of layer's activation function
                Matrix2D gradients = Matrix2D.mapMethod(layerOutputs, this.act, actFunctionDeriv);
                gradients.matmul(layerError);
                gradients.mapLambda((x) -> x * learningRate);

                // update weights and biases
                Matrix2D hiddenT = Matrix2D.transpose(layerError);
                Matrix2D weightDeltas = Matrix2D.matmul(gradients, hiddenT);
                layer.weights.add(weightDeltas);
                layer.biases.add(gradients);
            
            } catch (Exception e) {
                e.printStackTrace();
                return;
            }
        }
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
