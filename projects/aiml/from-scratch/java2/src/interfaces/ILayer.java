package interfaces;

import java.lang.reflect.Method;

public abstract class ILayer {
	public int unitCount;
	public Method activation;
	
	public IMatrix weights;
	public IMatrix biases;
	protected boolean isInitiated = false;
	
	protected void checkIfInitiated() {
		if (!this.isInitiated) {
			throw new RuntimeException(String.format(
					"Layer instance %s's parameters have not been initialised. Call Layer.initParameters to do so.",
					this.getClass().toString()
					));
		}
	}
	
	public abstract <T extends IMatrix> void initParameters(T weights, T biases);
	public abstract <T extends IMatrix> T feedforward(T inputs);
	public abstract <T extends IMatrix> T backpropagate(T outputs, T targets);
}
