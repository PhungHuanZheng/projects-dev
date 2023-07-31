package errors;

public class IncompatibleShapeException extends RuntimeException {
	private static final long serialVersionUID = 1L;

	public IncompatibleShapeException(String errorMessage) {
        super(errorMessage, null);
    }
}