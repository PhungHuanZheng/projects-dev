LabelledDataset train;
LabelledDataset test;
NeuralNetwork model;

void setup() {
    size(800, 600);

    //Matrix2D A = new Matrix2D(2, 1, false);
    //Matrix2D B = new Matrix2D(1, 2, false);
    //print(A.matmul(B).transpose().toStr());

    train = new LabelledDataset("data/MNIST_train.txt", ",", true);
    test = new LabelledDataset("data/MNIST_test.txt", ",", true);
    train.shuffle();
    test.shuffle();

    Matrix2D X = train.getData(0).transpose();
    Matrix2D y = train.getTarget(0, true);

    model = new NeuralNetwork(new int[]{784, 10, 10}, new String[]{"relu", "softmax"});
    OutputPair[] outputs = model.forwardPropagate(X);
    DerivPair[] derivs = model.backPropagate(outputs, X, y);
    //model.updateParameters(derivs, 0.01);
}

void draw() {
    background(0);
    //println(frameRate);
    //model.show();
}
