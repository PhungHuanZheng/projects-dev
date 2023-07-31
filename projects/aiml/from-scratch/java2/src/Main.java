import utils.LabelledDataset;
import interfaces.ILayer;
import ml.Sequential;
import ml.layers.Dense;

public class Main {
	public static void main(String[] args) {
//		load data
		LabelledDataset train = new LabelledDataset("../processing/NNFromScratch/data/8x8_train.txt", ",", 64)
				.scale(0, 1)
				.encodeTargets()
				.shuffle()
				.tranpose();

		LabelledDataset test = new LabelledDataset("../processing/NNFromScratch/data/8x8_test.txt", ",", 64)
				.scale(0, 1)
				.encodeTargets()
				.shuffle()
				.tranpose();
		
//		in case stupid and put wrong activation name
		try {
			Sequential model = new Sequential(new int[] {64}, new ILayer[] {
					new Dense(64, "relu"),
					new Dense(16, "relu"),
					new Dense(16, "relu"),
					new Dense(10, "relu"),
			});
			
		} catch (Exception e) {
			e.printStackTrace();
		}	
	}
}