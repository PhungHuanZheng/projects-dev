public class Main {
    public static void main(String[] args) {
        // load data from text file
        try {
            // LabelledDataset train = new LabelledDataset("../processing/NNFromScratch/data/MNIST_train.txt", ",", 10);
            LabelledDataset test = new LabelledDataset("../processing/NNFromScratch/data/MNIST_test.txt", ",", 10);
            System.out.println(test.data.shape[0]);
            System.out.println(test.data.shape[1]);


            NeuralNetwork nn = new NeuralNetwork(
                784,
                new int[] { 64, 64, 10 },
                new String[] { "sigmoid", "sigmoid", "sigmoid" });

            nn.feedforward(test.data);

        } catch (Exception e) {
            e.printStackTrace();
        }

        
    }

}
