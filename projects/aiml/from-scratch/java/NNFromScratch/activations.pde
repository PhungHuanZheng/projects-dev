public static class Activations {
    private static float[] relu(float[] z) {
        float[] newZ = new float[z.length];
        for (int i = 0; i < z.length; i++) {
            newZ[i] = z[i] > 0 ? z[i] : 0;
        }
        return newZ;
    }
    
    private static float[] derivRelu(float[] z) {
        float[] newZ = new float[z.length];
        for (int i = 0; i < z.length; i++) {
            newZ[i] = z[i] > 0 ? 1 : 0;
        }
        return newZ;
    }

    private static float[] softmax(float[] z) {
        // get sum of z
        float sum = 0;
        for (int i = 0; i < z.length; i++) {
            sum += Math.exp(z[i]);
        }

        float[] newZ = new float[z.length];
        for (int i = 0; i < newZ.length; i++) {
            newZ[i] = (float)Math.exp(z[i]) / sum;
        }
        return newZ;
    }

    public static float[] get(String methodName, float[] input) {
        switch (methodName.toLowerCase()) {
        case "relu":
            return relu(input);
        case "softmax":
            return softmax(input);
        default:
            return input;
        }
    }
}
