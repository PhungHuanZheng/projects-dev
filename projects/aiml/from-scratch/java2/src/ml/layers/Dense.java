package ml.layers;

import interfaces.ILayer;
import interfaces.IMatrix;
import ml.Activations;

public class Dense extends ILayer {
	
	public Dense(int unitCount, String activation) throws NoSuchMethodException, SecurityException {
		this.unitCount = unitCount;
		this.activation = Activations.Forward.class.getMethod(activation, IMatrix.class);
	}
	
	@Override
	public <T extends IMatrix> void initParameters(T weights, T biases) {
		this.weights = weights;
		this.biases = biases;
		this.isInitiated = true;
	}

	@Override
	public <T extends IMatrix> T feedforward(T inputs) {
		this.checkIfInitiated();
		
		return inputs;
	}

	@Override
	public <T extends IMatrix> T backpropagate(T outputs, T targets) {
		// TODO Auto-generated method stub
		return null;
	}

}
