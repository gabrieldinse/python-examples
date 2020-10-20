
public class Data {
	private String distancia_lida = "15";
	private String distancia_limite = "30";
	private String status_led = "OFF";
	private String status_arduino = "OFF";
	private String status_programa = "OFF";
	private static final Data instancia = new Data();
	
	private Data() {
		
	}
	
	public String getDistanciaLida() {
		return distancia_lida;
	}
	
	public void setDistanciaLida(String distancia_lida) {
		this.distancia_lida = distancia_lida;
	}
	
	public String getDistanciaLimite() {
		return distancia_limite;
	}
	
	public void setDistanciaLimite(String distancia_limite) {
		this.distancia_limite = distancia_limite;
	}
	
	public String getStatusLed() {
		return status_led;
	}
	
	public void setStatusLed(String status_led) {
		this.status_led = status_led;
	}
	
	public String getStatusPrograma() {
		return status_programa;
	}
	
	public void setStatusPrograma(String status_programa) {
		this.status_programa = status_programa;
	}
	
	public String getStatusArduino() {
		return status_arduino;
	}
	
	public void setStatusArduino(String status_arduino) {
		this.status_arduino = status_arduino;
	}
	
	public static Data getInstancia() {
		return instancia;
	}
	
}
