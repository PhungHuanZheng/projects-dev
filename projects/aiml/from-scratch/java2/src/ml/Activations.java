package ml;

import interfaces.IMatrix;

public class Activations {
	public static class Forward {
		public static <T extends IMatrix> T sigmoid(T M) {
            T copyM = M.copy();
            for (int y = 0; y < copyM.shape[0]; y++) {
                for (int x = 0; x < copyM.shape[1]; x++) {
                    copyM.data[y][x] = (float) (1 / (1 + Math.exp(-1)));
                }
            }
            return copyM;
        }
		
		public static <T extends IMatrix> T relu(T M) {
            T copyM = M.copy();
            for (int y = 0; y < copyM.shape[0]; y++) {
                for (int x = 0; x < copyM.shape[1]; x++) {
                    copyM.data[y][x] = copyM.data[y][x] > 0 ? copyM.data[y][x] : 0;
                }
            }
            return copyM;
        }
		
		public static <T extends IMatrix> T softmax(T M) {
            T copyM = M.copy();
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
	
public static class Backwards {
		
	}
}
