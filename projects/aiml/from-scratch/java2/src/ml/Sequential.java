package ml;

import java.util.ArrayList;

import interfaces.ILayer;

public class Sequential {
	public int layerCount;
	
	private ArrayList<ILayer> tempLayers = new ArrayList<ILayer>();
	public ILayer[] layers;
	
	public Sequential(int[] inputShape, ILayer[] layers) {
//		add to temp layers until compile
		for (int i = 0; i < layers.length; i++) {
			this.tempLayers.add(layers[i]);
		}
	}
	
	public void add(ILayer layer) {
		this.tempLayers.add(layer);
	}
	
//	method to be called once all layers finalized
	public void compile() {
//		build ILayer array
		this.layers = new ILayer[this.tempLayers.size()];
		for (int i = 0; i < this.tempLayers.size(); i++) {
			this.layers[i] = this.tempLayers.get(i);
		}
		
//		init first layer
		this.layers[0].initParameters(
				new Matrix2D(layerNeuronCounts[0], inputNeuronCount).randomize(-1, 1), 
				new Matrix2D(layerNeuronCounts[0], 1).randomize(-1, 1)
		);
		this.layers[0].weights = ;
		this.layers[0].biases = ;
        this.layers.add(firstLayer);
	}
}
