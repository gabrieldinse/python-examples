import javax.ws.rs.Consumes;
import javax.ws.rs.GET;
import javax.ws.rs.PUT;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;

@Path("/dados")
public class Servidor {
	// Checar status do servidor
	@GET
	public String sayHello()
	{
		return "Servidor online.";
	}
	
	// Arduino -----------------------------------------------
	@PUT
	@Path("/put_dist")
	@Consumes("text/plain")
	public void add_leitura(String distancia_lida) {
		Data.getInstancia().setDistanciaLida(distancia_lida);
	}
	
	@PUT
	@Path("/put_status_led")
	@Consumes("text/plain")
	public void add_status(String status) {
		Data.getInstancia().setStatusLed(status);
	}
	
	@PUT
	@Path("/put_arduino_status")
	@Consumes("text/plain")
	public void arduino_status(String status_arduino) {
		Data.getInstancia().setStatusArduino(status_arduino);
	}
	
	@GET
	@Path("/get_dist_limite")
	@Produces("text/plain")
	public String getDistanciaLimite() {
		return Data.getInstancia().getDistanciaLimite();
	}
	
	@GET
	@Path("/get_status_prog")
	@Produces("text/plain")
	public String getStatusPrograma() {
		return Data.getInstancia().getStatusPrograma();
	}

	// PC ----------------------------------------------------
	@PUT
	@Path("/put_dist_limite") 
	@Consumes("text/plain")
	public void setDistanciaLimite(String distancia_limite) {
		Data.getInstancia().setDistanciaLimite(distancia_limite);
	}
	
	@PUT
	@Path("/put_status_prog") 
	@Consumes("text/plain")
	public void setStatusPrograma(String status_programa) {
		Data.getInstancia().setStatusPrograma(status_programa);
	}
	
	@GET
	@Path("/get_dist")
	@Produces("text/plain")
	public String getDistanciaLida() {
		return Data.getInstancia().getDistanciaLida();
	}
	
	@GET
	@Path("/get_status_led")
	@Produces("text/plain")
	public String getStatusLed() {
		return Data.getInstancia().getStatusLed();
	}
	
	@GET
	@Path("/get_status_arduino")
	@Produces("text/plain")
	public String getStatusArduino() {
		return Data.getInstancia().getStatusArduino();
	}
		
}
