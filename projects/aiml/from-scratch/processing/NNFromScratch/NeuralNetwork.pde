public class NeuralNetwork {
    public ArrayList<Layer> layers = new ArrayList<Layer>();
    public int[] layerUnits;
    public String[] layerActivations;

    public int inputSize;
    public int outputSize;

    public NeuralNetwork(int[] layerUnits, String[] layerActivations) {
        // init input output
        this.inputSize = layerUnits[0];
        this.outputSize = layerUnits[layerUnits.length - 1];
        this.layerUnits = layerUnits;
        this.layerActivations = layerActivations;

        // init layers except last output layer
        for (int i = 0; i < layerUnits.length - 1; i++) {
            Matrix2D weights = new Matrix2D(layerUnits[i + 1], layerUnits[i], true);
            Matrix2D biases = new Matrix2D(layerUnits[i + 1], 1, true);
            layers.add(new Layer(weights, biases));
        }
    }

    public OutputPair[] forwardPropagate(Matrix2D X) {
        // store outputs of each forward prop
        OutputPair[] outputs = new OutputPair[this.layers.size()];
        Matrix2D[] layerOutput = new Matrix2D[this.layers.size()];
        float[][] actLayerOutput = new float[this.layers.size()][1];

        Matrix2D layerInput = X;
        for (int i = 0; i < this.layers.size(); i++) {
            Layer layer = this.layers.get(i);

            Matrix2D result = layer.weights.matmul(layerInput).add(layer.biases);
            float[] actResult = Activations.get(this.layerActivations[i], result.transpose().data[0]);

            // pass results as matrix to next layer
            Matrix2D matrix = new Matrix2D(result.shape[0], result.shape[1], false);
            matrix.data[0] = actResult;

            // store results
            outputs[i] = new OutputPair(result, matrix);

            layerInput = matrix;
        }
        return outputs;
    }

    public DerivPair[] backPropagate(OutputPair[] outputs, Matrix2D data, Matrix2D target) {
        int m = target.shape[1];
        DerivPair[] derivs = new DerivPair[this.layers.size()];
        
        // output layer backprop
        Matrix2D layerError = outputs[outputs.length - 1].actOut.transpose().sub(target.transpose());
        Matrix2D weightsDeriv = layerError.matmul(outputs[outputs.length - 1].actOut.transpose()).mult(1 / m);
        float biasesDeriv = layerError.sum() * (1 / m);
        derivs[outputs.length - 1] = new DerivPair(weightsDeriv, biasesDeriv);
        
        // hidden layers backprop
        for (int i = outputs.length - 2; i >= 1; i--) {
            println(1);
        }   
        
        // input layer backprop
        layerError = this.layers.get(outputs.length - 1).weights.transpose().matmul(layerError.transpose());
        float[] actDeriv_ = Activations.derivRelu(outputs[outputs.length - 1].out.transpose().data[0]);
        Matrix2D actDeriv = new Matrix2D(1, 1, false).fromArray(actDeriv_, new int[]{1, 10});
        Matrix2D a = layerError.mult(actDeriv);
        printArray(a.shape);
        
        //derivs[0] = new DerivPair(weightsDeriv, biasesDeriv);
        
        return derivs;
    }
    
    public void updateParameters(DerivPair[] derivs, float alpha) {
        //for (int i = 0; i < this.layers.size(); i++) {
        //    Layer layer = this.layers.get(i);
        //    layer.weights = layer.weights.sub(derivs[i].weights.mult(alpha));
        //}
    }

    public void show() {
        //get spacing interval between layers
        float margin = 64;
        float spacing = (width - (margin * 2)) / (layerUnits.length - 1);

        // draw units as circles
        fill(255);
        stroke(255);

        for (int i = 0; i < layerUnits.length; i++) {
            float unitCount = layerUnits[i];
            float unitDiameter = height / unitCount;

            for (int j = 0; j < unitCount; j++) {
                //if next layer exists
                if (i + 1 < layerUnits.length) {
                    float nextLayerUnitCount = layerUnits[i + 1];
                    float nextLayerUnitDiameter = height / nextLayerUnitCount;
                    strokeWeight((height / (unitCount)) / 25);

                    for (int k = 0; k < nextLayerUnitCount; k++) {
                        float r = map(layers.get(i).weights.data[k][j], -1, 1, 255, 0);
                        float g = 255 - r;
                        stroke(r, g, 0);
                        line(i * spacing + margin, (j * unitDiameter) + (unitDiameter / 2), ((i + 1) * spacing + margin), (k * nextLayerUnitDiameter) + (nextLayerUnitDiameter / 2));
                    }
                }

                // draw units as circles
                noStroke();
                circle(i * spacing + margin, (j * unitDiameter) + (unitDiameter / 2), unitDiameter);
            }
        }
    }
}

private class Layer {
    public Matrix2D weights;
    public Matrix2D biases;

    public Layer(Matrix2D weights, Matrix2D biases) {
        this.weights = weights;
        this.biases = biases;
    }
}
